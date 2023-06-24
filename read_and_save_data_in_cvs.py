from dwis import *
import pandas as pd
import time
from plot_para import plot_parameters

selected_parameters = [
    pit_density,
    pit_temperature,
    pit_volume,
    Annulus_Pressure,
    bit_depth,
    BOP_ChokeOpening,
    BOP_ChokePressure,
    MPD_ChokeOpening,
    MPD_ChokePressure,
    ECD_Downhole,
    Pressure_Downhole,
    Pressure_Downhole_WP,
    FLowRateIn,
    FLowRateOut,
    FLowRateOut_Gas,
    HookLoad,
    HookPosition,
    HookVelocity,
    ROP_Inst,
    SPP,
    RPM_Surf,
    Torque_Surf,
    TD,
    WOB
]



plot_parameters(selected_parameters)

# Create an empty DataFrame
df = pd.DataFrame()

counter = 0
start_time = time.time()
while time.time() - start_time < 10:
    # Create a dictionary to store the row data
    row_data = {}

    # Get the current timestamp
    timestamp = pd.Timestamp.now()

    # Add the timestamp to the row data
    row_data["timestamp"] = timestamp

    # Iterate over the parameters and fetch their values
    for parameter in selected_parameters:
        name = parameter[0]
        value = parameter[1]

        row_data[name] = value

    # Store row data in the DataFrame
    df = df.append(row_data, ignore_index=True)

    # Print the current values
    print(df.tail(1))
    counter +=1
    # Wait for 1 second before reading the next set of data
    time.sleep(1)

