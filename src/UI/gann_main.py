import os
import sys

# Adjust the system path to include the project root
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import streamlit as st
import pandas as pd
from src.Data_Retrieval.data_fetcher import DataFetcher
from src.Indicators.gann import GannHiLoActivatorIndicator

st.title("Prototype Trading System: Gann Hi-Lo Activator")

# Input field for the stock symbol
symbol = st.text_input("Enter Stock Symbol:", value="AAPL")

# Initialize the DataFetcher and retrieve stock data
data_fetcher = DataFetcher()
data = data_fetcher.get_stock_data(symbol)

# Debug: Display DataFrame columns to verify names
st.write("DataFrame Columns:", data.columns)

# Standardize column names to have an initial capital letter (if necessary)
data.rename(columns=lambda x: x.capitalize(), inplace=True)

# Display the original stock data
st.write(f"Original Stock Data for {symbol}:")
st.dataframe(data.tail())

# Button to calculate and display Gann Hi-Lo Activator values
if st.button("Calculate Gann Hi-Lo Activator"):
    # Allow the user to optionally define a smoothing factor.
    # Enter 0 if no smoothing is desired.
    smoothing_input = st.number_input("Enter smoothing factor (0-1, enter 0 for no smoothing):", 
                                      min_value=0.0, max_value=1.0, value=0.0, step=0.01)
    smoothing = None if smoothing_input == 0.0 else smoothing_input

    # Instantiate the Gann Hi-Lo Activator indicator with the chosen smoothing factor
    gann_indicator = GannHiLoActivatorIndicator(smoothing=smoothing)
    data_with_gann = gann_indicator.calculate(data)
    
    st.write("Stock Data with Gann Hi-Lo Activator:")
    st.dataframe(data_with_gann.tail())

# Button to fetch the latest stock data
if st.button("Fetch Latest Data"):
    data = data_fetcher.get_stock_data(symbol)
    # Ensure the column names are standardized
    data.rename(columns=lambda x: x.capitalize(), inplace=True)
    st.write(f"Latest Stock Data for {symbol}:")
    st.dataframe(data.tail())
