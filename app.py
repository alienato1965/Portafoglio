import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import numpy as np

# 1. SETUP ESTETICO PREMIUM
st.set_page_config(page_title="Wealth Terminal Elite", layout="wide")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
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
    .value-card { color: #50fa7b; font-size: 1.8rem; font-weight: 700; }

    /* Inputs */
    .stTextInput>div>div>input { background-color: #1c2128 !important; color: white !important; border: 1px solid #30363d !important; }
    
    /* Button */
    .stButton>button {
        width: 100%; background-color: #38d39f !important; color: #161b22 !important;
        font-weight: 700; border-radius: 8px; height: 3em; border: none;
    }
</style>
""", unsafe_allow_html=True)

# 2. SIDEBAR: INSERIMENTO ISIN/TICKER
with st.sidebar:
    st.markdown("### 🛠️ CONFIGURAZIONE ASSET")
    
    st.markdown("---")
    st.markdown("🌍 **CORE MONDO (45%)**")
    isin1 = st.text_input("Inserisci ISIN/Ticker 1", value="VWCE.DE", key="isin1")
    p1 = st.slider("% Asset 1", 0, 100, 45, key="p1")
    
    st.markdown("💻 **CORE TECH (25%)**")
    isin2 = st.text_input("Inserisci ISIN/Ticker 2", value="QDVE.DE", key="isin2")
    p2 = st.slider("% Asset 2", 0, 100, 25, key="p2")
    
    st.markdown("🟡 **SATELLITE ORO (20%)**")
    isin3 = st.text_input("Inserisci ISIN/Ticker 3", value="SGLN.L", key="isin3")
    p3 = st.slider("% Asset 3", 0, 100, 20, key="p3")
    
    st.markdown("⛏️ **SATELLITE MINERS (10%)**")
    isin4 = st.text_input("Inserisci ISIN/Ticker 4", value="GDXJ", key="isin4")
    p4 = st.slider("% Asset 4", 0, 100, 10, key="p4")
    
    st.markdown("---")
    cap = st.number_input("Capitale Attuale (€)", value=10000)
    pac = st.number_input("PAC Mensile (€)", value=500)
    cagr = st.slider("CAGR Atteso (%)", 1.0, 12.0, 7.5)
    
    attivato = st.button("AGGIORNA ANALISI")

# 3. AREA DASHBOARD
st.markdown("<h1>ANALISI PATRIMONIALE</h1>", unsafe_allow_html=True)

if attivato:
    # Calcolo Proiezioni [cite: 2026-02-15]
    r_m = (1 + cagr/100)**(1/12) - 1
    m20 = 20 * 12
    lordo_20 = cap * (1 + r_m)**m20 + pac * (((1 + r_m)**m20 - 1) / r_m)
    versato_20 = cap + (pac * m20)
    netto_20 = lordo_20 - (lordo_20 - versato_20) * 0.26
    rendita_20 = (netto_20 * 0.04) / 12

    # UI: CARD
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f"<div class='pro-card'><p class='label-card'>Netto (20 Anni)</p><p class='value-card'>{netto_20:,.0f} €</p></div>", unsafe_allow_html=True)
    with c2:
        st.markdown(f"<div class='pro-card'><p class='label-card'>Rendita Mensile</p><p class='value-card'>{rendita_20:,.0f} €</p></div>", unsafe_allow_html=True)
    with c3:
        st.markdown(f"<div class='pro-card'><p class='label-card'>Capitale Versato</p><p class='value-card' style='color:#8b949e;'>{versato_20:,.0f} €</p></div>", unsafe_allow_html=True)

    # TABELLA ORDINI CON ISIN
    st.markdown("### ⚖️ Piano Ordini Corrente")
    tot_port = cap + pac
    ordini = [
        {"ASSET": isin1, "ALLOCAZIONE": f"{p1}%", "VALORE TARGET": f"{(tot_port * p1/100):,.2f} €"},
        {"ASSET": isin2, "ALLOCAZIONE": f"{p2}%", "VALORE TARGET": f"{(tot_port * p2/100):,.2f} €"},
        {"ASSET": isin3, "ALLOCAZIONE": f"{p3}%", "VALORE TARGET": f"{(tot_port * p3/100):,.2f} €"},
        {"ASSET": isin4, "ALLOCAZIONE": f"{p4}%", "VALORE TARGET": f"{(tot_port * p4/100):,.2f} €"},
    ]
    st.table(pd.DataFrame(ordini))

    # GRAFICO
    timeline = np.arange(0, m20 + 1)
    y_lordo = [cap * (1+r_m)**m + pac * (((1+r_m)**m - 1)/r_m) for m in timeline]
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=timeline/12, y=y_lordo, name='Crescita Lorda', line=dict(color='#38d39f', width=4)))
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color="white"), height=350)
    st.plotly_chart(fig, use_container_width=True)

else:
    st.info("Configura i tuoi ISIN e clicca sul bottone verde per iniziare l'analisi.")
