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
    
    /* FORZA VISIBILITÀ ETICHETTE (Quelle che non vedevi negli screenshot) */
    label, p, span, .stMarkdown { color: #ffffff !important; font-weight: 600 !important; }
    
    /* Input Fields: sfondo scuro, testo verde smeraldo */
    input { background-color: #0d1117 !important; color: #50fa7b !important; border: 1px solid #30363d !important; }

    .pro-card {
        background: linear-gradient(145deg, #262c36, #1e242b);
        border: 1px solid #3d444d;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        margin-bottom: 15px;
    }
    .value-card { color: #50fa7b !important; font-size: 1.8rem !important; font-weight: 700; }
    
    [data-testid="stTable"] td, [data-testid="stTable"] th { color: white !important; }
</style>
""", unsafe_allow_html=True)

# 2. SIDEBAR - INPUT MODIFICABILI
with st.sidebar:
    st.markdown("<h2 style='color: #38d39f;'>🕹️ COMANDI</h2>", unsafe_allow_html=True)
    
    # Questi campi ora accettano qualsiasi cifra inserita dall'utente
    capitale_input = st.number_input("CAPITALE ATTUALE (€)", value=10000, step=1000)
    pac_input = st.number_input("PAC MENSILE (€)", value=500, step=50)
    
    st.markdown("---")
    st.markdown("### 📊 ALLOCAZIONE STRATEGICA")
    # Allineato alla strategia dell'utente [cite: 2026-02-15]
    p_core = st.slider("% CORE (VWCE + QDVE)", 0, 100, 70)
    p_sat = st.slider("% SATELLITE (GOLD)", 0, 100, 30)
    
    st.markdown("### 📈 STIMA CAGR %")
    c_core = st.number_input("Rendimento Core %", value=9.0)
    c_sat = st.number_input("Rendimento Satellite %", value=4.5)

# 3. MOTORE DI CALCOLO (REATTIVO)
cagr_pesato = ((p_core/100) * c_core) + ((p_sat/100) * c_sat)
r_m = (1 + cagr_pesato/100)**(1/12) - 1
mesi = 20 * 12

# Calcolo Patrimonio finale
val_lordo = capitale_input * (1 + r_m)**mesi + pac_input * (((1 + r_m)**mesi - 1) / r_m)
tot_versato = capitale_input + (pac_input * mesi)
netto = val_lordo - ((val_lordo - tot_versato) * 0.26)
rendita_m = (netto * 0.04) / 12

# 4. DASHBOARD
st.markdown("<h1 style='color: white;'>ANALISI PATRIMONIALE</h1>", unsafe_allow_html=True)

# Visualizzazione Risultati
c1, c2, c3 = st.columns(3)
with c1:
    st.markdown(f"<div class='pro-card'><p>PATRIMONIO NETTO (20Y)</p><p class='value-card'>{netto:,.0f} €</p></div>", unsafe_allow_html=True)
with c2:
    st.markdown(f"<div class='pro-card'><p>RENDITA MENSILE</p><p class='value-card' style='color:#8be9fd;'>{rendita_m:,.0f} €</p></div>", unsafe_allow_html=True)
with c3:
    st.markdown(f"<div class='pro-card'><p>CAGR STRATEGIA</p><p class='value-card' style='color:#ffffff;'>{cagr_pesato:.2f}%</p></div>", unsafe_allow_html=True)

# Grafico di crescita visibile
st.markdown("### 📈 Crescita Proiettata")
time = np.arange(0, mesi + 1)
y = [capitale_input * (1+r_m)**m + pac_input * (((1+r_m)**m - 1)/r_m) for m in time]
fig = go.Figure(go.Scatter(x=time/12, y=y, fill='tozeroy', line=dict(color='#38d39f', width=4)))
fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color="white"), height=350)
st.plotly_chart(fig, use_container_width=True)
