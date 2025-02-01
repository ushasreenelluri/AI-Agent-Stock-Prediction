import pandas as pd

class GannHiLoActivatorIndicator:
    def __init__(self, smoothing: float = None):
        """
        Initialize the Gann Hi-Lo Activator Indicator.

        :param smoothing: Optional smoothing factor (alpha) for exponential smoothing.
                          Should be a float between 0 and 1 (e.g., 0.2). If set to None, no smoothing is applied.
        """
        if smoothing is not None:
            if not (0 < smoothing < 1):
                raise ValueError("Smoothing factor must be between 0 and 1.")
        self.smoothing = smoothing

    def calculate(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Calculate the Gann Hi-Lo Activator for each row in the given DataFrame.

        The algorithm is as follows:
          - For the first row, the activator is set as the average of 'High' and 'Low'.
          - For each subsequent row:
              * If the current 'Close' is greater than the previous activator, then
                    activator = min(current 'Low', previous activator)
              * Otherwise,
                    activator = max(current 'High', previous activator)

        Optionally, if a smoothing factor is provided, an exponential weighted moving average
        (EWMA) is applied to the activator series.

        :param data: DataFrame with at least the following columns: 'High', 'Low', 'Close'
        :return: The same DataFrame with an added column 'Gann_HiLo' containing the computed values.
        """
        # Check if required columns exist in the DataFrame
        required_columns = {"High", "Low", "Close"}
        if not required_columns.issubset(data.columns):
            raise ValueError(f"Input data must contain the following columns: {required_columns}")

        activator = []  # To store calculated activator values

        # Loop over each row to calculate the activator
        for i in range(len(data)):
            if i == 0:
                # Initialize with the average of the first row's High and Low
                initial_value = (data.iloc[i]["High"] + data.iloc[i]["Low"]) / 2.0
                activator.append(initial_value)
            else:
                previous_activator = activator[i - 1]
                current_close = data.iloc[i]["Close"]
                current_high = data.iloc[i]["High"]
                current_low = data.iloc[i]["Low"]

                if current_close > previous_activator:
                    current_activator = min(current_low, previous_activator)
                else:
                    current_activator = max(current_high, previous_activator)
                activator.append(current_activator)

        # Add the activator values to the DataFrame
        data["Gann_HiLo"] = activator

        # Apply exponential smoothing if requested
        if self.smoothing is not None:
            data["Gann_HiLo"] = data["Gann_HiLo"].ewm(alpha=self.smoothing, adjust=False).mean()

        return data

    def respond(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Convenience method to calculate and return the DataFrame updated with the Gann Hi-Lo Activator.

        :param data: DataFrame with market data.
        :return: Updated DataFrame with the 'Gann_HiLo' column.
        """
        return self.calculate(data)
