import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np

# 1. SETUP ESTETICO - TESTO BIANCO E ALTO CONTRASTO
st.set_page_config(page_title="Wealth Terminal Elite", layout="wide")

st.markdown("""
<style>
    .stApp { background-color: #1e242b !important; }
    [data-testid="stSidebar"] { background-color: #161b22 !important; border-right: 1px solid #2d333b; }
    
    /* FORZA VISIBILITÀ ETICHETTE BIANCHE */
    label, p, span, h1, h2, h3 { color: #ffffff !important; font-weight: 600 !important; }
    
    /* Campi Input ISIN */
    .stTextInput>div>div>input {
        background-color: #0d1117 !important;
        color: #8be9fd !important; /* Colore azzurro per distinguere i testi inseriti */
        border: 1px solid #30363d !important;
    }

    .pro-card {
        background: linear-gradient(145deg, #262c36, #1e242b);
        border: 1px solid #3d444d;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        margin-bottom: 15px;
    }
    .value-card { color: #50fa7b !important; font-size: 1.8rem !important; font-weight: 700; }
    
    /* Tabelle High Contrast */
    [data-testid="stTable"] { background-color: #21262d !important; }
    [data-testid="stTable"] td, [data-testid="stTable"] th { color: white !important; border-bottom: 1px solid #30363d !important; }
</style>
""", unsafe_allow_html=True)

# 2. SIDEBAR - INPUT MODIFICABILI E SLOT ETF
with st.sidebar:
    st.markdown("<h2 style='color: #38d39f;'>⚙️ CONFIGURAZIONE</h2>", unsafe_allow_html=True)
    
    capitale_input = st.number_input("CAPITALE ATTUALE (€)", value=10000)
    pac_input = st.number_input("PAC MENSILE (€)", value=500)
    
    st.markdown("---")
    
    # --- SLOT CORE (70%) --- [cite: 2026-02-15]
    st.markdown("### 🌍 SEZIONE CORE (70%)")
    etf_core1 = st.text_input("ETF 1 (Mondo - 45%)", value="VWCE")
    etf_core2 = st.text_input("ETF 2 (Tech - 25%)", value="QDVE")
    
    # --- SLOT SATELLITE (30%) --- [cite: 2026-02-15]
    st.markdown("### 🛰️ SEZIONE SATELLITE (30%)")
    etf_sat1 = st.text_input("ETF 3 (Oro - 20%)", value="SGLN")
    etf_sat2 = st.text_input("ETF 4 (Miners - 10%)", value="GDXJ")
    
    st.markdown("---")
    st.markdown("### 📈 RENDIMENTI ATTESI")
    c_core = st.number_input("CAGR Core %", value=9.0)
    c_sat = st.number_input("CAGR Satellite %", value=4.5)

# 3. MOTORE DI CALCOLO
# Calcolo pesato basato sulla tua strategia CORE 70% (45+25) e SAT 30% (20+10) [cite: 2026-02-15]
cagr_pesato = (0.70 * c_core) + (0.30 * c_sat)
r_m = (1 + cagr_pesato/100)**(1/12) - 1
anni = 20
mesi = anni * 12

val_lordo = capitale_input * (1 + r_m)**mesi + pac_input * (((1 + r_m)**mesi - 1) / r_m)
tot_versato = capitale_input + (pac_input * mesi)
netto = val_lordo - ((val_lordo - tot_versato) * 0.26)
rendita_m = (netto * 0.04) / 12

# 4. DASHBOARD
st.markdown("<h1>DASHBOARD PATRIMONIALE</h1>", unsafe_allow_html=True)

# Visualizzazione Risultati
c1, c2, c3 = st.columns(3)
with c1:
    st.markdown(f"<div class='pro-card'><p>NETTO A {anni} ANNI</p><p class='value-card'>{netto:,.0f} €</p></div>", unsafe_allow_html=True)
with c2:
    st.markdown(f"<div class='pro-card'><p>RENDITA MENSILE</p><p class='value-card' style='color:#8be9fd;'>{rendita_m:,.0f} €</p></div>", unsafe_allow_html=True)
with c3:
    st.markdown(f"<div class='pro-card'><p>CAGR STRATEGIA</p><p class='value-card' style='color:#ffffff;'>{cagr_pesato:.2f}%</p></div>", unsafe_allow_html=True)

# TABELLA ORDINI CON GLI ETF INSERITI
st.markdown("### ⚖️ Piano Acquisti (Rebalancing)")
tot_da_investire = capitale_input + pac_input
ordini_data = [
    {"Asset": etf_core1, "Tipo": "Core Mondo", "Allocazione": "45%", "Target (€)": f"{(tot_da_investire * 0.45):,.2f}"},
    {"Asset": etf_core2, "Tipo": "Core Tech", "Allocazione": "25%", "Target (€)": f"{(tot_da_investire * 0.25):,.2f}"},
    {"Asset": etf_sat1, "Tipo": "Sat Oro", "Allocazione": "20%", "Target (€)": f"{(tot_da_investire * 0.20):,.2f}"},
    {"Asset": etf_sat2, "Tipo": "Sat Miners", "Allocazione": "10%", "Target (€)": f"{(tot_da_investire * 0.10):,.2f}"},
]
st.table(pd.DataFrame(ordini_data))

# Grafico di crescita
st.markdown("### 📈 Evoluzione Strategia 70/30")
time = np.arange(0, mesi + 1)
y = [capitale_input * (1+r_m)**m + pac_input * (((1+r_m)**m - 1)/r_m) for m in time]
fig = go.Figure(go.Scatter(x=time/12, y=y, fill='tozeroy', line=dict(color='#38d39f', width=4)))
fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color="white"), height=350)
st.plotly_chart(fig, use_container_width=True)
