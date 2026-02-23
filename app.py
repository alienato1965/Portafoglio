import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np

# 1. CONFIGURAZIONE ESTETICA
st.set_page_config(page_title="Wealth Terminal Elite", layout="wide")

st.markdown("""
<style>
    .stApp { background-color: #1e242b !important; }
    [data-testid="stSidebar"] { background-color: #161b22 !important; border-right: 1px solid #2d333b; }
    label, p, span, h1, h2, h3 { color: #ffffff !important; font-weight: 600 !important; }
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
    [data-testid="stTable"] td, [data-testid="stTable"] th { color: white !important; border-bottom: 1px solid #30363d !important; }
</style>
""", unsafe_allow_html=True)

# 2. SIDEBAR - GESTIONE DINAMICA 6 SLOT
with st.sidebar:
    st.markdown("<h2 style='color: #38d39f;'>⚙️ CONFIGURAZIONE</h2>", unsafe_allow_html=True)
    capitale_f = st.number_input("CAPITALE ATTUALE (€)", value=10000)
    pac_f = st.number_input("PAC MENSILE (€)", value=500)
    
    st.markdown("---")
    st.markdown("### 🧬 ASSET ALLOCATION (Max 6)")
    
    assets = []
    tot_perc = 0
    
    # Creazione dinamica di 6 slot
    for i in range(1, 7):
        col_name, col_perc, col_cagr = st.columns([2, 1, 1])
        with col_name:
            name = st.text_input(f"ETF {i}", value=f"Asset {i}" if i > 4 else ["VWCE", "QDVE", "SGLN", "GDXJ"][i-1])
        with col_perc:
            perc = st.number_input(f"%##{i}", value=[45, 25, 20, 10, 0, 0][i-1], min_value=0, max_value=100, label_visibility="collapsed")
        with col_cagr:
            cagr = st.number_input(f"CAGR##{i}", value=[8.0, 12.0, 4.0, 5.0, 0.0, 0.0][i-1], step=0.5, label_visibility="collapsed")
        
        assets.append({"name": name, "perc": perc, "cagr": cagr})
        tot_perc += perc

    st.markdown(f"**Totale Allocazione: {tot_perc}%**")
    if tot_perc != 100:
        st.warning("⚠️ Attenzione: La somma delle percentuali deve essere 100%.")

# 3. MOTORE DI CALCOLO INTERESSE COMPOSTO
# Calcolo CAGR Pesato: somma di (percentuale_asset * cagr_asset) [cite: 2026-02-15]
cagr_pesato = sum([(a['perc']/100) * a['cagr'] for a in assets if a['perc'] > 0])
r_m = (1 + cagr_pesato/100)**(1/12) - 1

def proietta_periodo(anni):
    m = anni * 12
    lordo = capitale_f * (1 + r_m)**m + pac_f * (((1 + r_m)**m - 1) / r_m) # Formula interesse composto [cite: 2026-02-15]
    versato = capitale_f + (pac_f * m)
    netto = lordo - ((lordo - versato) * 0.26) # Tassazione 26% [cite: 2026-02-15]
    return netto, versato

# 4. DASHBOARD
st.markdown("<h1>TERMINALE STRATEGICO</h1>", unsafe_allow_html=True)

# Card superiori (Orizzonte 20 Anni)
netto_20, versato_20 = proietta_periodo(20)
c1, c2, c3 = st.columns(3)
with c1:
    st.markdown(f"<div class='pro-card'><p>NETTO 20 ANNI</p><p class='value-card'>{netto_20:,.0f} €</p></div>", unsafe_allow_html=True)
with c2:
    st.markdown(f"<div class='pro-card'><p>RENDITA (4%)</p><p class='value-card' style='color:#8be9fd;'>{(netto_20*0.04)/12:,.0f} €</p></div>", unsafe_allow_html=True)
with c3:
    st.markdown(f"<div class='pro-card'><p>CAGR PESATO</p><p class='value-card' style='color:#ffffff;'>{cagr_pesato:.2f}%</p></div>", unsafe_allow_html=True)

# Sviluppo 5-10-15-20 anni [cite: 2026-02-15]
st.markdown("### ⏳ Timeline di Crescita Netta")
timeline_data = []
for a in [5, 10, 15, 20]:
    n, v = proietta_periodo(a)
    timeline_data.append({
        "Orizzonte": f"{a} Anni",
        "Capitale Versato": f"{v:,.0f} €",
        "Patrimonio Netto": f"{n:,.0f} €",
        "Rendita Mensile": f"{(n*0.04)/12:,.0f} €"
    })
st.table(pd.DataFrame(timeline_data))

# Piano Ordini Mensile
st.markdown("### ⚖️ Piano Ordini Corrente (Asset Allocation)")
tot_inv = capitale_f + pac_f
ordini_list = []
for a in assets:
    if a['perc'] > 0:
        ordini_list.append({
            "Asset": a['name'],
            "Allocazione": f"{a['perc']}%",
            "CAGR Stima": f"{a['cagr']}%",
            "Quota Target (€)": f"{(tot_inv * a['perc']/100):,.2f}"
        })
st.table(pd.DataFrame(ordini_list))
