import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px

# 1. DESIGN "ULTRA BLACK & NEON"
st.set_page_config(page_title="Finanza Elite 70/30", layout="wide")

st.markdown("""
    <style>
    /* Sfondo nero assoluto ovunque */
    .stApp, [data-testid="stSidebar"], .main {
        background-color: #000000 !important;
    }
    
    /* Testi chiari per lo sfondo nero */
    p, span, label, .stMarkdown, [data-testid="stMetricLabel"] {
        color: #ffffff !important;
        font-family: 'Inter', sans-serif;
    }
    
    /* Box delle metriche Neon */
    [data-testid="stMetric"] {
        background: #0a0a0a !important;
        padding: 25px !important;
        border-radius: 15px;
        border: 1px solid #00ff00 !important;
        box-shadow: 0 0 15px rgba(0, 255, 0, 0.2);
        text-align: center;
    }
    
    /* Valori metriche Verde Neon Giganti */
    [data-testid="stMetricValue"] {
        color: #00ff00 !important;
        font-size: 45px !important;
        font-weight: 800 !important;
        text-shadow: 0 0 10px rgba(0, 255, 0, 0.7);
    }
    
    /* Titoli Neon */
    h1, h2, h3 { 
        color: #00ff00 !important; 
        text-transform: uppercase;
        border-bottom: 1px solid #222;
        padding-bottom: 10px;
        letter-spacing: 2px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("📟 DASHBOARD ELITE 70/30")

# 2. SIDEBAR CONFIGURAZIONE (ETF E PESI)
with st.sidebar:
    st.header("⚙️ CONFIGURAZIONE")
    
    st.subheader("🏦 CORE (70%)")
    e1 = st.text_input("ETF 1", value="VWCE.DE")
    p1 = st.slider(f"% {e1}", 0, 100, 35)
    e2 = st.text_input("ETF 2", value="QDVE.DE")
    p2 = st.slider(f"% {e2}", 0, 100, 35)
    
    st.subheader("🚀 SATELLITE (30%)")
    e3 = st.text_input("ETF 3", value="SGLN.L")
    p3 = st.slider(f"% {e3}", 0, 100, 10)
    e4 = st.text_input("ETF 4", value="GDXJ")
    p4 = st.slider(f"% {e4}", 0, 100, 10)
    e5 = st.text_input("ETF 5", value="SMH")
    p5 = st.slider(f"% {e5}", 0, 100, 5)
    e6 = st.text_input("ETF 6", value="TSLA")
    p6 = st.slider(f"% {e6}", 0, 100, 5)
    
    # Conversione in decimale
    pesi = {e1: p1/100, e2: p2/100, e3: p3/100, e4: p4/100, e5: p5/100, e6: p6/100}
    tickers = [e1, e2, e3, e4, e5, e6]
    anni = st.slider("Analisi Storica (Anni)", 5, 20, 10)

# 3. CARICAMENTO DATI
@st.cache_data
def get_data(ticker_list):
    try:
        df = yf.download(ticker_list, period="25y")["Close"]
        return df.ffill()
    except:
        return pd.DataFrame()

try:
    data = get_data(tickers)
    
    # 4. RENDIMENTI (GRIGLIA NEON)
    st.subheader("🟢 RENDIMENTI ANNUALIZZATI")
    cols = st.columns(3)
    cols_extra = st.columns(3)
    all_cols = cols + cols_extra
    cagr_vals = {}

    for i, t in enumerate(tickers):
        serie = data[t].dropna()
        giorni = anni * 252
        if len(serie) >= giorni:
            v_i = float(serie.iloc[-giorni].iloc[0] if hasattr(serie.iloc[-giorni], 'iloc') else serie.iloc[-giorni])
            v_f = float(serie.iloc[-1].iloc[0] if hasattr(serie.iloc[-1], 'iloc') else serie.iloc[-1])
            cagr = ((v_f / v_i)**(1/anni)-1)*100
            cagr_vals[t] = cagr
            all_cols[i].metric(t, f"{cagr:.1f}%")
        else:
            cagr_vals[t] = 8.0
            all_cols[i].metric(t, "N/D")

    # 5. GRAFICO TREND (BASE 100)
    st.markdown("---")
    st.subheader("📈 TREND STORICO")
    plot_df = (data.tail(anni*252) / data.tail(anni*252).iloc[0]) * 100
    fig = px.line(plot_df, template="plotly_dark")
    fig.update_layout(plot_bgcolor='#000000', paper_bgcolor='#000000', font_color="#ffffff")
    st.plotly_chart(fig, use_container_width=True)

    # 6. RIBILANCIATORE & PROIEZIONE
    st.markdown("---")
    inf1, inf2 = st.columns(2)
    
    with inf1:
        st.subheader("⚖️ RIBILANCIAMENTO")
        cap = st.number_input("Valore Portafoglio (€)", value=10000)
        for t, p in pesi.items():
            st.markdown(f"**{t}**: <span style='color:#00ff00'>{cap*p:,.0f}€</span> ({p*100:.0f}%)", unsafe_allow_html=True)
