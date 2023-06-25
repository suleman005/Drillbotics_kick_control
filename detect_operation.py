from dwis import *
import pandas as pd
import time

def detect_operation():

    selected_parameters = [
        pit_volume,
        Annulus_Pressure,
        bit_depth,
        FlowRateIn,
        FlowRateOut,
        SPP,
        WOB,
        BOP_ChokePressure
    ]

    # Create an empty DataFrame
    df = pd.DataFrame()

    counter = 0
    start_time = time.time()
    while time.time() - start_time < 13:
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
        #print(df.tail(1))
        counter += 1
        # Wait for 1 second before reading the next set of data
        time.sleep(0.5)

    previous_value = df.iloc[-11]
    current_value = df.iloc[-1]
    
    previous_bit_depth = previous_value['bit_depth']
    current_bit_depth = current_value['bit_depth']

    previous_WOB = previous_value['WOB']
    current_WOB = current_value['WOB']

    current_flow_rate_in = current_value['FlowRateIn']
    current_flow_rate_out = current_value['FlowRateOut']

    previous_annulus_pressure = previous_value['Annulus_Pressure']
    current_annulus_pressure = current_value['Annulus_Pressure']
    
    previous_choke_pressure = previous_value['BOP_ChokePressure']
    current_choke_pressure = current_value['BOP_ChokePressure']

    previous_pit_volume = previous_value['pit_volume']
    current_pit_volume = current_value['pit_volume']

    previous_spp = previous_value['SPP']
    current_spp = current_value['SPP']

    if (current_annulus_pressure > 0 or current_choke_pressure > 0) and current_spp == 0:
        return "Well Control - Shut-in"

    elif current_flow_rate_in == 0 and current_flow_rate_out == 0 and abs(current_pit_volume - previous_pit_volume) < 500:
        return "Well Control - Shut-in"
    else:
        if current_WOB > 0 and current_bit_depth > previous_bit_depth:
            return "Drilling"
        elif current_WOB == 0 and current_bit_depth > previous_bit_depth:
            return "Tripping In"
        elif current_WOB == 0 and current_bit_depth < previous_bit_depth:
            return "Tripping Out"
        elif current_WOB == 0 and current_bit_depth == previous_bit_depth and current_flow_rate_in > 0 and current_flow_rate_out > 0:
            return "Mud Circulation"    
        elif current_WOB != 0 and current_bit_depth == previous_bit_depth:
            return "Stuck"
        else:
            return "Unknown"

while True:
    x= detect_operation()

    print(x)