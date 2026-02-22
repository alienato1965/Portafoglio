import streamlit as st
import yfinance as yf
import pandas as pd

# 1. Configurazione Base (Pulisce tutto il disordine precedente)
st.set_page_config(page_title="Il Mio Portafoglio 70/30", layout="wide")

st.title("📊 Terminale Strategia 70/30")
st.write("Versione ultra-stabile: VWCE, QDVE, ORO, MINERS")

# 2. Sidebar per i numeri
with st.sidebar:
    st.header("Impostazioni")
    cap_tot = st.number_input("Capitale già investito (€)", value=10000)
    pac_val = st.number_input("PAC da aggiungere oggi (€)", value=500)
    st.info("Pesi: 45% VWCE, 25% QDVE, 20% Oro, 10% Miners")

# 3. Definizione Fissa (Così non sbagliamo i calcoli)
pesi = {
    "VWCE.DE": 0.45, 
    "QDVE.DE": 0.25, 
    "SGLN.L": 0.20, 
    "GDXJ": 0.10
}

# 4. Recupero Prezzi (Semplificato al massimo)
@st.cache_data
def prendi_prezzi(lista):
    dati = yf.download(lista, period="1d")["Close"]
    return dati.iloc[-1]

try:
    prezzi = prendi_prezzi(list(pesi.keys()))
    
    # 5. Tabella Ordini (Niente CSS, solo dati chiari)
    st.header("⚖️ Quote da avere nel portafoglio")
    cap_finale = cap_tot + pac_val
    risultati = []
    
    for t, p in pesi.items():
        valore_target = cap_finale * p
        risultati.append({
            "Asset": t,
            "Target %": f"{p*100}%",
            "Valore (€)": round(valore_target, 2),
            "Quote Totali": round(valore_target / prezzi[t], 2)
        })
    
    st.table(pd.DataFrame(risultati))
    
    # 6. Prezzi Attuali
    st.header("📉 Prezzi di Mercato")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("VWCE", f"{prezzi['VWCE.DE']:.2f}€")
    c2.metric("QDVE", f"{prezzi['QDVE.DE']:.2f}€")
    c3.metric("ORO", f"{prezzi['SGLN.L']:.2f}€")
    c4.metric("MINERS", f"{prezzi['GDXJ']:.2f}€")

except Exception as e:
    st.error("Errore nel caricamento. Aspetta 10 secondi e ricarica la pagina.")
