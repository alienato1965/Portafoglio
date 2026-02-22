import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px

# Configurazione Pagina
st.set_page_config(page_title="Elite Command Center", layout="wide")

# CSS "MAGIA NERA": Bordi Neon, Font Tecnico e Spaziature calibrate
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&display=swap');
    
    .stApp, [data-testid="stSidebar"], .main { background-color: #000000 !important; }
    html, body, [class*="css"] { font-family: 'JetBrains Mono', monospace !important; color: #ffffff !important; }

    /* Box Performance: Effetto Neon */
    [data-testid="stMetric"] {
        background: linear-gradient(145deg, #050505, #101010) !important;
        border: 1px solid #00ff00 !important;
        box-shadow: 0 0 15px rgba(0, 255, 0, 0.2) !important;
        border-radius: 2px !important;
        padding: 15px !important;
    }
    [data-testid="stMetricValue"] { color: #00ff00 !important; text-shadow: 0 0 10px #00ff00; font-size: 28px !important; }
    [data-testid="stMetricLabel"] { color: #666 !important; text-transform: uppercase; font-size: 10px !important; }

    /* Sidebar Stealth */
    [data-testid="stSidebar"] { border-right: 1px solid #1a1a1a !important; width: 300px !important; }
    
    /* Input e Slider */
    .stSlider [data-baseweb="slider"] [role="slider"] { background-color: #fff !important; border: 2px solid #00ff00 !important; box-shadow: 0 0 10px #00ff00; }
    .stSlider [data-baseweb="slider"] [aria-valuemax] { background-image: linear-gradient(to right, #00ff00, #00ff00) !important; }

    /* Tabelle e Titoli */
    h1, h2, h3 { color: #00ff00 !important; text-shadow: 0 0 5px rgba(0,255,0,0.5); text-transform: uppercase; }
    .stTable { background-color: #050505 !important; border: 1px solid #1a1a1a !important; }
</style>
""", unsafe_allow_html=True)

st.title("📟 ELITE PORTFOLIO COMMAND")

# Sidebar: Strategia 70/30 (Dati salvati)
with st.sidebar:
    st.markdown("### 🖥️ CONFIGURAZIONE")
    st.markdown("**CORE (70%)**")
    e1 = st.text_input("VWCE (45%)", "VWCE.DE")
    e2 = st.text_input("QDVE (25%)", "QDVE.DE")
    st.markdown("---")
    st.markdown("**SATELLITE (30%)**")
    e3 = st.text_input("GOLD (20%)", "SGLN.L")
    e4 = st.text_input("JR MINERS (10%)", "GDXJ")
    
    tkrs = [e1, e2, e3, e4]
    pesi = {e1: 0.45, e2: 0.25, e3: 0.20, e4: 0.10}
    anni = st.slider("ANNI ANALISI", 5, 20, 10)

@st.cache_data
def get_data(list_tkrs):
    try:
        data = yf.download(list_tkrs, period="25y")["Close"]
        return data.ffill()
    except: return pd.DataFrame()

df = get_data(tkrs)

if not df.empty:
    prezzi_attuali = {t: float(df[t].iloc[-1]) for t in tkrs}
    
    # Sezione Rendimenti
    st.subheader("🟢 ANALISI RENDIMENTI")
    c1, c2, c3, c4 = st.columns(4)
    cols = [c1, c2, c3, c4]
    cagr_vals = {}
    
    for i, t in enumerate(tkrs):
        serie = df[t].dropna()
