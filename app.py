import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import numpy as np

# 1. SETUP ESTETICO PREMIUM
st.set_page_config(page_title="Wealth Terminal Elite", layout="wide")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&family=JetBrains+Mono&display=swap');
    
    .stApp { background-color: #1e242b !important; font-family: 'Inter', sans-serif !important; }
    [data-testid="stSidebar"] { background-color: #161b22 !important; border-right: 1px solid #2d333b; }
    
    /* Card Design */
    .pro-card {
        background: linear-gradient(145deg, #262c36, #1e242b);
        border: 1px solid #3d444d;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        margin-bottom: 15px;
    }
    .label-card { color: #8b949e; font-size: 0.8rem; text-transform: uppercase; margin-bottom: 5px; }
    .value-card { color: #50fa7b; font-size: 1.8rem; font-weight: 700; font-family: 'JetBrains Mono'; }

    /* Tabelle con testo Bianco */
    [data-testid="stTable"] td, [data-testid="stTable"] th {
        color: white !important;
        border-bottom: 1px solid #30363d !important;
    }
    [data-testid="stTable"] { background-color: #21262d !important; }

    .stButton>button {
        width: 100%; background-color: #38d39f !important; color: #161b22 !important;
        font-weight: 700; border-radius: 8px; height: 3.5em; border: none;
    }
</style>
""", unsafe_allow_html=True)

# 2. SIDEBAR: CONFIGURAZIONE
with st.sidebar:
    st.markdown("<h2 style='color: #38d39f;'>⚙️ STRATEGY</h2>", unsafe_allow_html=True)
    
    # Asset Inputs [cite: 2026-02-15]
    st.markdown("🌍 **CORE MONDO**")
    isin1 = st.text_input("ISIN 1", value="VWCE.DE")
    p1 = st.slider("% Asset 1", 0, 100, 45)
    
    st.markdown("💻 **CORE TECH**")
    isin2 = st.text_input("ISIN 2", value="QDVE.DE")
    p2 = st.slider("% Asset 2", 0, 100, 25)
    
    st.markdown("🟡 **GOLD & MINERS**")
    isin3 = st.text_input("ISIN 3", value="SGLN.L")
    p3 = st.slider("% Asset 3", 0, 100, 20)
    isin4 = st.text_input("ISIN 4", value="GDXJ")
    p4 = st.slider("% Asset 4", 0, 100, 10)
    
    st.markdown("---")
    cap = st.number_input("Capitale Attuale (€)", value=10000)
    pac = st.number_input("PAC Mensile (€)", value=500)
    
    st.markdown("### 📈 STIMA CAGR %")
    cagr_core = st.number_input("CAGR Core %", value=9.0)
    cagr_sat = st.number_input("CAGR Satellite %", value=4.5)
    
    attivato = st.button("AGGIORNA ANALISI")

# 3. AREA CENTRALE (SEMPRE VISIBILE)
st.markdown("<h1 style='color: white;'>ANALISI PATRIMONIALE</h1>", unsafe_allow_html=True)

# Logica di calcolo CAGR e Proiezione [cite: 2026-02-14, 2026-02-15]
peso_core = (p1 + p2) / 100
peso_sat = (p3 + p4) / 100
cagr_totale = (peso_core * cagr_core) + (peso_sat * cagr_sat)
r_m = (1 + cagr_totale/100)**(1/12) - 1
m20 = 20 * 12

# Valori per visualizzazione
lordo_20 = cap * (1 + r_m)**m20 + pac * (((1 + r_m)**m20 - 1) / r_m)
versato_20 = cap + (pac * m20)
netto_20 = lordo_20 - (lordo_20 - versato_20) * 0.26
rendita_20 = (netto_20 * 0.04) / 12

# UI: CARD SUPERIORI
c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown(f"<div class='pro-card'><p class='label-card'>Netto (20Y)</p><p class='value-card'>{netto_20:,.0f} €</p></div>", unsafe_allow_html=True)
with c2:
    st.markdown(f"<div class='pro-card'><p class='label-card'>Rendita Mensile</p><p class='value-card' style='color:#8be9fd;'>{rendita_20:,.0f} €</p></div>", unsafe_allow_html=True)
with c3:
    st.markdown(f"<div class='pro-card'><p class='label-card'>CAGR Totale</p><p class='value-card' style='color:#ffffff;'>{cagr_totale:.2f}%</p></div>", unsafe_allow_html=True)
with c4:
    st.markdown(f"<div class='pro-card'><p class='label-card'>Totale Versato</p><p class='value-card' style='color:#8b949e;'>{versato_20:,.0f} €</p></div>", unsafe_allow_html=True)

# TABELLA ORDINI
st.markdown("<h3 style='color: white; margin-top: 20px;'>⚖️ Piano Ordini Corrente</h3>", unsafe_allow_html=True)
tot_inv = cap + pac
ordini_df = pd.DataFrame([
    {"ASSET": isin1, "ALLOCAZIONE": f"{p1}%", "TARGET (€)": f"{(tot_inv * p1/100):,.2f}"},
    {"ASSET": isin2, "ALLOCAZIONE": f"{p2}%", "TARGET (€)": f"{(tot_inv * p2/100):,.2f}"},
    {"ASSET": isin3, "ALLOCAZIONE": f"{p3}%", "TARGET (€)": f"{(tot_inv * p3/100):,.2f}"},
    {"ASSET": isin4, "ALLOCAZIONE": f"{p4}%", "TARGET (€)": f"{(tot_inv * p4/100):,.2f}"},
])
st.table(ordini_df)

# GRAFICO
st.markdown("<h3 style='color: white; margin-top: 20px;'>📈 Evoluzione Patrimoniale</h3>", unsafe_allow_html=True)
timeline = np.arange(0, m20 + 1)
y_lordo = [cap * (1+r_m)**m + pac * (((1+r_m)**m - 1)/r_m) for m in timeline]
fig = go.Figure()
fig.add_trace(go.Scatter(x=timeline/12, y=y_lordo, fill='tozeroy', name='Crescita Lorda', line=dict(color='#38d39f', width=4)))
fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color="#8b949e"), height=350)
st.plotly_chart(fig, use_container_width=True)
