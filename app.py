import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px

# 1. DESIGN "DARK MODE PREMIUM"
st.set_page_config(page_title="Finanza Dark 70/30", layout="wide")

st.markdown("""
    <style>
    /* Sfondo totale Nero Profondo */
    .stApp {
        background-color: #050505;
    }
    
    /* Box delle metriche stile Card Moderna */
    [data-testid="stMetric"] {
        background: linear-gradient(145deg, #111111, #1a1a1a);
        padding: 25px !important;
        border-radius: 20px;
        border: 1px solid #00ff00;
        box-shadow: 0 4px 15px rgba(0, 255, 0, 0.1);
        text-align: center;
        transition: transform 0.3s;
    }
    [data-testid="stMetric"]:hover {
        transform: translateY(-5px);
        border: 2px solid #00ff00;
    }
    
    /* Testi: Bianco per le etichette, Verde Neon per i numeri */
    [data-testid="stMetricLabel"] {
        color: #ffffff !important;
        font-size: 18px !important;
        letter-spacing: 1px;
    }
    [data-testid="stMetricValue"] {
        color: #00ff00 !important;
        font-size: 42px !important;
        font-weight: 800 !important;
        text-shadow: 0 0 10px rgba(0, 255, 0, 0.5);
    }
    
    /* Titoli e Sidebar */
    h1, h2, h3 { 
        color: #00ff00 !important; 
        font-family: 'Inter', sans-serif;
        text-transform: uppercase;
        letter-spacing: 2px;
    }
    .stSlider > div > div > div > div {
        color: #00ff00;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("📟 Dashboard Elite 70/30")

# 2. SIDEBAR CONFIGURAZIONE (Strategia 70/30 salvata)
with st.sidebar:
    st.header("🛠️ Setup Strategia")
    st.subheader("Core Assets (70%)")
    e1 = st.text_input("ETF 1 (Core)", value="VWCE.DE") #
    p1 = st.slider(f"% {e1}", 0, 100, 35) / 100
    e2 = st.text_input("ETF 2 (Core)", value="QDVE.DE") #
    p2 = st.slider(f"% {e2}", 0, 100, 35) / 100
    
    st.subheader("Satellite Assets (30%)")
    e3 = st.text_input("ETF 3 (Gold)", value="SGLN.L") #
    p3 = st.slider(f"% {e3}", 0, 100, 10) / 100
    e4 = st.text_input("ETF 4 (Miners)", value="GDXJ") #
    p4 = st.slider(f"% {e4}", 0, 100, 10) / 100
    e5 = st.text_input("ETF 5", value="SMH")
    p5 = st.slider(f"% {e5}", 0, 100, 5) / 100
    e6 = st.text_input("ETF 6", value="TSLA")
    p6 = st.slider(f"% {e6}", 0, 100, 5) / 100
    
    tickers = [e1, e2, e3, e4, e5, e6]
    pesi = {e1: p1, e2: p2, e3: p3, e4: p4, e5: p5, e6: p6}
    anni = st.slider("Analisi Storica (Anni)", 5, 20, 10)

# 3. LOGICA DATI
@st.cache_data
def get_data(ticker_list):
    return yf.download(ticker_list, period="25y")["Close"].ffill()

try:
    df = get_data(tickers)
    
    # 4. RENDIMENTI (Griglia Neon)
    st.subheader("🟢 Rendimenti Annualizzati")
    r1 = st.columns(3)
    r2 = st.columns(3)
    cols = r1 + r2
    cagr_vals = {}

    for i, t in enumerate(tickers):
        serie = df[t].dropna()
        giorni = anni * 252
        if len(serie) >= giorni:
            v_i = float(serie.iloc[-giorni].iloc[0] if hasattr(serie.iloc[-giorni], 'iloc') else serie.iloc[-giorni])
            v_f = float(serie.iloc[-1].iloc[0] if hasattr(serie.iloc[-1], 'iloc') else serie.iloc[-1])
            cagr = ((v_f / v_i)**(1/anni)-1)*100
            cagr_vals[t] = cagr
            cols[i].metric(t, f"{cagr:.1f}%")
        else:
            cagr_vals[t] = 8.0
            cols[i].metric(t, "N/D")

    # 5. GRAFICO DARK
    st.markdown("---")
    st.subheader("📈 Trend di Crescita")
    plot_df = (df.tail(anni*252) / df.tail(anni*252).iloc[0]) * 100
    fig = px.line(plot_df, template="plotly_dark", color_discrete_sequence=px.colors.qualitative.Alphabet)
    fig.update_layout(plot_bgcolor='#050505', paper_bgcolor='#050505', font_color="#00ff00")
    st.plotly_chart(fig, use_container_width=True)

    # 6. RIBILANCIATORE & PROIEZIONE
    c_rib1, c_rib2 = st.columns(2)
    with c_rib1:
        st.subheader("⚖️ Ribilanciamento")
        cap = st.number_input("Valore Portafoglio (€)", value=10000)
        for t, p in pesi.items():
            st.write(f"**{t}**: {cap*p:,.0f}€ ({p*100:.0f}%)")
            
    with c_rib2:
        st.subheader("🔮 Obiettivo 10 Anni")
        risp = st.slider("PAC Mensile (€)", 0, 5000, 500)
        resa_m = sum(cagr_vals[t] * pesi[t] for t
