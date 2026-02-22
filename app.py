import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px

# Configurazione Pagina (Grafica Moderna)
st.set_page_config(page_title="MyFinance 70/30", layout="wide")
st.markdown("<style>body {background-color: #121212; color: white;}</style>", unsafe_allow_html=True)

st.title("📊 Portfolio Monitor: Strategy 70/30")

# --- SIDEBAR (Ricerca Nuovi ETF) ---
st.sidebar.header("🔍 Cerca e Confronta")
nuovo_etf = st.sidebar.text_input("Inserisci Ticker (es. NVDA, TSLA, BTC-EUR)", "")

# --- I TUOI ETF (Core & Satellite) ---
tickers = ["VWCE.DE", "QDVE.DE", "SGLN.L", "GDXJ"]
if nuovo_etf:
    tickers.append(nuovo_etf)

# --- CALCOLO DATI ---
@st.cache_data
def load_data(ticker_list):
    dati = yf.download(ticker_list, period="20y")["Close"]
    return dati.ffill()

data = load_data(tickers)

# --- TABELLA CAGR (La tua richiesta A) ---
st.subheader("🏆 Rendimenti Annui Composti (CAGR %)")

def get_cagr(serie, years):
    days = years * 252
    if len(serie.dropna()) < days: return "N/D"
    val_fin = serie.dropna().iloc[-1]
    val_ini = serie.dropna().iloc[-days]
    return round((((val_fin / val_ini) ** (1/years)) - 1) * 100, 2)

cagr_data = []
for t in tickers:
    row = {"Asset": t}
    for y in [5, 10, 15, 20]:
        row[f"{y}y"] = get_cagr(data[t], y)
    cagr_data.append(row)

df_cagr = pd.DataFrame(cagr_data).set_index("Asset")

# Grafica della tabella con colori
def style_cagr(val):
    if isinstance(val, str): return ""
    color = "#00ff00" if val > 10 else ("#ffa500" if val > 5 else "#ff4b4b")
    return f"color: {color}; font-weight: bold"

st.table(df_cagr.style.applymap(style_cagr))

# --- GRAFICO INTERATTIVO ---
st.subheader("📈 Crescita Storica (Base 100)")
start_y = st.select_slider("Seleziona anni indietro", options=[5, 10, 15, 20], value=10)
days_plot = start_y * 252
plot_data = data.iloc[-days_plot:]
plot_data_norm = (plot_data / plot_data.iloc[0]) * 100

fig = px.line(plot_data_norm, template="plotly_dark")
st.plotly_chart(fig, use_container_width=True)
