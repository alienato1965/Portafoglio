import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import numpy as np

# 1. CONFIGURAZIONE PAGINA ED ESTETICA AVANZATA
st.set_page_config(page_title="Wealth Terminal Elite", layout="wide")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    
    /* SFONDO GENERALE */
    .stApp {
        background-color: #1e242b !important;
        font-family: 'Inter', sans-serif !important;
    }
    
    /* SIDEBAR STRETTA E SCURA */
    [data-testid="stSidebar"] {
        background-color: #161b22 !important;
        min-width: 200px !important;
        max-width: 250px !important;
        border-right: 1px solid #2d333b;
    }

    /* TITOLI E TESTI */
    h1, h2, h3 { 
        color: #ffffff !important; 
        font-weight: 700 !important; 
        letter-spacing: -0.5px;
    }
    
    /* CARD STILE "PREMIUM SLATE" */
    .pro-card {
        background: linear-gradient(145deg, #262c36, #1e242b);
        border: 1px solid #3d444d;
        border-radius: 12px;
        padding: 25px;
        text-align: center;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        margin-bottom: 20px;
    }
    
    .label-card { color: #8b949e; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 8px; }
    .value-card { color: #50fa7b; font-size: 2.2rem; font-weight: 700; }
    .sub-value { color: #50fa7b; font-size: 0.9rem; opacity: 0.8; }

    /* BOTTONE CALCOLA (VERDE SMERALDO) */
    .stButton>button {
        width: 100%;
        background-color: #38d39f !important;
        color: #161b22 !important;
        font-weight: 700 !important;
        border-radius: 8px !important;
        border: none !important;
        height: 3.5em !important;
        text-transform: uppercase;
        transition: 0.3s ease;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(56, 211, 159, 0.4);
    }

    /* TABELLE PULITE */
    .stTable {
        background-color: #21262d !important;
        border-radius: 10px !important;
        color: #ffffff !important;
    }
</style>
""", unsafe_allow_html=True)

# 2. SIDEBAR CON ICONE (Come nell'immagine)
with st.sidebar:
    st.markdown("<h1 style='font-size: 2rem;'>💎</h1>", unsafe_allow_html=True)
    st.markdown("### ASSET")
    
    st.markdown("⚙️ **IMPOSTAZIONI**", unsafe_allow_html=True)
    cap = st.number_input("Capitale Iniziale (€)", value=10000, label_visibility="collapsed")
    pac = st.number_input("Versamento PAC (€)", value=500, label_visibility="collapsed")
    
    st.markdown("---")
    st.markdown("🌐 **Core Mondo (VWCE)**")
    p1 = st.slider("% VWCE", 0, 100, 45, label_visibility="collapsed")
    
    st.markdown("💡 **Core Tech (QDVE)**")
    p2 = st.slider("% QDVE", 0, 100, 25, label_visibility="collapsed")
    
    st.markdown("💰 **Satellite Oro**")
    p3 = st.slider("% Oro", 0, 100, 20, label_visibility="collapsed")
    
    st.markdown("⚒️ **Satellite Miners**")
    p4 = st.slider("% GDXJ", 0, 100, 10, label_visibility="collapsed")
    
    cagr = st.slider("CAGR Atteso (%)", 1.0, 12.0, 7.5)
    
    st.markdown("---")
    attivato = st.button("CALCOLA ORA")

# 3. AREA PRINCIPALE (DASHBOARD)
st.markdown("<h1 style='color: #ffffff;'>ANALISI PATRIMONIALE</h1>", unsafe_allow_html=True)

if attivato:
    # Calcoli logici [cite: 2026-02-15]
    anni = 25
    mesi = anni * 12
    r_m = (1 + cagr/100)**(1/12) - 1
    
    # Risultato a 20 anni (Target Principale) [cite: 2026-02-15]
    m20 = 20 * 12
    lordo_20 = cap * (1 + r_m)**m20 + pac * (((1 + r_m)**m20 - 1) / r_m)
    versato_20 = cap + (pac * m20)
    tasse_20 = (lordo_20 - versato_20) * 0.26
    netto_20 = lordo_20 - tasse_20
    rendita_20 = (netto_20 * 0.04) / 12

    # --- ROW 1: LE TRE CARD (STILE IMMAGINE) ---
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f"""<div class='pro-card'><p class='label-card'>Patrimonio Netto (20Y)</p><p class='value-card'>{netto_20:,.0f} €</p><p class='sub-value'>Tasse: -26%</p></div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""<div class='pro-card'><p class='label-card'>Valore Mensile Netto</p><p class='value-card'>{rendita_20:,.0f} €</p><p class='sub-value'>Prelievo 4%</p></div>""", unsafe_allow_html=True)
    with c3:
        st.markdown(f"""<div class='pro-card'><p class='label-card'>Rendita Mensile Netta</p><p class='value-card' style='color:#38d39f;'>{rendita_20:,.0f} €</p><p class='sub-value'>Orizzonte: 20 Anni</p></div>""", unsafe_allow_html=True)

    # --- ROW 2: EVOLUZIONE DEL CAPITALE (GRAFICO IDENTICO) ---
    st.markdown("### 📈 Evoluzione del Capitale")
    timeline = np.arange(0, mesi + 1)
    y_lordo = [cap * (1+r_m)**m + pac * (((1+r_m)**m - 1)/r_m) for m in timeline]
    y_versato = [cap + (pac * m) for m in timeline]

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=timeline/12, y=y_lordo, name='Patrimonio Lordo', line=dict(color='#38d39f', width=4)))
    fig.add_trace(go.Scatter(x=timeline/12, y=y_versato, name='Capitale Versato', line=dict(color='#8b949e', width=2, dash='dash')))
    
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color="#8b949e"), height=400,
        xaxis=dict(showgrid=True, gridcolor='#2d333b'), yaxis=dict(showgrid=True, gridcolor='#2d333b'),
        margin=dict(t=20, b=20, l=20, r=20), hovermode="x unified"
    )
    st.plotly_chart(fig, use_container_width=True)

    # --- ROW 3: ROADMAP FINANZIARIA (TABELLA) ---
    st.markdown("### 📋 Roadmap Finanziaria")
    checkpoints = [5, 10, 15, 20, 25]
    roadmap_data = []
    for a in checkpoints:
        m = a * 12
        l = cap * (1 + r_m)**m + pac * (((1 + r_m)**m - 1) / r_m)
        v = cap + (pac * m)
        n = l - (l-v)*0.26
        roadmap_data.append({
            "ANNI": f"{a}y",
            "VERSATO": f"{v:,.0f} €",
            "LORDO": f"{l:,.0f} €",
            "NETTO (Post-Tax)": f"{n:,.0f} €",
            "RENDITA MENS.": f"{(n*0.04)/12:,.0f} €"
        })
    
    st.table(pd.DataFrame(roadmap_data))

else:
    st.info("Configura la tua strategia nella sidebar e clicca su 'CALCOLA ORA' per generare il report.")
