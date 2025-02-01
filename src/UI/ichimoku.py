#!/usr/bin/env python3
import os
import sys
from textwrap import dedent
import pandas as pd
from yahooquery import Ticker
from dotenv import load_dotenv

# Load environment variables if you need to set API keys or other configurations
load_dotenv()

class IchimokuCalculator:
    """
    Calculates Ichimoku Cloud components:
      - Tenkan-sen (Conversion Line)
      - Kijun-sen (Base Line)
      - Senkou Span A (Leading Span A)
      - Senkou Span B (Leading Span B)
      - Chikou Span (Lagging Span)
      
    By default, standard periods are used:
      - Tenkan-sen period: 9
      - Kijun-sen period: 26
      - Senkou Span B period: 52
      - Displacement (for Senkou and Chikou): 26
    """
    def __init__(self, df, tenkan_period=9, kijun_period=26, senkou_b_period=52, displacement=26):
        # Work on a copy of the data to avoid modifying the original DataFrame
        self.df = df.copy()
        self.tenkan_period = tenkan_period
        self.kijun_period = kijun_period
        self.senkou_b_period = senkou_b_period
        self.displacement = displacement

    def calculate(self):
        # Ensure the DataFrame is sorted by date
        if 'date' in self.df.columns:
            self.df.sort_values(by='date', inplace=True)

        # Subtask 1: Calculate Tenkan-sen (Conversion Line)
        # Formula: (Highest High + Lowest Low) / 2 over the last 9 periods
        self.df['tenkan_sen'] = (
            self.df['high'].rolling(window=self.tenkan_period, min_periods=self.tenkan_period).max() +
            self.df['low'].rolling(window=self.tenkan_period, min_periods=self.tenkan_period).min()
        ) / 2

        # Calculate Kijun-sen (Base Line)
        # Formula: (Highest High + Lowest Low) / 2 over the last 26 periods
        self.df['kijun_sen'] = (
            self.df['high'].rolling(window=self.kijun_period, min_periods=self.kijun_period).max() +
            self.df['low'].rolling(window=self.kijun_period, min_periods=self.kijun_period).min()
        ) / 2

        # Calculate Senkou Span A (Leading Span A)
        # Formula: (Tenkan-sen + Kijun-sen) / 2, shifted forward by 26 periods
        self.df['senkou_span_a'] = (
            (self.df['tenkan_sen'] + self.df['kijun_sen']) / 2
        ).shift(self.displacement)

        # Calculate Senkou Span B (Leading Span B)
        # Formula: (Highest High + Lowest Low) / 2 over the last 52 periods, shifted forward by 26 periods
        self.df['senkou_span_b'] = (
            self.df['high'].rolling(window=self.senkou_b_period, min_periods=self.senkou_b_period).max() +
            self.df['low'].rolling(window=self.senkou_b_period, min_periods=self.senkou_b_period).min()
        ) / 2
        self.df['senkou_span_b'] = self.df['senkou_span_b'].shift(self.displacement)

        # Calculate Chikou Span (Lagging Span)
        # Formula: Today's closing price shifted backward by 26 periods
        self.df['chikou_span'] = self.df['close'].shift(-self.displacement)

        return self.df

def fetch_stock_data(ticker_symbol, period='1y'):
    """
    Fetches historical stock data for a given ticker symbol.
    Uses yahooquery to retrieve data for the specified period.
    """
    print(f"Fetching historical data for {ticker_symbol} (period={period})...")
    ticker = Ticker(ticker_symbol)
    data = ticker.history(period=period)
    
    # Reset the index so that 'date' becomes a column (if needed)
    if isinstance(data, pd.DataFrame):
        data.reset_index(inplace=True)
    else:
        raise ValueError("Failed to fetch data as a DataFrame.")
    
    # Ensure required columns exist and use lower-case names for consistency
    # (Some dataframes might have columns 'High', 'Low', 'Close', etc.)
    for col in ['date', 'high', 'low', 'close']:
        if col not in data.columns:
            # Try lower-case conversion if needed
            if col.capitalize() in data.columns:
                data.rename(columns={col.capitalize(): col}, inplace=True)
            else:
                raise ValueError(f"Required column '{col}' not found in the data.")
    return data

def main():
    print("## Ichimoku Cloud Calculation System")
    print("-------------------------------")
    
    # Prompt user for the ticker symbol
    ticker_symbol = input(dedent("""\
        Enter the ticker symbol you want to analyze (e.g., AAPL, MSFT):
        """)).strip().upper()
    
    try:
        # Fetch historical stock data
        stock_data = fetch_stock_data(ticker_symbol, period='1y')
        
        # Instantiate the Ichimoku Calculator with the fetched data
        ichimoku_calculator = IchimokuCalculator(stock_data)
        
        # Subtask 2: Process data in real-time using efficient, vectorized calculations.
        ichimoku_data = ichimoku_calculator.calculate()
        
        # Display a snapshot of the calculated Ichimoku Cloud data
        print("\n--- Recent Ichimoku Cloud Data ---")
        # Show the most recent 10 rows
        print(ichimoku_data.tail(100)[['date', 'tenkan_sen', 'kijun_sen', 'senkou_span_a', 'senkou_span_b', 'chikou_span']])
        
    except Exception as e:
        print(f"An error occurred: {e}", file=sys.stderr)

if __name__ == "__main__":
    main()
