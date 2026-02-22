import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px

# 1. CONFIGURAZIONE PAGINA E STILE ALTA LEGGIBILITÀ
st.set_page_config(page_title="Finanza Personale 70/30", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    [data-testid="stMetric"] {
        background-color: #1e2130;
        padding: 20px !important;
        border-radius: 15px;
        border: 2px solid #3e4253;
        text-align: center;
    }
    [data-testid="stMetricLabel"] {
        color: #FFFFFF !important;
        font-size: 20px !important;
        font-weight: bold !important;
    }
    [data-testid="stMetricValue"] {
        color: #00FF00 !important;
        font-size: 35px !important;
        font-weight: 900 !important;
    }
    h1, h2, h3 { color: #00ffcc; font-family: 'Arial Black', sans-serif; }
    </style>
    """, unsafe_allow_html=True)

st.title("💎 La Mia Strategia Personalizzata")

# 2. SIDEBAR: CONFIGURAZIONE ETF E PERCENTUALI
with st.sidebar:
    st.header("⚙️ Configura Asset e Pesi")
    
    st.subheader("🏦 CORE ASSETS")
    e1 = st.text_input("ETF 1", value="VWCE.DE")
    p1 = st.slider(f"% {e1}", 0, 100, 35) / 100
    
    e2 = st.text_input("ETF 2", value="QDVE.DE")
    p2 = st.slider(f"% {e2}", 0, 100, 35) / 100
    
    st.subheader("🚀 SATELLITE ASSETS")
    e3 = st.text_input("ETF 3", value="SGLN.L")
    p3 = st.slider(f"% {e3}", 0, 100, 10) / 100
    
    e4 = st.text_input("ETF 4", value="GDXJ")
    p4 = st.slider(f"% {e4}", 0, 100, 10) / 100
    
    e5 = st.text_input("ETF 5", value="SMH")
    p5 = st.slider(f"% {e5}", 0, 100, 5) / 100
    
    e6 = st.text_input("ETF 6", value="TSLA")
    p6 = st.slider(f"% {e6}", 0, 100, 5) / 100
    
    total_p = (p1+p2+p3+p4+p5+p6)*100
    st.write(f"**Totale Allocazione: {total_p:.0f}%**")
    if total_p != 100:
        st.warning("⚠️ Attenzione: Il totale deve essere 100%!")

    tickers = [e1, e2, e3, e4, e5, e6]
    pesi = {e1: p1, e2: p2, e3: p3, e4: p4, e5: p5, e6: p6}
    anni_cagr = st.slider("Anni per analisi", 5, 20, 10)

# 3. CARICAMENTO DATI
@st.cache_data
def get_data(ticker_list):
    return yf.download(ticker_list, period="25y")["Close"].ffill()

try:
    data = get_data(tickers)
    
    # 4. RENDIMENTI (VERDE ACCESO)
    st.subheader(f"📊 Rendimento Annuo Composto ({anni_cagr} anni)")
    r1 = st.columns(3)
    r2 = st.columns(3)
    cols = r1 + r2
    cagr_results = {}

    for i, t in enumerate(tickers):
        serie = data[t].dropna()
        days = anni_cagr * 252
        if len(serie) >= days:
            v_i = float(serie.iloc[-days].iloc[0] if hasattr(serie.iloc[-days], 'iloc') else serie.iloc[-days])
            v_f = float(serie.iloc[-1].iloc[0] if hasattr(serie.iloc[-1], 'iloc') else serie.iloc[-1])
            cagr = ((v_f / v_i)**(1/anni_cagr)-1)*100
            cagr_results[t] = cagr
            cols[i].metric(t, f"{cagr:.2f}%")
        else:
            cagr_results[t] = 5.0
            cols[i].metric(t, "N/D")

    # 5. GRAFICO STORICO
    st.markdown("---")
    plot_data = data.tail(anni_cagr * 252)
    plot_norm = (plot_data / plot_data.iloc[0]) * 100
    st.plotly_chart(px.line(plot_norm, title="📈 Crescita Comparativa", template="plotly_dark"), use_container_width=True)

    # 6. RIBILANCIATORE DINAMICO
    st.markdown("---")
    st.header("⚖️ Ribilanciatore in Tempo Reale")
    capitale = st.number_input("Valore Totale Portafoglio (€)", value=10000.0)
    
    c1, c2 = st.columns(2)
    with c1:
        st.write("### 🎯 Target in Euro")
        for etf, peso in pesi.items():
            st.write(f"**{etf}**: {capitale*peso:,.2f}€ ({peso*100:.0f}%)")
    
    # 7. PROIEZIONE FUTURA BASATA SUI NUOVI PESI
    st.markdown("---")
    st.header("🔮 Simulatore 2036")
    risparmio = st.slider("Risparmio mensile (€)", 0, 5000, 500)
    
    # Calcolo resa media pesata con le tue percentuali scelte
    resa_media = sum(cagr_results[t] * pesi[t] for t in tickers)
    mesi = 10 * 12
    r_mensile = (1 + (resa_media / 100)) ** (1/12) - 1
    proiezione = [capitale]
    for m in range(mesi):
        proiezione.append((proiezione[-1] * (1 + r_mensile)) + risparmio)
    
    st.success(f"## 💰 Capitale Stimato: {proiezione[-1]:,.2f}€")
    st.line_chart(proiezione)
    st.caption(f"Rendimento medio del portafoglio scelto: {resa_media:.2f}%")

except Exception as e:
    st.error(f"Errore nel caricamento dei dati: {e}")
