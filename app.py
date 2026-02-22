import streamlit as st
import yfinance as yf
import pandas as pd

# 1. FORZA TEMA DARK E LEGGIBILITÀ
st.set_page_config(page_title="Elite Terminal 70/30", layout="wide")

st.markdown("""
<style>
    /* Sfondo nero totale */
    .stApp { background-color: #000000 !important; }
    
    /* Forza testo BIANCO ovunque (per evitare nero su nero) */
    p, div, label, span, .stMarkdown { color: #ffffff !important; font-family: 'Courier New', monospace; }
    
    /* Titoli in VERDE NEON */
    h1, h2, h3 { color: #00ff66 !important; text-transform: uppercase; border-bottom: 1px solid #333; }
    
    /* Metriche (i riquadri con i numeri) */
    [data-testid="stMetric"] { 
        background-color: #111111 !important; 
        border: 2px solid #00ff66 !important; 
        border-radius: 10px;
    }
    [data-testid="stMetricValue"] { color: #00ff66 !important; font-weight: bold; }
    [data-testid="stMetricLabel"] { color: #aaaaaa !important; }

    /* Tabelle leggibili: sfondo scuro, testo bianco */
    .stTable, table { background-color: #0a0a0a !important; color: white !important; border: 1px solid #444; }
    th { background-color: #222 !important; color: #00ff66 !important; }
</style>
""", unsafe_allow_html=True)

# 2. DEFINIZIONE STRATEGIA (VWCE 45%, QDVE 25%, ORO 20%, MINERS 10%)
pesi = {
    "VWCE.DE": 0.45, 
    "QDVE.DE": 0.25, 
    "SGLN.L": 0.20, 
    "GDXJ": 0.10
}

st.title("📟 TERMINALE OPERATIVO 70/30")

with st.sidebar:
    st.header("⚙️ CONFIGURAZIONE")
    # Nota: Questi input avranno testo bianco su sfondo grigio scuro
    capitale = st.number_input("Capitale Totale (€)", value=10000)
    pac = st.number_input("PAC Mensile (€)", value=500)
    st.markdown("---")
    st.info("Strategia: 70% Core (VWCE+QDVE) e 30% Satellite (Oro+Miners)")

# 3. LOGICA DATI E ORDINI
@st.cache_data
def get_prices(list_tkrs):
    try:
        df = yf.download(list_tkrs, period="5d")["Close"]
        return df.ffill().iloc[-1]
    except:
        return None

prezzi_last = get_prices(list(pesi.keys()))

if prezzi_last is not None:
    # SEZIONE ORDINI
    st.subheader("⚖️ ORDINI DA ESEGUIRE (Ribilanciati)")
    cap_investito = capitale + pac
    
    res_list = []
    for t, p in pesi.items():
        v_target = cap_investito * p
        res_list.append({
            "ETF": t,
            "Target %": f"{p*100:.0f}%",
            "Valore (€)": f"{v_target:,.0f} €",
            "Quote Totali": round(v_target / prezzi_last[t], 2)
        })
    
    st.table(pd.DataFrame(res_list))

    # SEZIONE PERFORMANCE RAPIDA
    st.subheader("📈 STATUS MERCATO")
    c1, c2, c3, c4 = st.columns(4)
    cols = [c1, c2, c3, c4]
    for i, (t, p) in enumerate(pesi.items()):
        cols[i].metric(label=t, value=f"{prezzi_last[t]:.2f}€")

else:
    st.error("ERRORE: Impossibile leggere i prezzi. Controlla la connessione.")
