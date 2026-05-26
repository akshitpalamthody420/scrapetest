import os
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

from fetch_news import fetch_news
from fetch_stock import get_stock_data
from sentiment import analyze_sentiment
from visualization import plot_sentiment_summary

st.title("Real-Time Stock Sentiment Analyzer")

# Data mode selection
data_mode = st.radio("Select Data Mode:", ("Real-Time", "Sample Data"))

# Two ticker inputs instead of one
col1, col2 = st.columns(2)
with col1:
    ticker1 = st.text_input("Enter First Stock Ticker:", "AAPL").upper().strip()
with col2:
    ticker2 = st.text_input("Enter Second Stock Ticker:", "MSFT").upper().strip()

if st.button("Fetch Data"):
    st.subheader("Stock Price Comparison")

    # Load stock data
    if data_mode == "Real-Time":
        data1 = get_stock_data(ticker1)
        data2 = get_stock_data(ticker2)
    else:
        data1 = pd.read_csv("data/sample_stock.csv", parse_dates=["Date"], index_col="Date")
        data2 = pd.read_csv("data/sample_stock.csv", parse_dates=["Date"], index_col="Date")

    # Plot both closing prices together
    norm1 = data1["Close"] / data1["Close"].iloc[0] * 100
    norm2 = data2["Close"] / data2["Close"].iloc[0] * 100

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(data1.index, norm1, label=ticker1)
    ax.plot(data2.index, norm2, label=ticker2)
    ax.set_title(f"{ticker1} vs {ticker2} Normalized Performance")
    ax.set_xlabel("Time")
    ax.set_ylabel("Indexed Price (Start = 100)")
    ax.legend()
    st.pyplot(fig)

    # News + sentiment side by side
    st.subheader("News Sentiment Comparison")
    news_col1, news_col2 = st.columns(2)

    with news_col1:
        st.markdown(f"### {ticker1}")
        sentiments1 = []
        try:
            articles1 = fetch_news(ticker1)
            for title, desc in articles1:
                sentiment = analyze_sentiment(title + " " + str(desc))
                sentiments1.append(sentiment)
                st.write(f"**{title}** - Sentiment: {sentiment}")

            if sentiments1:
                plot_sentiment_summary(sentiments1)
        except Exception as e:
            st.warning(f"Could not fetch news for {ticker1}: {e}")

    with news_col2:
        st.markdown(f"### {ticker2}")
        sentiments2 = []
        try:
            articles2 = fetch_news(ticker2)
            for title, desc in articles2:
                sentiment = analyze_sentiment(title + " " + str(desc))
                sentiments2.append(sentiment)
                st.write(f"**{title}** - Sentiment: {sentiment}")

            if sentiments2:
                plot_sentiment_summary(sentiments2)
        except Exception as e:
            st.warning(f"Could not fetch news for {ticker2}: {e}")