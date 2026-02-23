import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import numpy as np

# 1. SETUP ESTETICO
st.set_page_config(page_title="Portfolio Overview & Projections", layout="wide")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap');
    .stApp { background-color: #1e2127 !important; font-family: 'Inter', sans-serif !important; }
    [data-testid="stSidebar"] { background-color: #262a33 !important; border-right: 1px solid #3e4451; }
    .stMetric, .stTable, .css-1r6slb0, div[data-testid="stBlock"] {
        background-color: #262a33 !important;
        border: 1px solid #3e4451 !important;
        border-radius: 12px !important;
        padding: 15px !important;
    }
    h1, h2, h3, p, label { color: #ffffff !important; }
    [data-testid="stMetricValue"] { color: #50fa7b !important; }
    .stButton>button {
        width: 100%; background-color: #50fa7b !important; color: #1e2127 !important;
        border-radius: 8px !important; font-weight: 600 !important; height: 3em !important;
    }
</style>
""", unsafe_allow_html=True)

# 2. SIDEBAR CON INPUT
with st.sidebar:
    st.markdown("### ⚙️ ASSET ALLOCATION")
    s1, p1 = st.text_input("TICKER 1", value="VWCE.DE"), st.slider("% Slot 1", 0, 100, 45)
    s2, p2 = st.text_input("TICKER 2", value="QDVE.DE"), st.slider("% Slot 2", 0, 100, 25)
    s3, p3 = st.text_input("TICKER 3", value="SGLN.L"), st.slider("% Slot 3", 0, 100, 20)
    s4, p4 = st.text_input("TICKER 4", value="GDXJ"), st.slider("% Slot 4", 0, 100, 10)
    s5, p5 = st.text_input("TICKER 5", value=""), st.slider("% Slot 5", 0, 100, 0)
    
    st.markdown("---")
    cap = st.number_input("CAPITALE ATTUALE (€)", value=10000)
    pac = st.number_input("PAC MENSILE (€)", value=500)
    resa_annua = st.slider("RESA ANNUA STIMATA (%)", 1.0, 12.0, 7.0)
    
    attivato = st.button("AGGIORNA DASHBOARD")

# 3. LOGICA E VISUALIZZAZIONE
st.markdown("<h2 style='text-align: center;'>✅ PORTFOLIO STRATEGY 70/30</h2>", unsafe_allow_html=True)

if attivato:
    config = {t: p for t, p in zip([s1, s2, s3, s4, s5], [p1, p2, p3, p4, p5]) if t}
    if sum(config.values()) != 100:
        st.error("Il totale delle percentuali deve essere 100%.")
    else:
        # Recupero Prezzi
        prezzi = yf.download(list(config.keys()), period="1d")["Close"].iloc[-1]
        
        # Righe Metriche
        cols = st.columns(len(config))
        for i, (t, p) in enumerate(config.items()):
            pr = prezzi[t] if len(config) > 1 else prezzi
            cols[i].metric(t, f"{pr:.2f} €", f"{p}%")

        # --- SEZIONE PROIEZIONI (NOVITÀ) ---
        st.markdown("### 📈 PROIEZIONE DI CRESCITA (5-20 ANNI)")
        
        periodi = [5, 10, 15, 20]
        dati_proiezione = []
        r_mensile = (1 + resa_annua/100)**(1/12) - 1
        
        for anno in periodi:
            mesi = anno * 12
            # Formula Montante: Capitale * (1+r)^n + PAC * [((1+r)^n - 1) / r]
            futuro = cap * (1 + r_mensile)**mesi + pac * (((1 + r_mensile)**mesi - 1) / r_mensile)
            contributi = cap + (pac * mesi)
            dati_proiezione.append({
                "Anni": f"{anno} Anni",
                "Capitale Stimato (€)": f"{futuro:,.0f}",
                "Totale Versato (€)": f"{contributi:,.0f}",
                "Interessi Generati (€)": f"{(futuro - contributi):,.0f}"
            })
        
        st.table(pd.DataFrame(dati_proiezione))

        # Grafico Proiezione Lineare
        x_range = np.arange(0, 21)
        y_val = [cap * (1 + resa_annua/100)**x + (pac * 12) * (((1 + resa_annua/100)**x - 1) / (resa_annua/100)) for x in x_range]
        
        fig_line = go.Figure()
        fig_line.add_trace(go.Scatter(x=x_range, y=y_val, mode='lines+markers', name='Crescita', line=dict(color='#50fa7b', width=4)))
        fig_line.update_layout(
            title="Evoluzione del Capitale nel Tempo",
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color="white"), xaxis_title="Anni", yaxis_title="Euro (€)"
        )
        st.plotly_chart(fig_line, use_container_width=True)

        # Tabella Ordini (Sotto)
        st.markdown("### ⚖️ PIANO ORDINI ATTUALE")
        tot_inv = cap + pac
        ordini = [{"ASSET": t, "QUOTE": round((tot_inv * (p/100)) / (prezzi[t] if len(config)>1 else prezzi), 2)} for t, p in config.items()]
        st.table(pd.DataFrame(ordini))
