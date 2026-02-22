import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(page_title="Elite Terminal 70/30", layout="wide")

# CSS PER LEGGIBILITÀ TOTALE
st.markdown("""
<style>
    .stApp { background-color: #000000 !important; }
    p, span, label, th, td, div { color: #ffffff !important; }
    h1, h2, h3 { color: #00ff66 !important; }
    [data-testid="stMetric"] { background-color: #111 !important; border: 1px solid #333 !important; }
    [data-testid="stSidebar"] { background-color: #0a0a0a !important; }
</style>
""", unsafe_allow_html=True)

# 1. TUA STRATEGIA SALVATA (2026)
# Core: 45% VWCE + 25% QDVE | Satellite: 20% Oro + 10% Miners
pesi = {"VWCE.DE": 0.45, "QDVE.DE": 0.25, "SGLN.L": 0.20, "GDXJ": 0.10}

st.title("📟 TERMINALE OPERATIVO 70/30")

# 2. SIDEBAR CON GLI ETF (Eccoli qui!)
with st.sidebar:
    st.header("🗂️ STRATEGIA 2026")
    st.markdown("---")
    st.subheader("🏦 CORE (70%)")
    st.write("• **VWCE**: 45% (Mondiale)")
    st.write("• **QDVE**: 25% (Tech S&P500)")
    st.markdown("---")
    st.subheader("🛰️ SATELLITE (30%)")
    st.write("• **ORO**: 20% (Amundi Physical)")
    st.write("• **MINERS**: 10% (VanEck Junior)")
    st.markdown("---")
    cap_tot = st.number_input("Capitale Attuale (€)", value=10000)
    pac_val = st.number_input("PAC da investire oggi (€)", value=500)

# 3. LOGICA PREZZI E ORDINI
@st.cache_data
def get_live_prices(tickers):
    try:
        data = yf.download(tickers, period="5d")["Close"]
        return data.ffill().iloc[-1]
    except: return None

prezzi = get_live_prices(list(pesi.keys()))

if prezzi is not None:
    st.subheader("⚖️ ORDINI DA ESEGUIRE")
    nuovo_totale = cap_tot + pac_val
    
    lista_ordini = []
    for t, p in pesi.items():
        v_target = nuovo_totale * p
        lista_ordini.append({
            "ASSET": t,
            "TARGET (%)": f"{p*100:.0f}%",
            "VALORE TARGET (€)": f"{v_target:,.0f} €",
            "QUOTE TOTALI": round(v_target / prezzi[t], 2)
        })
    st.table(pd.DataFrame(lista_ordini))

    st.subheader("📈 PREZZI LIVE")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("VWCE", f"{prezzi['VWCE.DE']:.2f}€")
    c2.metric("QDVE", f"{prezzi['QDVE.DE']:.2f}€")
    c3.metric("ORO", f"{prezzi['SGLN.L']:.2f}€")
    c4.metric("MINERS", f"{prezzi['GDXJ']:.2f}€")
else:
    st.error("Connessione ai mercati fallita.")
