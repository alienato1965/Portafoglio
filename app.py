import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="Elite Terminal", layout="wide")

# CSS "CATTIVO": SFONDO OPACO, BORDI NEON, FONT MONOSPACE
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&display=swap');
    
    .stApp {
        background: radial-gradient(circle, #1a1a1a 0%, #000000 100%) !important;
        font-family: 'JetBrains Mono', monospace !important;
    }
    
    /* Sidebar Minimalista */
    [data-testid="stSidebar"] {
        background-color: rgba(10, 10, 10, 0.9) !important;
        border-right: 1px solid #222;
    }

    /* Card per le Metriche con Glow Effect */
    [data-testid="stMetric"] {
        background: rgba(20, 20, 20, 0.8) !important;
        border: 1px solid #333 !important;
        box-shadow: 0px 4px 15px rgba(0, 255, 102, 0.1);
        border-radius: 10px !important;
        padding: 20px !important;
    }
    
    [data-testid="stMetricValue"] {
        color: #00ff66 !important;
        text-shadow: 0 0 10px rgba(0, 255, 102, 0.5);
    }

    /* Tabella High-Tech */
    .stTable {
        background-color: transparent !important;
        border-radius: 10px;
        overflow: hidden;
    }
    
    thead tr th {
        background-color: #111 !important;
        color: #00ff66 !important;
        text-transform: uppercase;
        font-size: 12px !important;
    }

    /* Divider Neon */
    .neon-hr {
        height: 2px;
        background: linear-gradient(90deg, transparent, #00ff66, transparent);
        margin: 20px 0;
    }
</style>
""", unsafe_allow_html=True)

# 1. SETUP ASSET (45% VWCE, 25% QDVE, 20% ORO, 10% MINERS)
assets = {
    "VWCE.DE": {"peso": 0.45, "tipo": "CORE", "color": "#00ff66"},
    "QDVE.DE": {"peso": 0.25, "tipo": "CORE", "color": "#00cc55"},
    "SGLN.L": {"peso": 0.20, "tipo": "SATELLITE", "color": "#ffd700"},
    "GDXJ": {"peso": 0.10, "tipo": "SATELLITE", "color": "#ffaa00"}
}

# 2. SIDEBAR OPERATIVA
with st.sidebar:
    st.markdown("<h2 style='color: #00ff66;'>🕹️ COMMAND</h2>", unsafe_allow_html=True)
    cap_tot = st.number_input("CAPITALE ATTUALE (€)", value=10000, step=1000)
    pac_val = st.number_input("PAC MENSILE (€)", value=500, step=100)
    st.markdown("<div class='neon-hr'></div>", unsafe_allow_html=True)
    st.markdown("### 🏷️ ASSETS")
    for t, info in assets.items():
        st.write(f"**{t}** | {info['tipo']} ({info['peso']*100:.0f}%)")

# 3. DOWNLOAD DATI
@st.cache_data
def get_data(tickers):
    d = yf.download(tickers, period="5d")["Close"]
    return d.ffill().iloc[-1]

st.markdown("<h1 style='text-align: center; color: white;'>ELITE STRATEGY TERMINAL</h1>", unsafe_allow_html=True)
st.markdown("<div class='neon-hr'></div>", unsafe_allow_html=True)

prezzi = get_data(list(assets.keys()))

if prezzi is not None:
    # 4. MONITOR REAL-TIME (Grid Layout)
    cols = st.columns(4)
    for i, (t, info) in enumerate(assets.items()):
        cols[i].metric(t, f"{prezzi[t]:.2f}€", f"{info['peso']*100}% TARGET")

    st.markdown("<br>", unsafe_allow_html=True)

    # 5. PIANO ORDINI (Tabella con stile)
    st.subheader("⚖️ REBALANCING ORDERS")
    nuovo_tot = cap_tot + pac_val
    ordini_df = []
    for t, info in assets.items():
        val_target = nuovo_tot * info['peso']
        ordini_df.append({
            "ASSET": t,
            "TARGET %": f"{info['peso']*100:.0f}%",
            "VALORE TARGET (€)": f"{val_target:,.0f} €",
            "QUOTE TOTALI": round(val_target / prezzi[t], 2)
        })
    st.table(pd.DataFrame(ordini_df))

    # 6. GRAFICO ALLOCAZIONE (Donut Chart Neon)
    st.markdown("<div class='neon-hr'></div>", unsafe_allow_html=True)
    fig = go.Figure(data=[go.Pie(
        labels=[f"{t} ({info['tipo']})" for t, info in assets.items()],
        values=[info['peso'] for info in assets.values()],
        hole=.7,
        marker=dict(colors=[info['color'] for info in assets.values()], line=dict(color='#000', width=2))
    )])
    fig.update_layout(
        showlegend=True,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color="white"),
        margin=dict(t=0, b=0, l=0, r=0)
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("<p style='text-align: center; color: #444;'>2026 ELITE STRATEGY - NO PENSION - NO REAL ESTATE</p>", unsafe_allow_html=True)
else:
    st.error("DATA LINK FAILED")
