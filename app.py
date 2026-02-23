import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

# 1. SETUP SPAZIALE
st.set_page_config(page_title="Space Command 70/30", layout="wide")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=JetBrains+Mono&display=swap');
    .stApp { background: #000000 !important; }
    .glass-card {
        background: rgba(20, 20, 20, 0.8);
        border: 1px solid #00ff66;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px;
    }
    h1, h2, h3 { font-family: 'Orbitron'; color: #00ff66 !important; }
    p, label, div, th, td { font-family: 'JetBrains Mono'; color: #ffffff !important; }
    /* Bottone Spaziale */
    .stButton>button {
        width: 100%;
        background-color: #00ff66 !important;
        color: black !important;
        font-weight: bold !important;
        border-radius: 5px !important;
        height: 3em !important;
        box-shadow: 0 0 15px rgba(0, 255, 102, 0.4);
    }
</style>
""", unsafe_allow_html=True)

# 2. SIDEBAR: I 5 SLOT + IL PULSANTE
with st.sidebar:
    st.markdown("### 🛠️ CONFIGURAZIONE SLOT")
    st.write("Inserisci Ticker o ISIN")
    s1 = st.text_input("SLOT 1 (45% CORE)", value="VWCE.DE")
    s2 = st.text_input("SLOT 2 (25% CORE)", value="QDVE.DE")
    s3 = st.text_input("SLOT 3 (20% GOLD)", value="SGLN.L")
    s4 = st.text_input("SLOT 4 (10% MINER)", value="GDXJ")
    s5 = st.text_input("SLOT 5 (CASH/EXTRA)", value="")
    
    st.markdown("---")
    cap = st.number_input("CAPITALE (€)", value=10000)
    pac = st.number_input("PAC (€)", value=500)
    
    st.markdown("---")
    # IL PULSANTE CHE MANCAVA
    attivato = st.button("🚀 ATTIVA / AGGIORNA TERMINALE")

# 3. LOGICA DI CALCOLO (Si attiva solo al click)
if attivato:
    tickers = [t.strip() for t in [s1, s2, s3, s4, s5] if t.strip()]
    # Riferimento strategia salvata [cite: 2026-02-15]
    pesi_dict = {s1: 0.45, s2: 0.25, s3: 0.20, s4: 0.10}
    if s5: pesi_dict[s5] = 0.0

    st.markdown("<h1>📡 SYSTEM STATUS: ONLINE</h1>", unsafe_allow_html=True)
    
    try:
        # Scarichiamo i dati
        with st.spinner('Aggancio segnale mercati...'):
            data = yf.download(tickers, period="1d", group_by='ticker')
        
        prezzi = {}
        for t in tickers:
            # Gestione caso ticker singolo o multiplo
            if len(tickers) == 1:
                prezzi[t] = data['Close'].iloc[-1]
            else:
                prezzi[t] = data[t]['Close'].iloc[-1]

        # Monitor Metriche
        cols = st.columns(len(tickers))
        for i, t in enumerate(tickers):
            cols[i].metric(t, f"{prezzi[t]:.2f}€")

        # Tabella Ordini
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("⚖️ MODULO DI ESECUZIONE")
        tot_val = cap + pac
        ordini = []
        for t, p in pesi_dict.items():
            if t in prezzi:
                val_target = tot_val * p
                ordini.append({
                    "STRUMENTO": t,
                    "PESO TARGET": f"{p*100:.0f}%",
                    "VALORE (€)": f"{val_target:,.2f}",
                    "QUOTE": round(val_target / prezzi[t], 3)
                })
        st.table(pd.DataFrame(ordini))
        st.markdown('</div>', unsafe_allow_html=True)

        # Grafico 70/30
        fig = go.Figure(data=[go.Pie(
            labels=list(pesi_dict.keys()),
            values=list(pesi_dict.values()),
            hole=.7,
            marker=dict(colors=['#00ff66', '#00cc55', '#ffd700', '#ffaa00'])
        )])
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', font=dict(color="white"))
        st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error(f"ERRORE: Uno degli ISIN/Ticker non è valido. Prova a usare i Ticker (es. 'VWCE.DE' invece dell'ISIN).")
else:
    st.markdown("<h2 style='text-align: center; margin-top: 100px;'>PREMI 'ATTIVA TERMINALE' NELLA SIDEBAR PER INIZIARE</h2>", unsafe_allow_html=True)
