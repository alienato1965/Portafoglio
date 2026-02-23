import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np

# 1. CONFIGURAZIONE ESTETICA ELITE SLATE
st.set_page_config(page_title="Wealth Terminal Elite", layout="wide")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&family=JetBrains+Mono&display=swap');
    
    .stApp { background-color: #1e242b !important; font-family: 'Inter', sans-serif !important; }
    [data-testid="stSidebar"] { background-color: #161b22 !important; border-right: 1px solid #2d333b; padding-top: 2rem; }
    
    /* Forza visibilità etichette in bianco */
    label, p, span, h1, h2, h3 { color: #ffffff !important; font-weight: 600 !important; }
    
    /* Input Fields Style */
    input { background-color: #0d1117 !important; color: #50fa7b !important; border: 1px solid #30363d !important; }
    
    /* Card Design per Risultati */
    .pro-card {
        background: linear-gradient(145deg, #262c36, #1e242b);
        border: 1px solid #3d444d;
        border-radius: 12px;
        padding: 25px;
        text-align: center;
        margin-bottom: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }
    .label-card { color: #8b949e !important; font-size: 0.85rem !important; text-transform: uppercase; letter-spacing: 1px; }
    .value-card { color: #50fa7b !important; font-size: 2.2rem !important; font-weight: 700 !important; font-family: 'JetBrains Mono'; }
    
    /* Tabelle High Contrast */
    [data-testid="stTable"] { background-color: #21262d !important; border-radius: 8px; border: 1px solid #30363d; }
    [data-testid="stTable"] td, [data-testid="stTable"] th { 
        color: white !important; 
        border-bottom: 1px solid #30363d !important; 
        padding: 15px !important;
        text-align: left !important;
    }
</style>
""", unsafe_allow_html=True)

# 2. SIDEBAR - INPUT REATTIVI (CAPITALE, PAC, ASSET)
with st.sidebar:
    st.markdown("<h2 style='color: #38d39f; margin-bottom:20px;'>🛠️ TERMINALE</h2>", unsafe_allow_html=True)
    
    # Input Finanziari
    capitale_f = st.number_input("CAPITALE ATTUALE (€)", value=10000, step=1000)
    pac_f = st.number_input("PAC MENSILE (€)", value=500, step=50)
    
    st.markdown("---")
    
    # Slot Asset Strategia 70/30 [cite: 2026-02-15]
    st.markdown("### 🌍 CORE (70%)")
    etf1 = st.text_input("Core Mondo (45%)", value="VWCE.DE")
    etf2 = st.text_input("Core IT Tech (25%)", value="QDVE.DE")
    
    st.markdown("### 🛰️ SATELLITE (30%)")
    etf3 = st.text_input("Physical Gold (20%)", value="SGLN.L")
    etf4 = st.text_input("Junior Miners (10%)", value="GDXJ")
    
    st.markdown("---")
    
    # Rendimenti CAGR [cite: 2026-02-15]
    c_core = st.number_input("Stima CAGR Core %", value=9.0, step=0.1)
    c_sat = st.number_input("Stima CAGR Satellite %", value=4.5, step=0.1)

# 3. MOTORE DI CALCOLO INTERESSE COMPOSTO [cite: 2026-02-15]
cagr_pesato = (0.70 * c_core) + (0.30 * c_sat)
r_m = (1 + cagr_pesato/100)**(1/12) - 1

def proietta_dati(anni):
    m = anni * 12
    # Formula interesse composto: Capitale + Rendita PAC [cite: 2026-02-15]
    lordo = capitale_f * (1 + r_m)**m + pac_f * (((1 + r_m)**m - 1) / r_m)
    versato = capitale_f + (pac_f * m)
    interessi = lordo - versato
    netto = lordo - (interessi * 0.26) # Tassazione Capital Gain 26% [cite: 2026-02-15]
    return netto, versato, interessi

# 4. AREA DASHBOARD PRINCIPALE
st.markdown("<h1 style='text-align: center; color: white; margin-bottom: 40px;'>Wealth Analysis Terminal</h1>", unsafe_allow_html=True)

# Card di Sintesi (Orizzonte 20 Anni)
netto_20, versato_20, int_20 = proietta_dati(20)
c1, c2, c3 = st.columns(3)
with c1:
    st.markdown(f"<div class='pro-card'><p class='label-card'>Netto Finale (20 Anni)</p><p class='value-card'>{netto_20:,.0f} €</p></div>", unsafe_allow_html=True)
with c2:
    st.markdown(f"<div class='pro-card'><p class='label-card'>Rendita Mensile (4%)</p><p class='value-card' style='color:#8be9fd;'>{(netto_20*0.04)/12:,.0f} €</p></div>", unsafe_allow_html=True)
with c3:
    st.markdown(f"<div class='pro-card'><p class='label-card'>CAGR Strategia</p><p class='value-card' style='color:#ffffff;'>{cagr_pesato:.2f}%</p></div>", unsafe_allow_html=True)

# SVILUPPO TEMPORALE 5-10-15-20 ANNI [cite: 2026-02-15]
st.markdown("### ⏳ Sviluppo Esponenziale del Patrimonio")
timeline_rows = []
for a in [5, 10, 15, 20]:
    n, v, i = proietta_dati(a)
    timeline_rows.append({
        "Orizzonte": f"{a} Anni",
        "Capitale Versato": f"{v:,.0f} €",
        "Interessi Maturati": f"{i:,.0f} €",
        "Patrimonio Netto": f"{n:,.0f} €",
        "Rendita Mensile": f"{(n*0.04)/12:,.0f} €"
    })
st.table(pd.DataFrame(timeline_rows))

# PIANO ACQUISTI MENSILE
st.markdown("### ⚖️ Piano Ordini Corrente (Asset Allocation)")
tot_investimento = capitale_f + pac_f
ordini = [
    {"Asset": etf1, "Tag": "Core Mondo", "Allocazione": "45%", "Quota (€)": f"{(tot_investimento * 0.45):,.2f}"},
    {"Asset": etf2, "Tag": "Core Tech", "Allocazione": "25%", "Quota (€)": f"{(tot_investimento * 0.25):,.2f}"},
    {"Asset": etf3, "Tag": "Sat Oro", "Allocazione": "20%", "Quota (€)": f"{(tot_investimento * 0.20):,.2f}"},
    {"Asset": etf4, "Tag": "Sat Miners", "Allocazione": "10%", "Quota (€)": f"{(tot_investimento * 0.10):,.2f}"},
]
st.table(pd.DataFrame(ordini))

# GRAFICO INTERATTIVO
time_axis = np.arange(0, 20 * 12 + 1)
growth_curve = [capitale_f * (1+r_m)**m + pac_f * (((1+r_m)**m - 1)/r_m) for m in time_axis]

fig = go.Figure(go.Scatter(x=time_axis/12, y=growth_curve, fill='tozeroy', name='Patrimonio Lordo', line=dict(color='#38d39f', width=4)))
fig.update_layout(
    paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
    font=dict(color="white"), height=400, margin=dict(t=20, b=20, l=10, r=10),
    xaxis=dict(title="Anni di Investimento", showgrid=True, gridcolor='#2d333b'),
    yaxis=dict(title="Valore (€)", showgrid=True, gridcolor='#2d333b')
)
st.plotly_chart(fig, use_container_width=True)
