import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from plotly.subplots import make_subplots
import plotly.graph_objects as go


# Fetch historical stock data
class DataFetcher:
    def __init__(self, start_date: datetime = None, end_date: datetime = None):
        self.start_date = start_date or datetime.today() - timedelta(days=365)  # Default: 1 year of data
        self.end_date = end_date or datetime.today()

    def get_stock_data(self, symbol: str) -> pd.DataFrame:
        start_date_str = self.start_date.strftime('%Y-%m-%d')
        end_date_str = self.end_date.strftime('%Y-%m-%d')

        df = yf.download(symbol, start=start_date_str, end=end_date_str)
        df.index = pd.to_datetime(df.index)
        return df


# Calculate USI values
def calculate_su_sd(prices):
    su = np.zeros(len(prices))
    sd = np.zeros(len(prices))

    for i in range(1, len(prices)):
        if prices[i] > prices[i - 1]:
            su[i] = prices[i] - prices[i - 1]
        elif prices[i] < prices[i - 1]:
            sd[i] = prices[i - 1] - prices[i]

    return su, sd


def ultimate_smoother(data, period):
    a1 = np.exp(-1.414 * np.pi / period)
    b1 = 2 * a1 * np.cos(1.414 * 180 / period)
    c2 = b1
    c3 = -a1 * a1
    c1 = (1 + c2 - c3) / 4

    smoothed = np.zeros_like(data)
    for i in range(len(data)):
        if i >= 3:
            smoothed[i] = (
                (1 - c1) * data[i]
                + (2 * c1 - c2) * data[i - 1]
                - (c1 + c3) * data[i - 2]
                + c2 * smoothed[i - 1]
                + c3 * smoothed[i - 2]
            )
        else:
            smoothed[i] = data[i]

    return smoothed


def calculate_usi(prices, period):
    su, sd = calculate_su_sd(prices)
    usu = ultimate_smoother(su, period)
    usd = ultimate_smoother(sd, period)

    usi = np.zeros(len(prices))
    for i in range(len(prices)):
        if (usu[i] + usd[i] > 0) and (usu[i] > 0.01) and (usd[i] > 0.01):
            usi[i] = (usu[i] - usd[i]) / (usu[i] + usd[i])

    return usi


# Visualization Agent
class VisualizationAgent:
    @staticmethod
    def plot_swing_vs_trend_comparison(dates, swing_usi, trend_usi):
        fig = make_subplots(
            rows=1, cols=2,
            subplot_titles=("Swing Trading (Short-Term)", "Trend Trading (Long-Term)")
        )

        # Plot Swing Trading USI
        fig.add_trace(
            go.Scatter(
                x=dates, y=swing_usi,
                mode='lines',
                name='Swing USI',
                line=dict(color='blue', width=2)
            ),
            row=1, col=1
        )

        swing_zero_crossings = np.where(np.diff(np.sign(swing_usi)))[0]
        fig.add_trace(
            go.Scatter(
                x=dates[swing_zero_crossings],
                y=swing_usi[swing_zero_crossings],
                mode='markers',
                name='Swing Zero Crossings',
                marker=dict(color='red', size=8)
            ),
            row=1, col=1
        )

        # Plot Trend Trading USI
        fig.add_trace(
            go.Scatter(
                x=dates, y=trend_usi,
                mode='lines',
                name='Trend USI',
                line=dict(color='green', width=2)
            ),
            row=1, col=2
        )

        trend_zero_crossings = np.where(np.diff(np.sign(trend_usi)))[0]
        fig.add_trace(
            go.Scatter(
                x=dates[trend_zero_crossings],
                y=trend_usi[trend_zero_crossings],
                mode='markers',
                name='Trend Zero Crossings',
                marker=dict(color='orange', size=8)
            ),
            row=1, col=2
        )

        fig.update_layout(
            title="Swing vs. Trend Trading: USI Comparison",
            template="plotly_white",
            height=500, width=1000
        )

        fig.show()


# Test usability with real-world data
if __name__ == "__main__":
    # Fetch real-world stock data
    fetcher = DataFetcher()
    stock_data = fetcher.get_stock_data("AAPL")  # Example: Apple stock

    # Extract closing prices
    closing_prices = stock_data['Close'].values
    dates = stock_data.index

    # Calculate USI for Swing and Trend Trading
    swing_usi = calculate_usi(closing_prices, period=14)  # Short-term USI
    trend_usi = calculate_usi(closing_prices, period=112)  # Long-term USI

    # Visualize Swing vs. Trend Trading
    VisualizationAgent.plot_swing_vs_trend_comparison(dates, swing_usi, trend_usi)
