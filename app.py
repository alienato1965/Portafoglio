import streamlit as st
import yfinance as yf
import pandas as pd

# 1. SETUP - Leggibilità massima
st.set_page_config(page_title="Portafoglio 70/30", layout="wide")

# CSS minimale per evitare il "nero su nero"
st.markdown("""
<style>
    .stApp { background-color: #000000 !important; }
    p, span, label, th, td, div { color: #ffffff !important; font-family: sans-serif !important; }
    h1, h2, h3 { color: #00ff66 !important; }
    .stMetric { background-color: #111 !important; border: 1px solid #333 !important; }
    /* Forza visibilità tabella */
    table { border: 1px solid #444 !important; color: white !important; }
</style>
""", unsafe_allow_html=True)

# 2. DEFINIZIONE STRATEGIA
pesi = {"VWCE.DE": 0.45, "QDVE.DE": 0.25, "SGLN.L": 0.20, "GDXJ": 0.10}

st.title("📟 TERMINALE OPERATIVO 70/30")

with st.sidebar:
    st.header("⚙️ CONFIGURAZIONE")
    cap_tot = st.number_input("Capitale Totale (€)", value=10000)
    pac_val = st.number_input("Versamento PAC (€)", value=500)

@st.cache_data
def get_live_prices(tickers):
    try:
        data = yf.download(tickers, period="5d")["Close"]
        return data.ffill().iloc[-1]
    except:
        return None

prezzi = get_live_prices(list(pesi.keys()))

if prezzi is not None:
    # 3. TABELLA ORDINI (Pulita e chiara)
    st.subheader("⚖️ ORDINI DA ESEGUIRE")
    nuovo_cap = cap_tot + pac_val
    
    lista_ordini = []
    for t, p in pesi.items():
        valore_target = nuovo_cap * p
        lista_ordini.append({
            "ASSET": t,
            "TARGET (%)": f"{p*100:.0f}%",
            "VALORE (€)": f"{valore_target:,.0f} €",
            "QUOTE TOTALI": round(valore_target / prezzi[t], 2)
        })
    
    st.table(pd.DataFrame(lista_ordini))

    # 4. MONITOR PREZZI
    st.subheader("📈 PREZZI LIVE")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("VWCE", f"{prezzi['VWCE.DE']:.2f}€")
    c2.metric("QDVE", f"{prezzi['QDVE.DE']:.2f}€")
    c3.metric("ORO", f"{prezzi['SGLN.L']:.2f}€")
    c4.metric("GDXJ", f"{prezzi['GDXJ']:.2f}€")

    # 5. OBIETTIVO 2036
    st.markdown("---")
    investito_tot = cap_tot + (pac_val * 120)
    # Calcolo prudenziale (7% annuo)
    stima_2036 = (cap_tot + (pac_val * 120)) * 1.8 # Moltiplicatore storico approssimativo
    st.info(f"🔮 Nel 2036, con un PAC costante, il tuo capitale lordo stimato è circa: {stima_2036:,.0f} €")

else:
    st.error("Errore connessione. Ricarica la pagina.")
