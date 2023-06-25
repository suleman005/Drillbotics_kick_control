import openlab
import matplotlib.pyplot as plt
import numpy as np
import time
import pandas as pd
import time

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression


def detect_future_kick(df, future_values):
    future_kick_columns = []

    # Exclude 'timeStep' from kick detection
    values_to_check = {name: value for name, value in future_values.items() if name != 'timeStep'}

    for name, value in values_to_check.items():
        avg_value = df[name][-RED_LINE_START_TIME:].mean()

        upper_threshold = avg_value * 1.05
        lower_threshold = avg_value * 0.95

        if value > upper_threshold or value < lower_threshold:
            print(f"Potential future kick detected in {name} at timeStep {len(df)}")
            future_kick_columns.append(name)

    return future_kick_columns
# Function to get data from simulation


    return {
        'SPP': sim.results.SPP[timeStep],
        'FlowRateOut': sim.results.FlowRateOut[timeStep],
        'HookLoad': sim.results.HookLoad[timeStep],
        'DownholePressure': sim.results.DownholePressure[timeStep] / 60000,
        'WOB': sim.results.WOB[timeStep],
        'FlowRateIn': sim.results.FlowRateIn[timeStep],
        'MainPitVolume': sim.results.MainPitVolume[timeStep]
    }
# Function to calculate slope and predict data
def calculate_slope_and_predict(df):
    if len(df) < N_STEPS:
        return None

    last_n_steps_df = df.iloc[-N_STEPS:]

    slopes = {col: (last_n_steps_df[col].values[1] - last_n_steps_df[col].values[0])
              for col in last_n_steps_df.columns}

    future_data = {col: np.arange(1, PREDICTION_STEPS + 1) * slope + last_n_steps_df[col].values[1]
                   for col, slope in slopes.items()}

    future_indices = np.arange(last_n_steps_df.index.values[1] + 1,
                               last_n_steps_df.index.values[1] + 1 + PREDICTION_STEPS)

    return pd.DataFrame(future_data, index=future_indices)
# Define your constants here
TAGS = ['SPP', 'FlowRateOut', 'HookLoad','DownholePressure','WOB', 'FlowRateIn','MainPitVolume']

START_TIME = 1
END_TIME = 500
RED_LINE_START_TIME = 100
PREDICTION_STEPS = 100
N_STEPS = 2
WINDOW_SIZE = 100

# Prepare dataframe
df = pd.DataFrame(columns=TAGS + ["timeStep"])

# Initialize the list of columns where a kick was detected in the previous time step
prev_kick_columns = []
# Prepare figure
fig, axs = plt.subplots(len(TAGS), 1, figsize=(16, 50))  # Change the height of the plots here

# Main loop
for timeStep in range(START_TIME, END_TIME + 1):
    # Clear axes
    for ax in axs:
        ax.clear()

    # Get data from sim
    values = get_sim_data(sim, timeStep)

    # Append new data to df
    df = df.append({**values, 'timeStep': timeStep}, ignore_index=True)

    # Train models and predict future values
    future_df = calculate_slope_and_predict(df)

    # Detect kicks
    kick_columns = detect_kick(df, values)

    # Detect future kicks if future_df is not None
    future_kick_columns = []
    if future_df is not None:
        # Future values will be the values at the end of the prediction line
        future_values = future_df.iloc[-1]
        future_kick_columns = detect_future_kick(df, future_values)

    # Plot data
    for i, (name, value) in enumerate(values.items()):
        ax = axs[i]
        ax.plot(df['timeStep'], df[name], label=f'original {name}')

        if future_df is not None and name in future_df.columns:
            ax.plot(future_df.index, future_df[name], label=f'predicted {name}')

        # Change xlim to always show the last WINDOW_SIZE timeSteps (plus the length of the prediction line) after reaching 100 timeSteps
        if timeStep > WINDOW_SIZE:
            ax.set_xlim([timeStep - WINDOW_SIZE, timeStep + PREDICTION_STEPS])

        # Plot the red lines after RED_LINE_START_TIME time steps
        if timeStep > RED_LINE_START_TIME:
            avg_value = df[name][-RED_LINE_START_TIME:].mean()
            ax.axhline(y=avg_value * 1.10, color='r', linestyle='--')  # 10% above the average
            ax.axhline(y=avg_value * 0.90, color='r', linestyle='--')  # 10% below the average

        ax.grid(True)  # Enable grid
        ax.legend()

        # Check for each column from the previous kick detection if the current value is within the threshold
        # Also check the same for future_kick_columns
        if name in kick_columns and name in future_kick_columns:
            ax.set_facecolor((1, 0.5, 0.5, 0.3))  # RGBA color for light, transparent red
        elif name in kick_columns or name in future_kick_columns:
            ax.set_facecolor((1, 0.8, 0.5, 0.3))  # RGBA color for light, transparent orange
        else:
            ax.set_facecolor('white')

    # Redraw the figure
    fig.canvas.draw()

    # Store the current kick columns for the next iteration
    prev_kick_columns = kick_columns

    # Redraw the figure
    fig.canvas.draw()

plt.show()