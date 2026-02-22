import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Elite Terminal v10", layout="wide")

# CSS: LOOK MINIMALISTA (NERO E GRIGIO ANTRACITE)
st.markdown("""
<style>
    .stApp { background-color: #000000 !important; font-family: monospace; }
    [data-testid="stSidebar"] { background-color: #050505 !important; border-right: 1px solid #1a1a1a; }
    [data-testid="stMetric"] {
        background: #0a0a0a !important; border: 1px solid #222 !important;
        border-radius: 4px; padding: 15px;
    }
    [data-testid="stMetricValue"] { color: #00ff66 !important; }
    h1, h2, h3 { color: #ffffff !important; font-weight: bold; }
    .stTable { background-color: #0d0d0d !important; border: 1px solid #1a1a1a !important; }
</style>
""", unsafe_allow_html=True)

# 1. PARAMETRI STRATEGIA DEFINITIVA
assets = {
    "VWCE.DE": 0.45, "QDVE.DE": 0.25, 
    "SGLN.L": 0.20, "GDXJ": 0.10
}

with st.sidebar:
    st.header("⚙️ CONFIGURAZIONE")
    capitale = st.number_input("CAPITALE ATTUALE (€)", value=10000)
    pac = st.number_input("PAC MENSILE (€)", value=500)
    st.markdown("---")
    anni_storia = st.slider("ANNI ANALISI", 5, 20, 10)

# 2. CARICAMENTO DATI (BLINDATO)
@st.cache_data
def get_clean_data(tickers):
    try:
        data = yf.download(tickers, period="25y")["Close"]
        return data.ffill()
    except Exception as e:
        st.error(f"Errore download: {e}")
        return pd.DataFrame()

df = get_clean_data(list(assets.keys()))

if not df.empty:
    prezzi_oggi = {t: float(df[t].iloc[-1]) for t in assets.keys()}
    
    st.title("ELITE PORTFOLIO COMMAND")
    
    # 3. COMPOSIZIONE E STATUS
    c1, c2 = st.columns([1, 2])
    
    with c1:
        # Donut Chart professionale
        fig_pie = go.Figure(data=[go.Pie(
            labels=list(assets.keys()), 
            values=list(assets.values()), 
            hole=.7,
            marker=dict(colors=['#00ff66', '#00cc55', '#ccaa00', '#886600'])
        )])
        fig_pie.update_layout(showlegend=False, margin=dict(t=0, b=0, l=0, r=0), paper_bgcolor='black')
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with c2:
        st.subheader("STATUS OPERATIVO")
        # Calcolo rendimento pesato reale degli ultimi X anni
        rend_tot = 0
        for t, p in assets.items():
            s = df[t].tail(anni_storia * 252)
            rend_tot += ((s.iloc[-1] / s.iloc[0])**(1/anni_storia)-1) * p
        
        m1, m2 = st.columns(2)
        m1.metric("RENDIMENTO STORICO", f"{rend_tot*100:.1f}%", "Annuo")
        m2.metric("OBIETTIVO FINALE", "2036")

    # 4. PIANO ORDINI (TABELLA OPERATIVA)
    st.markdown("---")
    st.subheader("⚖️ ORDINI DI RIBILANCIAMENTO")
    cap_investito = capitale + pac
    ordini_data = []
    for t, p in assets.items():
        v_target = cap_investito * p
        ordini_data.append({
            "ASSET": t,
            "TARGET %": f"{p*100}%",
            "VALORE TARGET (€)": f"{v_target:,.0f}",
            "QUOTE TOTALI": round(v_target / prezzi_oggi[t], 2)
        })
    st.table(pd.DataFrame(ordini_data))

    # 5. TREND STORICO
    st.subheader("📈 CONFRONTO PERFORMANCE")
    p_df = (df.tail(anni_storia*252) / df.tail(anni_storia*252).iloc[0]) * 100
    fig_line = px.line(p_df, color_discrete_sequence=['#00ff66', '#00cc55', '#ccaa00', '#886600'])
    fig_line.update_layout(height=400, paper_bgcolor='black', plot_bgcolor='black', font_color='#666')
    st.plotly_chart(fig_line, use_container_width=True)

    # 6. PROIEZIONE 2036 (LOGICA FISSA)
    st.markdown("---")
    r_m = (1 + rend_tot)**(1/12) - 1
    valori = [float(capitale)]
    for _ in range(120): # 10 anni (2026-2036)
        valori.append((valori[-1] * (1 + r_m)) + pac)
    
    cap_finale = valori[-1]
    netto_stimato = cap_finale - ((cap_finale - (capitale + pac*120)) * 0.26)
    
    st.success(f"🔮 CAPITALE NETTO STIMATO 2036: {netto_stimato:,.0f} € (LORDO: {cap_finale:,.0f} €)")

else:
    st.error("Sincronizzazione dati fallita. Ricarica la pagina.")
