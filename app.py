import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px

# 1. STYLE CSS
st.set_page_config(page_title="Elite 70/30", layout="wide")
st.markdown("""
<style>
    .stApp, [data-testid="stSidebar"], .main { background-color: #000000 !important; }
    p, span, label, .stMarkdown { color: #ffffff !important; }
    /* Slider: Linea Verde e Punto Bianco */
    .stSlider [data-baseweb="slider"] [role="slider"] { background-color: #ffffff !important; border: 2px solid #00ff00 !important; }
    .stSlider [data-baseweb="slider"] [aria-valuemax] { background-image: linear-gradient(to right, #00ff00, #00ff00) !important; }
    /* Metriche */
    [data-testid="stMetric"] { background: #0a0a0a !important; border: 1px solid #00ff00 !important; border-radius: 10px; }
    [data-testid="stMetricValue"] { color: #00ff00 !important; text-shadow: 0 0 10px #00ff00; }
    h1, h2, h3 { color: #00ff00 !important; }
</style>
""", unsafe_allow_html=True)

st.title("📟 DASHBOARD ELITE 70/30")

# 2. SIDEBAR
with st.sidebar:
    st.header("⚙️ SETUP")
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
    tkrs = [e1, e2, e3, e4, e5, e6]
    pesi = {e1: p1/100, e2: p2/100, e3: p3/100, e4: p4/100, e5: p5/100, e6: p6/100}
    anni = st.slider("Anni Storici", 5, 20, 10)

# 3. DATI
@st.cache_data
def get_data(l):
    d = yf.download(l, period="25y")["Close"]
    return d.ffill()

try:
    df = get_data(tkrs)
    prezzi = {t: float(df[t].iloc[-1]) for t in tkrs}
    
    # 4. PERFORMANCE
    st.subheader("🟢 PERFORMANCE")
    cols = st.columns(3) + st.columns(3)
    cagr_dict = {}
    for i, t in enumerate(tkrs):
        s = df[t].dropna()
        n = anni * 252
        if len(s) >= n:
            v_i, v_f = float(s.iloc[-n].iloc[0] if hasattr(s.iloc[-n], 'iloc') else s.iloc[-n]), prezzi[t]
            c = ((v_f / v_i)**(1/anni)-1)*100
            cagr_dict[t] = c
            cols[i].metric(t, f"{c:.1f}%")
        else:
            cagr_dict[t] = 8.0
            cols[i].metric(t, "N/D")

    # 5. GRAFICO
    st.markdown("---")
    p_df = (df.tail(anni*252) / df.tail(anni*252).iloc[0]) * 100
    st.plotly_chart(px.line(p_df, template="plotly_dark", color_discrete_sequence=['#00ff00']), use_container_width=True)

    # 6. RIBILANCIAMENTO
    st.markdown("---")
    cap = st.number_input("Valore Portafoglio (€)", value=10000)
    res = []
    for t, p in pesi.items():
        v_target = cap * p
        res.append({"Asset": t, "Target (€)": round(v_target, 0), "Quote": round(v_target/prezzi[t], 2)})
    st.table(pd.DataFrame(res))

    # 7. PAC
    st.markdown("---")
    pac = st.slider("PAC Mensile (€)", 0, 5000, 500)
    r_m = (1 + (sum([cagr_dict[t] * pesi[t] for t in tkrs]) / 100))**(1/12) - 1
    v_f = [float(cap)]
    for _ in range(120): v_f.append((v_f[-1] * (1 + r_m)) + pac)
    st.success(f"### Capitale 2036: {v_f[-1]:,.0f} €")
    st.line_chart(v_f)

except Exception as e:
    st.error(f"Errore: {e}")
