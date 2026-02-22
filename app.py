import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Elite Terminal v4", layout="wide")

# CSS DEFINITIVO: SCURO, PULITO, PROFESSIONALE
st.markdown("""
<style>
    .stApp { background-color: #000000 !important; }
    font-family: 'JetBrains Mono', monospace;
    [data-testid="stMetric"] {
        background: #0a0a0a !important;
        border: 1px solid #00ff00 !important;
        border-radius: 5px;
    }
    h1, h2, h3 { color: #00ff00 !important; }
    .stSlider [data-baseweb="slider"] [role="slider"] { background-color: #00ff00 !important; }
</style>
""", unsafe_allow_html=True)

# CONFIGURAZIONE ASSET (STRATEGIA SALVATA)
# Core: 45% VWCE, 25% QDVE | Satellite: 20% Oro, 10% Junior Miners
assets = {
    "VWCE.DE": 0.45,
    "QDVE.DE": 0.25,
    "SGLN.L": 0.20,
    "GDXJ": 0.10
}

st.title("📟 ELITE STRATEGY COMMAND v4.0")

with st.sidebar:
    st.header("⚙️ PARAMETRI")
    capitale_iniziale = st.number_input("Capitale Attuale (€)", value=10000)
    pac_mensile = st.slider("PAC Mensile (€)", 0, 2000, 500)
    anni_analisi = st.slider("Anni Storici", 5, 20, 10)
    inflazione_stima = st.slider("Inflazione stimata %", 0.0, 5.0, 2.5)

@st.cache_data
def get_market_data(tickers):
    d = yf.download(tickers, period="25y")["Close"]
    return d.ffill()

df = get_market_data(list(assets.keys()))

if not df.empty:
    # CALCOLO PERFORMANCE STORICA
    st.subheader("📊 ANALISI ASSET")
    cols = st.columns(4)
    cagr_list = {}
    
    for i, (t, peso) in enumerate(assets.items()):
        prezzo_f = float(df[t].iloc[-1])
        prezzo_i = float(df[t].tail(anni_analisi*252).iloc[0])
        cagr = ((prezzo_f / prezzo_i)**(1/anni_analisi)-1)*100
        cagr_list[t] = cagr
        cols[i].metric(t, f"{cagr:.1f}%", f"Peso: {peso*100}%")

    # PROIEZIONE 2036 (10 ANNI)
    st.markdown("---")
    st.subheader("🔮 PROIEZIONE 2036 (POTERE D'ACQUISTO)")
    
    resa_media = sum([cagr_list[t] * assets[t] for t in assets])
    r_mensile = (1 + (resa_media / 100))**(1/12) - 1
    inf_mensile = (1 + (inflazione_stima / 100))**(1/12) - 1
    
    valore_nominale = [float(capitale_iniziale)]
    valore_reale = [float(capitale_iniziale)]
    
    for m in range(120): # 10 anni
        nuovo_nom = (valore_nominale[-1] * (1 + r_mensile)) + pac_mensile
        valore_nominale.append(nuovo_nom)
        # Scontiamo l'inflazione mensilmente
        valore_reale.append(nuovo_nom / (1 + inf_mensile)**(m+1))

    # RISULTATI FINALI
    lordo = valore_nominale[-1]
    investito = capitale_iniziale + (pac_mensile * 120)
    tasse = (lordo - investito) * 0.26 if lordo > investito else 0
    netto = lordo - tasse
    
    c1, c2, c3 = st.columns(3)
    c1.metric("CAPITALE LORDO", f"€ {lordo:,.0f}")
    c2.metric("NETTO TASSE (26%)", f"€ {netto:,.0f}")
    c3.metric("VALORE REALE (OGGI)", f"€ {valore_reale[-1]:,.0f}")
    
    st.info(f"💡 Tra 10 anni, i tuoi {lordo:,.0f}€ avranno lo stesso potere d'acquisto di {valore_reale[-1]:,.0f}€ oggi.")

    # GRAFICO PROIEZIONE
    proiezione_df = pd.DataFrame({
        "Nominale (Numeri)": valore_nominale,
        "Reale (Potere Acquisto)": valore_reale
    })
    st.line_chart(proiezione_df)

else:
    st.error("Connessione ai dati fallita. Riprova tra un istante.")
