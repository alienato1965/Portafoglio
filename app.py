import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Elite 70/30", layout="wide")

# CSS: NERO TOTALE + SLIDER VERDE/BIANCO
st.markdown("""
<style>
    .stApp, [data-testid="stSidebar"], .main { background-color: #000000 !important; }
    p, span, label, .stMarkdown { color: #ffffff !important; }
    .stSlider [data-baseweb="slider"] [role="slider"] { background-color: #ffffff !important; border: 2px solid #00ff00 !important; }
    .stSlider [data-baseweb="slider"] [aria-valuemax] { background-image: linear-gradient(to right, #00ff00, #00ff00) !important; }
    [data-testid="stMetric"] { background: #0a0a0a !important; border: 1px solid #00ff00 !important; border-radius: 10px; }
    [data-testid="stMetricValue"] { color: #00ff00 !important; text-shadow: 0 0 10px #00ff00; }
    h1, h2, h3 { color: #00ff00 !important; }
</style>
""", unsafe_allow_html=True)

st.title("📟 DASHBOARD ELITE 70/30")

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
    pesi = {e1:p1/100, e2:p2/100, e3:p3/100, e4:p4/100, e5:p5/100, e6:p6/100}
    anni = st.slider("Anni", 5, 20, 10)

@st.cache_data
def load_data(l):
    try:
        d = yf.download(l, period="25y")["Close"]
        return d.ffill()
    except: return pd.DataFrame()

df = load_data(tkrs)

if not df.empty:
    prezzi = {t: float(df[t].iloc[-1]) for t in tkrs}
    st.subheader("🟢 PERFORMANCE")
    cl = st.columns(3) + st.columns(3)
    cagr = {}
    for i, t in enumerate(tkrs):
        s = df[t].dropna()
        n = anni * 252
        if len(s) >= n:
            v_i, v_f = float(s.iloc[-n]), prezzi[t]
            val = ((v_f / v_i)**(1/anni)-1)*100
            cagr[t] = val
            cl[i].metric(t, f"{val:.1f}%")
        else:
            cagr[t] = 8.0
            cl[i].metric(t, "N/D")

    st.markdown("---")
    st.subheader("📈 TREND STORICO MULTICOLORE")
    p_df = (df.tail(anni*252) / df.tail(anni*252).iloc[0]) * 100
    # Palette Neon: Verde, Ciano, Oro, Magenta, Arancio, Bianco
    fig = px.line(p_df, color_discrete_sequence=['#00ff00', '#00ffff', '#ffd700', '#ff00ff', '#ff8c00', '#ffffff'])
    fig.update_layout(plot_bgcolor='#000000', paper_bgcolor='#000000', font_color="#ffffff",
                      legend=dict(bgcolor="rgba(0,0,0,0)"))
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    st.header("⚖️ RIBILANCIAMENTO")
    cap = st.number_input("Valore Portafoglio (€)", value=10000)
    res = []
    for t, p in pesi.items():
        v_t = cap * p
        res.append({"Asset": t, "Target (€)": round(v_t, 0), "Quote": round(v_t/prezzi[t], 2)})
    st.table(pd.DataFrame(res))

    st.markdown("---")
    pac = st.slider("PAC Mensile (€)", 0, 5000, 500)
    r_m = (1 + (sum([cagr[t] * pesi[t] for t in tkrs]) / 100))**(1/12) - 1
    v_f = [float(cap)]
    for _ in range(120): v_f.append((v_f[-1] * (1 + r_m)) + pac)
    st.success(f"### Capitale Finale 2036: {v_f[-1]:,.0f} €")
    st.line_chart(v_f)
else:
    st.error("Errore caricamento dati.")
