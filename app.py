import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="Elite Dynamic Terminal", layout="wide")

# CSS: LEGGIBILITÀ E STILE NEON (CORRETTO)
st.markdown("""
<style>
    .stApp { background-color: #000000 !important; }
    p, span, label, th, td, div { color: #ffffff !important; font-family: 'Courier New', monospace; }
    h1, h2, h3 { color: #00ff66 !important; text-shadow: 0 0 5px #00ff66; }
    [data-testid="stMetric"] { 
        background-color: #111 !important; 
        border: 1px solid #00ff66 !important; 
        border-radius: 8px;
    }
    .stTable { background-color: #050505 !important; border: 1px solid #222 !important; }
</style>
""", unsafe_allow_html=True)

st.title("📟 DYNAMIC STRATEGY COMMAND")

# 1. SIDEBAR: QUI RENDIAMO TUTTO MODIFICABILE
with st.sidebar:
    st.header("⚙️ ASSET ALLOCATION")
    st.write("Modifica i pesi per ricalcolare gli ordini")
    
    # Input dinamici per i 4 pilastri della tua strategia
    w_vwce = st.slider("VWCE (Mondiale) %", 0, 100, 45)
    w_qdve = st.slider("QDVE (S&P500 IT) %", 0, 100, 25)
    w_gold = st.slider("GOLD (Oro) %", 0, 100, 20)
    w_miners = st.slider("GDXJ (Miners) %", 0, 100, 10)
    
    tot_pesi = w_vwce + w_qdve + w_gold + w_miners
    
    if tot_pesi != 100:
        st.error(f"ATTENZIONE: Il totale è {tot_pesi}%. Deve essere 100%!")
    
    st.markdown("---")
    cap_tot = st.number_input("Capitale Attuale (€)", value=10000)
    pac_val = st.number_input("Iniezione PAC (€)", value=500)

# Dictionary dinamico basato sugli input
assets = {
    "VWCE.DE": w_vwce / 100,
    "QDVE.DE": w_qdve / 100,
    "SGLN.L": w_gold / 100,
    "GDXJ": w_miners / 100
}

# 2. DOWNLOAD DATI
@st.cache_data
def load_prices(tickers):
    try:
        df = yf.download(tickers, period="5d")["Close"]
        return df.ffill().iloc[-1]
    except: return None

prezzi = load_prices(list(assets.keys()))

if prezzi is not None and tot_pesi == 100:
    # 3. MONITOR PREZZI
    cols = st.columns(4)
    for i, (t, p) in enumerate(assets.items()):
        cols[i].metric
