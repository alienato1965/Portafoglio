import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import numpy as np

# 1. SETUP ESTETICO UNIFORMATO
st.set_page_config(page_title="Portfolio Overview", layout="wide")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&family=JetBrains+Mono&display=swap');
    .stApp { background-color: #1e2127 !important; font-family: 'Inter', sans-serif !important; }
    [data-testid="stSidebar"] { background-color: #1a1d23 !important; border-right: 1px solid #3e4451; }
    .stMetric, .stTable, div[data-testid="stBlock"] {
        background-color: #262a33 !important;
        border: 1px solid #3e4451 !important;
        border-radius: 12px !important;
        padding: 20px !important;
    }
    h1, h2, h3, p, label { color: #ffffff !important; }
    [data-testid="stMetricValue"] { color: #50fa7b !important; font-family: 'JetBrains Mono'; }
    .stButton>button {
        width: 100%; background-color: #50fa7b !important; color: #1e2127 !important;
        border-radius: 8px !important; font-weight: bold; height: 3.5em;
    }
</style>
""", unsafe_allow_html=True)

# 2. SIDEBAR
with st.sidebar:
    st.markdown("<h2 style='color: #50fa7b;'>🕹️ SETTINGS</h2>", unsafe_allow_html=True)
    s1, p1 = st.text_input("TICKER 1", value="VWCE.DE"), st.slider("% Slot 1", 0, 100, 45)
    s2, p2 = st.text_input("TICKER 2", value="QDVE.DE"), st.slider("% Slot 2", 0, 100, 25)
    s3, p3 = st.text_input("TICKER 3", value="SGLN.L"), st.slider("% Slot 3", 0, 100, 20)
    s4, p4 = st.text_input("TICKER 4", value="GDXJ"), st.slider("% Slot 4", 0, 100, 10)
    
    st.markdown("---")
    cap = st.number_input("CAPITALE ATTUALE (€)", value=10000, step=1000)
    pac = st.number_input("PAC MENSILE (€)", value=500, step=50)
    st.markdown("---")
    cagr_manuale = st.slider("CAGR ATTESO (%)", 1.0, 12.0, 7.0)
    
    attivato = st.button("AGGIORNA PROIEZIONI")

# 3. CONTENUTO CENTRALE
if attivato:
    st.markdown("<h1 style='text-align: center;'>🔮 PROIEZIONE STRATEGICA 2026-2046</h1>", unsafe_allow_html=True)
    
    # CALCOLI PROIEZIONE
    anni = 20
    mesi = anni * 12
    r_mensile = (1 + cagr_manuale/100)**(1/12) - 1
    
    timeline = np.arange(0, mesi + 1)
    capitale_storia = []
    versato_storia = []
    
    for m in timeline:
        val = cap * (1 + r_mensile)**m + pac * (((1 + r_mensile)**m - 1) / r_mensile)
        capitale_storia.append(val)
        versato_storia.append(cap + (pac * m))

    # GRAFICO AD AREA MODERNO
    fig_growth = go.Figure()
    fig_growth.add_trace(go.Scatter(
        x=timeline/12, y=capitale_storia, fill='tozeroy', 
        name='Capitale Totale (Lordo)', line=dict(color='#50fa7b', width=3),
        fillcolor='rgba(80, 250, 123, 0.1)'
    ))
    fig_growth.add_trace(go.Scatter(
        x=timeline/12, y=versato_storia, name='Capitale Versato', 
        line=dict(color='#ffffff', width=2, dash='dash')
    ))
    
    fig_growth.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color="white"), xaxis_title="Anni", yaxis_title="Valore Portafoglio (€)",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    st.plotly_chart(fig_growth, use_container_width=True)

    # TABELLA DETTAGLIATA (NETTA)
    st.markdown("### 📊 DETTAGLIO CRESCITA NETTA (Tasse 26% incluse)")
    
    checkpoints = [5, 10, 15, 20]
    final_data = []
    
    for a in checkpoints:
        m = a * 12
        lordo = capitale_storia[m]
        versato = versato_storia[m]
        plusvalenza = lordo - versato
        tasse = plusvalenza * 0.26
        netto = lordo - tasse
        
        final_data.append({
            "Periodo": f"{a} Anni",
            "Valore Lordo (€)": f"{lordo:,.0f}",
            "Totale Versato (€)": f"{versato:,.0f}",
            "Tasse Stimante (€)": f"-{tasse:,.0f}",
            "VALORE NETTO (€)": f"{netto:,.0f}"
        })
    
    st.table(pd.DataFrame(final_data))
    
    st.info(f"💡 Nota: Questa proiezione assume un CAGR costante del {cagr_manuale}%. Non avendo una pensione, il tuo obiettivo minimo è la colonna 'VALORE NETTO'.")

else:
    st.markdown("<div style='text-align: center; margin-top: 100px;'><h2 style='color: #3e4451;'>CONFIGURA I DATI E PREMI AGGIORNA</h2></div>", unsafe_allow_html=True)
