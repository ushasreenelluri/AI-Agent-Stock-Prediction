import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta


class DataFetcher:
    def __init__(self, start_date: datetime = None, end_date: datetime = None):
        """
        Initializes the DataFetcher with a default start date of 60 days ago and an end date of today.

        Args:
            start_date (datetime, optional): The start date for data retrieval. Defaults to 60 days ago.
            end_date (datetime, optional): The end date for data retrieval. Defaults to today.
        """
        self.start_date = start_date or datetime.today() - timedelta(days=60)
        self.end_date = end_date or datetime.today()

    def get_stock_data(self, symbol: str, start_date: datetime = None, end_date: datetime = None) -> pd.DataFrame:
        """
        Fetches historical stock data for the given symbol.

        Args:
            symbol (str): The stock symbol to fetch data for.
            start_date (datetime, optional): The start date for data retrieval. If None, uses self.start_date.
            end_date (datetime, optional): The end date for data retrieval. If None, uses self.end_date.

        Returns:
            pd.DataFrame: A DataFrame containing the historical stock data.
        """
        start_date = start_date or self.start_date
        end_date = end_date or self.end_date

        start_date_str = start_date.strftime('%Y-%m-%d')
        end_date_str = end_date.strftime('%Y-%m-%d')

        # Download historical stock data
        df = yf.download(symbol, start=start_date_str, end=end_date_str)
        df.index = pd.to_datetime(df.index)
        return df


def calculate_su_sd(prices):
    """
    Calculate Strength Up (SU) and Strength Down (SD) from price data.

    Parameters:
        prices (list or np.array): List of closing prices.

    Returns:
        su (np.array): Strength Up values.
        sd (np.array): Strength Down values.
    """
    su = np.zeros(len(prices))
    sd = np.zeros(len(prices))

    for i in range(1, len(prices)):
        if prices[i] > prices[i - 1]:
            su[i] = prices[i] - prices[i - 1]
        elif prices[i] < prices[i - 1]:
            sd[i] = prices[i - 1] - prices[i]

    return su, sd


# **Integrated Example Usage**
if __name__ == "__main__":
    # Create a DataFetcher instance
    fetcher = DataFetcher()

    # Fetch stock data for a symbol (e.g., Apple stock: "AAPL")
    stock_data = fetcher.get_stock_data("AAPL")

    # Extract the closing prices
    closing_prices = stock_data['Close'].values

    # Calculate SU and SD using the closing prices
    su, sd = calculate_su_sd(closing_prices)

    # Print results
    print("Closing Prices:", closing_prices)
    print("Strength Up (SU):", su)
    print("Strength Down (SD):", sd)
