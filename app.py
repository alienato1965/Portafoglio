import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import numpy as np

# 1. SETUP ESTETICO UNIFORMATO
st.set_page_config(page_title="Wealth Terminal", layout="wide")

st.markdown("""
<style>
    .stApp { background-color: #1e2127 !important; font-family: 'Inter', sans-serif !important; }
    [data-testid="stSidebar"] { background-color: #1a1d23 !important; border-right: 1px solid #3e4451; }
    .pro-card {
        background-color: #262a33; border: 1px solid #3e4451; border-radius: 15px;
        padding: 20px; margin-bottom: 15px; text-align: center;
    }
    .label-card { color: #8be9fd; font-size: 0.9rem; text-transform: uppercase; }
    .value-card { color: #50fa7b; font-size: 2rem; font-weight: bold; }
    .growth-value { color: #50fa7b; font-size: 1.5rem; font-weight: bold; }
    h1, h2, h3 { color: #ffffff !important; }
</style>
""", unsafe_allow_html=True)

# 2. SIDEBAR
with st.sidebar:
    st.markdown("<h2 style='color: #50fa7b;'>🕹️ SETTINGS</h2>", unsafe_allow_html=True)
    cap = st.number_input("CAPITALE INIZIALE (€)", value=10000)
    pac = st.number_input("PAC MENSILE (€)", value=500)
    cagr = st.slider("CAGR ATTESO (%)", 1.0, 15.0, 7.5)
    st.markdown("---")
    attivato = st.button("VISUALIZZA CRESCITA")

# 3. LOGICA DI CALCOLO
if attivato:
    st.markdown("<h1 style='text-align: center;'>📈 RENDIMENTO DELLA CRESCITA</h1>", unsafe_allow_html=True)
    
    anni_target = 20
    r_m = (1 + cagr/100)**(1/12) - 1
    m_target = anni_target * 12
    
    # Calcolo Valori Finali
    lordo = cap * (1 + r_m)**m_target + pac * (((1 + r_m)**m_target - 1) / r_m)
    versato = cap + (pac * m_target)
    rendimento_puro = lordo - versato # LA CRESCITA CHE NON SI VEDEVA
    percentuale_crescita = (rendimento_puro / versato) * 100

    # BOX RENDIMENTO CHIARO
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f"<div class='pro-card'><p class='label-card'>Totale Versato</p><p class='value-card' style='color:white;'>{versato:,.0f} €</p></div>", unsafe_allow_html=True)
    with c2:
        st.markdown(f"<div class='pro-card'><p class='label-card'>Rendimento Generato</p><p class='value-card'>{rendimento_puro:,.0f} €</p></div>", unsafe_allow_html=True)
    with c3:
        st.markdown(f"<div class='pro-card'><p class='label-card'>Moltiplicatore</p><p class='value-card' style='color:#8be9fd;'>+{percentuale_crescita:.0f}%</p></div>", unsafe_allow_html=True)

    # GRAFICO DI CRESCITA (DISTINZIONE NETTA)
    st.markdown("### 📊 PROGRESSIONE NEL TEMPO")
    timeline = np.arange(0, m_target + 1)
    valori_lordi = [cap * (1 + r_m)**m + pac * (((1 + r_m)**m - 1) / r_m) for m in timeline]
    valori_versati = [cap + (pac * m) for m in timeline]
    valori_rendimento = [l - v for l, v in zip(valori_lordi, valori_versati)]

    fig = go.Figure()
    # Parte Versata (Base)
    fig.add_trace(go.Scatter(x=timeline/12, y=valori_versati, fill='tozeroy', name='Capitale Versato', line=dict(color='white')))
    # Parte Rendimento (Sopra)
    fig.add_trace(go.Scatter(x=timeline/12, y=valori_lordi, fill='tonexty', name='Rendimento Mercato (Crescita)', line=dict(color='#50fa7b')))

    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color="white"), xaxis_title="Anni", yaxis_title="Valore (€)",
        hovermode="x unified"
    )
    st.plotly_chart(fig, use_container_width=True)

    # TABELLA RENDIMENTO ANNUALE
    st.markdown("### 📅 RENDIMENTO PER TAPPE")
    tappe = [5, 10, 15, 20]
    df_tappe = []
    for a in tappe:
        m = a * 12
        l = cap * (1 + r_m)**m + pac * (((1 + r_m)**m - 1) / r_m)
        v = cap + (pac * m)
        df_tappe.append({
            "ANNI": f"{a}y",
            "CAPITALE VERSATO (€)": f"{v:,.0f}",
            "RENDIMENTO ACCUMULATO (€)": f"{(l-v):,.0f}",
            "TOTALE LORDO (€)": f"{l:,.0f}"
        })
    st.table(pd.DataFrame(df_tappe))

else:
    st.info("Clicca 'VISUALIZZA CRESCITA' per generare i grafici di rendimento.")
