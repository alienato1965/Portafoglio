import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np

# 1. SETUP ESTETICO (SLATE DARK)
st.set_page_config(page_title="Wealth Terminal Elite", layout="wide")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700&family=JetBrains+Mono&display=swap');
    .stApp { background-color: #1e242b !important; font-family: 'Inter', sans-serif !important; }
    [data-testid="stSidebar"] { background-color: #161b22 !important; border-right: 1px solid #2d333b; }
    
    /* Card con contrasto migliorato per i testi */
    .pro-card {
        background: linear-gradient(145deg, #262c36, #1e242b);
        border: 1px solid #3d444d;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        margin-bottom: 15px;
    }
    .label-card { color: #8b949e !important; font-size: 0.8rem; text-transform: uppercase; font-weight: bold; }
    .value-card { color: #50fa7b !important; font-size: 1.8rem; font-weight: 700; font-family: 'JetBrains Mono'; }
    
    /* Forza testo bianco nelle tabelle */
    [data-testid="stTable"] td, [data-testid="stTable"] th { color: white !important; }
    
    .stButton>button {
        width: 100%; background-color: #38d39f !important; color: #161b22 !important;
        font-weight: 700; border-radius: 8px; height: 3.5em;
    }
</style>
""", unsafe_allow_html=True)

# 2. SIDEBAR (LOGICA ASSET 70/30)
with st.sidebar:
    st.markdown("<h2 style='color: #38d39f;'>⚙️ STRATEGY</h2>", unsafe_allow_html=True)
    
    # Core (70%)
    isin1 = st.text_input("ISIN Core 1", value="VWCE.DE")
    p1 = st.slider("% Core 1", 0, 100, 45)
    isin2 = st.text_input("ISIN Core 2", value="QDVE.DE")
    p2 = st.slider("% Core 2", 0, 100, 25)
    
    # Satellite (30%)
    isin3 = st.text_input("ISIN Sat 1", value="SGLN.L")
    p3 = st.slider("% Sat 1", 0, 100, 20)
    isin4 = st.text_input("ISIN Sat 2", value="GDXJ")
    p4 = st.slider("% Sat 2", 0, 100, 10)
    
    st.markdown("---")
    capitale = st.number_input("Capitale Attuale (€)", value=10000)
    pac_mensile = st.number_input("PAC Mensile (€)", value=500)
    
    # Calcolo CAGR Dinamico
    c_core = st.number_input("CAGR Core %", value=9.0)
    c_sat = st.number_input("CAGR Sat %", value=4.5)
    
    # Calcolo pesato del CAGR
    peso_c = (p1 + p2) / 100
    peso_s = (p3 + p4) / 100
    cagr_tot = (peso_c * c_core) + (peso_s * c_sat)

# 3. AREA CENTRALE (CALCOLO DINAMICO SENZA ERRORI)
st.markdown("<h1 style='color: white;'>ANALISI PATRIMONIALE</h1>", unsafe_allow_html=True)

# Calcolo Proiezione 20 Anni
r_m = (1 + cagr_tot/100)**(1/12) - 1
m20 = 20 * 12
valore_lordo = capitale * (1 + r_m)**m20 + pac_mensile * (((1 + r_m)**m20 - 1) / r_m)
tot_versato = capitale + (pac_mensile * m20)
plusvalenza = valore_lordo - tot_versato
tasse = plusvalenza * 0.26
netto_20 = valore_lordo - tasse
rendita_mens = (netto_20 * 0.04) / 12  # Prelievo 4%

# UI: CARD RISULTATI (Corrette senza errori di sintassi)
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown(f"<div class='pro-card'><p class='label-card'>Netto 20Y</p><p class='value-card'>{netto_20:,.0f} €</p></div>", unsafe_allow_html=True)
with col2:
    st.markdown(f"<div class='pro-card'><p class='label-card'>Rendita Mensile</p><p class='value-card' style='color:#8be9fd;'>{rendita_mens:,.0f} €</p></div>", unsafe_allow_html=True)
with col3:
    st.markdown(f"<div class='pro-card'><p class='label-card'>CAGR Strategia</p><p class='value-card' style='color:#ffffff;'>{cagr_tot:.2f}%</p></div>", unsafe_allow_html=True)
with col4:
    st.markdown(f"<div class='pro-card'><p class='label-card'>Versato</p><p class='value-card' style='color:#8b949e;'>{tot_versato:,.0f} €</p></div>", unsafe_allow_html=True)

# TABELLA ORDINI SEMPRE AGGIORNATA
st.markdown("<h3 style='color: white;'>⚖️ Piano Ordini Mensile</h3>", unsafe_allow_html=True)
tot_inv = capitale + pac_mensile
df_ordini = pd.DataFrame([
    {"ASSET": isin1, "ALLOCAZIONE": f"{p1}%", "TARGET (€)": f"{(tot_inv * p1/100):,.2f}"},
    {"ASSET": isin2, "ALLOCAZIONE": f"{p2}%", "TARGET (€)": f"{(tot_inv * p2/100):,.2f}"},
    {"ASSET": isin3, "ALLOCAZIONE": f"{p3}%", "TARGET (€)": f"{(tot_inv * p3/100):,.2f}"},
    {"ASSET": isin4, "ALLOCAZIONE": f"{p4}%", "TARGET (€)": f"{(tot_inv * p4/100):,.2f}"},
])
st.table(df_ordini)

# GRAFICO DI CRESCITA
timeline = np.arange(0, m20 + 1)
y_growth = [capitale * (1+r_m)**m + pac_mensile * (((1+r_m)**m - 1)/r_m) for m in timeline]
fig = go.Figure()
fig.add_trace(go.Scatter(x=timeline/12, y=y_growth, fill='tozeroy', name='Patrimonio Lordo', line=dict(color='#38d39f', width=4)))
fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color="white"), height=350, margin=dict(t=0, b=0))
st.plotly_chart(fig, use_container_width=True)
