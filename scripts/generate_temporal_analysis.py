import duckdb
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Caminhos
SILVER_OD_PARQUET = "data/02_silver/matriz_od_amostra_1semana.parquet"
OUTPUT_HTML = "docs/dashboard_temporal.html"

def main():
    print("Conectando ao DuckDB e processando dados temporais...")
    con = duckdb.connect()
    
    # ==========================================
    # 1. Agrupamento por Faixa Horária
    # ==========================================
    query_faixa = f"""
        SELECT 
            CASE 
                WHEN date_part('hour', hora_inicio) >= 6 AND date_part('hour', hora_inicio) < 12 THEN '2. Manhã (06h-12h)'
                WHEN date_part('hour', hora_inicio) >= 12 AND date_part('hour', hora_inicio) < 18 THEN '3. Tarde (12h-18h)'
                WHEN date_part('hour', hora_inicio) >= 18 AND date_part('hour', hora_inicio) < 24 THEN '4. Noite (18h-00h)'
                ELSE '1. Madrugada (00h-06h)'
            END as faixa,
            COUNT(*) as volume
        FROM read_parquet('{SILVER_OD_PARQUET}')
        GROUP BY 1
        ORDER BY 1
    """
    df_faixa = con.execute(query_faixa).df()
    # Limpar o prefixo numérico para o gráfico
    df_faixa['faixa_limpa'] = df_faixa['faixa'].apply(lambda x: x.split('. ')[1])
    
    # ==========================================
    # 2. Agrupamento por Tipo de Dia
    # ==========================================
    query_dia = f"""
        SELECT 
            CASE 
                WHEN dayofweek(hora_inicio) IN (0, 6) THEN 'Fim de Semana'
                ELSE 'Dia Útil'
            END as tipo_dia,
            COUNT(*) as volume
        FROM read_parquet('{SILVER_OD_PARQUET}')
        GROUP BY 1
    """
    df_dia = con.execute(query_dia).df()
    
    # ==========================================
    # 3. Série Temporal (Respirar da Cidade)
    # ==========================================
    query_tempo = f"""
        SELECT 
            date_trunc('hour', hora_inicio) as hora_absoluta,
            COUNT(*) as volume
        FROM read_parquet('{SILVER_OD_PARQUET}')
        GROUP BY 1
        ORDER BY 1
    """
    df_tempo = con.execute(query_tempo).df()
    
    # ==========================================
    # MONTAGEM DO DASHBOARD COM PLOTLY
    # ==========================================
    print("Gerando painel interativo (Plotly)...")
    
    fig = make_subplots(
        rows=2, cols=2,
        specs=[[{"type": "bar"}, {"type": "pie"}],
               [{"type": "scatter", "colspan": 2}, None]],
        subplot_titles=(
            "Volume de Viagens por Faixa Horária", 
            "Proporção: Dia Útil vs Fim de Semana", 
            "Série Temporal Contínua (Densidade Hora a Hora)"
        ),
        vertical_spacing=0.25
    )
    
    # Gráfico 1: Barras (Faixa Horária)
    fig.add_trace(
        go.Bar(
            x=df_faixa['faixa_limpa'], 
            y=df_faixa['volume'],
            marker_color=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728'],
            name="Faixa Horária",
            text=df_faixa['volume'],
            texttemplate='%{text:,.0f}',
            textposition='outside'
        ),
        row=1, col=1
    )
    
    # Gráfico 2: Donut (Dia Útil vs FDS)
    fig.add_trace(
        go.Pie(
            labels=df_dia['tipo_dia'], 
            values=df_dia['volume'],
            hole=0.4,
            marker_colors=['#9467bd', '#8c564b'],
            name="Tipo de Dia",
            textinfo='label+percent'
        ),
        row=1, col=2
    )
    
    # Gráfico 3: Linha (Série Temporal)
    fig.add_trace(
        go.Scatter(
            x=df_tempo['hora_absoluta'], 
            y=df_tempo['volume'],
            mode='lines+markers',
            line=dict(color='#17becf', width=2),
            name="Fluxo Horário",
            fill='tozeroy',
            fillcolor='rgba(23, 190, 207, 0.2)'
        ),
        row=2, col=1
    )
    
    # Layout Global do Dashboard
    fig.update_layout(
        title_text="<b>Gêmeos Digitais: Dinâmica O-D Sorocaba</b><br><sup>Segmentação Temporal de Mobilidade Urbana</sup>",
        title_x=0.5,
        height=800,
        showlegend=False,
        template="plotly_dark",
        font=dict(family="Arial, sans-serif")
    )
    
    # Salvando em HTML
    fig.write_html(OUTPUT_HTML)
    print(f"[SUCESSO] Dashboard temporal salvo em: {OUTPUT_HTML}")

if __name__ == "__main__":
    main()
