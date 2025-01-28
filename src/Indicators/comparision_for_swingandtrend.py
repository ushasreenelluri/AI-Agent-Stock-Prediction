import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import pandas as pd


class VisualizationAgent:
    @staticmethod
    def plot_swing_vs_trend_comparison(dates, swing_usi, trend_usi):
        """
        Plot side-by-side comparisons for swing and trend trading data using Plotly Subplots.

        Args:
            dates (list or np.array): List of dates corresponding to the USI values.
            swing_usi (list or np.array): USI values for swing trading.
            trend_usi (list or np.array): USI values for trend trading.
        """
        # Create subplots: 1 row, 2 columns
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
        # Highlight zero crossings in Swing Trading
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
        # Highlight zero crossings in Trend Trading
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

        # Update layout
        fig.update_layout(
            title="Swing vs. Trend Trading: USI Comparison",
            xaxis_title="Date",
            yaxis_title="USI Value",
            template="plotly_white",
            height=500, width=1000,
            showlegend=True
        )

        # Add a zero line to both subplots
        fig.add_shape(
            type="line", x0=dates[0], x1=dates[-1], y0=0, y1=0,
            line=dict(color="black", dash="dash"), row=1, col=1
        )
        fig.add_shape(
            type="line", x0=dates[0], x1=dates[-1], y0=0, y1=0,
            line=dict(color="black", dash="dash"), row=1, col=2
        )

        # Show plot
        fig.show()


# Example Usage
if __name__ == "__main__":
    # Generate sample data
    dates = pd.date_range(start="2023-01-01", periods=50)
    swing_usi = np.sin(np.linspace(0, 10, 50))  # Example short-term USI
    trend_usi = np.cos(np.linspace(0, 5, 50))   # Example long-term USI

    # Call the VisualizationAgent
    VisualizationAgent.plot_swing_vs_trend_comparison(dates, swing_usi, trend_usi)
