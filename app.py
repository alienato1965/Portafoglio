import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px

# 1. SETUP PAGINA
st.set_page_config(page_title="Elite Terminal 70/30", layout="wide")

# 2. CSS "VERA MAGIA": Bordi Neon, Font Tecnico e Layout Denso
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&display=swap');
    
    .stApp, [data-testid="stSidebar"], .main { background-color: #000000 !important; }
    html, body, [class*="css"] { font-family: 'JetBrains Mono', monospace !important; color: #ffffff !important; }

    /* Box Performance con Glow Verde */
    [data-testid="stMetric"] {
        background: linear-gradient(145deg, #050505, #121212) !important;
        border: 1px solid #00ff00 !important;
        box-shadow: 0 0 15px rgba(0, 255, 0, 0.2) !important;
        border-radius: 4px !important;
        padding: 12px !important;
    }
    [data-testid="stMetricValue"] { color: #00ff00 !important; text-shadow: 0 0 10px #00ff00; font-size: 24px !important; }
    [data-testid="stMetricLabel"] { color: #888 !important; text-transform: uppercase; font-size: 11px !important; }

    /* Sidebar Stealth */
    [data-testid="stSidebar"] { border-right: 1px solid #1a1a1a !important; width: 320px !important; }
    
    /* Slider: Linea Verde Neon e Punto Bianco */
    .stSlider [data-baseweb="slider"] [role="slider"] { background-color: #ffffff !important; border: 2px solid #00ff00 !important; box-shadow: 0 0 10px #00ff00; }
    .stSlider [data-baseweb="slider"] [aria-valuemax] { background-image: linear-gradient(to right, #00ff00, #00ff00) !important; }

    /* Tabelle e Titoli */
    h1, h2, h3 { color: #00ff00 !important; text-shadow: 0 0 8px rgba(0,255,0,0.5); text-transform: uppercase; }
    .stTable { background-color: #050505 !important; border: 1px solid #1a1a1a !important; color: #fff !important; }
    
    /* Riduzione spazi */
    .block-container { padding-top: 1.5rem !important; }
</style>
""", unsafe_allow_html=True)

st.title("📟 ELITE PORTFOLIO COMMAND")

# 3. SIDEBAR: TUA STRATEGIA DEFINITIVA 70/30
with st.sidebar:
    st.markdown("### 🛠️ CONFIGURAZIONE ASSET")
    
    st.markdown("**CORE (70%)**")
    e1 = st.text_input("VWCE (Mondiale 45%)", "VWCE.DE")
    e2 = st.text_input("QDVE (S&P IT 25%)", "QDVE.DE")
    
    st.markdown("---")
    st.markdown("**SATELLITE (30%)**")
    e3 = st.text_input("GOLD (Oro 20%)", "SGLN.L")
    e4 = st.text_input("GDXJ (Junior Miners 10%)", "GDXJ")
    
    st.markdown("---")
    st.markdown("**EXTRA / MONITORAGGIO**")
    e5 = st.text_input("SMH (Semiconductors)", "SMH")
    e6 = st.text_input("TSLA (Speculativo)", "TSLA")
    
    tkrs = [e1, e2, e3, e4, e5, e6]
    # Pesi basati sulla tua strategia salvata
    pesi = {e1: 0.45, e2: 0.25, e3: 0.20, e4: 0.10, e5: 0.0, e6: 0.0}
    anni = st.slider("ANNI ANALISI STORICA", 5, 20, 10)

# 4. DOWNLOAD DATI
@st.cache_data
def load_market_data(t_list):
    try:
        data = yf.download(t_list, period="25y")["Close"]
        return data.ffill()
    except: return pd.DataFrame()

df = load_market_data(tkrs)

if not df.empty:
    prezzi_live = {t: float(df[t].iloc[-1]) for t in tkrs}
    
    # 🟢 PERFORMANCE
    st.subheader("🟢 ANALISI PERFORMANCE NEON")
    cl = st.columns(3) + st.columns(3)
    cagr_vals = {}
    
    for i, t in enumerate(tkrs):
        s = df[t].dropna()
        n = anni * 252
        if len(s) >= n:
            v_i, v_f = float(s.iloc[-n]), prezzi_live[t]
            c = ((v_f / v_i)**(1/anni)-1)*100
            cagr_vals[t] = c
            cl[i].metric(t.split('.')[0], f"{c:.1f}%")
        else:
            cagr_vals[t] = 8.0
            cl[i].metric(t, "N/D")

    # 📈 GRAFICO TREND (MULTICOLORE)
    st.markdown("### 📈 TREND STORICO (BASE 100)")
    p_df = (df.tail(anni*252) / df.tail(anni*252).iloc[0]) * 100
    # Palette neon: Verde, Ciano, Oro, Magenta, Arancio, Bianco
    fig = px.line(p_df, color_discrete_sequence=['#00ff00', '#00ffff', '#ffd700', '#ff00ff', '#ff8c00', '#ffffff'])
    fig.update_layout(
        height=400, margin=dict(l=0, r=0, t=20, b=0),
        plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_color="#666",
        xaxis=dict(gridcolor='#111', showline=False), yaxis=dict(gridcolor='#111', showline=False),
        legend=dict(orientation="h", y=1.1, x=1, bgcolor="rgba(0,0,0,0)", font=dict(color="#fff"))
    )
    st.plotly_chart(fig, use_container_width=True)

    # ⚖️ RIBILANCIAMENTO
    st.markdown("### ⚖️ MOTORE DI RIBILANCIAMENTO")
    cap = st.number_input("VALORE PORTAFOGLIO ATTUALE (€)", value=10000, step=1000)
    rb_res = []
    for t, p in pesi.items():
        if p > 0:
            v_t = cap * p
            rb_res.append({
                "ASSET": t,
                "PESO TARGET": f"{p*100}%",
                "VALORE TARGET (€)": f"{v_t:,.0f}",
                "QUOTE DA AVERE": round(v_t/prezzi_live[t], 2)
            })
    st.table(pd.DataFrame(rb_res))

    # 🔮 PROIEZIONE 2036
    st.markdown("---")
    pac = st.slider("INVESTIMENTO MENSILE (PAC €)", 0, 5000, 500)
    # Calcolo resa media pesata basata su strategia
    resa_p = sum([cagr_vals[t] * pesi[t] for t in tkrs if t in cagr_vals])
    r_m = (1 + (resa_p / 100))**(1/12) - 1
    v_f = [float(cap)]
    for _ in range(120): v_f.append((v_f[-1] * (1 + r_m)) + pac)
    
    st.success(f"🔮 CAPITALE STIMATO AL 2036: {v_f[-1]:,.0f} €")
    st.line_chart(v_f)

else:
    st.error("ERRORE: Impossibile caricare i dati dai mercati.")
