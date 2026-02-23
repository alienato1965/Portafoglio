import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

# 1. SETUP SPAZIALE
st.set_page_config(page_title="Cyber-Terminal 70/30", layout="wide")

# CSS: MODERN DARK & NEON GLOW
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=JetBrains+Mono&display=swap');
    
    .stApp { background: radial-gradient(circle at center, #0a0a0c 0%, #000000 100%) !important; }
    
    /* Container Effetto Vetro (Glassmorphism) */
    .glass-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(0, 255, 102, 0.3);
        border-radius: 15px;
        padding: 25px;
        box-shadow: 0 8px 32px 0 rgba(0, 255, 102, 0.1);
        margin-bottom: 20px;
    }

    /* Sidebar Stealth */
    [data-testid="stSidebar"] { background-color: #050505 !important; border-right: 1px solid #00ff66; }
    
    /* Font High-Tech */
    h1, h2, h3 { font-family: 'Orbitron', sans-serif !important; color: #00ff66 !important; text-transform: uppercase; letter-spacing: 2px; }
    p, label, div, th, td { font-family: 'JetBrains Mono', monospace !important; color: #ffffff !important; }

    /* Metriche Glow */
    [data-testid="stMetricValue"] { color: #00ff66 !important; text-shadow: 0 0 10px rgba(0, 255, 102, 0.5); }
</style>
""", unsafe_allow_html=True)

# 2. COMMAND CENTER (SIDEBAR)
with st.sidebar:
    st.markdown("### 🕹️ SYSTEM SLOTS")
    s1 = st.text_input("SLOT 1 (45%)", value="VWCE.DE")
    s2 = st.text_input("SLOT 2 (25%)", value="QDVE.DE")
    s3 = st.text_input("SLOT 3 (20%)", value="SGLN.L")
    s4 = st.text_input("SLOT 4 (10%)", value="GDXJ")
    s5 = st.text_input("SLOT 5 (CASH/EXTRA)", value="")
    st.markdown("---")
    cap = st.number_input("CAPITALE (€)", value=10000, step=1000)
    pac = st.number_input("PAC (€)", value=500, step=100)

# 3. LOGICA DATI
tickers = [t for t in [s1, s2, s3, s4, s5] if t]
pesi = {s1: 0.45, s2: 0.25, s3: 0.20, s4: 0.10}
if s5: pesi[s5] = 0.0

@st.cache_data(ttl=600)
def get_data(tkrs):
    try:
        df = yf.download(tkrs, period="5d")["Close"]
        return df.ffill().iloc[-1]
    except: return None

prezzi = get_data(tickers)

# 4. DASHBOARD PRINCIPALE
st.markdown("<h1 style='text-align: center;'>ELITE STRATEGY COMMAND</h1>", unsafe_allow_html=True)

if prezzi is not None:
    # Metriche Prezzi
    cols = st.columns(len(tickers))
    for i, t in enumerate(tickers):
        if t in prezzi:
            cols[i].metric(t, f"{prezzi[t]:.2f}€")

    # Modulo Ordini (In un container Glass)
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("⚖️ REBALANCING MODULE")
    tot_val = cap + pac
    ordini_df = []
    for t, p in pesi.items():
        if t in prezzi:
            target_eur = tot_val * p
            ordini_df.append({
                "ASSET": t,
                "TARGET %": f"{p*100:.0f}%",
                "VALORE (€)": f"{target_eur:,.0f}",
                "QUOTE TOTALI": round(target_eur / prezzi[t], 3)
            })
    st.table(pd.DataFrame(ordini_df))
    st.markdown('</div>', unsafe_allow_html=True)

    # Grafico Allocazione (Glass Chart)
    c1, c2 = st.columns([2, 1])
    with c1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        fig = go.Figure(data=[go.Pie(
            labels=list(pesi.keys()),
            values=list(pesi.values()),
            hole=.7,
            marker=dict(colors=['#00ff66', '#00cc55', '#ffd700', '#ffaa00'])
        )])
        fig.update_layout(showlegend=True, paper_bgcolor='rgba(0,0,0,0)', font=dict(color="white"), margin=dict(t=0, b=0, l=0, r=0))
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with c2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("🔮 2036")
        stima = (tot_val * (1.07**10))
        st.write(f"PROIEZIONE LORDA:")
        st.markdown(f"<h2 style='color:#00ff66'>{stima:,.0f} €</h2>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

else:
    st.error("📡 SEGNALE ASSENTE: Controlla la connessione o i Ticker negli slot.")
