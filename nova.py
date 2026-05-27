import streamlit as st
import yfinance as yf
import pandas as pd
import time
import random

st.set_page_config(page_title="NOVA India", layout="wide")

st.title("🇮🇳 NOVA - Stock Recommender")

stocks = [
    "RELIANCE.NS", "TCS.NS", "INFY.NS", "HDFCBANK.NS",
    "ICICIBANK.NS", "SBIN.NS", "ITC.NS", "LT.NS",
    "AXISBANK.NS", "KOTAKBANK.NS", "BAJFINANCE.NS",
    "ASIANPAINT.NS", "MARUTI.NS", "SUNPHARMA.NS"
]

def calculate_rsi(data, window=14):
    delta = data.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

results = []

for stock in stocks:
    try:
        data = yf.download(stock, period="120d", interval="1d", progress=False)

        if data.empty:
            raise Exception("No data")

        data["MA50"] = data["Close"].rolling(50).mean()
        data["RSI"] = calculate_rsi(data["Close"])

        valid_data = data.dropna(subset=["MA50", "RSI"])
        latest = valid_data.iloc[-1]

        close_price = float(latest["Close"])
        ma50 = float(latest["MA50"])
        rsi = float(latest["RSI"])

        # Signal logic
        if close_price > ma50 and rsi < 60:
            signal = "STRONG BUY ✅✅"
            score = 3
        elif close_price > ma50:
            signal = "BUY ✅"
            score = 2
        elif rsi < 40:
            signal = "REVERSAL ⚠️"
            score = 1
        else:
            signal = "AVOID ❌"
            score = 0

        source = "REAL ✅"

    except:
        # ✅ fallback (ALWAYS triggered if API fails)
        close_price = random.randint(1000, 3000)
        rsi = random.randint(30, 70)
        score = 1
        signal = "SIMULATED 📊"
        source = "FALLBACK ⚠️"

    # ✅ ALWAYS append result (important fix)
    results.append({
        "Stock": stock.replace(".NS", ""),
        "Price": round(close_price, 2),
        "RSI": round(rsi, 2),
        "Score": score,
        "Signal": signal,
        "Source": source
    })

# ✅ DataFrame ALWAYS has data
df = pd.DataFrame(results)

st.subheader("📊 Recommendations")

df = df.sort_values(by="Score", ascending=False)

st.dataframe(df, use_container_width=True)

st.subheader("🔥 Top Picks")

top_picks = df.head(3)

for _, row in top_picks.iterrows():
    st.write(f"""
    **{row['Stock']}**
    - Price: ₹{row['Price']}
    - RSI: {row['RSI']}
    - Signal: {row['Signal']}
    - Source: {row['Source']}
    """)
