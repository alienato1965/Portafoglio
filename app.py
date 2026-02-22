import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px

# 1. SETUP ESSENZIALE
st.set_page_config(page_title="Monitor Strategia 70/30", layout="wide")

# 2. STILE PROFESSIONALE (Deep Black & Silver)
st.markdown("""
<style>
    .stApp { background-color: #000000; color: #e0e0e0; }
    [data-testid="stSidebar"] { background-color: #0a0a0a; border-right: 1px solid #333; }
    .stMetric { background-color: #111; border: 1px solid #333; border-radius: 5px; padding: 15px; }
    h1, h2, h3 { color: #ffffff; font-family: 'Inter', sans-serif; }
    .stTable { background-color: #000; border: 1px solid #333; }
</style>
""", unsafe_allow_html=True)

# 3. DATI STRATEGIA (VWCE 45%, QDVE 25%, ORO 20%, MINERS 10%)
pesi = {"VWCE.DE": 0.45, "QDVE.DE": 0.25, "SGLN.L": 0.20, "GDXJ": 0.10}

st.title("📟 TERMINALE PORTAFOGLIO 70/30")

with st.sidebar:
    st.header("⚙️ INPUT")
    capitale = st.number_input("Capitale Totale (€)", value=10000)
    pac = st.number_input("PAC Mensile (€)", value=500)
    st.markdown("---")
    anni_backtest = st.slider("Anni Storici", 1, 15, 10)

# 4. DOWNLOAD DATI BLINDATO
@st.cache_data
def load_data(tkrs):
    try:
        df = yf.download(tkrs, period="20y")["Close"]
        return df.ffill()
    except:
        return pd.DataFrame()

data = load_data(list(pesi.keys()))

if not data.empty:
    prezzi = {t: float(data[t].iloc[-1]) for t in pesi.keys()}
    
    # 5. QUADRO ORDINI (CHIAREZZA MASSIMA)
    st.subheader("⚖️ ORDINI PER IL RIBILANCIAMENTO")
    cap_investito = capitale + pac
    piano = []
    for t, p in pesi.items():
        v_target = cap_investito * p
        piano.append({
            "Asset": t,
            "Peso (%)": f"{p*100}%",
            "Valore (€)": f"{v_target:,.0f}",
            "Quote Totali": round(v_target / prezzi[t], 2)
        })
    st.table(pd.DataFrame(piano))

    # 6. ANALISI RISCHIO
    st.subheader("📈 PERFORMANCE E DRAWDOWN")
    c1, c2, c3, c4 = st.columns(4)
    cols = [c1, c2, c3, c4]
    
    for i, t in enumerate(pesi.keys()):
        s = data[t].tail(anni_backtest * 252)
        rend = ((s.iloc[-1] / s.iloc[0])**(1/anni_backtest) - 1) * 100
        dd = ((s / s.cummax() - 1).min()) * 100
        cols[i].metric(t.split('.')[0], f"{rend:.1f}%", f"Rischio: {dd:.1f}%", delta_color="inverse")

    # 7. PROIEZIONE 2036
    st.markdown("---")
    resa_media = 8.5 / 100 # Stima prudenziale
    v_f = [float(capitale)]
    for _ in range(120):
        v_f.append((v_f[-1] * (1 + (resa_media/12))) + pac)
    
    st.success(f"🔮 OBIETTIVO NETTO 2036 (Stima): € {v_f[-1] * 0.74:,.0f}")
else:
    st.error("Errore di connessione ai mercati. Ricarica.")
