import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(page_title="NOVA India", layout="wide")

st.title("🇮🇳 NOVA - Stock Recommender")

stocks = [
    "RELIANCE.NS", "TCS.NS", "INFY.NS",
    "HDFCBANK.NS", "ICICIBANK.NS", "LT.NS"
]

# ✅ RSI function
def calculate_rsi(data, window=14):
    delta = data.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

results = []

for stock in stocks:
    try:
        data = yf.download(stock, period="120d", interval="1d")

        if data.empty:
            continue

        # Indicators
        data["MA50"] = data["Close"].rolling(50).mean()
        data["RSI"] = calculate_rsi(data["Close"])

        valid_data = data.dropna(subset=["MA50", "RSI"])

        if valid_data.empty:
            continue

        latest = valid_data.iloc[-1]

        close_price = float(latest["Close"])
        ma50 = float(latest["MA50"])
        rsi = float(latest["RSI"])

        # ✅ FLEXIBLE LOGIC (always assigns something useful)
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

        results.append({
            "Stock": stock.replace(".NS", ""),
            "Price": round(close_price, 2),
            "RSI": round(rsi, 2),
            "Score": score,
            "Signal": signal
        })

    except Exception:
        continue

# ✅ Create DataFrame
df = pd.DataFrame(results)

st.subheader("📊 Recommendations")

if df.empty:
    st.error("Data not available. Check internet or API.")
else:
    # ✅ SORT by best opportunities
    df = df.sort_values(by="Score", ascending=False)

    st.dataframe(df, use_container_width=True)

    st.subheader("🔥 Top Picks")

    # ✅ Always show top 3 (even if weak)
    top_picks = df.head(3)

    for _, row in top_picks.iterrows():
        st.write(f"""
        **{row['Stock']}**
        - Price: ₹{row['Price']}
        - RSI: {row['RSI']}
        - Signal: {row['Signal']}
        """)
