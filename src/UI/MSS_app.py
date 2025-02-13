import os
import sys
import streamlit as st
import pandas as pd
import yfinance as yf
import requests
import json
import matplotlib.pyplot as plt
import seaborn as sns
from textblob import TextBlob
import pandas_ta as ta

# Ensure correct path imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

# Import existing modules
from src.Data_Retrieval.data_fetcher import DataFetcher
from src.Indicators.sma import SMAIndicator  # Import the SMAIndicator class

# Streamlit UI
st.title("Prototype Trading System")

# Input field to choose stock symbol
symbol = st.text_input("Enter Stock Symbol:", value="AAPL")

# Initialize the DataFetcher and retrieve the data
data_fetcher = DataFetcher()
data = data_fetcher.get_stock_data(symbol)

# Display the original data
st.write(f"Original Stock Data for {symbol}:")
st.dataframe(data.tail())

# Add a button to calculate and display SMA using SMAIndicator class
if st.button("Calculate SMA"):
    period = st.number_input("Enter SMA period:", min_value=1, max_value=100, value=14)
    sma_indicator = SMAIndicator(period=period)  # Instantiate the SMAIndicator class
    data_with_sma = sma_indicator.calculate(data)  # Calculate the SMA
    st.write(f"Stock Data with SMA{period} for {symbol}:")
    st.dataframe(data_with_sma.tail())

# Add a button to calculate and display RSI using pandas_ta
if st.button("Calculate RSI"):
    period = st.number_input("Enter RSI period:", min_value=1, max_value=100, value=14)
    data[f"RSI{period}"] = ta.rsi(data['Close'], length=period)
    st.write(f"Stock Data with RSI{period} for {symbol}:")
    st.dataframe(data.tail())

# Add a button to fetch the latest data for the selected symbol
if st.button("Fetch Latest Data"):
    latest_data = data_fetcher.get_stock_data(symbol)
    st.write(f"Latest Stock Data for {symbol}:")
    st.dataframe(latest_data.tail())


# === Data Collection Agent ===
class DataCollectionAgent:
    """Agent to collect and process financial data, news, and social media insights."""

    def fetch_news_articles(self, symbol):
        """Fetch financial news articles related to the stock symbol."""
        url = f"https://finnhub.io/api/v1/news?category=general&token=cuik1g1r01qtqfmisj9gcuik1g1r01qtqfmisja0"
        response = requests.get(url)
        if response.status_code == 200:
            articles = response.json()
            return articles[:5]  # Return top 5 news articles
        return []

    def collect_social_media_data(self, symbol):
        """Perform sentiment analysis on social media posts (simulated)."""
        sample_posts = [
            f"{symbol} is on the rise! 🚀 #bullish",
            f"Worried about {symbol}'s volatility today...",
            f"Market analysts predict a strong quarter for {symbol}.",
        ]
        sentiment_scores = [TextBlob(post).sentiment.polarity for post in sample_posts]
        return sentiment_scores

    def get_financial_reports(self, symbol):
        """Retrieve stock's financial data using Yahoo Finance."""
        stock = yf.Ticker(symbol)
        return stock.financials

    def preprocess_data(self, data):
        """Perform basic data cleaning."""
        data = data.dropna()  # Remove missing values
        return data

    def exploratory_data_analysis(self, data):
        """Perform basic exploratory data analysis (EDA)."""
        plt.figure(figsize=(8, 4))
        sns.histplot(data['Close'], bins=30, kde=True)
        st.pyplot(plt)


# Initialize the Data Collection Agent
data_agent = DataCollectionAgent()

# Button to fetch news articles
if st.button("Fetch News Articles"):
    articles = data_agent.fetch_news_articles(symbol)
    for article in articles:
        st.write(f"**{article['headline']}** - {article['source']}")
        st.write(article['summary'])
        st.write("---")

# Button to analyze social media sentiment
if st.button("Analyze Social Media Sentiment"):
    sentiment_scores = data_agent.collect_social_media_data(symbol)
    st.write("Sentiment Scores:", sentiment_scores)
    st.bar_chart(sentiment_scores)

# Button to fetch financial reports
if st.button("Fetch Financial Reports"):
    reports = data_agent.get_financial_reports(symbol)
    st.write("Financial Reports:")
    st.dataframe(reports)

# Button to perform EDA
if st.button("Perform Exploratory Data Analysis"):
    cleaned_data = data_agent.preprocess_data(data)
    data_agent.exploratory_data_analysis(cleaned_data)
