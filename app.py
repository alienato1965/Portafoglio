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
# --- SEZIONE RIBILANCIAMENTO ---
    st.markdown("---")
    st.header("⚖️ Calcolatore di Ribilanciamento Strategico")
    st.write("Inserisci il valore attuale dei tuoi investimenti per vedere come tornare al target 70/30.")

    # Input del capitale totale
    capitale_totale = st.number_input("Valore totale del portafoglio (€)", min_value=0.0, value=10000.0, step=100.0)

    # I tuoi target definitivi
    targets = {
        "VWCE.DE": 0.35, # 35% Core Mondo
        "QDVE.DE": 0.35, # 35% Core Tech
        "SGLN.L": 0.20,  # 20% Satellite Oro
        "GDXJ": 0.10     # 10% Satellite Junior Miners
    }

    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🎯 Target Ideale")
        for etf, peso in targets.items():
            valore_target = capitale_totale * peso
            st.write(f"**{etf}**: {valore_target:,.2f}€ ({peso*100:.0f}%)")

    with col2:
        st.subheader("📝 Note Operative")
        st.info(f"""

        # --- PROIEZIONE FUTURA (PAC) ---
    st.markdown("---")
    st.header("🔮 Simulatore di Ricchezza Futura")
    st.write("Dato che non hai immobili o pensioni, la tua ricchezza dipende dal tuo portafoglio. Vediamo dove sarai tra 10 anni.")

    # Slider interattivo per il risparmio
    risparmio_mensile = st.slider("Quanto puoi investire ogni mese (€)?", 0, 5000, 500)
    
    # Calcolo rendimento medio pesato della tua strategia 70/30
    # Usiamo i rendimenti reali a 10 anni calcolati dal software
    try:
        r_vwce = float(df_cagr.loc["VWCE.DE", "10y"].replace('%','')) if "VWCE.DE" in df_cagr.index else 7.0
        r_qdve = float(df_cagr.loc["QDVE.DE", "10y"].replace('%','')) if "QDVE.DE" in df_cagr.index else 12.0
        r_sgln = float(df_cagr.loc["SGLN.L", "10y"].replace('%','')) if "SGLN.L" in df_cagr.index else 5.0
        r_gdxj = float(df_cagr.loc["GDXJ", "10y"].replace('%','')) if "GDXJ" in df_cagr.index else 2.0
        
        # Media pesata: 35% VWCE + 35% QDVE + 20% Oro + 10% Minatori
        resa_media = (r_vwce * 0.35) + (r_qdve * 0.35) + (r_sgln * 0.20) + (r_gdxj * 0.10)
    except:
        resa_media = 8.0 # Valore di sicurezza se i dati mancano

    # Calcolo proiezione 10 anni (120 mesi)
    mesi = 10 * 12
    resa_mensile = (1 + (resa_media / 100)) ** (1/12) - 1
    valore_nel_tempo = [capitale_totale]
    
    for m in range(mesi):
        nuovo_valore = (valore_nel_tempo[-1] * (1 + resa_mensile)) + risparmio_mensile
        valore_nel_tempo.append(nuovo_valore)

    # Visualizzazione Risultato
    st.success(f"### 💰 Valore stimato tra 10 anni: {valore_nel_tempo[-1]:,.2f}€")
    st.line_chart(valore_nel_tempo)
    st.caption(f"Proiezione basata su un rendimento annuo medio del {resa_media:.2f}% (dati reali ultimi 10 anni).")
        **Strategia Attuale:**
        - **CORE (70%):** All-World + S&P 500 IT
        - **SATELLITE (30%):** Gold + Junior Miners
        
        Se un asset devia di oltre il 5% dal target, valuta di vendere la parte in eccedenza per comprare quella in difetto.
        """)
