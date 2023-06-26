from dwis import *
import pandas as pd
import time
from operations import *


def confirm_kick_loss(threshold):
    selected_parameters = [pit_volume, Annulus_Pressure]

    # Create an empty DataFrame
    df = pd.DataFrame()

    counter = 0

    while counter < 5:

        # Create a dictionary to store the row data
        row_data = {}

        # Get the current timestamp
        timestamp = pd.Timestamp.now()

        # Add the timestamp to the row data
        row_data["timestamp"] = timestamp

        # Iterate over the parameters and fetch their values
        for parameter in selected_parameters:
            name = parameter[0]
            value = eval(parameter[1]) if parameter[1] is not None else 0

            row_data[name] = value

        # Store row data in the DataFrame
        df = df.append(row_data, ignore_index=True)

        # Print the current values
        # print(df.tail(1))
        counter += 1

        # Wait for 2 second before reading the next set of data
        time.sleep(2)

    # Calculate the difference between consecutive pit_volume values
    df['pit_volume_diff'] = df['pit_volume'].diff()
    print(df['pit_volume_diff'])
    # Identify rows where the pit_volume_diff exceeds the threshold
    kick_rows = df[abs(df['pit_volume_diff']) > threshold]

    kick = 0
    loss = 0

    if not kick_rows.empty:
        # Kick detected

        if kick_rows['pit_volume_diff'].iloc[0] > 0:
            # Kick detected
            kick = 1
            loss = 0
            print("Kick confirmed at the following timesteps:")
        else:
            # Loss detected
            kick = 0
            loss = 1
            print("Loss confirmed at the following timesteps:")

        print(kick_rows)
        # Additional actions or analysis can be performed here

    else:
        # No kick detected
        kick = 0
        print("No kick or Loss detected.")

    return kick, loss
