import plotly.graph_objects as go
import numpy as np
import pandas as pd

class VisualizationAgent:
    @staticmethod
    def plot_usi_with_trends(dates, usi_values):
        """
        Plot USI graph with zero crossings and trend lines using Plotly.

        Args:
            dates (list or np.array): List of dates corresponding to the USI values.
            usi_values (list or np.array): Calculated USI values.
        """
        # Convert dates to a pandas Series if necessary
        if not isinstance(dates, pd.Series):
            dates = pd.Series(dates)
        
        # Find zero crossings
        zero_crossings = np.where(np.diff(np.sign(usi_values)))[0]

        # Create the main USI line plot
        fig = go.Figure()

        # Add USI line
        fig.add_trace(go.Scatter(
            x=dates, 
            y=usi_values, 
            mode='lines', 
            name='USI',
            line=dict(color='blue', width=2)
        ))

        # Highlight zero crossings with markers
        fig.add_trace(go.Scatter(
            x=dates.iloc[zero_crossings], 
            y=usi_values[zero_crossings], 
            mode='markers',
            name='Zero Crossings',
            marker=dict(color='red', size=8)
        ))

        # Add shaded regions for bullish and bearish trends
        fig.add_trace(go.Scatter(
            x=dates,
            y=[val if val > 0 else None for val in usi_values],
            mode='lines',
            fill='tozeroy',
            name='Bullish Trend',
            line=dict(color='green', width=0),
            opacity=0.3
        ))

        fig.add_trace(go.Scatter(
            x=dates,
            y=[val if val < 0 else None for val in usi_values],
            mode='lines',
            fill='tozeroy',
            name='Bearish Trend',
            line=dict(color='red', width=0),
            opacity=0.3
        ))

        # Add the zero line
        fig.add_trace(go.Scatter(
            x=dates,
            y=[0] * len(dates),
            mode='lines',
            name='Zero Line',
            line=dict(color='black', dash='dash')
        ))

        # Update layout
        fig.update_layout(
            title='Ultimate Strength Index (USI) with Zero Crossings and Trends',
            xaxis_title='Date',
            yaxis_title='USI Value',
            legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01),
            template='plotly_white'
        )

        # Show the plot
        fig.show()


# **Example Usage**
if __name__ == "__main__":
    # Sample data
    dates = pd.date_range(start="2023-01-01", periods=50)
    usi_values = np.sin(np.linspace(0, 10, 50))  # Example USI values (sinusoidal for demo)

    # Call the VisualizationAgent
    VisualizationAgent.plot_usi_with_trends(dates, usi_values)
