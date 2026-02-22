import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px

# 1. CONFIGURAZIONE PAGINA E STILE "ALTA LEGGIBILITÀ"
st.set_page_config(page_title="Finanza Personale 70/30", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    
    /* Box delle metriche più grandi e spaziati */
    [data-testid="stMetric"] {
        background-color: #1e2130;
        padding: 20px !important;
        border-radius: 15px;
        border: 2px solid #3e4253;
        text-align: center;
    }
    
    /* Nomi ETF: Grandi e Bianchi */
    [data-testid="stMetricLabel"] {
        color: #FFFFFF !important;
        font-size: 20px !important;
        font-weight: bold !important;
    }
    
    /* Numeri Rendimento: VERDE ACCESO E GIGANTI */
    [data-testid="stMetricValue"] {
        color: #00FF00 !important;
        font-size: 35px !important;
        font-weight: 900 !important;
    }
    
    h1, h2, h3 { color: #00ffcc; font-family: 'Arial Black', sans-serif; }
    </style>
    """, unsafe_allow_html=True)

st.title("💎 La Mia Strategia 70/30")
st.write("Dati in tempo reale: 70% Core | 30% Satellite")

# 2. SELEZIONE DEI 6 ETF (Sidebar)
with st.sidebar:
    st.header("⚙️ Configura i 6 ETF")
    e1 = st.text_input("ETF 1 (Core 35%)", value="VWCE.DE")
    e2 = st.text_input("ETF 2 (Core 35%)", value="QDVE.DE")
    e3 = st.text_input("ETF 3 (Sat 10%)", value="SGLN.L")
    e4 = st.text_input("ETF 4 (Sat 10%)", value="GDXJ")
    e5 = st.text_input("ETF 5 (Sat 5%)", value="SMH")
    e6 = st.text_input("ETF 6 (Sat 5%)", value="TSLA")
    
    tickers = [e1, e2, e3, e4, e5, e6]
    anni_cagr = st.slider("Anni per calcolo CAGR", 5, 20, 10)

# 3. CARICAMENTO DATI
@st.cache_data
def get_data(ticker_list):
    df = yf.download(ticker_list, period="25y")["Close"].ffill()
    return df

try:
    data = get_data(tickers)
    
    # 4. RENDIMENTI (Griglia 3x2 per maggiore spazio)
    st.subheader(f"📊 Rendimento Annuo Composto ({anni_cagr} anni)")
    
    # Dividiamo in due righe da 3 per far respirare i numeri
    riga1 = st.columns(3)
    riga2 = st.columns(3)
    tutte_le_cols = riga1 + riga2
    
    cagr_results = {}

    for i, t in enumerate(tickers):
        serie = data[t].dropna()
        days = anni_cagr * 252
        if len(serie) >= days:
            v_ini, v_fin = serie.iloc[-days], serie.iloc[-1]
            v_i = float(v_ini.iloc[0] if hasattr(v_ini, 'iloc') else v_ini)
            v_f = float(v_fin.iloc[0] if hasattr(v_fin, 'iloc') else v_fin)
            cagr = ((v_f / v_i)**(1/anni_cagr)-1)*100
            cagr_results[t] = cagr
            tutte_le_cols[i].metric(t, f"{cagr:.2f}%")
        else:
            cagr_results[t] = 8.0 
            tutte_le_cols[i].metric(t, "N/D")

    # 5. GRAFICO STORICO
    st.markdown("---")
    st.subheader("📈 Crescita Comparativa")
    plot_data = data.tail(anni_cagr * 252)
    plot_norm = (plot_data / plot_data.iloc[0]) * 100
    fig = px.line(plot_norm, template="plotly_dark")
    fig.update_layout(font=dict(size=15)) # Testi del grafico più grandi
    st.plotly_chart(fig, use_container_width=True)

    # 6. RIBILANCIAMENTO (Strategia 70/30)
    st.markdown("---")
    st.header("⚖️ Ribilanciatore")
    capitale = st.number_input("Valore Totale Portafoglio attuale (€)", value=10000.0)
    pesi = {e1: 0.35, e2: 0.35, e3: 0.10, e4: 0.10, e5: 0.05, e6: 0.05}
    
    c1, c2 = st.columns(2)
    with c1:
        st.write("### 🎯 Target Ideale")
        for etf, peso in pesi.items():
            st.write(f"**{etf}**: {capitale*peso:,.2f}€")

    # 7. PROIEZIONE FUTURA
    st.markdown("---")
    st.header("🔮 Dove sarai tra 10 anni?")
    risparmio = st.slider("Risparmio mensile (€)", 0, 5000, 500)
    
    resa_media = sum(cagr_results[t] * pesi[t] for t in tickers)
    mesi = 10 * 12
    resa_mensile = (1 + (resa_media / 100)) ** (1/12) - 1
    proiezione = [capitale]
    for m in range(mesi):
        proiezione.append((proiezione[-1] * (1 + resa_mensile)) + risparmio)
    
    st.success(f"## 💰 Capitale nel 2036: {proiezione[-1]:,.2f}€")
    st.line_chart(proiezione)

except Exception as e:
    st.error(f"Controlla la connessione o i Ticker: {e}")
