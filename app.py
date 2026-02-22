import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Elite Terminal", layout="wide")

# MAGIC CSS: Riduzione dimensioni e densità dati
st.markdown("""
<style>
    /* Sfondo e Font Generale */
    .stApp, [data-testid="stSidebar"], .main { background-color: #000000 !important; }
    html, body, [class*="css"]  { font-size: 14px !important; font-family: 'JetBrains Mono', 'Courier New', monospace !important; }
    
    /* Riduzione Margini e Padding */
    .block-container { padding-top: 1rem !important; padding-bottom: 0rem !important; }
    .stMetric { padding: 5px 10px !important; }
    
    /* Metriche compatte con Glow Verde */
    [data-testid="stMetric"] { 
        background: #050505 !important; 
        border: 1px solid #00ff00 !important; 
        box-shadow: 0 0 8px rgba(0, 255, 0, 0.2);
        border-radius: 5px;
        margin-bottom: 5px !important;
    }
    [data-testid="stMetricValue"] { font-size: 22px !important; color: #00ff00 !important; }
    [data-testid="stMetricLabel"] { font-size: 12px !important; color: #aaaaaa !important; }

    /* Slider piccoli e verdi */
    .stSlider { padding-bottom: 0px !important; }
    .stSlider [data-baseweb="slider"] [role="slider"] { width: 12px !important; height: 12px !important; background-color: #fff !important; border: 1px solid #00ff00 !important; }

    /* Tabelle compatte */
    .stTable { font-size: 12px !important; }
    
    /* Header e testi */
    h1 { font-size: 24px !important; color: #00ff00 !important; text-shadow: 0 0 5px #00ff00; }
    h2, h3 { font-size: 18px !important; color: #00ff00 !important; margin-top: 10px !important; }
    
    /* Sidebar compatta */
    [data-testid="stSidebar"] { width: 250px !important; }
</style>
""", unsafe_allow_html=True)

st.title("📟 ELITE SYSTEM v2.0")

# Parametri fissi dalla tua strategia
with st.sidebar:
    st.markdown("### 🛠 CONFIG")
    e1 = st.text_input("CORE 1", "VWCE.DE")
    p1 = st.slider(f"% {e1}", 0, 100, 35)
    e2 = st.text_input("CORE 2", "QDVE.DE")
    p2 = st.slider(f"% {e2}", 0, 100, 35)
    e3 = st.text_input("GOLD", "SGLN.L")
    p3 = st.slider(f"% {e3}", 0, 100, 20)
    e4 = st.text_input("MINERS", "GDXJ")
    p4 = st.slider(f"% {e4}", 0, 100, 10)
    tkrs = [e1, e2, e3, e4]
    pesi = {e1:p1/100, e2:p2/100, e3:p3/100, e4:p4/100}
    anni = st.number_input("ANNI ANALISI", 5, 20, 10)

@st.cache_data
def load_data(l):
    try:
        d = yf.download(l, period="25y")["Close"]
        return d.ffill()
    except: return pd.DataFrame()

df = load_data(tkrs)

if not df.empty:
    prezzi = {t: float(df[t].iloc[-1]) for t in tkrs}
    
    # 4 PERFORMANCE COMPATTE
    st.markdown("### 🟢 PERFORMANCE")
    cols = st.columns(4)
    cagr = {}
    for i, t in enumerate(tkrs):
        s = df[t].dropna()
        n = anni * 252
        if len(s) >= n:
            v_i, v_f = float(s.iloc[-n]), prezzi[t]
            val = ((v_f / v_i)**(1/anni)-1)*100
            cagr[t] = val
            cols[i].metric(t, f"{val:.1f}%")
        else:
            cagr[t] = 8.0
            cols[i].metric(t, "N/A")

    # TREND STORICO BASSO
    st.markdown("---")
    p_df = (df.tail(anni*252) / df.tail(anni*252).iloc[0]) * 100
    fig = px.line(p_df, color_discrete_sequence=['#00ff00', '#00ffff', '#ffd700', '#ff00ff'])
    fig.update_layout(
        height=300, # Più basso per non occupare tutto lo schermo
        margin=dict(l=0, r=0, t=20, b=0),
        plot_bgcolor='#000000', paper_bgcolor='#000000', font_color="#ffffff",
        xaxis=dict(gridcolor='#111'), yaxis=dict(gridcolor='#111'),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    st.plotly_chart(fig, use_container_width=True)

    # REBALANCING COMPATTO
    st.markdown("### ⚖ REBALANCING")
    cap = st.number_input("CAPITALE (€)", value=10000, step=1000)
    res = []
    for t, p in pesi.items():
        v_t = cap * p
        res.append({"Asset": t, "Target €": f"{v_t:,.0f}", "Quote": round(v_t/prezzi[t], 2)})
    st.table(pd.DataFrame(res))

    # PAC 10 ANNI
    st.markdown("---")
    pac = st.number_input("PAC MENSILE (€)", 0, 5000, 500)
    r_m = (1 + (sum([cagr[t] * pesi[t] for t in tkrs]) / 100))**(1/12) - 1
    v_f = [float(cap)]
    for _ in range(120): v_f.append((v_f[-1] * (1 + r_m)) + pac)
    
    st.success(f"🔮 PROIEZIONE 2036: {v_f[-1]:,.0f} €")
else:
    st.error("ERRORE DATI")
