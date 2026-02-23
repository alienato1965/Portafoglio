import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np

# 1. SETUP ESTETICO - RISOLUZIONE VISIBILITÀ TESTI
st.set_page_config(page_title="Wealth Terminal Elite", layout="wide")

st.markdown("""
<style>
    /* Sfondo scuro professionale */
    .stApp { background-color: #1e242b !important; font-family: 'Inter', sans-serif !important; }
    [data-testid="stSidebar"] { background-color: #161b22 !important; border-right: 1px solid #2d333b; }
    
    /* FORZA TESTO BIANCO PER ETICHETTE E INPUT */
    label, p, span, .stMarkdown { color: #ffffff !important; font-size: 0.95rem !important; font-weight: 600 !important; }
    
    /* Migliora visibilità dei numeri inseriti */
    input { color: #50fa7b !important; font-weight: bold !important; }

    /* Card Design Slate */
    .pro-card {
        background: linear-gradient(145deg, #262c36, #1e242b);
        border: 1px solid #3d444d;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        margin-bottom: 15px;
    }
    .label-card { color: #8b949e !important; font-size: 0.8rem !important; text-transform: uppercase; }
    .value-card { color: #50fa7b !important; font-size: 2rem !important; font-weight: 700 !important; }
    
    /* Tabelle High Contrast */
    [data-testid="stTable"] td, [data-testid="stTable"] th { color: white !important; background-color: #21262d !important; }
</style>
""", unsafe_allow_html=True)

# 2. SIDEBAR - POSSIBILITÀ DI INSERIRE ALTRE CIFRE
with st.sidebar:
    st.markdown("<h2 style='color: #38d39f;'>⚙️ DATI INPUT</h2>", unsafe_allow_html=True)
    
    # Campi liberi per inserire qualsiasi cifra
    capitale_user = st.number_input("Capitale Attuale (€)", value=10000, step=1000, help="Cancella e inserisci la tua cifra")
    pac_user = st.number_input("PAC Mensile (€)", value=500, step=50, help="Importo che risparmi ogni mese")
    
    st.markdown("---")
    st.markdown("### 📊 ALLOCAZIONE STRATEGICA")
    p_core = st.slider("% Portafoglio CORE", 0, 100, 70)
    p_sat = st.slider("% Portafoglio SATELLITE", 0, 100, 30)
    
    st.markdown("### 📈 RENDIMENTI ATTESI")
    c_core = st.number_input("Stima CAGR Core %", value=9.0, step=0.1)
    c_sat = st.number_input("Stima CAGR Satellite %", value=4.5, step=0.1)

# 3. CALCOLI FINANZIARI (Dinamici in base agli input sopra)
# Strategia definita: 70% Core, 30% Satellite
cagr_pesato = ((p_core/100) * c_core) + ((p_sat/100) * c_sat)
r_mensile = (1 + cagr_pesato/100)**(1/12) - 1
anni_orizzonte = 20
mesi_totali = anni_orizzonte * 12

# Formula Interesse Composto con PAC
val_finale_lordo = capitale_user * (1 + r_mensile)**mesi_totali + pac_user * (((1 + r_mensile)**mesi_totali - 1) / r_mensile)
tot_investito = capitale_user + (pac_user * mesi_totali)
tasse_capital_gain = (val_finale_lordo - tot_investito) * 0.26
netto_finale = val_finale_lordo - tasse_capital_gain
rendita_stimata = (netto_finale * 0.04) / 12  # SWR 4%

# 4. DASHBOARD PRINCIPALE
st.markdown("<h1 style='color: white;'>ANALISI PATRIMONIALE DINAMICA</h1>", unsafe_allow_html=True)

# Card dei Risultati
c1, c2, c3 = st.columns(3)
with c1:
    st.markdown(f"<div class='pro-card'><p class='label-card'>Capitale Netto (20Y)</p><p class='value-card'>{netto_finale:,.0f} €</p></div>", unsafe_allow_html=True)
with c2:
    st.markdown(f"<div class='pro-card'><p class='label-card'>Rendita Mensile Netta</p><p class='value-card' style='color:#8be9fd;'>{rendita_stimata:,.0f} €</p></div>", unsafe_allow_html=True)
with c3:
    st.markdown(f"<div class='pro-card'><p class='label-card'>CAGR Strategia</p><p class='value-card' style='color:#ffffff;'>{cagr_pesato:.2f}%</p></div>", unsafe_allow_html=True)

# Tabella Riassuntiva
st.markdown("### 📋 Dettaglio Piano Investimento")
dati_piano = {
    "Descrizione": ["Capitale Iniziale", "Versamento Mensile (PAC)", "Totale Versato in 20 anni", "Rendimento Medio Annuo"],
    "Valore": [f"{capitale_user:,.0f} €", f"{pac_user:,.0f} €", f"{tot_investito:,.0f} €", f"{cagr_pesato:.2f}%"]
}
st.table(pd.DataFrame(dati_piano))

# Grafico della Crescita
st.markdown("### 📈 Proiezione Esponenziale")
time_axis = np.arange(0, mesi_totali + 1)
growth_curve = [capitale_user * (1+r_mensile)**m + pac_user * (((1+r_mensile)**m - 1)/r_mensile) for m in time_axis]

fig = go.Figure(go.Scatter(x=time_axis/12, y=growth_curve, fill='tozeroy', name='Crescita Lorda', line=dict(color='#38d39f', width=3)))
fig.update_layout(
    paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
    font=dict(color="white"), height=350, margin=dict(t=10, b=10, l=10, r=10),
    xaxis=dict(title="Anni", showgrid=True, gridcolor='#2d333b'),
    yaxis=dict(title="Valore Portafoglio (€)", showgrid=True, gridcolor='#2d333b')
)
st.plotly_chart(fig, use_container_width=True)
