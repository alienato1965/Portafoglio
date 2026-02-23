import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np

# 1. SETUP ESTETICO - TESTI BIANCHI FORZATI
st.set_page_config(page_title="Wealth Terminal Elite", layout="wide")

st.markdown("""
<style>
    .stApp { background-color: #1e242b !important; }
    [data-testid="stSidebar"] { background-color: #161b22 !important; border-right: 1px solid #2d333b; }
    
    /* FORZA TESTI ETICHETTE IN BIANCO */
    label, p, span, .stMarkdown { color: #ffffff !important; font-weight: 600 !important; }
    
    .pro-card {
        background: linear-gradient(145deg, #262c36, #1e242b);
        border: 1px solid #3d444d;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        margin-bottom: 15px;
    }
    .value-card { color: #50fa7b !important; font-size: 1.8rem; font-weight: 700; }
    
    /* TABELLE */
    [data-testid="stTable"] td, [data-testid="stTable"] th { color: white !important; }
</style>
""", unsafe_allow_html=True)

# 2. SIDEBAR - DATI UTENTE
with st.sidebar:
    st.markdown("### ⚙️ CONFIGURAZIONE")
    capitale = st.number_input("Capitale Attuale (€)", value=10000)
    pac = st.number_input("PAC Mensile (€)", value=500)
    
    st.markdown("---")
    p1 = st.slider("% Asset Core", 0, 100, 70)
    p2 = st.slider("% Asset Satelliti", 0, 100, 30)
    
    c_core = st.number_input("CAGR Stima Core %", value=9.0)
    c_sat = st.number_input("CAGR Stima Sat %", value=4.5)

# 3. CALCOLO REATTIVO (Ogni modifica aggiorna i numeri)
# Strategia: 70% Core, 30% Satellite [cite: 2026-02-14, 2026-02-15]
cagr_tot = ((p1/100) * c_core) + ((p2/100) * c_sat)
r_m = (1 + cagr_tot/100)**(1/12) - 1
m20 = 20 * 12

val_lordo = capitale * (1 + r_m)**m20 + pac * (((1 + r_m)**m20 - 1) / r_m)
versato = capitale + (pac * m20)
netto = val_lordo - ((val_lordo - versato) * 0.26)
rendita = (netto * 0.04) / 12

# 4. DASHBOARD CENTRALE
st.markdown("<h1>ANALISI PATRIMONIALE</h1>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(f"<div class='pro-card'><p>NETTO 20 ANNI</p><p class='value-card'>{netto:,.0f} €</p></div>", unsafe_allow_html=True)
with col2:
    st.markdown(f"<div class='pro-card'><p>RENDITA MENSILE</p><p class='value-card' style='color:#8be9fd;'>{rendita:,.0f} €</p></div>", unsafe_allow_html=True)
with col3:
    st.markdown(f"<div class='pro-card'><p>CAGR STRATEGIA</p><p class='value-card' style='color:#ffffff;'>{cagr_tot:.2f}%</p></div>", unsafe_allow_html=True)

# Grafico semplice e pulito
timeline = np.arange(0, m20 + 1)
y_p = [capitale * (1+r_m)**m + pac * (((1+r_m)**m - 1)/r_m) for m in timeline]
fig = go.Figure(go.Scatter(x=timeline/12, y=y_p, fill='tozeroy', line=dict(color='#38d39f')))
fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color="white"), height=300)
st.plotly_chart(fig, use_container_width=True)
