import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import numpy as np

# 1. SETUP ESTETICO UNIFORMATO (SLATE & EMERALD)
st.set_page_config(page_title="Wealth Terminal", layout="wide")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700&family=JetBrains+Mono&display=swap');
    
    .stApp { background-color: #1e2127 !important; font-family: 'Inter', sans-serif !important; }
    [data-testid="stSidebar"] { background-color: #1a1d23 !important; border-right: 1px solid #3e4451; }
    
    /* Card Stile Slate */
    .pro-card {
        background-color: #262a33;
        border: 1px solid #3e4451;
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 15px;
        text-align: center;
    }
    
    .label-card { color: #8be9fd; font-size: 0.9rem; text-transform: uppercase; margin-bottom: 5px; }
    .value-card { color: #50fa7b; font-size: 2rem; font-weight: bold; font-family: 'JetBrains Mono'; }
    
    h1, h2, h3 { color: #ffffff !important; }
    .stButton>button {
        width: 100%; background-color: #50fa7b !important; color: #1e2127 !important;
        font-weight: bold; border-radius: 10px; height: 3.5em; border: none;
    }
</style>
""", unsafe_allow_html=True)

# 2. PANNELLO DI CONTROLLO (SIDEBAR)
with st.sidebar:
    st.markdown("<h2 style='color: #50fa7b;'>🕹️ SETTINGS</h2>", unsafe_allow_html=True)
    cap = st.number_input("CAPITALE INIZIALE (€)", value=10000, step=1000)
    pac = st.number_input("PAC MENSILE (€)", value=500, step=50)
    cagr = st.slider("CAGR ATTESO (%)", 1.0, 12.0, 7.5)
    swr = st.slider("TASSO PRELIEVO RENDITA (%)", 2.0, 5.0, 4.0)
    st.markdown("---")
    st.subheader("ASSET TICKERS")
    t1 = st.text_input("Core 1", "VWCE.DE")
    t2 = st.text_input("Core 2", "QDVE.DE")
    t3 = st.text_input("Satellite 1", "SGLN.L")
    t4 = st.text_input("Satellite 2", "GDXJ")
    
    attivato = st.button("ESEGUI ANALISI")

# 3. LOGICA DI CALCOLO
if attivato:
    st.markdown("<h1 style='text-align: center;'>🔮 PROIEZIONE PATRIMONIALE NETTA</h1>", unsafe_allow_html=True)
    
    # Calcolo 20 anni (Target)
    anni_proiezione = 20
    r_m = (1 + cagr/100)**(1/12) - 1
    m_target = anni_proiezione * 12
    
    lordo = cap * (1 + r_m)**m_target + pac * (((1 + r_m)**m_target - 1) / r_m)
    versato = cap + (pac * m_target)
    plusvalenza = lordo - versato
    tasse = plusvalenza * 0.26
    netto = lordo - tasse
    rendita_netta = (netto * (swr/100)) / 12

    # BOX RIASSUNTIVI (Sostituiti i div problematici con colonne Streamlit native)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""<div class='pro-card'><p class='label-card'>Netto a 20 Anni</p><p class='value-card'>{netto:,.0f} €</p></div>""", unsafe_allow_html=True)
    with col2:
        st.markdown(f"""<div class='pro-card'><p class='label-card'>Rendita Mensile</p><p class='value-card' style='color:#8be9fd;'>{rendita_netta:,.0f} €</p></div>""", unsafe_allow_html=True)
    with col3:
        st.markdown(f"""<div class='pro-card'><p class='label-card'>Tasse Totali</p><p class='value-card' style='color:#ff5555;'>{tasse:,.0f} €</p></div>""", unsafe_allow_html=True)

    # DETTAGLIO CRESCITA NETTA (MIGLIORATO)
    st.markdown("### 📊 ROADMAP DELLA CRESCITA")
    
    checkpoints = [5, 10, 15, 20, 25]
    data_list = []
    
    for a in checkpoints:
        m = a * 12
        l_check = cap * (1 + r_m)**m + pac * (((1 + r_m)**m - 1) / r_m)
        v_check = cap + (pac * m)
        t_check = (l_check - v_check) * 0.26
        n_check = l_check - t_check
        rend_check = (n_check * (swr/100)) / 12
        
        data_list.append({
            "ANNI": f"{a}y",
            "LORDO (€)": f"{l_check:,.0f}",
            "VERSATO (€)": f"{v_check:,.0f}",
            "TASSE (€)": f"{t_check:,.0f}",
            "NETTO (€)": f"{n_check:,.0f}",
            "RENDITA NETTA/MESE": f"{rend_check:,.0f}"
        })
    
    st.table(pd.DataFrame(data_list))

    # GRAFICO VISIVO RENDITA vs VERSATO
    st.markdown("### 📈 EVOLUZIONE PATRIMONIO vs VERSAMENTO")
    timeline = np.arange(0, (25*12)+1)
    y_lordo = [cap * (1+r_m)**m + pac * (((1+r_m)**m - 1)/r_m) for m in timeline]
    y_versato = [cap + (pac * m) for m in timeline]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=timeline/12, y=y_lordo, fill='tozeroy', name='Valore Lordo', line=dict(color='#50fa7b')))
    fig.add_trace(go.Scatter(x=timeline/12, y=y_versato, name='Capitale Versato', line=dict(color='#ffffff', dash='dash')))
    
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color="white"), xaxis_title="Anni", yaxis_title="Euro (€)"
    )
    st.plotly_chart(fig, use_container_width=True)

else:
    st.info("Regola i parametri a sinistra e clicca 'ESEGUI ANALISI' per vedere il tuo futuro finanziario.")
