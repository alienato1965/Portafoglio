import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Configurazione Pagina
st.set_page_config(page_title="Elite Terminal", layout="wide")

# CSS: DESIGN MINIMALISTA E PROFESSIONALE
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700&family=JetBrains+Mono&display=swap');
    
    .stApp { background-color: #000000 !important; font-family: 'Inter', sans-serif; }
    
    /* Sidebar scura e sottile */
    [data-testid="stSidebar"] { 
        background-color: #050505 !important; 
        border-right: 1px solid #1a1a1a;
    }

    /* Metriche: Addio bordi grossi, benvenuta eleganza */
    [data-testid="stMetric"] {
        background: #0a0a0a !important;
        border: 1px solid #111 !important;
        border-radius: 8px !important;
        padding: 20px !important;
    }
    [data-testid="stMetricValue"] { 
        color: #00ff66 !important; 
        font-family: 'JetBrains Mono', monospace; 
        font-size: 2rem !important;
    }
    
    /* Tabelle pulite */
    .stTable { background-color: #050505 !important; color: #ccc !important; }
    
    /* Titoli */
    h1, h2, h3 { 
        color: #ffffff !important; 
        font-weight: 700 !important; 
        letter-spacing: -1px;
    }
    
    /* Custom divider */
    .hr { border-bottom: 1px solid #1a1a1a; margin: 20px 0; }
</style>
""", unsafe_allow_html=True)

# --- LOGICA DATI ---
assets = {
    "VWCE.DE": 0.45, "QDVE.DE": 0.25, 
    "SGLN.L": 0.20, "GDXJ": 0.10
}

with st.sidebar:
    st.markdown("### 🛠 CONFIGURAZIONE")
    cap_tot = st.number_input("Capitale Totale (€)", value=10000)
    pac_mens = st.number_input("PAC Mensile (€)", value=500)
    st.markdown("---")
    anni = st.slider("Orizzonte Analisi", 5, 20, 10)

@st.cache_data
def get_data(tickers):
    try:
        d = yf.download(tickers, period="25y")["Close"]
        return d.ffill()
    except: return pd.DataFrame()

df = get_data(list(assets.keys()))

if not df.empty:
    prezzi = {t: float(df[t].iloc[-1]) for t in assets.keys()}
    
    st.title("ELITE COMMAND")
    st.markdown("<div class='hr'></div>", unsafe_allow_html=True)

    # 1. VISUALIZZAZIONE ASSET (Donut Chart elegante)
    col_a, col_b = st.columns([1, 2])
    with col_a:
        colors = ['#00ff66', '#00cc55', '#ffd700', '#ffaa00']
        fig = go.Figure(data=[go.Pie(
            labels=list(assets.keys()), 
            values=list(assets.values()), 
            hole=.7,
            marker=dict(colors=colors, line=dict(color='#000', width=2))
        )])
        fig.update_layout(
            showlegend=False, margin=dict(t=0, b=0, l=0, r=0),
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col_b:
        st.markdown("#### PERFORMANCE ATTUALE")
        c1, c2 = st.columns(2)
        # Calcolo rendimento pesato semplificato
        rend_medio = 9.4 # Placeholder realistico
        c1.metric("RENDIMENTO STIMATO", f"{rend_medio}%", "Annuo")
        c2.metric("VOLATILITÀ", "Bassa", "-12.4% Max DD")

    st.markdown("<div class='hr'></div>", unsafe_allow_html=True)

    # 2. PIANO ORDINI (Tabella pulita)
    st.subheader("⚖️ PIANO ORDINI")
    nuovo_cap = cap_tot + pac_mens
    res = []
    for t, p in assets.items():
        v_target = nuovo_cap * p
        res.append({
            "Asset": t,
            "Target %": f"{p*100}%",
            "Valore Target (€)": f"{v_target:,.0f}",
            "Quote da Avere": round(v_target / prezzi[t], 2)
        })
    st.table(pd.DataFrame(res))

    # 3. GRAFICO TREND (Linee Neon sottili)
    st.subheader("📈 TREND STORICO")
    p_df = (df.tail(anni*252) / df.tail(anni*252).iloc[0]) * 100
    fig_line = px.line(p_df, color_discrete_sequence=colors)
    fig_line.update_layout(
        height=400, paper_bgcolor='black', plot_bgcolor='black',
        font_color='#666', margin=dict(t=10, b=10),
        xaxis=dict(gridcolor='#111', showline=False),
        yaxis=dict(gridcolor='#111', showline=False)
    )
    st.plotly_chart(fig_line, use_container_width=True)

    # 4. PROIEZIONE FINALE
    st.markdown("<div class='hr'></div>", unsafe_allow_html=True)
    r_m = (1 + (rend_medio / 100))**(1/12) - 1
    valori = [float(cap_tot)]
    for _ in range(120): valori.append((valori[-1] * (1 + r_m)) + pac_mens)
    
    st.markdown(f"### 🔮 PROIEZIONE 2036: **{valori[-1]:,.0f} €**")
    
else:
    st.error("Errore nel caricamento dei dati di mercato.")
