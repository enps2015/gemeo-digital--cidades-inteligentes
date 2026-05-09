import os
import duckdb
import pandas as pd
import folium
from folium import plugins

# ==============================================================================
# MVP: GERAÇÃO DE MAPA INTERATIVO O-D (CAMADA GOLD - IA)
# ==============================================================================

GOLD_SENSORS_PARQUET = "data/03_gold/sensores_clusterizados.parquet"
GOLD_MACRO_OD_PARQUET = "data/03_gold/matriz_od_macro_zonas.parquet"
OUTPUT_MAP = "docs/mapa_fluxo_sorocaba.html"

def main():
    print("[1/3] Conectando à Camada Gold...")
    con = duckdb.connect()
    
    # 1. Carregar Sensores Agrupados
    query_sensors = f"SELECT * FROM read_parquet('{GOLD_SENSORS_PARQUET}')"
    df_sensors = con.execute(query_sensors).df()
    
    # 2. Carregar Matriz O-D de Macro-Zonas
    query_edges = f"""
        SELECT * FROM read_parquet('{GOLD_MACRO_OD_PARQUET}')
        WHERE origem_zona != destino_zona
    """
    df_edges = con.execute(query_edges).df()
    
    # 3. Renderizar o mapa geoespacial
    print("[2/3] Renderizando sensores e zonas de calor...")
    avg_lat = df_sensors['lat'].mean()
    avg_lon = df_sensors['lon'].mean()
    
    # CartoDB dark_matter ressalta as cores vibrantes
    mapa = folium.Map(location=[avg_lat, avg_lon], zoom_start=13, tiles='CartoDB dark_matter')
    
    # Paleta de cores para os Clusters
    cluster_colors = {
        0: '#FF3366', # Rosa choque (Macro-Zona A)
        1: '#33CCFF', # Azul ciano (Macro-Zona B)
        2: '#33FF33', # Verde neon (Macro-Zona C)
        3: '#FFCC00', # Amarelo ouro (Macro-Zona D)
        -1: '#555555' # Cinza (Ruído / Isolados)
    }
    
    # Dicionário de Centróides
    centroids = {}
    
    # Plotar os sensores físicos (Nós Menores)
    for _, row in df_sensors.iterrows():
        cid = row['cluster_id']
        nserie = row['sensor_id']
        lat, lon = row['lat'], row['lon']
        vol = row['volume']
        zona = row['nome_zona']
        
        color = cluster_colors.get(cid, '#FFFFFF')
        
        # Salva o centróide para desenhar linhas depois
        if cid != -1 and zona not in centroids:
            centroids[zona] = (row['centroide_lat'], row['centroide_lon'])
            
        folium.CircleMarker(
            location=[lat, lon],
            radius=4,
            color=color,
            fill=True,
            fill_opacity=0.6,
            tooltip=f"Sensor: {nserie}<br>Pertence a: {zona}",
            popup=f"Volume no sensor: {vol:,}"
        ).add_to(mapa)

    # Plotar os Centróides (Centros de Massa da IA)
    for zona, (clat, clon) in centroids.items():
        # Achar a cor da zona baseada na string (A=0, B=1, C=2)
        idx = ord(zona.split(' ')[-1]) - 65
        color = cluster_colors.get(idx, '#FFFFFF')
        
        folium.CircleMarker(
            location=[clat, clon],
            radius=15,
            color='#FFFFFF',
            weight=2,
            fill=True,
            fill_color=color,
            fill_opacity=0.3,
            tooltip=f"<b>Centróide: {zona}</b>",
            popup="Centro de Massa definido pelo DBSCAN"
        ).add_to(mapa)

    # 4. Plotar as Arestas (Fluxos O-D entre Macro-Zonas)
    print("[3/3] Desenhando Macro-Corredores de mobilidade...")
    if not df_edges.empty:
        max_peso = df_edges['volume_viagens'].max()
        for _, row in df_edges.iterrows():
            orig = row['origem_zona']
            dest = row['destino_zona']
            peso = row['volume_viagens']
            duracao = row['duracao_media_minutos']
            
            if orig in centroids and dest in centroids:
                coord_orig = centroids[orig]
                coord_dest = centroids[dest]
                
                # Espessura dinâmica
                weight = max(2, (peso / max_peso) * 12)
                
                # Usar AntPath para mostrar a direção do fluxo
                plugins.AntPath(
                    locations=[coord_orig, coord_dest],
                    delay=400,
                    dash_array=[15, 30],
                    weight=weight,
                    color='#FFFFFF',
                    pulse_color='#000000',
                    opacity=0.6,
                    tooltip=f"<b>Corredor:</b> {orig} ➔ {dest}<br><b>Volume:</b> {peso:,} viagens<br><b>Duração Média:</b> {duracao:.1f} min"
                ).add_to(mapa)

    # Legendas HTML atualizadas para IA (Com Responsividade Mobile)
    css_mobile = '''<style>
        @media (max-width: 768px) {
            .map-legend { display: none !important; }
            .map-title { top: 10px !important; padding: 10px !important; width: 85% !important; }
            .map-title h2 { font-size: 16px !important; }
            .map-title p { font-size: 11px !important; }
            .map-logo { display: none !important; }
        }
    </style>'''
    mapa.get_root().html.add_child(folium.Element(css_mobile))

    legend_html = '''
     <div class="map-legend" style="position: fixed; 
     bottom: 50px; left: 50px; width: 340px; height: auto; 
     background-color: rgba(20, 20, 20, 0.95); z-index:9999; font-size:14px;
     border: 1px solid #666; color: #FFF; padding: 15px; border-radius: 8px; font-family: Arial, sans-serif;">
     <h4 style="margin-top: 0; color: #FFF;">Macro-Zonas (IA DBSCAN)</h4>
     <p style="margin-bottom: 5px;"><i class="fa fa-circle" style="color:#FF3366"></i> Macro-Zona A (Centro/Norte)</p>
     <p style="margin-bottom: 5px;"><i class="fa fa-circle" style="color:#33CCFF"></i> Macro-Zona B (Leste/Sul)</p>
     <p style="margin-bottom: 5px;"><i class="fa fa-circle" style="color:#33FF33"></i> Macro-Zona C (Oeste/Industrial)</p>
     <p style="margin-bottom: 5px;"><i class="fa fa-circle" style="color:#555555"></i> Ruído/Sensores Isolados</p>
     <p style="font-size: 12px; color: #BBB;"><em>* Círculos maiores indicam o Centróide da Zona.</em></p>
     <hr style="border: 0.5px solid #444;">
     <h4 style="margin-top: 5px; margin-bottom: 5px; color: #FFF;">Fluxos Consolidados (O-D)</h4>
     <p style="margin-bottom: 2px;">Linhas Animadas (Formigas)</p>
     <p style="font-size: 12px; color: #BBB; margin-top: 0;"><em>* A espessura da linha indica o volume de viagens reais. A animação aponta a direção do fluxo dominante.</em></p>
     </div>
     '''
    mapa.get_root().html.add_child(folium.Element(legend_html))
    
    title_html = '''
     <div class="map-title" style="position: fixed; 
     top: 20px; left: 50%; transform: translateX(-50%); width: auto; height: auto; 
     background-color: rgba(20, 20, 20, 0.95); z-index:9999; text-align: center;
     border: 1px solid #666; padding: 15px 40px; border-radius: 8px; font-family: Arial, sans-serif;
     box-shadow: 0px 4px 10px rgba(0,0,0,0.5);">
     <h2 style="margin: 0; color: #FFF; font-size: 24px;">Inteligência Artificial Não-Supervisionada</h2>
     <p style="margin: 5px 0 0 0; color: #00BFFF; font-size: 15px; font-weight: bold;">Identificação de Macro-Corredores de Fluxo em Sorocaba-SP</p>
     </div>
     '''
    mapa.get_root().html.add_child(folium.Element(title_html))
    
    # Adicionar Logo dos Patrocinadores no Canto Inferior Direito
    logo_html = '''
     <div class="map-logo" style="position: fixed; 
     bottom: 50px; right: 50px; width: auto; height: auto; 
     z-index:9999; border-radius: 8px; overflow: hidden;
     box-shadow: 0px 4px 10px rgba(0,0,0,0.5); background-color: rgba(255, 255, 255, 0.85); padding: 8px;">
     <img src="../img/logo_patrocinadores.png" style="max-height: 70px; display: block;">
     </div>
     '''
    mapa.get_root().html.add_child(folium.Element(logo_html))
            
    mapa.save(OUTPUT_MAP)
    print(f"[SUCESSO] Mapa de IA salvo em: {OUTPUT_MAP}")

if __name__ == "__main__":
    main()
