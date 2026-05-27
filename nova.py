import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(page_title="NOVA India", layout="wide")

st.title("🇮🇳 NOVA - Stock Recommender")

stocks = [
    "RELIANCE.NS", "TCS.NS", "INFY.NS",
    "HDFCBANK.NS", "ICICIBANK.NS", "LT.NS"
]

results = []

for stock in stocks:
    try:
        data = yf.download(stock, period="90d", interval="1d")

        # Skip if no data
        if data.empty or len(data) < 50:
            continue

        data["MA50"] = data["Close"].rolling(50).mean()
        data = data.dropna()

        if data.empty:
            continue

        latest = data.iloc[-1]

        close_price = float(latest["Close"])
        ma50 = float(latest["MA50"])

        if close_price > ma50:
            signal = "BUY ✅"
        else:
            signal = "AVOID ❌"

        results.append({
            "Stock": stock.replace(".NS", ""),
            "Price": round(close_price, 2),
            "Signal": signal
        })

    except Exception:
        continue

# ✅ Create dataframe safely
df = pd.DataFrame(results)

st.subheader("📊 Recommendations")

# ✅ Handle empty case safely
if df.empty:
    st.warning("No data available. Try again later.")
else:
    st.dataframe(df, use_container_width=True)

    st.subheader("🔥 Top Picks")

    buy_stocks = df[df["Signal"] == "BUY ✅"]

    if not buy_stocks.empty:
        for _, row in buy_stocks.iterrows():
            st.write(f"✅ {row['Stock']} at ₹{row['Price']}")
    else:
        st.info("No BUY signals today.")
