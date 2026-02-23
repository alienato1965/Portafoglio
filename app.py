import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import numpy as np

# 1. STYLE SLATE & EMERALD (UNIFORMATO)
st.set_page_config(page_title="Wealth Terminal", layout="wide")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700&family=JetBrains+Mono&display=swap');
    .stApp { background-color: #1e2127 !important; font-family: 'Inter', sans-serif !important; }
    [data-testid="stSidebar"] { background-color: #1a1d23 !important; border-right: 1px solid #3e4451; }
    
    /* Card Speciali */
    .pro-card {
        background-color: #262a33;
        border: 1px solid #3e4451;
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 20px;
    }
    
    .net-value { color: #50fa7b; font-size: 2.2rem; font-weight: bold; font-family: 'JetBrains Mono'; }
    .tax-value { color: #ff5555; font-size: 1.2rem; }
    
    h1, h2, h3 { color: #ffffff !important; letter-spacing: -1px; }
    .stButton>button {
        width: 100%; background-color: #50fa7b !important; color: #1e2127 !important;
        font-weight: bold; border-radius: 10px; height: 3.5em;
    }
</style>
""", unsafe_allow_html=True)

# 2. SIDEBAR CONFIG
with st.sidebar:
    st.markdown("<h2 style='color: #50fa7b;'>🕹️ CONTROLLO</h2>", unsafe_allow_html=True)
    cap = st.number_input("CAPITALE INIZIALE (€)", value=10000, step=1000)
    pac = st.number_input("PAC MENSILE (€)", value=500, step=50)
    cagr = st.slider("CAGR ATTESO (%)", 1.0, 12.0, 7.5)
    swr = st.slider("TASSO PRELIEVO RENDITA (%)", 2.0, 5.0, 4.0) # Safe Withdrawal Rate
    st.markdown("---")
    attivato = st.button("CALCOLA DESTINO FINANZIARIO")

# 3. LOGICA E GRAFICA MIGLIORATA
if attivato:
    st.markdown("<h1 style='text-align: center;'>📉 ANALISI CRESCITA NETTA E RENDITA</h1>", unsafe_allow_html=True)
    
    anni_range = [5, 10, 15, 20, 25]
    r_m = (1 + cagr/100)**(1/12) - 1
    
    # Creazione Dashboard a colonne per i risultati finali (Target 20 anni)
    target_anni = 20
    m_target = target_anni * 12
    lordo_f = cap * (1 + r_m)**m_target + pac * (((1 + r_m)**m_target - 1) / r_m)
    versato_f = cap + (pac * m_target)
    tasse_f = (lordo_f - versato_f) * 0.26
    netto_f = lordo_f - tasse_f
    rendita_mensile = (netto_f * (swr/100)) / 12

    # BOX RIASSUNTIVI (STILE MODERN DASHBOARD)
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f"<div class='pro-card'><h3>PATRIMONIO NETTO (20Y)</h3><p class='net-value'>{netto_f:,.0f} €</p><p>Dopo tasse 26%</p></div>", unsafe_allow_html=True)
    with c2:
        st.markdown(f darkness='pro-card'><h3>RENDITA MENSILE NETTA</h3><p class='net-value' style='color:#8be9fd;'>{rendita_mensile:,.0f} €</p><p>Sostenibile al {swr}%</p></div>", unsafe_allow_html=True)
    with c3:
        st.markdown(f darkness='pro-card'><h3>TASSE TOTALI</h3><p class='tax-value'>{tasse_f:,.0f} €</p><p>Prelievo Capital Gain</p></div>", unsafe_allow_html=True)

    # TABELLA EVOLUTIVA DETTAGLIATA
    st.markdown("### 📋 TABELLA DI MARCIA (ROADMAP)")
    
    rows = []
    for a in anni_range:
        m = a * 12
        l = cap * (1 + r_m)**m + pac * (((1 + r_m)**m - 1) / r_m)
        v = cap + (pac * m)
        gain = l - v
        t = gain * 0.26
        n = l - t
        r_m_netta = (n * (swr/100)) / 12
        
        rows.append({
            "ANNI": f"{a} ANNI",
            "LORDO PROIETTATO": f"{l:,.0f} €",
            "CAPITALE VERSATO": f"{v:,.0f} €",
            "TASSE (26%)": f"{t:,.0f} €",
            "NETTO DISPONIBILE": f"{n:,.0f} €",
            "RENDITA MENS. NETTA": f"{r_m_netta:,.0f} €"
        })
    
    df = pd.DataFrame(rows)
    st.table(df)

    # GRAFICO A BARRE STACKED: CHI SI MANGIA I SOLDI?
    st.markdown("### 📊 COMPOSIZIONE DEL PATRIMONIO")
    
    # Dati per il grafico
    labels = [f"{a}y" for a in anni_range]
    versati = [cap + (pac * a * 12) for a in anni_range]
    interessi_netti = [( (cap * (1+r_m)**(a*12) + pac * (((1+r_m)**(a*12) - 1)/r_m)) - (cap + pac*a*12) ) * 0.74 for a in anni_range]
    tasse = [( (cap * (1+r_m)**(a*12) + pac * (((1+r_m)**(a*12) - 1)/r_m)) - (cap + pac*a*12) ) * 0.26 for a in anni_range]

    fig = go.Figure(data=[
        go.Bar(name='Capitale Versato', x=labels, y=versati, marker_color='#ffffff'),
        go.Bar(name='Interesse Netto', x=labels, y=interessi_netti, marker_color='#50fa7b'),
        go.Bar(name='Tasse (Stato)', x=labels, y=tasse, marker_color='#ff5555')
    ])
    fig.update_layout(
        barmode='stack', paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color="white"), height=400, margin=dict(t=20, b=20)
    )
    st.plotly_chart(fig, use_container_width=True)

    st.warning("⚠️ Nota: Senza pensione e immobili, il tuo obiettivo è la colonna 'RENDITA MENS. NETTA'. Assicurati che quel valore sia superiore alle tue spese future previste.")

else:
    st.info("Configura il tuo piano e premi il pulsante verde per visualizzare il dettaglio netto.")
