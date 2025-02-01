import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import streamlit as st
import pandas as pd
import numpy as np
import pandas_ta as ta

# Import your existing modules
from src.Data_Retrieval.data_fetcher import DataFetcher
from src.Indicators.sma import SMAIndicator  # Import the SMAIndicator class

# ==============================
# Gann Hi-Lo Activator Function
# ==============================
def calculate_gann_hi_lo_activator(df: pd.DataFrame, smoothing_period: int = 0) -> pd.DataFrame:
    """
    Calculates the Gann Hi-Lo Activator indicator with dynamic column handling.
    """
    # Check for variations in column names
    possible_low_columns = ['Low', 'low', 'Low AAPL']
    possible_high_columns = ['High', 'high', 'High AAPL']
    possible_close_columns = ['Close', 'close', 'Close AAPL']

    # Dynamically select columns
    low_col = next((col for col in possible_low_columns if col in df.columns), None)
    high_col = next((col for col in possible_high_columns if col in df.columns), None)
    close_col = next((col for col in possible_close_columns if col in df.columns), None)

    if not low_col or not high_col or not close_col:
        raise KeyError(f"Required columns 'Low', 'High', or 'Close' not found in the DataFrame. Columns found: {df.columns.tolist()}")

    # Initialize the activator list
    activator = [np.nan] * len(df)
    
    # Set the first activator value
    activator[0] = float(df[low_col].iloc[0])
    
    # Process each row
    for i in range(1, len(df)):
        current_close  = float(df[close_col].iloc[i])
        current_low    = float(df[low_col].iloc[i])
        current_high   = float(df[high_col].iloc[i])
        prev_activator = float(activator[i - 1])
        
        if current_close > prev_activator:
            activator[i] = min(current_low, prev_activator)
        else:
            activator[i] = max(current_high, prev_activator)
    
    # Add the raw activator values
    df['Gann Hi-Lo'] = activator

    # Apply EMA smoothing
    if smoothing_period > 1:
        ema_series = pd.Series(activator, index=df.index).ewm(span=smoothing_period, adjust=False).mean()
        ema_series.name = 'Gann Hi-Lo Smoothed'
        df['Gann Hi-Lo Smoothed'] = ema_series
    else:
        df['Gann Hi-Lo Smoothed'] = df['Gann Hi-Lo']

    return df

# ==============================
# Streamlit UI
# ==============================
st.title("Gann Hi Lo Trading System")

# Input field to choose stock symbol
symbol = st.text_input("Enter Stock Symbol:", value="AAPL")

# Initialize the DataFetcher and retrieve the data
data_fetcher = DataFetcher()
data = data_fetcher.get_stock_data(symbol)

# Flatten multi-level columns if present
if isinstance(data.columns, pd.MultiIndex):
    data.columns = [' '.join(col).strip() for col in data.columns]

# Debugging: Display column names to ensure correct structure
st.write("DataFrame Columns:", data.columns.tolist())

# Display the original stock data
st.write(f"Original Stock Data for {symbol}:")
st.dataframe(data.tail())

# Button and input for calculating the Gann Hi-Lo Activator
gann_smoothing = st.number_input("Enter Gann Hi-Lo Smoothing Period:", min_value=1, max_value=100, value=10, key="gann_smoothing")
if st.button("Calculate Gann Hi-Lo Activator"):
    try:
        data_with_gann = calculate_gann_hi_lo_activator(data.copy(), smoothing_period=gann_smoothing)
        st.write(f"Stock Data with Gann Hi-Lo Activator for {symbol}:")
        st.dataframe(data_with_gann[['Close', 'High', 'Low', 'Gann Hi-Lo', 'Gann Hi-Lo Smoothed']].tail())
    except KeyError as e:
        st.error(f"Error: {e}")

# Button to fetch the latest stock data for the selected symbol
if st.button("Fetch Latest Data"):
    latest_data = data_fetcher.get_stock_data(symbol)
    st.write(f"Latest Stock Data for {symbol}:")
    st.dataframe(latest_data.tail())
