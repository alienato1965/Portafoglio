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
    
    /* FORZA VISIBILITÀ TESTO BIANCO */
    label, p, span, h1, h2, h3 { color: #ffffff !important; font-weight: 600 !important; }
    
    .pro-card {
        background: linear-gradient(145deg, #262c36, #1e242b);
        border: 1px solid #3d444d;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        margin-bottom: 15px;
    }
    .value-card { color: #50fa7b !important; font-size: 1.8rem !important; font-weight: 700; }
    
    /* Tabelle con bordi chiari e testo bianco */
    [data-testid="stTable"] { background-color: #21262d !important; border-radius: 10px; overflow: hidden; }
    [data-testid="stTable"] td, [data-testid="stTable"] th { 
        color: white !important; 
        border-bottom: 1px solid #30363d !important; 
        padding: 12px !important;
    }
</style>
""", unsafe_allow_html=True)

# 2. SIDEBAR - INPUT REATTIVI
with st.sidebar:
    st.markdown("<h2 style='color: #38d39f;'>⚙️ PARAMETRI</h2>", unsafe_allow_html=True)
    capitale_f = st.number_input("CAPITALE ATTUALE (€)", value=10000)
    pac_f = st.number_input("PAC MENSILE (€)", value=500)
    
    st.markdown("---")
    st.markdown("### 🧬 ASSET SLOTS")
    etf1 = st.text_input("Core Mondo (45%)", value="VWCE")
    etf2 = st.text_input("Core Tech (25%)", value="QDVE")
    etf3 = st.text_input("Sat Oro (20%)", value="SGLN")
    etf4 = st.text_input("Sat Miners (10%)", value="GDXJ")
    
    st.markdown("---")
    c_core = st.number_input("CAGR Core %", value=9.0)
    c_sat = st.number_input("CAGR Satellite %", value=4.5)

# 3. MOTORE DI CALCOLO DINAMICO
cagr_pesato = (0.70 * c_core) + (0.30 * c_sat)
r_m = (1 + cagr_pesato/100)**(1/12) - 1

def calcola_patrimonio(anni):
    m = anni * 12
    lordo = capitale_f * (1 + r_m)**m + pac_f * (((1 + r_m)**m - 1) / r_m)
    versato = capitale_f + (pac_f * m)
    netto = lordo - ((lordo - versato) * 0.26)
    return netto

# Dati per la nuova tabella temporale
scenari = [5, 10, 15, 20]
dati_timeline = []
for a in scenari:
    patrimonio_n = calcola_patrimonio(a)
    rendita_n = (patrimonio_n * 0.04) / 12
    dati_timeline.append({
        "ORIZZONTE": f"{a} ANNI",
        "PATRIMONIO NETTO": f"{patrimonio_n:,.0f} €",
        "RENDITA MENS. (4%)": f"{rendita_n:,.0f} €"
    })

# 4. DASHBOARD
st.markdown("<h1>PROIEZIONE DI CRESCITA</h1>", unsafe_allow_html=True)

# Card Finali (20 Anni)
c1, c2, c3 = st.columns(3)
netto_20 = calcola_patrimonio(20)
with c1:
    st.markdown(f"<div class='pro-card'><p>OBIETTIVO 20 ANNI</p><p class='value-card'>{netto_20:,.0f} €</p></div>", unsafe_allow_html=True)
with c2:
    st.markdown(f"<div class='pro-card'><p>RENDITA TARGET</p><p class='value-card' style='color:#8be9fd;'>{(netto_20*0.04)/12:,.0f} €</p></div>", unsafe_allow_html=True)
with c3:
    st.markdown(f"<div class='pro-card'><p>CAGR ATTESO</p><p class='value-card' style='color:#ffffff;'>{cagr_pesato:.2f}%</p></div>", unsafe_allow_html=True)

# TABELLA SVILUPPO TEMPORALE (5-10-15-20 ANNI)
st.markdown("### ⏳ Sviluppo del Capitale nel Tempo")
st.table(pd.DataFrame(dati_timeline))

# PIANO ORDINI CORRENTE
st.markdown("### ⚖️ Piano Ordini Corrente (Asset Allocation)")
tot_da_inv = capitale_f + pac_f
ordini = [
    {"Asset": etf1, "Target %": "45%", "Quota Ordine (€)": f"{(tot_da_inv * 0.45):,.2f}"},
    {"Asset": etf2, "Target %": "25%", "Quota Ordine (€)": f"{(tot_da_inv * 0.25):,.2f}"},
    {"Asset": etf3, "Target %": "20%", "Quota Ordine (€)": f"{(tot_da_inv * 0.20):,.2f}"},
    {"Asset": etf4, "Target %": "10%", "Quota Ordine (€)": f"{(tot_da_inv * 0.10):,.2f}"},
]
st.table(pd.DataFrame(ordini))

# Grafico
time_plot = np.arange(0, 20 * 12 + 1)
y_plot = [capitale_f * (1+r_m)**m + pac_f * (((1+r_m)**m - 1)/r_m) for m in time_plot]
fig = go.Figure(go.Scatter(x=time_plot/12, y=y_plot, fill='tozeroy', line=dict(color='#38d39f', width=4)))
fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color="white"), height=300)
st.plotly_chart(fig, use_container_width=True)
