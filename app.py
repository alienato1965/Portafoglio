import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

# Configurazione Browser
st.set_page_config(page_title="Cyber Terminal 70/30", layout="wide")

# IL MOTORE ESTETICO: CSS SPAZIALE AVANZATO
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=JetBrains+Mono&display=swap');
    
    .stApp {
        background: radial-gradient(circle at center, #0d1117 0%, #000000 100%) !important;
        color: #e0e0e0 !important;
    }
    
    /* Font per titoli e dati */
    h1, h2, h3 { font-family: 'Orbitron', sans-serif !important; }
    div, p, label { font-family: 'JetBrains Mono', monospace !important; }

    /* Container con effetto Neon */
    .cyber-card {
        background: rgba(10, 10, 10, 0.8);
        border: 1px solid #00ff66;
        box-shadow: 0 0 20px rgba(0, 255, 102, 0.15);
        border-radius: 10px;
        padding: 25px;
        margin-bottom: 20px;
    }

    /* Sidebar Stealth */
    [data-testid="stSidebar"] {
        background-color: #050505 !important;
        border-right: 2px solid #00ff66;
    }

    /* Metriche Glow */
    [data-testid="stMetric"] {
        background: transparent !important;
        border: 1px solid #333 !important;
        border-radius: 8px !important;
        transition: 0.3s;
    }
    [data-testid="stMetric"]:hover {
        border: 1px solid #00ff66 !important;
        box-shadow: 0 0 10px rgba(0, 255, 102, 0.3);
    }
    [data-testid="stMetricValue"] { color: #00ff66 !important; font-weight: bold !important; }

    /* Tabelle Dark */
    .stTable { background-color: transparent !important; }
    thead tr th { background-color: #111 !important; color: #00ff66 !important; border-bottom: 2px solid #00ff66 !important; }
</style>
""", unsafe_allow_html=True)

# 1. COMMAND CENTER (SIDEBAR)
with st.sidebar:
    st.markdown("<h1 style='color: #00ff66; font-size: 24px;'>🛸 SLOTS</h1>", unsafe_allow_html=True)
    st.markdown("---")
    s1 = st.text_input("SLOT 1 (45%)", value="VWCE.DE")
    s2 = st.text_input("SLOT 2 (25%)", value="QDVE.DE")
    s3 = st.text_input("SLOT 3 (20%)", value="SGLN.L")
    s4 = st.text_input("SLOT 4 (10%)", value="GDXJ")
    s5 = st.text_input("SLOT 5 (OPTIONAL)", value="")
    st.markdown("---")
    cap = st.number_input("CAPITALE ATTUALE (€)", value=10000, step=1000)
    pac = st.number_input("PAC DA INIETTARE (€)", value=500, step=100)

# 2. LOGICA DATI (CON GESTIONE ERRORI)
@st.cache_data(ttl=600)
def fetch_data(tkrs):
    try:
        data = yf.download([t for t in tkrs if t], period="5d")["Close"]
        return data.ffill().iloc[-1]
    except Exception:
        return None

# Definizione Pesi
config_pesi = {s1: 0.45, s2: 0.25, s3: 0.20, s4: 0.10}
if s5: config_pesi[s5] = 0.0

prezzi = fetch_data(list(config_pesi.keys()))

# 3. INTERFACCIA PRINCIPALE
st.markdown("<h1 style='text-align: center; color: white;'>SYSTEM STATUS: ACTIVE</h1>", unsafe_allow_html=True)
st.markdown("<div style='height: 2px; background: linear-gradient(90deg, transparent, #00ff66, transparent); margin-bottom: 40px;'></div>", unsafe_allow_html=True)

if prezzi is not None:
    # Monitor Prezzi in tempo reale
    cols = st.columns(4)
    tickers_list = [s1, s2, s3, s4]
    for i, t in enumerate(tickers_list):
        if t in prezzi:
            cols[i].metric(t, f"{prezzi[t]:.2f}€", "LIVE")

    st.markdown("<br>", unsafe_allow_html=True)

    # Area Ordini
    st.markdown("<div class='cyber-card'>", unsafe_allow_html=True)
    st.subheader("⚖️ REBALANCING ENGINE")
    tot_cap = cap + pac
    ordini_data = []
    
    for t, p in config_pesi.items():
        if t and t in prezzi:
            v_target = tot_cap * p
            ordini_data.append({
                "ASSET": t,
                "ALLOCATION": f"{p*100:.0f}%",
                "TARGET (€)": f"{v_target:,.2f} €",
                "QUOTE TOTALI": round(v_target / prezzi[t], 4)
            })
    
    st.table(pd.DataFrame(ordini_data))
    st.markdown("</div>", unsafe_allow_html=True)

    # Grafico Allocazione Spaziale
    c1, c2 = st.columns([1, 1])
    with c1:
        st.markdown("<div class='cyber-card'>", unsafe_allow_html=True)
        st.subheader("🎯 TARGET PIE")
        fig = go.Figure(data=[go.Pie(
            labels=list(config_pesi.keys()),
            values=list(config_pesi.values()),
            hole=.7,
            marker=dict(colors=['#00ff66', '#00cc55', '#ccaa00', '#886600'])
        )])
        fig.update_layout(showlegend=False,
