import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(page_title="NOVA India", layout="wide")

st.title("🇮🇳 NOVA - Stock Recommender")

# List of stocks (you can expand later)
stocks = [
    "RELIANCE.NS", "TCS.NS", "INFY.NS",
    "HDFCBANK.NS", "ICICIBANK.NS", "LT.NS"
]

results = []

for stock in stocks:
    data = yf.download(stock, period="60d", interval="1d")

    if len(data) < 50:
        continue

    data["MA50"] = data["Close"].rolling(50).mean()
    latest = data.iloc[-1]

    if latest["Close"] > latest["MA50"]:
        signal = "BUY ✅"
    else:
        signal = "AVOID ❌"

    results.append({
        "Stock": stock.replace(".NS", ""),
        "Price": round(latest["Close"], 2),
        "Signal": signal
    })

df = pd.DataFrame(results)

st.subheader("📊 Recommendations")
st.dataframe(df)

st.subheader("🔥 Top Picks")

for _, row in df.iterrows():
    if row["Signal"] == "BUY ✅":
        st.write(f"✅ {row['Stock']} at ₹{row['Price']}")