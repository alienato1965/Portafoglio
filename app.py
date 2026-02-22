import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px
import numpy as np

st.set_page_config(page_title="Elite Terminal 70/30", layout="wide")

# CSS: ESTETICA "BLACK OPS"
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&display=swap');
    .stApp, [data-testid="stSidebar"], .main { background-color: #000000 !important; }
    html, body, [class*="css"] { font-family: 'JetBrains Mono', monospace !important; color: #ffffff !important; }
    [data-testid="stMetric"] {
        background: #080808 !important; border: 1px solid #00ff00 !important;
        box-shadow: 0 0 10px rgba(0, 255, 0, 0.2) !important; border-radius: 4px; padding: 12px;
    }
    [data-testid="stMetricValue"] { color: #00ff00 !important; text-shadow: 0 0 8px #00ff00; }
    .stSlider [data-baseweb="slider"] [role="slider"] { background-color: #fff !important; border: 2px solid #00ff00 !important; }
    .stSlider [data-baseweb="slider"] [aria-valuemax] { background-image: linear-gradient(to right, #00ff00, #00ff00) !important; }
    h1, h2, h3 { color: #00ff00 !important; text-transform: uppercase; }
</style>
""", unsafe_allow_html=True)

st.title("📟 ELITE PORTFOLIO COMMAND v3.0")

with st.sidebar:
    st.markdown("### 🛠️ STRATEGIA 70/30")
    e1 = st.text_input("CORE: VWCE (45%)", "VWCE.DE")
    e2 = st.text_input("CORE: QDVE (25%)", "QDVE.DE")
    e3 = st.text_input("SAT: ORO (20%)", "SGLN.L")
    e4 = st.text_input("SAT: MINERS (10%)", "GDXJ")
    tkrs = [e1, e2, e3, e4]
    pesi = {e1: 0.45, e2: 0.25, e3: 0.20, e4: 0.10}
    anni = st.slider("ORIZZONTE ANALISI", 5, 20, 10)
    inflazione = st.slider("INFLAZIONE STIMATA (%)", 0.0, 5.0, 2.0)

@st.cache_data
def load_data(l):
    try:
        d = yf.download(l, period="25y")["Close"]
        return d.ffill()
    except: return pd.DataFrame()

df = load_data(tkrs)

if not df.empty:
    prezzi = {t: float(df[t].iloc[-1]) for t in tkrs}
    
    # 🟢 PERFORMANCE E DRAWDOWN
    st.subheader("🟢 STATUS ATTUALE E RISCHIO")
    c1, c2, c3, c4 = st.columns(4)
    cols = [c1, c2, c3, c4]
    cagr_v = {}
    
    for i, t in enumerate(tkrs):
        s = df[t].dropna()
        n = anni * 252
        if len(s) >= n:
            v_i, v_f = float(s.iloc[-n]), prezzi[t]
            c = ((v_f / v_i)**(1/anni)-1)*100
            cagr_v[t] = c
            # Calcolo Drawdown Massimo
            window = s.tail(n)
            dd = (window / window.cummax() - 1).min() * 100
            cols[i].metric(t.split('.')[0], f"{c:.1f}%", f"DD: {dd:.1f}%", delta_color="inverse")
        else:
            cagr_v[t] = 8.0
            cols[i].metric(t, "N/D")

    # 📈 TREND
    st.markdown("---")
    p_df = (df.tail(anni*252) / df.tail(anni*252).iloc[0]) * 100
    fig = px.line(p_df, color_discrete_sequence=['#00ff00', '#00ffff', '#ffd700', '#ff00ff'])
    fig.update_layout(height=350, plot_bgcolor='black', paper_bgcolor='black', font_color="#666")
    st.plotly_chart(fig, use_container_width=True)

    # ⚖️ RIBILANCIAMENTO
    st.markdown("### ⚖️ ORDINI NECESSARI")
    cap = st.number_input("CAPITALE ATTUALE (€)", value=10000)
    res = []
    for t, p in pesi.items():
        v_t = cap * p
        res.append({"ASSET": t, "TARGET €": f"{v_t:,.0f}", "QUOTE": round(v_t/prezzi[t], 2)})
    st.table(pd.DataFrame(res))

    # 🔮 PROIEZIONE REALE 2036
    st.markdown("### 🔮 PROIEZIONE NETTA 2036")
    pac = st.slider("PAC MENSILE (€)", 0, 5000, 500)
    r_a = sum([cagr_v[t] * pesi[t] for t in tkrs])
    r_m = (1 + (r_a / 100))**(1/12) - 1
    inf_m = (1 + (inflazione / 100))**(1/12) - 1
    
    v_f = [float(cap)]
    v_reale = [float(cap)]
    
    for _ in range(120):
        v_f.append((v_f[-1] * (1 + r_m)) + pac)
        v_reale.append((v_reale[-1] * (1 + r_m - inf_m)) + (pac / (1 + inf_m)**(_)))

    lordo = v_f[-1]
    tasse = (lordo - cap - (pac * 120)) * 0.26
    netto = lordo - tasse
    potere_acquisto = v_reale[-1] - (tasse / (1 + inflazione/100)**10)

    col1, col2, col3 = st.columns(3)
    col1.metric("LORDO STIMATO", f"{lordo:,.0f} €")
    col2.metric("NETTO (Tasse 26%)", f"{netto:,.0f} €")
    col3.metric("VALORE REALE (Inflazione)", f"{potere_acquisto:,.0f} €", border=True)

    st.info(f"💡 Nel 2036, i tuoi {lordo:,.0f}€ varranno come
