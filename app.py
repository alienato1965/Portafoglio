import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(page_title="Configuratore ETF 70/30", layout="wide")

st.title("🖥️ Terminale Asset Personalizzati")

# 1. SIDEBAR: GLI SLOT PER GLI ETF
with st.sidebar:
    st.header("🎛️ SLOT ETF")
    st.write("Inserisci i Ticker (es. VWCE.DE, QDVE.DE, SGLN.L, GDXJ)")
    
    # Creazione dei 5 slot di input
    slot1 = st.text_input("Slot 1 (45%)", value="VWCE.DE")
    slot2 = st.text_input("Slot 2 (25%)", value="QDVE.DE")
    slot3 = st.text_input("Slot 3 (20%)", value="SGLN.L")
    slot4 = st.text_input("Slot 4 (10%)", value="GDXJ")
    slot5 = st.text_input("Slot 5 (Opzionale %)", value="")

    st.markdown("---")
    capitale = st.number_input("Capitale Totale (€)", value=10000)
    pac = st.number_input("Versamento PAC (€)", value=500)

# 2. CONFIGURAZIONE DINAMICA DEI PESI
# Gestiamo i 5 slot assegnando i pesi della tua strategia 70/30
config = {}
if slot1: config[slot1] = 0.45
if slot2: config[slot2] = 0.25
if slot3: config[slot3] = 0.20
if slot4: config[slot4] = 0.10
# Il quinto slot è un "bonus" se vuoi splittare ulteriormente
if slot5: st.warning("Nota: Il 5° slot richiede di ricalcolare le % totali nel codice.")

# 3. RECUPERO PREZZI
@st.cache_data(ttl=600)
def get_prices(tickers):
    if not tickers: return None
    try:
        data = yf.download(tickers, period="5d")["Close"]
        return data.ffill().iloc[-1]
    except: return None

prezzi_live = get_prices(list(config.keys()))

if prezzi_live is not None:
    st.subheader("⚖️ Calcolo Quote per i 5 Slot")
    tot_investito = capitale + pac
    
    report = []
    for ticker, peso in config.items():
        val_target = tot_investito * peso
        prezzo = prezzi_live[ticker] if len(config) > 1 else prezzi_live
        
        report.append({
            "TICKER": ticker,
            "PESO": f"{peso*100:.0f}%",
            "VALORE TARGET (€)": f"{val_target:,.2f} €",
            "QUOTE TOTALI": round(val_target / prezzo, 4),
            "PREZZO ATTUALE": f"{prezzo:.2f} €"
        })
    
    st.table(pd.DataFrame(report))
    st.success(f"✅ Analisi completata per {len(config)} strumenti finanziari.")
else:
    st.error("Inserisci ticker validi per attivare gli slot.")
