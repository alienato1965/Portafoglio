import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px

# 1. DESIGN "TOTAL BLACK & NEON"
st.set_page_config(page_title="Finanza Elite 70/30", layout="wide")

st.markdown("""
    <style>
    /* Forza sfondo nero ovunque (Main e Sidebar) */
    .stApp, [data-testid="stSidebar"], .main {
        background-color: #000000 !important;
    }
    
    /* Testi generali chiari */
    p, span, label, .stMarkdown {
        color: #e0e0e0 !important;
        font-family: 'Inter', sans-serif;
    }
    
    /* Sidebar: testi e input */
    [data-testid="stSidebar"] .stMarkdown p, [data-testid="stSidebar"] label {
        color: #00ff00 !important;
        font-weight: bold;
    }

    /* Card dei rendimenti */
    [data-testid="stMetric"] {
        background: #0a0a0a !important;
        padding: 25px !important;
        border-radius: 15px;
        border: 1px solid #00ff00 !important;
        box-shadow: 0 0 15px rgba(0, 255, 0, 0.2);
    }
    
    /* Valori metriche Verde Neon */
    [data-testid="stMetricValue"] {
        color: #00ff00 !important;
        font-size: 45px !important;
        text-shadow: 0 0 10px rgba(0, 255, 0, 0.8);
    }
    
    /* Titoli */
    h1, h2, h3 { 
        color: #00ff00 !important; 
        text-transform: uppercase;
        border-bottom: 1px solid #333;
        padding-bottom: 10px;
    }

    /* Colore degli slider */
    .stSlider [data-baseweb="slider"] {
        background-color: #00ff00;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("📟 DASHBOARD ELITE 70/30")

# 2. CONFIGURAZIONE STRATEGIA (Sidebar)
with st.sidebar:
    st.header("⚙️ ASSET & PESI")
    
    st.subheader("CORE (70%)")
    e1 = st.text_input("ETF 1", value="VWCE.DE")
    p1 = st.slider(f"% {e1}", 0, 100, 35) / 100
    e2 = st.text_input("ETF 2", value="QDVE.DE")
    p2 = st.slider(f"% {e2}", 0, 100, 35) /
