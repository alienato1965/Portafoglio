
import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import numpy as np

# 1. SETUP ESTETICO UNIFORMATO (SLATE DARK)
st.set_page_config(page_title="Portfolio Overview", layout="wide")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&family=JetBrains+Mono&display=swap');
    
    /* SFONDO UNIFORME PER TUTTA LA PAGINA */
    .stApp {
        background-color: #1e2127 !important;
        font-family: 'Inter', sans-serif !important;
    }
    
    /* SIDEBAR UNIFORMATA (Stesso grigio o appena più scuro) */
    [data-testid="stSidebar"] {
        background-color: #1a1d23 !important;
        border-right: 1px solid #3e4451;
    }

    /* CARD E BLOCCHI (Grigio leggermente più chiaro per profondità) */
    .stMetric, .stTable, div[data-testid="stBlock"], .css-1r6slb0 {
        background-color: #262a33 !important;
        border: 1px solid #3e4451 !important;
        border-radius: 12px !important;
        padding: 15px !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
    }

    /* Testi e Dettagli Verde Emerald */
    h1, h2, h3, p, label { color: #ffffff !important; }
    [data-testid="stMetricValue"] {
        color: #50fa7b !important;
        font-family: 'JetBrains Mono', monospace !important;
    }
    
    /* Bottone Moderno */
    .stButton>button {
        width: 100%;
        background-color: #50fa7b !important;
        color: #1e2127 !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        height: 3.5em !important;
    }

    /* Slider personalizzati per non sparire nel grigio */
    .stSlider [data-baseweb="slider"] { background-color: #3e4451; }
</style>
""", unsafe_allow_html=True)

# 2. SIDEBAR (PANNELLO INTEGRATO)
with st.sidebar:
    st.markdown("<h2 style='color: #50fa7b;'>🕹️ COMMANDS</h2>", unsafe_allow_html=True)
    
    # Slot e Slider [cite: 2026-02-15]
    s1, p1 = st.text_input("TICKER 1", value="VWCE.DE"), st.slider("% Slot 1", 0, 100, 45)
    s2, p2 = st.text_input("TICKER 2", value="QDVE.DE"), st.slider("% Slot 2", 0, 100, 25)
    s3, p3 = st.text_input("TICKER 3", value="SGLN.L"), st.slider("% Slot 3", 0, 100, 20)
    s4, p4 = st.text_input("TICKER 4", value="GDXJ"), st.slider("% Slot 4", 0, 100, 10)
    s5, p5 = st.text_input("TICKER 5", value=""), st.slider("% Slot 5", 0, 100, 0)
    
    st.markdown("---")
    cap = st.number_input("CAPITALE ATTUALE (€)", value=10000, step=1000)
    pac = st.number_input("PAC MENSILE (€)", value=500, step=50)
    
    tot_pesi = p1 + p2 + p3 + p4 + p5
    st.markdown(f"**TOTALE: {tot_pesi}%**")
    
    attivato = st.button("AGGIORNA DASHBOARD")

# 3. CONTENUTO CENTRALE
if attivato and tot_pesi == 100:
    st.markdown("<h1 style='text-align: center;'>✅ PORTFOLIO ANALYSIS</h1>", unsafe_allow_html=True)
    
    config = {t: p for t, p in zip([s1, s2, s3, s4, s5], [p1, p2, p3, p4, p5]) if t}
    
    try:
        data = yf.download(list(config.keys()), period="1d")["Close"]
        prezzi = data.iloc[-1] if len(config) > 1 else data

        # Metriche Prezzi
        cols = st.columns(len(config))
        for i, (t, p) in enumerate(config.items()):
            pr_att = prezzi[t] if len(config) > 1 else prezzi
            cols[i].metric(label=t, value=f"{pr_att:.2f} €", delta=f"{p}%")

        # Proiezioni 5-20 Anni [cite: 2026-02-15]
        st.markdown("### 📈 PROIEZIONE DI CRESCITA")
        cagr_stimato = ((p1+p2)/100 * 0.08) + ((p3+p4+p5)/100 * 0.04) # Core 8% / Sat 4%
        
        periodi = [5, 10, 15, 20]
        proiezioni = []
        r_mensile = (1 + cagr_stimato)**(1/12) - 1
        
        for anno in periodi:
            mesi = anno * 12
            val_futuro = cap * (1 + r_mensile)**mesi + pac * (((1 + r_mensile)**mesi - 1) / r_mensile)
            proiezioni.append({
                "Anni": f"{anno} Anni",
                "Capitale Stimato (€)": f"{val_futuro:,.0f}",
                "CAGR Atteso": f"{cagr_stimato*100:.1f}%"
            })
        st.table(pd.DataFrame(proiezioni))

        # Grafico Donut
        fig = go.Figure(data=[go.Pie(
            labels=list(config.keys()), values=list(config.values()), hole=.7,
            marker=dict(colors=['#50fa7b', '#40c963', '#2d323c', '#3e4451'])
        )])
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', font=dict(color="white"))
        st.plotly_chart(fig, use_container_width=True)

    except:
        st.error("Errore nel recupero dati. Verifica i Ticker.")
else:
    st.info("Regola i pesi nella sidebar e premi il pulsante verde.")
