import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Elite Terminal v6", layout="wide")

# CSS: STILE COMANDO OPERATIVO
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&display=swap');
    .stApp { background-color: #000000 !important; font-family: 'JetBrains Mono', monospace; }
    [data-testid="stMetric"] {
        background: #080808 !important; border: 1px solid #00ff00 !important;
        box-shadow: 0 0 10px rgba(0, 255, 0, 0.2); border-radius: 4px; padding: 12px;
    }
    [data-testid="stMetricValue"] { color: #00ff00 !important; text-shadow: 0 0 8px #00ff00; }
    h1, h2, h3 { color: #00ff00 !important; text-transform: uppercase; }
    .stTable { background-color: #050505 !important; color: white !important; }
</style>
""", unsafe_allow_html=True)

st.title("📟 ELITE STRATEGY COMMAND v6.0")

# DEFINIZIONE STRATEGIA 70/30 (Core/Satellite)
assets = {
    "VWCE.DE": 0.45, # Core Mondiale
    "QDVE.DE": 0.25, # Core Tech
    "SGLN.L": 0.20,  # Satellite Oro
    "GDXJ": 0.10     # Satellite Junior Miners
}

with st.sidebar:
    st.header("⚙️ OPERATIVITÀ")
    cap_totale = st.number_input("Capitale Totale (€)", value=10000, step=1000)
    pac_mensile = st.number_input("PAC da investire oggi (€)", value=500, step=100)
    st.markdown("---")
    anni_analisi = st.slider("Anni Storici", 5, 20, 10)

@st.cache_data
def load_market_data(tickers):
    return yf.download(tickers, period="25y")["Close"].ffill()

df = load_market_data(list(assets.keys()))

if not df.empty:
    prezzi_oggi = {t: float(df[t].iloc[-1]) for t in assets.keys()}
    
    # 1. ANALISI PERFORMANCE
    st.subheader("🟢 ANALISI RENDIMENTI E RISCHIO")
    cols = st.columns(4)
    cagr_list = {}
    
    for i, (t, peso) in enumerate(assets.items()):
        s = df[t].tail(anni_analisi*252)
        cagr = ((s.iloc[-1] / s.iloc[0])**(1/anni_analisi)-1)*100
        cagr_list[t] = cagr
        dd = ((s / s.cummax() - 1).min()) * 100
        cols[i].metric(t.split('.')[0], f"{cagr:.1f}%", f"Max DD: {dd:.1f}%", delta_color="inverse")

    # 2. MOTORE DI RIBILANCIAMENTO (ORDINI)
    st.markdown("---")
    st.subheader("⚖️ ORDINI PER IL RIBILANCIAMENTO")
    st.write(f"Distribuzione del capitale totale ({cap_totale + pac_mensile:,.0f} €) inclusa la quota PAC:")
    
    nuovo_totale = cap_totale + pac_mensile
    dati_ordini = []
    
    for t, peso in assets.items():
        valore_target = nuovo_totale * peso
        quote_necessarie = valore_target / prezzi_oggi[t]
        dati_ordini.append({
            "Asset": t,
            "Peso Target": f"{peso*100}%",
            "Valore Target (€)": f"{valore_target:,.0f}",
            "Prezzo Attuale (€)": round(prezzi_oggi[t], 2),
            "Quote Totali da Avere": round(quote_necessarie, 2)
        })
    
    st.table(pd.DataFrame(dati_ordini))

    # 3. TREND STORICO CONSOLIDATO
    st.markdown("---")
    st.subheader("📈 CONFRONTO STORICO ASSET")
    p_df = (df.tail(anni_analisi*252) / df.tail(anni_analisi*252).iloc[0]) * 100
    fig = px.line(p_df, color_discrete_sequence=['#00ff00', '#00ffff', '#ffd700', '#ff00ff'])
    fig.update_layout(height=400, plot_bgcolor='black', paper_bgcolor='black', font_color='white',
                      xaxis=dict(gridcolor='#111'), yaxis=dict(gridcolor='#111'))
    st.plotly_chart(fig, use_container_width=True)

    # 4. TARGET 2036
    st.markdown("---")
    st.subheader("🔮 OBIETTIVO 2036")
    resa_p = sum([cagr_list[t] * assets[t] for t in assets])
    r_m = (1 + (resa_p / 100))**(1/12) - 1
    
    valori = [float(cap_totale)]
    for _ in range(120): # 10 anni
        valori.append((valori[-1] * (1 + r_m)) + (pac_mensile if pac_mensile > 0 else 500))
    
    st.success(f"PROIEZIONE FINALE: {valori[-1]:,.0f} € (Resa media stimata: {resa_p:.2f}%)")

else:
    st.error("ERRORE: Impossibile recuperare i prezzi di mercato.")
