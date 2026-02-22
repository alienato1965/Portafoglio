import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px

# 1. SETUP GRAFICO PREMIUM
st.set_page_config(page_title="Portfolio Elite", layout="wide")

st.markdown("""
    <style>
    .stApp, [data-testid="stSidebar"], .main { background-color: #000000 !important; }
    p, span, label, .stMarkdown { color: #ffffff !important; }
    [data-testid="stMetric"] {
        background: #0a0a0a !important;
        padding: 20px !important;
        border-radius: 15px;
        border: 1px solid #00ff00 !important;
    }
    [data-testid="stMetricValue"] {
        color: #00ff00 !important;
        font-size: 40px !important;
        text-shadow: 0 0 10px #00ff00;
    }
    h1, h2, h3 { color: #00ff00 !important; }
    </style>
    """, unsafe_allow_html=True)

st.title("📟 DASHBOARD ELITE 70/30")

# 2. SIDEBAR CON INPUT
with st.sidebar:
    st.header("⚙️ CONFIGURAZIONE")
    e1 = st.text_input("ETF 1", "VWCE.DE")
    p1 = st.slider(f"% {e1}", 0, 100, 35)
    e2 = st.text_input("ETF 2", "QDVE.DE")
    p2 = st.slider(f"% {e2}", 0, 100, 35)
    e3 = st.text_input("ETF 3", "SGLN.L")
    p3 = st.slider(f"% {e3}", 0, 100, 10)
    e4 = st.text_input("ETF 4", "GDXJ")
    p4 = st.slider(f"% {e4}", 0, 100, 10)
    e5 = st.text_input("ETF 5", "SMH")
    p5 = st.slider(f"% {e5}", 0, 100, 5)
    e6 = st.text_input("ETF 6", "TSLA")
    p6 = st.slider(f"% {e6}", 0, 100, 5)
    
    tickers = [e1, e2, e3, e4, e5, e6]
    pesi = {e1: p1/100, e2: p2/100, e3: p3/100, e4: p4/100, e5: p5/100, e6: p6/100}
    anni = st.slider("Anni Storici", 5, 20, 10)

# 3. LOGICA DATI
@st.cache_data
def get_data(tkrs):
    d = yf.download(tkrs, period="25y")["Close"]
    return d.ffill()

try:
    df = get_data(tickers)
    st.subheader("🟢 PERFORMANCE ANNUALIZZATA")
    c = st.columns(3)
    c2 = st.columns(3)
    cols = c + c2
    cagr_vals = {}

    for i, t in enumerate(tickers):
        s = df[t].dropna()
        n = anni * 252
        if len(s) >= n:
            v_i = float(s.iloc[-n].iloc[0] if hasattr(s.iloc[-n], 'iloc') else s.iloc[-n])
            v_f = float(s.iloc[-1].iloc[0] if hasattr(s.iloc[-1], 'iloc') else s.iloc[-1])
            res = ((v_f / v_i)**(1/anni)-1)*100
            cagr_vals[t] = res
            cols[i].metric(t, f"{res:.1f}%")
        else:
            cagr_vals[t] = 8.0
            cols[i].metric(t, "N/D")

    # 4. GRAFICO & RIBILANCIATORE
    st.markdown("---")
    p_df = (df.tail(anni*252) / df.tail(anni*252).iloc[0]) * 100
    st.plotly_chart(px.line(p_df, template="plotly_dark"), use_container_width=True)

    st.markdown("---")
    inf1, inf2 = st.columns(2)
    with inf1:
        st.subheader("⚖️ RIBILANCIAMENTO")
        cap = st.number_input("Valore Portafoglio (€)", value=10000)
        for t, p in pesi.items():
            st.write(f"**{t}**: {cap*p:,.0f}€ ({p*100:.0f}%)")
            
    with inf2:
        st.subheader("🔮 PROIEZIONE 10 ANNI")
        pac = st.slider("PAC Mensile (€)", 0, 5000, 500)
        resa = sum([cagr_vals[t] * pesi[t] for t in tickers])
        r_m = (1 + (resa / 100))**(1/12) - 1
        v_f = [float(cap)]
        for _ in range(120): v_f.append((v_f[-1] * (1 + r_m)) + pac)
        st.success(f"### Capitale 2036: {v_f[-1]:,.0f}€")
        st.line_chart(v_f)

except Exception as ex:
    st.error(f"Errore: {ex}")
