import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(page_title="NOVA India", layout="wide")

st.title("🇮🇳 NOVA - Stock Recommender")

# List of stocks
stocks = [
    "RELIANCE.NS", "TCS.NS", "INFY.NS",
    "HDFCBANK.NS", "ICICIBANK.NS", "LT.NS"
]

results = []

for stock in stocks:
    try:
        data = yf.download(stock, period="90d", interval="1d")

        # Skip if insufficient data
        if data.empty or len(data) < 50:
            continue

        # Calculate Moving Average
        data["MA50"] = data["Close"].rolling(50).mean()

        # Drop NaN rows
        data = data.dropna()

        # Get latest valid row
        latest = data.iloc[-1]

        close_price = float(latest["Close"])
        ma50 = float(latest["MA50"])

        # Safe comparison
        if close_price > ma50:
            signal = "BUY ✅"
        else:
            signal = "AVOID ❌"

        results.append({
            "Stock": stock.replace(".NS", ""),
            "Price": round(close_price, 2),
            "Signal": signal
        })

    except Exception as e:
        # Skip problematic stock instead of crashing
        continue

# Create dataframe
df = pd.DataFrame(results)

st.subheader("📊 Recommendations")
st.dataframe(df, use_container_width=True)

# Filter BUY signals
st.subheader("🔥 Top Picks")

buy_stocks = df[df["Signal"] == "BUY ✅"]

if not buy_stocks.empty:
    for _, row in buy_stocks.iterrows():
        st.write(f"✅ {row['Stock']} at ₹{row['Price']}")
else:
    st.write("No strong buy signals today.")
