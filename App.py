import streamlit as st
import yfinance as yf
import pandas as pd

st.title("🎯 Precision Finance Predictor")
st.write("Analyzing High-Volatility Entries for AVGO & CGAU")

ticker = st.selectbox("Select Asset", ["AVGO", "CGAU", "GUSH"])

if st.button("Generate Prediction"):
    data = yf.download(ticker, period="1mo", interval="1d")
    
    # Simple RSI Logic
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs)).iloc[-1]
    
    price = data['Close'].iloc[-1]
    
    st.metric(label="Current Price", value=f"${price:.2f}")
    
    if rsi < 35:
        st.success(f"🔥 BUY SIGNAL: RSI is {rsi:.2f} (Oversold).")
        st.write(f"Target Exit: ${price * 1.05:.2f} | Stop-Loss: ${price * 0.98:.2f}")
    elif rsi > 65:
        st.warning(f"⚠️ SELL/AVOID: RSI is {rsi:.2f} (Overbought).")
    else:
        st.info(f"Neutral: RSI is {rsi:.2f}. Waiting for pinpoint entry.")
