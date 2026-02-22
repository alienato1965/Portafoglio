import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Elite Terminal v5", layout="wide")

# CSS: NERO TOTALE, BORDI NEON E FONT TECNICO
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&display=swap');
    .stApp { background-color: #000000 !important; font-family: 'JetBrains Mono', monospace; }
    [data-testid="stSidebar"] { background-color: #050505 !important; border-right: 1px solid #1a1a1a; }
    [data-testid="stMetric"] {
        background: #080808 !important; border: 1px solid #00ff00 !important;
        box-shadow: 0 0 10px rgba(0, 255, 0, 0.2); border-radius: 4px; padding: 12px;
    }
    [data-testid="stMetricValue"] { color: #00ff00 !important; text-shadow: 0 0 8px #00ff00; }
    h1, h2, h3 { color: #00ff00 !important; text-transform: uppercase; }
</style>
""", unsafe_allow_html=True)

st.title("📟 ELITE STRATEGY COMMAND v5.0")

# STRATEGIA DEFINITIVA 70/30 (Dati salvati)
assets = {
    "VWCE.DE": 0.45, # Core Mondiale
    "QDVE.DE": 0.25, # Core Tech
    "SGLN.L": 0.20,  # Satellite Oro
    "GDXJ": 0.10     # Satellite Junior Miners
}

with st.sidebar:
    st.header("⚙️ PARAMETRI 2026-2036")
    cap_iniziale = st.number_input("Capitale Attuale (€)", value=10000)
    pac_mensile = st.slider("PAC Mensile (€)", 0, 3000, 500)
    anni_analisi = st.slider("Anni Storici Analisi", 5, 20, 10)
    inflazione = st.slider("Inflazione annua (%)", 0.0, 5.0, 2.0)

@st.cache_data
def get_data(tickers):
    return yf.download(tickers, period="25y")["Close"].ffill()

df = get_data(list(assets.keys()))

if not df.empty:
    st.subheader("🟢 ANALISI PERFORMANCE E RISCHIO")
    cols = st.columns(4)
    cagr_list = {}
    
    for i, (t, peso) in enumerate(assets.items()):
        # Calcolo Performance
        s = df[t].tail(anni_analisi*252)
        cagr = ((s.iloc[-1] / s.iloc[0])**(1/anni_analisi)-1)*100
        cagr_list[t] = cagr
        
        # Calcolo Drawdown (Massima perdita)
        dd = ((s / s.cummax() - 1).min()) * 100
        cols[i].metric(t, f"{cagr:.1f}%", f"Drawdown: {dd:.1f}%", delta_color="inverse")

    # TREND STORICO
    st.markdown("---")
    p_df = (df.tail(anni_analisi*252) / df.tail(anni_analisi*252).iloc[0]) * 100
    fig = px.line(p_df, color_discrete_sequence=['#00ff00', '#00ffff', '#ffd700', '#ff00ff'])
    fig.update_layout(height=350, plot_bgcolor='black', paper_bgcolor='black', font_color='white')
    st.plotly_chart(fig, use_container_width=True)

    # PROIEZIONE FINALE (10 ANNI)
    st.markdown("---")
    st.subheader("🔮 PROIEZIONE STRATEGICA 2036")
    
    resa_pesata = sum([cagr_list[t] * assets[t] for t in assets])
    r_m = (1 + (resa_pesata / 100))**(1/12) - 1
    inf_m = (1 + (inflazione / 100))**(1/12) - 1
    
    nominale = [float(cap_iniziale)]
    reale = [float(cap_iniziale)]
    
    for m in range(120): # 10 anni
        nuovo_val = (nominale[-1] * (1 + r_m)) + pac_mensile
        nominale.append(nuovo_val)
        reale.append(nuovo_val / (1 + inf_m)**(m+1))

    lordo = nominale[-1]
    tot_investito = cap_iniziale + (pac_mensile * 120)
    tasse = (lordo - tot_investito) * 0.26 if lordo > tot_investito else 0
    netto = lordo - tasse

    c1, c2, c3 = st.columns(3)
    c1.metric("CAPITALE LORDO", f"€ {lordo:,.0f}")
    c2.metric("NETTO (26% TASSE)", f"€ {netto:,.0f}")
    c3.metric("POTERE ACQUISTO REALE", f"€ {reale[-1]:,.0f}")

    st.info(f"💡 Il tuo portafoglio 70/30 punta a una resa annua media stimata del {resa_pesata:.2f}%.")
else:
    st.error("Dati non disponibili.")
