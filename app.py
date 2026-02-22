import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px

# 1. SETUP ESTETICO AVANZATO
st.set_page_config(page_title="Dashboard Elite 70/30", layout="wide")

st.markdown("""
    <style>
    /* Sfondo Nero Assoluto */
    .stApp, [data-testid="stSidebar"], .main { background-color: #000000 !important; }
    
    /* Testi Bianchi e Gialli */
    p, span, label, .stMarkdown { color: #ffffff !important; }
    
    /* Slider Giallo Ocrat */
    .stSlider [data-baseweb="slider"] [role="slider"] { background-color: #FFD700 !important; }
    .stSlider [data-baseweb="slider"] [aria-valuemax] { background-image: linear-gradient(to right, #FFD700, #FFD700) !important; }

    /* Box Metriche Neon */
    [data-testid="stMetric"] {
        background: #0a0a0a !important;
        border-radius: 15px;
        border: 1px solid #00ff00 !important;
        box-shadow: 0 0 10px rgba(0, 255, 0, 0.2);
    }
    [data-testid="stMetricValue"] {
        color: #00ff00 !important;
        font-size: 40px !important;
        text-shadow: 0 0 8px #00ff00;
    }
    
    /* Titoli Neon */
    h1, h2, h3 { color: #00ff00 !important; font-family: 'Inter', sans-serif; }
    </style>
    """, unsafe_allow_html=True)

st.title("📟 DASHBOARD ELITE 70/30")

# 2. SIDEBAR (Configurazione con Slider Gialli)
with st.sidebar:
    st.header("⚙️ CONFIGURAZIONE")
    e1 = st.text_input("ETF 1 (Core)", "VWCE.DE")
    p1 = st.slider(f"% {e1}", 0, 100, 35)
    e2 = st.text_input("ETF 2 (Core)", "QDVE.DE")
    p2 = st.slider(f"% {e2}", 0, 100, 35)
    e3 = st.text_input("ETF 3 (Gold)", "SGLN.L")
    p3 = st.slider(f"% {e3}", 0, 100, 10)
    e4 = st.text_input("ETF 4 (Miners)", "GDXJ")
    p4 = st.slider(f"% {e4}", 0, 100, 10)
    e5 = st.text_input("ETF 5", "SMH")
    p5 = st.slider(f"% {e5}", 0, 100, 5)
    e6 = st.text_input("ETF 6", "TSLA")
    p6 = st.slider(f"% {e6}", 0, 100, 5)
    
    tickers = [e1, e2, e3, e4, e5, e6]
    pesi = {e1: p1/100, e2: p2/100, e3: p3/100, e4: p4/100, e5: p5/100, e6: p6/100}
    anni = st.slider("Analisi Storica (Anni)", 5, 20, 10)

# 3. LOGICA DATI E PREZZI
@st.cache_data
def get_full_data(tkrs):
    d = yf.download(tkrs, period="25y")["Close"]
    return d.ffill()

try:
    df = get_full_data(tickers)
    prezzi_attuali = {t: float(df[t].iloc[-1]) for t
