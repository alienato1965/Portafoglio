import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import numpy as np

# 1. SETUP ESTETICO "SLATE & EMERALD" (MODERNO E DARK)
st.set_page_config(page_title="Portfolio Terminal 70/30", layout="wide")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&family=JetBrains+Mono&display=swap');
    
    /* Sfondo Grigio Scuro Antracite */
    .stApp {
        background-color: #1e2127 !important;
        font-family: 'Inter', sans-serif !important;
    }
    
    /* Sidebar Nero Dark Assoluto */
    [data-testid="stSidebar"] {
        background-color: #000000 !important;
        border-right: 1px solid #3e4451;
    }

    /* Container Card Moderne */
    .stMetric, .stTable, div[data-testid="stBlock"] {
        background-color: #262a33 !important;
        border: 1px solid #3e4451 !important;
        border-radius: 12px !important;
        padding: 15px !important;
    }

    /* Testo e Titoli */
    h1, h2, h3, p, label { color: #ffffff !important; }
    
    /* Dettagli Verde Smeraldo */
    [data-testid="stMetricValue"] {
        color: #50fa7b !important;
        font-family: 'JetBrains Mono', monospace !important;
    }
    
    /* Bottone Moderno Verde */
    .stButton>button {
        width: 100%;
        background-color: #50fa7b !important;
        color: #1e2127 !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        height: 3.5em !important;
        box-shadow: 0 4px 15px rgba(80, 250, 123, 0.2);
    }
</style>
""", unsafe_allow_html=True)

# 2. SIDEBAR: PANNELLO DI CONTROLLO NERO
with st.sidebar:
    st.markdown("<h2 style='color: #50fa7b;'>🕹️ COMMANDS</h2>", unsafe_allow_html=True)
    
    st.subheader("🏦 CORE ALLOCATION")
    s1 = st.text_input("TICKER 1", value="VWCE.DE")
    p1 = st.slider("% Slot 1", 0, 100, 45)
    
    s2 = st.text_input("TICKER 2", value="QDVE.DE")
    p2 = st.slider("% Slot 2", 0, 100, 25)
    
    st.markdown("---")
    st.subheader("🛰️ SATELLITE")
    s3 = st.text_input("TICKER 3", value="SGLN.L")
    p3 = st.slider("% Slot 3", 0, 100, 20)
    
    s4 = st.text_input("TICKER 4", value="GDXJ")
    p4 = st.slider("% Slot 4", 0, 100, 10)
    
    s5 = st.text_input("TICKER 5 (CASH/EXTRA)", value="")
    p5 = st.slider("% Slot 5", 0, 100, 0)
    
    tot_pesi = p1 + p2 + p3 + p4 + p5
    
    st.markdown("---")
    cap = st.number_input("CAPITALE ATTUALE (€)", value=10000, step=1000)
    pac = st.number_input("PAC MENSILE (€)", value=500, step=50)
    
    st.markdown(f"**ALLOCAZIONE TOTALE: {tot_pesi}%**")
    
    # Pulsante di attivazione
    attivato = st.button("AGGIORNA TERMINALE")

# 3. LOGICA PRINCIPALE
if attivato:
    if tot_pesi != 100:
        st.error(f"ATTENZIONE: Il totale delle percentuali è {tot_pesi}%. Deve essere 100% per funzionare.")
    else:
        st.markdown("<h1 style='text-align: center;'>✅ PORTFOLIO OVERVIEW</h1>", unsafe_allow_html=True)
        
        config = {t: p for t, p in zip([s1, s2, s3, s4, s5], [p1, p2, p3, p4, p5]) if t}
        
        try:
            # Download dati in tempo reale
            with st.spinner('Sincronizzazione mercati...'):
                data = yf.download(list(config.keys()), period="1d")["Close"]
                prezzi = data.iloc[-1] if len(config) > 1 else data

            # --- SEZIONE 1: METRICHE PREZZI ---
            cols = st.columns(len(config))
            for i, (t, p) in enumerate(config.items()):
                pr_att = prezzi[t] if len(config) > 1 else prezzi
                cols[i].metric(label=t, value=f"{pr_att:.2f} €", delta=f"{p}%")

            # --- SEZIONE 2: PROIEZIONI 5-20 ANNI (CAGR) ---
            st.markdown("### 📈 PROIEZIONE DI CRESCITA & CAGR")
            
            # Stima CAGR basata sulla tua strategia [cite: 2026-02-15]
            # Assumiamo rendimenti medi: Core 8.5%, Satellite 4.5%
            cagr_stimato = ((p1+p2)/100 * 0.085) + ((p3+p4+p5)/100 * 0.045)
            
            c1, c2 = st.columns([1, 2])
            
            with c1:
                st.metric("CAGR STIMATO", f"{cagr_stimato*100:.2f}%")
                st.write("Basato su pesi Core/Satellite attuali.")
            
            with c2:
                periodi = [5, 10, 15, 20]
                proiezioni = []
                r_mensile = (1 + cagr_stimato)**(1/12) - 1
                
                for anno in periodi:
                    mesi = anno * 12
                    val_futuro = cap * (1 + r_mensile)**mesi + pac * (((1 + r_mensile)**mesi - 1) / r_mensile)
                    investito = cap + (pac * mesi)
                    proiezioni.append({
                        "Orizzonte": f"{anno} Anni",
                        "Capitale Finale (€)": f"{val_futuro:,.0f}",
                        "Interessi Generati (€)": f"{(val_futuro - investito):,.0f}"
                    })
                st.table(pd.DataFrame(proiezioni))

            # --- SEZIONE 3: PIANO ORDINI ---
            st.markdown("### ⚖️ REBALANCING ORDERS")
            tot_investito = cap + pac
            ordini_data = []
            
            for t, p in config.items():
                pr_att = prezzi[t] if len(config) > 1 else prezzi
                val_target = tot_investito * (p / 100)
                ordini_data.append({
                    "ASSET": t,
                    "PESO": f"{p}%",
                    "VALORE TARGET (€)": f"{val_target:,.2f}",
                    "QUOTE TOTALI": round(val_target / pr_att, 2)
                })
            
            st.table(pd.DataFrame(ordini_data))

            # --- SEZIONE 4: GRAFICO ALLOCAZIONE ---
            fig = go.Figure(data=[go.Pie(
                labels=list(config.keys()),
                values=list(config.values()),
                hole=.6,
                marker=dict(colors=['#50fa7b', '#40c963', '#28a745', '#1e7e34', '#145223'])
            )])
            fig.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color="white"),
                margin=dict(t=30, b=30, l=30, r=30)
            )
            st.plotly_chart(fig, use_container_width=True)

        except Exception as e:
            st.error(f"Errore tecnico: Verificare che i Ticker siano corretti (es. VWCE.DE).")
else:
    st.markdown("""
        <div style='text-align: center; margin-top: 100px;'>
            <h2 style='color: #3e4451;'>TERMINALE IN STANDBY</h2>
            <p style='color: #3e4451;'>Regola i parametri e premi il pulsante <b>AGGIORNA TERMINALE</b></p>
        </div>
    """, unsafe_allow_html=True)
