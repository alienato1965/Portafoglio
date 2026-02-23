import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

# 1. SETUP ESTETICO RADICALE
st.set_page_config(page_title="Deep Dark Terminal", layout="wide")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&display=swap');
    
    /* Sfondo Nero Assoluto */
    .stApp { background-color: #000000 !important; font-family: 'JetBrains Mono', monospace; }
    
    /* Sidebar Nero Dark Profondo */
    [data-testid="stSidebar"] {
        background-color: #000000 !important;
        border-right: 1px solid #1a1a1a;
    }
    
    /* Input e Slider */
    .stSlider [data-baseweb="slider"] { background-color: #1a1a1a; }
    div[data-testid="stMarkdownContainer"] p { color: #00ff66 !important; font-weight: bold; }
    
    /* Card ordini */
    .reportview-container .main .block-container { padding-top: 2rem; }
    .css-1r6slb0 { background-color: #0a0a0a; border: 1px solid #333; border-radius: 10px; padding: 20px; }

    /* Tabelle */
    .stTable { background-color: #050505 !important; color: white !important; }
    thead tr th { background-color: #000 !important; color: #00ff66 !important; border-bottom: 1px solid #00ff66 !important; }
</style>
""", unsafe_allow_html=True)

# 2. COLONNA DI SINISTRA (NERO DARK CON PERCENTUALI)
with st.sidebar:
    st.markdown("<h2 style='color: white;'>🛸 CONTROL PANEL</h2>", unsafe_allow_html=True)
    st.markdown("---")
    
    st.subheader("🏦 CORE (70%)")
    t1 = st.text_input("TICKER 1", value="VWCE.DE")
    p1 = st.slider("% Slot 1", 0, 100, 45) # [cite: 2026-02-15]
    
    t2 = st.text_input("TICKER 2", value="QDVE.DE")
    p2 = st.slider("% Slot 2", 0, 100, 25) # [cite: 2026-02-15]
    
    st.markdown("---")
    st.subheader("🛰️ SATELLITE (30%)")
    t3 = st.text_input("TICKER 3", value="SGLN.L")
    p3 = st.slider("% Slot 3", 0, 100, 20) # [cite: 2026-02-15]
    
    t4 = st.text_input("TICKER 4", value="GDXJ")
    p4 = st.slider("% Slot 4", 0, 100, 10) # [cite: 2026-02-15]
    
    t5 = st.text_input("TICKER 5 (EXTRA)", value="")
    p5 = st.slider("% Slot 5", 0, 100, 0)
    
    tot_pesi = p1 + p2 + p3 + p4 + p5
    
    st.markdown("---")
    cap = st.number_input("CAPITALE TOTALE (€)", value=10000)
    pac = st.number_input("VERSAMENTO PAC (€)", value=500)
    
    st.markdown(f"**TOTALE ALLOCAZIONE: {tot_pesi}%**")
    if tot_pesi != 100:
        st.error("IL TOTALE DEVE ESSERE 100%")
    
    attiva = st.button("🔴 AGGIORNA CALCOLI")

# 3. LOGICA DI CALCOLO E GRAFICA
if attiva and tot_pesi == 100:
    st.markdown("<h1 style='text-align: center; color: #00ff66;'>SYSTEM STATUS: ONLINE</h1>", unsafe_allow_html=True)
    
    config = {t1: p1/100, t2: p2/100, t3: p3/100, t4: p4/100}
    if t5: config[t5] = p5/100
    
    try:
        data = yf.download(list(config.keys()), period="1d")["Close"]
        prezzi = data.iloc[-1] if len(config) > 1 else data
        
        # Tabella Ordini
        st.subheader("⚖️ ORDINI DA ESEGUIRE")
        tot_investito = cap + pac
        ordini_lista = []
        
        for t, p in config.items():
            prezzo = prezzi[t] if len(config) > 1 else prezzi
            v_target = tot_investito * p
            ordini_lista.append({
                "ASSET": t,
                "TARGET %": f"{p*100:.0f}%",
                "VALORE TARGET (€)": f"{v_target:,.2f}",
                "QUOTE TOTALI": round(v_target / prezzo, 4)
            })
        
        st.table(pd.DataFrame(ordini_lista))
        
        # Grafico Donut High-Contrast
        fig = go.Figure(data=[go.Pie(
            labels=list(config.keys()),
            values=list(config.values()),
            hole=.7,
            marker=dict(colors=['#00ff00', '#009900', '#ffff00', '#ccaa00', '#444444'])
        )])
        fig.update_layout(paper_bgcolor='black', font=dict(color="white"))
        st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error("ERRORE NEL RECUPERO DATI. CONTROLLA I TICKER.")
else:
    st.info("Imposta i pesi (totale 100%) e premi il tasto rosso a sinistra per caricare i dati.")
