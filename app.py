import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Cyber Elite", layout="wide")

# CSS: DESIGN MINIMALISTA PROFESSIONALE
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&display=swap');
    
    .stApp { background-color: #0d0d0d !important; font-family: 'JetBrains Mono', monospace; }
    
    /* Sidebar ultra-scura */
    [data-testid="stSidebar"] { background-color: #050505 !important; border-right: 1px solid #1a1a1a; }

    /* Box Metriche Stealth */
    [data-testid="stMetric"] {
        background: #111111 !important;
        border: 1px solid #222 !important;
        border-radius: 4px !important;
        padding: 15px !important;
    }
    [data-testid="stMetricValue"] { color: #00ff99 !important; font-size: 1.8rem !important; }
    
    /* Tabelle High-Tech */
    .stTable { background-color: #0d0d0d !important; color: #888 !important; border: 1px solid #222 !important; }
    
    /* Titoli */
    h1, h2, h3 { color: #ffffff !important; letter-spacing: -1px; text-transform: uppercase; }
    
    /* Linea di separazione sottile */
    .divider { border-bottom: 1px solid #222; margin: 25px 0; }
</style>
""", unsafe_allow_html=True)

# CONFIGURAZIONE STRATEGIA 70/30 (Dati salvati)
# Core: 45% VWCE, 25% QDVE | Satellite: 20% Gold, 10% Jr Miners
assets = {
    "VWCE.DE": 0.45, "QDVE.DE": 0.25, 
    "SGLN.L": 0.20, "GDXJ": 0.10
}

with st.sidebar:
    st.markdown("### 📟 SYSTEM CONFIG")
    cap_totale = st.number_input("CAPITALE ATTUALE (€)", value=10000)
    pac_mensile = st.number_input("VERSAMENTO MENSILE (€)", value=500)
    st.markdown("---")
    anni_analisi = st.slider("ANNI STORICI", 5, 20, 10)

@st.cache_data
def fetch_clean_data(tickers):
    try:
        data = yf.download(tickers, period="25y")["Close"]
        return data.ffill()
    except:
        return pd.DataFrame()

df = fetch_clean_data(list(assets.keys()))

if not df.empty:
    prezzi_attuali = {t: float(df[t].iloc[-1]) for t in assets.keys()}
    
    st.title("ELITE COMMAND CENTER")
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    # 1. VISUALIZZAZIONE COMPOSIZIONE (Stile Desaturato)
    c_pie, c_stat = st.columns([1, 2])
    
    with c_pie:
        # Colori cyber: Smeraldo, Foresta, Oro spento, Ambra
        cyber_colors = ['#00ff99', '#008855', '#ccaa00', '#886600']
        fig_pie = go.Figure(data=[go.Pie(
            labels=list(assets.keys()), 
            values=list(assets.values()), 
            hole=.75,
            marker=dict(colors=cyber_colors, line=dict(color='#0d0d0d', width=3))
        )])
        fig_pie.update_layout(
            showlegend=False, margin=dict(t=0, b=0, l=0, r=0),
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with c_stat:
        st.markdown("#### PERFORMANCE ATTUALE")
        m1, m2 = st.columns(2)
        # Calcolo rendimento medio pesato reale
        rend_storico = sum([((df[t].iloc[-1]/df[t].tail(anni_analisi*252).iloc[0])**(1/anni_analisi)-1)*100 * p for t,p in assets.items()])
        m1.metric("RENDIMENTO MEDIO", f"{rend_storico:.1f}%")
        m2.metric("OBIETTIVO FINALE", "2036")

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    # 2. PIANO OPERATIVO (Niente variabili troncate qui)
    st.subheader("⚖️ PIANO ORDINI MENSILE")
    cap_investito = cap_totale + pac_mensile
    tabella_dati = []
    for t, p in assets.items():
        v_target = cap_investito * p
        tabella_dati.append({
            "ASSET": t,
            "TARGET (%)": f"{p*100}%",
            "VALORE TARGET (€)": f"{v_target:,.0f}",
            "QUOTE TOTALI": round(v_target / prezzi_attuali[t], 2)
        })
    st.table(pd.DataFrame(tabella_dati))

    # 3. TREND STORICO (Linee sottili, niente caos)
    st.subheader("📈 PERFORMANCE STORICA ASSET")
    p_df = (df.tail(anni_analisi*252) / df.tail(anni_analisi*252).iloc[0]) * 100
    fig_line = px.line(p_df, color_discrete_sequence=cyber_colors)
    fig_line.update_layout(
        height=350, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font_color='#444', margin=dict(t=10, b=10),
        xaxis=dict(gridcolor='#1a1a1a', showline=False),
        yaxis=dict(gridcolor='#1a1a1a', showline=False),
        legend=dict(orientation="h", y=1.1, x=0.5, xanchor="center")
    )
    st.plotly_chart(fig_line, use_container_width=True)

    # 4. PROIEZIONE 2036
    r_mensile = (1 + (rend_storico / 100))**(1/12) - 1
    val_nominale = [float(cap_totale)]
    for _ in range(120):
        val_nominale.append((val_nominale[-1] * (1 + r_m if 'r_m' in locals() else 1 + r_mensile)) + pac_mensile)
    
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    st.success(f"🔮 PROIEZIONE CAPITALE NETTO 2036: {val_nominale[-1] * 0.85:,.0f} €")

else:
    st.error("ERRORE DI CONNESSIONE AI MERCATI.")
