import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

# Forza il tema scuro profondo e la leggibilità
st.set_page_config(page_title="Elite Terminal v12", layout="wide")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;700&display=swap');
    
    /* Sfondo nero assoluto */
    .stApp { background-color: #000000 !important; font-family: 'Fira Code', monospace !important; }
    
    /* Forza testo bianco brillante */
    p, span, label, th, td, div { color: #ffffff !important; }
    
    /* Sidebar scura con bordo neon sottile */
    [data-testid="stSidebar"] { 
        background-color: #050505 !important; 
        border-right: 1px solid #00ff66; 
    }

    /* Card prezzi con bagliore */
    [data-testid="stMetric"] {
        background: rgba(10, 10, 10, 0.9) !important;
        border: 1px solid #00ff66 !important;
        box-shadow: 0 0 10px rgba(0, 255, 102, 0.2);
        border-radius: 4px !important;
    }
    
    /* Tabelle: Addio nero su nero */
    .stTable { 
        background-color: #0a0a0a !important; 
        border: 1px solid #333 !important;
    }
    thead tr th { 
        background-color: #111 !important; 
        color: #00ff66 !important; 
        font-weight: bold !important;
    }
    
    /* Titoli */
    h1, h2, h3 { color: #00ff66 !important; text-shadow: 0 0 5px #00ff66; }
</style>
""", unsafe_allow_html=True)

# 1. PARAMETRI STRATEGIA 2026
assets = {
    "VWCE.DE": {"p": 0.45, "n": "Mondiale (Core)"},
    "QDVE.DE": {"p": 0.25, "n": "Tech S&P (Core)"},
    "SGLN.L": {"p": 0.20, "n": "Oro (Sat)"},
    "GDXJ": {"p": 0.10, "n": "Junior Miners (Sat)"}
}

with st.sidebar:
    st.title("🕹️ COMMAND")
    cap_attuale = st.number_input("CAPITALE TOTALE (€)", value=10000, step=1000)
    pac_oggi = st.number_input("PAC DA INVESTIRE (€)", value=500, step=100)
    st.markdown("---")
    st.write("🎯 **TARGET 70/30**")
    for t, v in assets.items():
        st.write(f"• {t}: {v['p']*100:.0f}%")

# 2. DOWNLOAD DATI MERCATO
@st.cache_data
def load_market():
    try:
        d = yf.download(list(assets.keys()), period="5d")["Close"]
        return d.ffill().iloc[-1]
    except: return None

prezzi = load_market()

st.title("ELITE STRATEGY COMMAND")

if prezzi is not None:
    # 3. MONITOR PREZZI (Grid)
    cols = st.columns(4)
    for i, (t, v) in enumerate(assets.items()):
        cols[i].metric(t, f"{prezzi[t]:.2f} €", f"{v['p']*100}% TGT")

    st.markdown("### ⚖️ PIANO ORDINI OPERATIVO")
    
    # 4. CALCOLO ORDINI (Senza bug di variabili)
    tot_investito = cap_attuale + pac_oggi
    data_tabella = []
    
    for t, v in assets.items():
        v_target = tot_investito * v['p']
        data_tabella.append({
            "TICKER": t,
            "NOME": v['n'],
            "TARGET (€)": f"{v_target:,.0f} €",
            "QUOTE TOTALI": round(v_target / prezzi[t], 2)
        })
    
    st.table(pd.DataFrame(data_tabella))

    # 5. GRAFICO ALLOCAZIONE (Visuale)
    fig = go.Figure(data=[go.Pie(
        labels=list(assets.keys()),
        values=[v['p'] for v in assets.values()],
        hole=.6,
        marker=dict(colors=['#00ff66', '#00cc55', '#ffd700', '#ffaa00'], line=dict(color='#000', width=2))
    )])
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', 
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color="white"),
        margin=dict(t=30, b=0, l=0, r=0)
    )
    st.plotly_chart(fig, use_container_width=True)

else:
    st.error("ERRORE DI CONNESSIONE - MERCATI CHIUSI O ASSENZA SEGNALE")
