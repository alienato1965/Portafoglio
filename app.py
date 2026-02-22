import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px

# 1. SETUP ESTETICO AVANZATO
st.set_page_config(page_title="Dashboard Elite 70/30", layout="wide")

st.markdown("""
    <style>
    /* Sfondo Nero Assoluto */
    .stApp, [data-testid="stSidebar"], .main { background-color: #000000 !important; }
    
    /* Testi Bianchi e Gialli */
    p, span, label, .stMarkdown { color: #ffffff !important; }
    
    /* Slider Giallo Ocrat */
    .stSlider [data-baseweb="slider"] [role="slider"] { background-color: #FFD700 !important; }
    .stSlider [data-baseweb="slider"] [aria-valuemax] { background-image: linear-gradient(to right, #FFD700, #FFD700) !important; }

    /* Box Metriche Neon */
    [data-testid="stMetric"] {
        background: #0a0a0a !important;
        border-radius: 15px;
        border: 1px solid #00ff00 !important;
        box-shadow: 0 0 10px rgba(0, 255, 0, 0.2);
    }
    [data-testid="stMetricValue"] {
        color: #00ff00 !important;
        font-size: 40px !important;
        text-shadow: 0 0 8px #00ff00;
    }
    
    /* Titoli Neon */
    h1, h2, h3 { color: #00ff00 !important; font-family: 'Inter', sans-serif; }
    </style>
    """, unsafe_allow_html=True)

st.title("📟 DASHBOARD ELITE 70/30")

# 2. SIDEBAR (Configurazione con Slider Gialli)
with st.sidebar:
    st.header("⚙️ CONFIGURAZIONE")
    e1 = st.text_input("ETF 1 (Core)", "VWCE.DE")
    p1 = st.slider(f"% {e1}", 0, 100, 35)
    e2 = st.text_input("ETF 2 (Core)", "QDVE.DE")
    p2 = st.slider(f"% {e2}", 0, 100, 35)
    e3 = st.text_input("ETF 3 (Gold)", "SGLN.L")
    p3 = st.slider(f"% {e3}", 0, 100, 10)
    e4 = st.text_input("ETF 4 (Miners)", "GDXJ")
    p4 = st.slider(f"% {e4}", 0, 100, 10)
    e5 = st.text_input("ETF 5", "SMH")
    p5 = st.slider(f"% {e5}", 0, 100, 5)
    e6 = st.text_input("ETF 6", "TSLA")
    p6 = st.slider(f"% {e6}", 0, 100, 5)
    
    tickers = [e1, e2, e3, e4, e5, e6]
    pesi = {e1: p1/100, e2: p2/100, e3: p3/100, e4: p4/100, e5: p5/100, e6: p6/100}
    anni = st.slider("Analisi Storica (Anni)", 5, 20, 10)

# 3. LOGICA DATI E PREZZI
@st.cache_data
def get_full_data(tkrs):
    d = yf.download(tkrs, period="25y")["Close"]
    return d.ffill()

try:
    df = get_full_data(tickers)
    prezzi_attuali = {t: float(df[t].iloc[-1]) for t in tickers}
    
    # 4. RENDIMENTI
    st.subheader("🟢 PERFORMANCE ANNUALIZZATA")
    cols = st.columns(3)
    cols2 = st.columns(3)
    all_cols = cols + cols2
    cagr_vals = {}

    for i, t in enumerate(tickers):
        s = df[t].dropna()
        n = anni * 252
        if len(s) >= n:
            v_i = float(s.iloc[-n].iloc[0] if hasattr(s.iloc[-n], 'iloc') else s.iloc[-n])
            v_f = prezzi_attuali[t]
            res = ((v_f / v_i)**(1/anni)-1)*100
            cagr_vals[t] = res
            all_cols[i].metric(t, f"{res:.1f}%")
        else:
            cagr_vals[t] = 8.0
            all_cols[i].metric(t, "N/D")

    # 5. GRAFICO TREND
    st.markdown("---")
    p_df = (df.tail(anni*252) / df.tail(anni*252).iloc[0]) * 100
    st.plotly_chart(px.line(p_df, template="plotly_dark", color_discrete_sequence=['#00ff00', '#FFD700', '#ffffff']), use_container_width=True)

    # 6. RIBILANCIATORE AVANZATO (EURO + QUOTE)
    st.markdown("---")
    st.header("⚖️ RIBILANCIAMENTO E QUOTE")
    cap = st.number_input("Valore Totale Portafoglio (€)", value=10000)
    
    st.write("### 🎯 Target Ideale")
    # Tabella per pulizia visiva
    dati_rib = []
    for t, p in pesi.items():
        valore_target = cap * p
        quote_necessarie = valore_target / prezzi_attuali[t]
        dati_rib.append({
            "Ticker": t,
            "Peso (%)": f"{p*100:.0f}%",
            "Valore Target (€)": f"{valore_target:,.2f} €",
            "Prezzo Attuale (€)": f"{prezzi_attuali[t]:,.2f} €",
            "Quote Target (Pezzi)": round(quote_necessarie, 2)
        })
    st.table(pd.DataFrame(dati_rib))

    # 7. PROIEZIONE 10 ANNI
    st.markdown("---")
    st.subheader("🔮 PROIEZIONE 2036")
    pac = st.slider("Risparmio Mensile (€)", 0, 5000, 500)
    resa = sum([cagr_vals[t] * pesi[t] for t in tickers])
    r_m = (1 + (resa / 100))**(1/12) - 1
    v_f = [float(cap)]
    for _ in range(120): v_f.append((v_f[-1] * (1 + r_m)) + pac)
    
    st.success(f"### Capitale Finale Stimato: {v_f[-1]:,.0f} €")
    st.line_chart(v_f)

except Exception as ex:
    st.error(f"Errore: {ex}")
