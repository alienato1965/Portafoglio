import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Elite Terminal v7", layout="wide")

# CSS: LOOK FINALE "COMMAND CENTER"
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&display=swap');
    .stApp { background-color: #000000 !important; font-family: 'JetBrains Mono', monospace; }
    [data-testid="stMetric"] {
        background: #080808 !important; border: 1px solid #00ff00 !important;
        box-shadow: 0 0 12px rgba(0, 255, 0, 0.25); border-radius: 4px; padding: 15px;
    }
    [data-testid="stMetricValue"] { color: #00ff00 !important; text-shadow: 0 0 10px #00ff00; }
    h1, h2, h3 { color: #00ff00 !important; text-transform: uppercase; letter-spacing: 2px; }
    .stTable { background-color: #050505 !important; border: 1px solid #1a1a1a !important; }
</style>
""", unsafe_allow_html=True)

st.title("📟 ELITE STRATEGY COMMAND v7.0")

# DEFINIZIONE STRATEGIA DEFINITIVA 2026
assets = {
    "VWCE.DE": 0.45, # Core 1
    "QDVE.DE": 0.25, # Core 2
    "SGLN.L": 0.20,  # Satellite 1
    "GDXJ": 0.10     # Satellite 2
}

with st.sidebar:
    st.header("⚙️ OPERATIVITÀ")
    cap_totale = st.number_input("Capitale Totale (€)", value=10000, step=1000)
    pac_mensile = st.number_input("Versamento PAC (€)", value=500, step=100)
    st.markdown("---")
    anni_analisi = st.slider("Anni Storici", 5, 20, 10)

@st.cache_data
def load_all_data(tickers):
    return yf.download(tickers, period="25y")["Close"].ffill()

df = load_all_data(list(assets.keys()))

if not df.empty:
    prezzi = {t: float(df[t].iloc[-1]) for t in assets.keys()}
    
    # 1. VISUALIZZAZIONE COMPOSIZIONE (GRAFICO NEON)
    st.subheader("🎯 ALLOCAZIONE TARGET 70/30")
    col_chart, col_metrics = st.columns([1, 2])
    
    with col_chart:
        fig_pie = px.pie(
            values=list(assets.values()), 
            names=list(assets.keys()),
            hole=0.6,
            color_discrete_sequence=['#00ff00', '#00ffff', '#ffd700', '#ff00ff']
        )
        fig_pie.update_layout(
            showlegend=False, 
            paper_bgcolor='rgba(0,0,0,0)', 
            plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(t=0, b=0, l=0, r=0)
        )
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with col_metrics:
        c1, c2 = st.columns(2)
        c1.metric("CORE (STRUTTURA)", "70%", delta="VWCE + QDVE")
        c2.metric("SATELLITE (SPINTA)", "30%", delta="GOLD + MINERS")

    # 2. ORDINI E RIBILANCIAMENTO
    st.markdown("---")
    st.subheader("⚖️ PIANO ORDINI ATTUALE")
    nuovo_cap = cap_totale + pac_
