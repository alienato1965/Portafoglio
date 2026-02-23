import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import numpy as np

# 1. SETUP ESTETICO PREMIUM CON TESTO BIANCO FORZATO
st.set_page_config(page_title="Wealth Terminal Elite", layout="wide")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    
    .stApp { background-color: #1e242b !important; font-family: 'Inter', sans-serif !important; }
    [data-testid="stSidebar"] { background-color: #161b22 !important; border-right: 1px solid #2d333b; }
    
    /* Card Design con Testo Bianco */
    .pro-card {
        background: linear-gradient(145deg, #262c36, #1e242b);
        border: 1px solid #3d444d;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        margin-bottom: 15px;
        color: white !important;
    }
    .label-card { color: #8b949e; font-size: 0.8rem; text-transform: uppercase; margin-bottom: 5px; }
    .value-card { color: #50fa7b; font-size: 1.8rem; font-weight: 700; }

    /* TABELLA ORDINI: TESTO BIANCO E SFONDO DARK */
    .stTable, [data-testid="stTable"] {
        background-color: #21262d !important;
        color: white !important;
        border-radius: 10px;
    }
    
    /* Forzatura colore celle tabella */
    [data-testid="stTable"] td, [data-testid="stTable"] th {
        color: white !important;
        border-bottom: 1px solid #30363d !important;
    }

    /* Button Verde Smeraldo */
    .stButton>button {
        width: 100%; background-color: #38d39f !important; color: #161b22 !important;
        font-weight: 700; border-radius: 8px; height: 3.5em; border: none;
        margin-top: 20px;
    }
</style>
""", unsafe_allow_html=True)

# 2. SIDEBAR: CONFIGURAZIONE CON ISIN [cite: 2026-02-15]
with st.sidebar:
    st.markdown("<h2 style='color: #38d39f;'>💎 SETTINGS</h2>", unsafe_allow_html=True)
    
    st.markdown("🌍 **CORE MONDO**")
    isin1 = st.text_input("ISIN 1", value="VWCE.DE")
    p1 = st.slider("% Asset 1", 0, 100, 45)
    
    st.markdown("💻 **CORE TECH**")
    isin2 = st.text_input("ISIN 2", value="QDVE.DE")
    p2 = st.slider("% Asset 2", 0, 100, 25)
    
    st.markdown("🟡 **SATELLITE ORO**")
    isin3 = st.text_input("ISIN 3", value="SGLN.L")
    p3 = st.slider("% Asset 3", 0, 100, 20)
    
    st.markdown("⛏️ **SATELLITE MINERS**")
    isin4 = st.text_input("ISIN 4", value="GDXJ")
    p4 = st.slider("% Asset 4", 0, 100, 10)
    
    st.markdown("---")
    cap = st.number_input("Capitale Attuale (€)", value=10000)
    pac = st.number_input("PAC Mensile (€)", value=500)
    cagr = st.slider("CAGR Atteso (%)", 1.0, 12.0, 7.5)
    
    attivato = st.button("ESEGUI ANALISI")

# 3. AREA DASHBOARD PRINCIPALE
st.markdown("<h1 style='color: white;'>ANALISI PATRIMONIALE</h1>", unsafe_allow_html=True)

if attivato:
    # Verifica che la somma sia 100% [cite: 2026-02-14, 2026-02-15]
    if p1 + p2 + p3 + p4 != 100:
        st.error(f"Errore: Il totale è {p1+p2+p3+p4}%. Deve essere 100%.")
    else:
        # Calcolo Proiezioni [cite: 2026-02-15]
        r_m = (1 + cagr/100)**(1/12) - 1
        m20 = 20 * 12
        lordo_20 = cap * (1 + r_m)**m20 + pac * (((1 + r_m)**m20 - 1) / r_m)
        versato_20 = cap + (pac * m20)
        netto_20 = lordo_20 - (lordo_20 - versato_20) * 0.26
        rendita_20 = (netto_20 * 0.04) / 12

        # UI: CARD SUPERIORI
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown(f"<div class='pro-card'><p class='label-card'>Netto (20 Anni)</p><p class='value-card'>{netto_20:,.0f} €</p></div>", unsafe_allow_html=True)
        with c2:
            st.markdown(f"<div class='pro-card'><p class='label-card'>Rendita Mensile</p><p class='value-card' style='color:#8be9fd;'>{rendita_20:,.0f} €</p></div>", unsafe_allow_html=True)
        with c3:
            st.markdown(f"<div class='pro-card'><p class='label-card'>Totale Versato</p><p class='value-card' style='color:#ffffff;'>{versato_20:,.0f} €</p></div>", unsafe_allow_html=True)

        # TABELLA ORDINI CON TESTO BIANCO FORZATO [cite: 2026-02-15]
        st.markdown("<h3 style='color: white; margin-top: 30px;'>⚖️ Piano Ordini Corrente</h3>", unsafe_allow_html=True)
        tot_port = cap + pac
        ordini = [
            {"ASSET (ISIN/Ticker)": isin1, "ALLOCAZIONE": f"{p1}%", "VALORE TARGET (€)": f"{(tot_port * p1/100):,.2f}"},
            {"ASSET (ISIN/Ticker)": isin2, "ALLOCAZIONE": f"{p2}%", "VALORE TARGET (€)": f"{(tot_port * p2/100):,.2f}"},
            {"ASSET (ISIN/Ticker)": isin3, "ALLOCAZIONE": f"{p3}%", "VALORE TARGET (€)": f"{(tot_port * p3/100):,.2f}"},
            {"ASSET (ISIN/Ticker)": isin4, "ALLOCAZIONE": f"{p4}%", "VALORE TARGET (€)": f"{(tot_port * p4/100):,.2f}"},
        ]
        # Visualizzazione tabella
        st.table(pd.DataFrame(ordini))

        # GRAFICO DI CRESCITA [cite: 2026-02-15]
        st.markdown("<h3 style='color: white; margin-top: 30px;'>📈 Evoluzione Patrimoniale</h3>", unsafe_allow_html=True)
        timeline = np.arange(0, m20 + 1)
        y_lordo = [cap * (1+r_m)**m + pac * (((1+r_m)**m - 1)/r_m) for m in timeline]
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=timeline/12, y=y_lordo, name='Patrimonio Lordo', fill='tozeroy', line=dict(color='#38d39f', width=4)))
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color="#8b949e"), height=400,
            xaxis=dict(showgrid=True, gridcolor='#2d333b'), yaxis=dict(showgrid=True, gridcolor='#2d333b'),
            margin=dict(t=20, b=20, l=20, r=20)
        )
        st.plotly_chart(fig, use_container_width=True)

else:
    st.markdown("<div style='text-align: center; margin-top: 100px; color: #8b949e;'><h2>CONFIGURA E PREMI IL BOTTONE VERDE</h2></div>", unsafe_allow_html=True)
