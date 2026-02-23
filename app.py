import streamlit as st
import yfinance as yf
import pandas as pd

# 1. Configurazione - Tema scuro nativo (il più leggibile)
st.set_page_config(page_title="Gestione 70/30", layout="wide")

st.title("📟 Terminale Operativo Strategia 70/30")

# 2. La tua strategia (Dati salvati)
# CORE (70%): 45% VWCE + 25% QDVE | SATELLITE (30%): 20% ORO + 10% MINERS
pesi = {
    "VWCE.DE": 0.45, 
    "QDVE.DE": 0.25, 
    "SGLN.L": 0.20, 
    "GDXJ": 0.10
}

# 3. Sidebar con gli input
with st.sidebar:
    st.header("⚙️ Parametri")
    cap_investito = st.number_input("Capitale già nel broker (€)", value=10000)
    pac_fresco = st.number_input("Nuova liquidità da investire (€)", value=500)
    st.markdown("---")
    st.subheader("🎯 Target Allocazione")
    for t, p in pesi.items():
        st.write(f"**{t}**: {p*100:.0f}%")

# 4. Funzione recupero prezzi "blindata"
@st.cache_data(ttl=3600)
def get_clean_prices(tickers):
    try:
        data = yf.download(tickers, period="5d")["Close"]
        return data.ffill().iloc[-1]
    except:
        return None

prezzi = get_clean_prices(list(pesi.keys()))

if prezzi is not None:
    # 5. Tabella Ordini (Il cuore dell'app)
    st.header("⚖️ Calcolo Quote per il Ribilanciamento")
    nuovo_totale = cap_investito + pac_fresco
    
    tabella = []
    for t, p in pesi.items():
        valore_target = nuovo_totale * p
        tabella.append({
            "ETF": t,
            "Peso": f"{p*100:.0f}%",
            "Valore (€)": f"{valore_target:,.2f} €",
            "Quote Totali da Avere": round(valore_target / prezzi[t], 2),
            "Prezzo Attuale": f"{prezzi[t]:.2f} €"
        })
    
    st.table(pd.DataFrame(tabella))
    
    st.info(f"💡 Per mantenere la strategia 70/30, il tuo portafoglio totale (dopo il PAC) deve valere {nuovo_totale:,.2f} €.")

else:
    st.error("⚠️ Errore di connessione. I mercati potrebbero essere chiusi o Yahoo Finance non risponde. Riprova tra un istante.")

# 6. Proiezione 2036 (Versione sicura senza bug)
st.markdown("---")
st.subheader("🔮 Obiettivo 2036")
# Calcolo basato su rendimento medio prudenziale del 7%
anni = 10
capitale_stimato = (cap_investito + (pac_fresco * 12 * anni)) * (1.07 ** anni)
st.write(f"Con un rendimento medio stimato del 7%, nel 2036 il capitale lordo sarà circa: **{capitale_stimato:,.0f} €**")
