import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px

# 1. SETUP PAGINA
st.set_page_config(
    page_title="Elite Terminal", 
    layout="wide"
)

# 2. CSS COMPATTO (NERO E NEON)
st.markdown("""
<style>
    .stApp, [data-testid="stSidebar"], .main { 
        background-color: #000000 !important; 
    }
    p, span, label, .stMarkdown { 
        color: #ffffff !important; 
        font-family: monospace; 
    }
    [data-testid="stMetric"] {
        background: #080808 !important; 
        border: 1px solid #00ff00 !important;
        padding: 10px;
    }
    [data-testid="stMetricValue"] { 
        color: #00ff00 !important; 
    }
    h1, h2, h3 { 
        color: #00ff00 !important; 
    }
    .stSlider [data-baseweb="slider"] [role="slider"] {
        background-color: #fff !important;
        border: 2px solid #00ff00 !important;
    }
</style>
""", unsafe_allow_html=True)

st.title("📟 ELITE PORTFOLIO COMMAND")

# 3. SIDEBAR CON TUA STRATEGIA 2026
with st.sidebar:
    st.header("⚙️ SETUP")
    e1 = st.text_input("CORE 1 (45%)", "VWCE.DE")
    e2 = st.text_input("CORE 2 (25%)", "QDVE.DE")
    e3 = st.text_input("GOLD (20%)", "SGLN.L")
    e4 = st.text_input("MINERS (10%)", "GDXJ")
    
    tkrs = [e1, e2, e3, e4]
    pesi = {e1: 0.45, e2: 0.25, e3: 0.20, e4: 0.10}
    anni = st.slider("ANNI ANALISI", 5, 20, 10)

# 4. DOWNLOAD DATI
@st.cache_data
def load_data(lista):
    try:
        d = yf.download(lista, period="25y")["Close"]
        return d.ffill()
    except:
        return pd.DataFrame()

df = load_data(tkrs)

# 5. LOGICA PRINCIPALE
if not df.empty:
    prezzi = {t: float(df[t].iloc[-1]) for t in tkrs}
    
    st.subheader("🟢 RENDIMENTI ANNUI")
    cl = st.columns(4)
    cagr_v = {}
    
    for i, t in enumerate(tkrs):
        s = df[t].dropna()
        n = anni * 252
        if len(s) >= n:
            v_i = float(s.iloc[-n])
            v_f = prezzi[t]
            c = ((v_f / v_i)**(1/anni)-1)*100
            cagr_v[t] = c
            cl[i].metric(t.split('.')[0], f"{c:.1f}%")
        else:
            cagr_v[t] = 8.0
            cl[i].metric(t, "N/D")

    # 6. GRAFICO TREND
    st.markdown("---")
    st.subheader("📈 TREND STORICO")
    p_df = (df.tail(anni*252) / df.tail(anni*252).iloc[0]) * 100
    
    fig = px.line(
        p_df, 
        color_discrete_sequence=['#00ff00', '#00ffff', '#ffd700', '#ff00ff']
    )
    fig.update_layout(
        plot_bgcolor='black',
        paper_bgcolor='black',
        font_color='white',
        height=400
    )
    st.plotly_chart(fig, use_container_width=True)

    # 7. RIBILANCIAMENTO
    st.markdown("---")
    st.subheader("⚖️ TARGET PORTAFOGLIO")
    cap = st.number_input("CAPITALE ATTUALE (€)", value=10000)
    
    for t, p in pesi.items():
        v_t = cap * p
        q = round(v_t/prezzi[t], 2)
        st.write(f"**{t}**: {v_t:,.0f}€ ({q} quote)")

    # 8. PROIEZIONE 2036
    st.markdown("---")
    pac = st.slider("PAC MENSILE (€)", 0, 5000, 500)
    r_a = sum([cagr_v[t] * pesi[t] for t in tkrs])
    r_m = (1 + (r_a / 100))**(1/12) - 1
    
    v_f = [float(cap)]
    for _ in range(120):
        v_f.append((v_f[-1] * (1 + r_m)) + pac)
    
    st.success(f"🔮 CAPITALE STIMATO 2036: {v_f[-1]:,.0f} €")
    st.line_chart(v_f)

else:
    st.error("ERRORE CARICAMENTO DATI")
