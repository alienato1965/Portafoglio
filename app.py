import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px

# 1. DESIGN "DARK MODE PREMIUM"
st.set_page_config(page_title="Finanza Dark 70/30", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #050505; }
    [data-testid="stMetric"] {
        background: linear-gradient(145deg, #111111, #1a1a1a);
        padding: 25px !important;
        border-radius: 20px;
        border: 1px solid #00ff00;
        box-shadow: 0 4px 15px rgba(0, 255, 0, 0.1);
        text-align: center;
    }
    [data-testid="stMetricLabel"] { color: #ffffff !important; font-size: 18px !important; }
    [data-testid="stMetricValue"] {
        color: #00ff00 !important;
        font-size: 40px !important;
        font-weight: 800 !important;
        text-shadow: 0 0 10px rgba(0, 255, 0, 0.5);
    }
    h1, h2, h3 { color: #00ff00 !important; letter-spacing: 2px; }
    </style>
    """, unsafe_allow_html=True)

st.title("📟 DASHBOARD ELITE 70/30")

# 2. SIDEBAR CONFIGURAZIONE
with st.sidebar:
    st.header("🛠️ Setup Strategia")
    st.subheader("Core Assets (70%)")
    e1 = st.text_input("ETF 1", value="VWCE.DE")
    p1 = st.slider(f"% {e1}", 0, 100, 35) / 100
    e2 = st.text_input("ETF 2", value="QDVE.DE")
    p2 = st.slider(f"% {e2}", 0, 100, 35) / 100
    
    st.subheader("Satellite Assets (30%)")
    e3 = st.text_input("ETF 3", value="SGLN.L")
    p3 = st.slider(f"% {e3}", 0, 100, 10) / 100
    e4 = st.text_input("ETF 4", value="GDXJ")
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
    d = yf.download(ticker_list, period="25y")["Close"]
    return d.ffill()

try:
    df = get_data(tickers)
    
    # 4. RENDIMENTI (GRIGLIA NEON)
    st.subheader("🟢 RENDIMENTI ANNUALIZZATI")
    r1 = st.columns(3)
    r2 = st.columns(3)
    cols = r1 + r2
    cagr_vals = {}

    for i, t in enumerate(tickers):
        serie = df[t].dropna()
        g = anni * 252
        if len(serie) >= g:
            v_i = float(serie.iloc[-g].iloc[0] if hasattr(serie.iloc[-g], 'iloc') else serie.iloc[-g])
            v_f = float(serie.iloc[-1].iloc[0] if hasattr(serie.iloc[-1], 'iloc') else serie.iloc[-1])
            cagr = ((v_f / v_i)**(1/anni)-1)*100
            cagr_vals[t] = cagr
            cols[i].metric(t, f"{cagr:.1f}%")
        else:
            cagr_vals[t] = 8.0
            cols[i].metric(t, "N/D")

    # 5. GRAFICO DARK
    st.markdown("---")
    st.subheader("📈 TREND DI CRESCITA (BASE 100)")
    # RIGA CORRETTA 99:
    plot_df = (df.tail(anni*252) / df.tail(anni*252).iloc[0]) * 100
    fig = px.line(plot_df, template="plotly_dark")
    fig.update_layout(plot_bgcolor='#050505', paper_bgcolor='#050505', font_color="#00ff00")
    st.plotly_chart(fig, use_container_width=True)

    # 6. RIBILANCIATORE & PROIEZIONE
    st.markdown("---")
    c_rib1, c_rib2 = st.columns(2)
    with c_rib1:
        st.subheader("⚖️ RIBILANCIAMENTO")
        cap = st.number_input("Valore Portafoglio (€)", value=10000)
        for t, p in pesi.items():
            st.write(f"**{t}**: {cap*p:,.0f}€ ({p*100:.0f}%)")
            
    with c_rib2:
        st.subheader("🔮 PROIEZIONE 10 ANNI")
        risp = st.slider("PAC Mensile (€)", 0, 5000, 500)
        # RIGA CORRETTA 129:
        resa_m = sum([cagr_vals[t] * pesi[t] for t in tickers if t in cagr_vals])
        r_mensile = (1 + (resa_m / 100)) ** (1/12) - 1
        val_list = [float(cap)]
        for m in range(120):
            val_list.append((val_list[-1] * (1 + r_mensile)) + risp)
        st.success(f"### Capitale Finale: {val_list[-1]:,.0f}€")
        st.line_chart(val_list)

except Exception as e:
    st.error(f"Si è verificato un errore: {e}")
