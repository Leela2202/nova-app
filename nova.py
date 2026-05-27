import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(page_title="NOVA India", layout="wide")

st.title("🇮🇳 NOVA - Stock Recommender")

stocks = [
    "RELIANCE.NS", "TCS.NS", "INFY.NS",
    "HDFCBANK.NS", "ICICIBANK.NS", "LT.NS"
]

# ✅ RSI calculation function
def calculate_rsi(data, window=14):
    delta = data.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

results = []

for stock in stocks:
    try:
        data = yf.download(stock, period="120d", interval="1d")

        if data.empty:
            continue

        # Moving Average
        data["MA50"] = data["Close"].rolling(50).mean()

        # RSI
        data["RSI"] = calculate_rsi(data["Close"])

        # Get valid rows
        valid_data = data.dropna(subset=["MA50", "RSI"])

        if valid_data.empty:
            continue

        latest = valid_data.iloc[-1]

        close_price = float(latest["Close"])
        ma50 = float(latest["MA50"])
        rsi = float(latest["RSI"])

        # ✅ Improved logic
        if close_price > ma50 and rsi < 60:
            signal = "STRONG BUY ✅✅"
        elif close_price > ma50 and rsi < 75:
            signal = "BUY ✅"
        else:
            signal = "AVOID ❌"

        results.append({
            "Stock": stock.replace(".NS", ""),
            "Price": round(close_price, 2),
            "RSI": round(rsi, 2),
            "Signal": signal
        })

    except Exception:
        continue

df = pd.DataFrame(results)

st.subheader("📊 Recommendations")

if df.empty:
    st.warning("No strong signals right now. Market may be weak or sideways.")
else:
    st.dataframe(df, use_container_width=True)

    st.subheader("🔥 Top Picks")

    strong_buys = df[df["Signal"] == "STRONG BUY ✅✅"]

    buys = df[df["Signal"] == "BUY ✅"]

    if not strong_buys.empty:
        st.success("✅ STRONG BUY Opportunities")
        for _, row in strong_buys.iterrows():
            st.write(f"🔥 {row['Stock']} | ₹{row['Price']} | RSI: {row['RSI']}")

    if not buys.empty:
        st.info("✅ BUY Opportunities")
        for _, row in buys.iterrows():
            st.write(f"✅ {row['Stock']} | ₹{row['Price']}")

    if strong_buys.empty and buys.empty:
        st.warning("No BUY signals today.")
