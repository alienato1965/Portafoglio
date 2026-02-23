import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

# Configurazione Pagina
st.set_page_config(page_title="Space Terminal 70/30", layout="wide")

# CSS: ESTETICA SPAZIALE DARK
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&display=swap');
    
    /* Sfondo Spaziale */
    .stApp {
        background: radial-gradient(circle, #0a0c10 0%, #000000 100%) !important;
        font-family: 'JetBrains Mono', monospace !important;
    }

    /* Sidebar Stealth */
    [data-testid="stSidebar"] {
        background-color: rgba(5, 5, 5, 0.95) !important;
        border-right: 1px solid #00ff66;
    }

    /* Input Fields Space Style */
    input {
        background-color: #000 !important;
        color: #00ff66 !important;
        border: 1px solid #1a1a1a !important;
    }

    /* Card Metriche "Glow" */
    [data-testid="stMetric"] {
        background: rgba(0, 20, 10, 0.5) !important;
        border: 1px solid #00ff66 !important;
        box-shadow: 0 0 15px rgba(0, 255, 102, 0.1);
        border-radius: 4px !important;
        padding: 20px !important;
    }
    
    [data-testid="stMetricValue"] {
        color: #00ff66 !important;
        text-shadow: 0 0 8px rgba(0, 255, 102, 0.6);
    }

    /* Tabelle Cyberpunk */
    .stTable {
        background-color: rgba(0, 0, 0, 0.8) !important;
        border: 1px solid #1a1a1a !important;
    }
    th { color: #00ff66 !important; text-transform: uppercase; letter-spacing: 2px; }
    td { color: #ffffff !important; border-bottom: 1px solid #111 !important; }

    /* Titoli Neon */
    h1, h2, h3 {
        color: #ffffff !important;
        text-transform: uppercase;
        letter-spacing: 4px;
        text-shadow: 0 0 10px rgba(255, 255, 255, 0.2);
    }
</style>
""", unsafe_allow_html=True)

# 1. SIDEBAR: I 5 SLOT DINAMICI
with st.sidebar:
    st.markdown("<h2 style='color: #00ff66;'>🛸 SLOTS</h2>", unsafe_allow_html=True)
    s1 = st.text_input("SLOT 1 (45% CORE)", value="VWCE.DE")
    s2 = st.text_input("SLOT 2 (25% CORE)", value="QDVE.DE")
    s3 = st.text_input("SLOT 3 (20% GOLD)", value="SGLN.L")
    s4 = st.text_input("SLOT 4 (10% MINER)", value="GDXJ")
    s5 = st.text_input("SLOT 5 (OPTIONAL)", value="")
    
    st.markdown("---")
    cap = st.number_input("CAPITALE (€)", value=10000, step=1000)
    pac = st.number_input("PAC ATTUALE (€)", value=500, step=100)

# Costruiamo il dizionario asset in base agli slot compilati
config_pesi = {s1: 0.45, s2: 0.25, s3: 0.20, s4: 0.10}
if s5: config_pesi[s5] = 0.0 # Gestione slot extra

st.markdown("<h1 style='text-align: center;'>SYSTEM COMMAND: 70/30 STRATEGY</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #444;'>[ CORE: 70% | SATELLITE: 30% ]</p>", unsafe_allow_html=True)

# 2. DOWNLOAD DATI
@st.cache_data(ttl=600)
def fetch_space_data(tkrs):
    try:
        data = yf.download([t for t in tkrs if t], period="5d")["Close"]
        return data.ffill().iloc[-1]
    except: return None

prezzi = fetch_space_data(list(config_pesi.keys()))

if prezzi is not None:
    # 3. DASHBOARD METRICHE
    cols = st.columns(4)
    tickers_list = [s1, s2, s3, s4]
    for i, t in enumerate(tickers_list):
        if t in prezzi:
            cols[i].metric(t, f"{prezzi[t]:.2f}€", f"{config_pesi[t]*100:.0f}% TGT")

    # 4. TABELLA ORDINI SPAZIALE
    st.markdown("### 🛰️ REBALANCING MODULE")
    tot_investito = cap + pac
    ordini_data = []
    
    for t, p in config_pesi.items():
        if t and t in prezzi:
            val_target = tot_investito * p
            ordini_data.append({
                "TICKER": t,
                "ALLOCATION": f"{p*100:.0f}%",
                "TARGET (€)": f"{val_target:,.2f}",
                "TOTAL SHARES": round(val_target / prezzi[t], 4)
            })
    
    st.table(pd.DataFrame(ordini_data))

    # 5. VISUAL ALLOCATION
    fig = go.Figure(data=[go.Pie(
        labels=list(config_pesi.keys()),
        values=list(config_pesi.values()),
        hole=.7
