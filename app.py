import streamlit as st
import yfinance as yf
import pandas as pd

# 1. SETUP PAGINA E TEMA FORZATO
st.set_page_config(page_title="Terminale Operativo 70/30", layout="wide")

st.markdown("""
<style>
    .stApp { background-color: #000000 !important; }
    /* Forza testo bianco ovunque */
    p, span, label, th, td, div { color: #ffffff !important; font-family: 'monospace'; }
    h1, h2, h3 { color: #00ff66 !important; }
    /* Riquadri prezzi */
    [data-testid="stMetric"] { 
        background-color: #111 !important; 
        border: 1px solid #00ff66 !important; 
    }
</style>
""", unsafe_allow_html=True)

# 2. DATI STRATEGIA (Tua configurazione salvata)
pesi = {
    "VWCE.DE": 0.45, 
    "QDVE.DE": 0.25, 
    "SGLN.L": 0.20, 
    "GDXJ": 0.10
}

st.title("📟 TERMINALE 70/30 - STABLE VER.")

with st.sidebar:
    st.header("⚙️ CONFIG")
    # Variabili pulite per evitare NameError
    capitale_tot = st.number_input("Capitale Totale (€)", value=10000)
    investimento_pac = st.number_input("PAC Mensile (€)", value=500)

@st.cache_data
def get_prices(tickers):
    try:
        data = yf.download(tickers, period="5d")["Close"]
        return data.ffill().iloc[-1]
    except:
        return None

prezzi = get_prices(list(pesi.keys()))

if prezzi is not None:
    # 3. TABELLA ORDINI (Alta Leggibilità)
    st.subheader("⚖️ PIANO ORDINI ATTUALE")
    nuovo_totale = capitale_tot + investimento_pac
    
    df_ordini = []
    for t, p in pesi.items():
        val_target = nuovo_totale * p
        df_ordini.append({
            "ETF": t,
            "Target (%)": f"{p*100:.0f}%",
            "Valore Target (€)": f"{val_target:,.0f} €",
            "Quote Totali": round(val_target / prezzi[t], 2)
        })
    
    st.table(pd.DataFrame(df_ordini))

    # 4. STATUS PREZZI
    st.subheader("📈 PREZZI DI MERCATO")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("VWCE", f"{prezzi['VWCE.DE']:.2f}€")
    c2.metric("QDVE", f"{prezzi['QDVE.DE']:.2f}€")
    c3.metric("ORO", f"{prezzi['SGLN.L']:.2f}€")
    c4.metric("GDXJ", f"{prezzi['GDXJ']:.2f}€")

    # 5. PROIEZIONE SEMPLIFICATA (Senza bug f-string)
    st.markdown("---")
    # Calcolo rapido per il 2036 (10 anni) al 7% annuo medio
    tot_stima = (capitale_tot + (investimento_pac * 120)) * (1.07**10)
    st.write(f"🔮 Stima capitale lordo nel 2036 (resa 7%): **{tot_stima:,.0f} €**")

else:
    st.error("Errore nel caricamento dei dati. Controlla la connessione internet.")
