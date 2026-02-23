import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

# 1. SETUP ESTETICO "SLATE & EMERALD"
st.set_page_config(page_title="Portfolio Overview", layout="wide")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap');
    
    /* Sfondo Grigio Scuro Antracite */
    .stApp {
        background-color: #1e2127 !important;
        font-family: 'Inter', sans-serif !important;
    }
    
    /* Sidebar Grigio Piombo */
    [data-testid="stSidebar"] {
        background-color: #262a33 !important;
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
        font-size: 1.8rem !important;
    }
    
    /* Bottone Moderno Verde */
    .stButton>button {
        width: 100%;
        background-color: #50fa7b !important;
        color: #1e2127 !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        height: 3em !important;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #40c963 !important;
        box-shadow: 0 4px 15px rgba(80, 250, 123, 0.3);
    }

    /* Tabelle Pulite */
    thead tr th {
        background-color: #2d323c !important;
        color: #50fa7b !important;
        border-radius: 5px;
    }
</style>
""", unsafe_allow_html=True)

# 2. SIDEBAR DINAMICA (GRIGIO SCURO)
with st.sidebar:
    st.markdown("### ⚙️ ASSET ALLOCATION")
    
    # Slot e Slider con i tuoi pesi definitivi [cite: 2026-02-15]
    s1 = st.text_input("TICKER 1", value="VWCE.DE")
    p1 = st.slider("% Slot 1", 0, 100, 45)
    
    s2 = st.text_input("TICKER 2", value="QDVE.DE")
    p2 = st.slider("% Slot 2", 0, 100, 25)
    
    s3 = st.text_input("TICKER 3", value="SGLN.L")
    p3 = st.slider("% Slot 3", 0, 100, 20)
    
    s4 = st.text_input("TICKER 4", value="GDXJ")
    p4 = st.slider("% Slot 4", 0, 100, 10)
    
    s5 = st.text_input("TICKER 5", value="")
    p5 = st.slider("% Slot 5", 0, 100, 0)
    
    st.markdown("---")
    cap = st.number_input("CAPITALE TOTALE (€)", value=10000)
    pac = st.number_input("VERSAMENTO PAC (€)", value=500)
    
    attivato = st.button("AGGIORNA TERMINALE")

# 3. DASHBOARD CENTRALE
st.markdown("<h2 style='text-align: center;'>✅ PORTFOLIO OVERVIEW</h2>", unsafe_allow_html=True)

if attivato:
    config = {t: p for t, p in zip([s1, s2, s3, s4, s5], [p1, p2, p3, p4, p5]) if t}
    tot_pesi = sum(config.values())

    if tot_pesi != 100:
        st.error(f"Errore: Il totale è {tot_pesi}%. Deve essere 100%.")
    else:
        try:
            # Download Dati
            prezzi = yf.download(list(config.keys()), period="1d")["Close"].iloc[-1]
            
            # Griglia Prezzi (Metriche con bordo verde)
            cols = st.columns(len(config))
            for i, (t, p) in enumerate(config.items()):
                prezzo_attuale = prezzi[t] if len(config) > 1 else prezzi
                cols[i].metric(label=t, value=f"{prezzo_attuale:.2f} €")

            # Tabella Ordini Professionale
            st.markdown("### ⚖️ ORDINIS DI ACQUISTO/VENDITA")
            tot_inv = cap + pac
            data_tab = []
            for t, p in config.items():
                prezzo_attuale = prezzi[t] if len(config) > 1 else prezzi
                val_target = tot_inv * (p / 100)
                data_tab.append({
                    "ASSET": t,
                    "TARGET %": f"{p}%",
                    "VALORE TARGET (€)": f"{val_target:,.2f}",
                    "QUOTE TOTALI": round(val_target / prezzo_attuale, 2)
                })
            st.table(pd.DataFrame(data_tab))

            # Grafico a ciambella moderno
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
                margin=dict(t=20, b=20, l=20, r=20)
            )
            st.plotly_chart(fig, use_container_width=True)

        except Exception as e:
            st.warning("Inserisci ticker validi e premi il tasto AGGIORNA.")
else:
    st.info("Configura gli asset nella colonna di sinistra e premi il tasto verde per generare la dashboard.")
