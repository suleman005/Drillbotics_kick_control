import plotly.graph_objs as go
from plotly.subplots import make_subplots
from opcua import Client
import pandas as pd
import time

# Connect to the OPC-UA server
client_read = Client("opc.tcp://localhost:48030")
client_write = Client("opc.tcp://localhost:48031")
client_read.connect()
client_write.connect()

# Read NodeIds

ID_PitDensity = "ns=6;s=openLAB.ActivePitDensity"
ID_PitTemperature = "ns=6;s=openLAB.ActivePitTemperature"
ID_PitVolume = "ns=6;s=openLAB.ActivePitVolume"
ID_AnnulusPressure = "ns=6;s=openLAB.AnnulusPressure"
ID_BitDepth = "ns=6;s=openLAB.BitDepth"
ID_BOPChokeOpening = "ns=6;s=openLAB.BopChokeOpening"
ID_BOPChokePressure = "ns=6;s=openLAB.BopChokePressure"
ID_MPDChokeOpening = "ns=6;s=openLAB.ChokeOpening"
ID_MPDChokePressure = "ns=6;s=openLAB.ChokePressure"
ID_ECDDownhole = "ns=6;s=openLAB.DownholeECD"
ID_PressureDownhole = "ns=6;s=openLAB.DownholePressure"
ID_PressureDownhole_WP = "ns=6;s=openLAB.DownholePressure_WP"
ID_FLowRateIn = "ns=6;s=openLAB.FlowRateIn"
ID_FLowRateOut = "ns=6;s=openLAB.FlowRateOut"
ID_FLowRateOut_Gas = "ns=6;s=openLAB.GasFlowRateOut"
ID_HookLoad = "ns=6;s=openLAB.HookLoad"
ID_HookPosition = "ns=6;s=openLAB.HookPosition"
ID_HookVelocity = "ns=6;s=openLAB.HookVelocity"
ID_ROPInst = "ns=6;s=openLAB.InstantaneousROP"
ID_SPP = "ns=6;s=openLAB.SPP"
ID_RPMSurf = "ns=6;s=openLAB.SurfaceRPM"
ID_TorqueSurf = "ns=6;s=openLAB.SurfaceTorque"
ID_TD = "ns=6;s=openLAB.TD"
ID_WOB = "ns=6;s=openLAB.WOB"

# Write NodeIds

WID_BOPOpening = "ns=2;s=BOPOpeningSetPoint" # 0 = close, 1 = open
WID_MPDOpening = "ns=2;s=ChokeOpeningSetPoint" # 0 = close, 1 = open
WID_FlowRateIn = "ns=6;s=openLAB.FlowRateInSetPoint" # m^3/sec
WID_RPM = "ns=6;s=openLAB.SurfaceRPMSetPoint" # Units = rev/sec
WID_StringVelocity = "ns=6;s=openLAB.TopOfStringVelocitySetPoint"




active_pit_density = client_read.get_node(ID_ActivePitDensity).get_value()
active_pit_density = round(active_pit_density / 1000, 2)  # Convert from Kg/m^3 to sg

bit_depth = client_read.get_node("ns=6;s=openLAB.BitDepth").get_value()
bit_depth = round(bit_depth, 1)

def read_and_save_data(node_ids, filter_ids, df):
    # Assuming the 'client_read' object is already defined

    # Read and save data continuously
    while True:
        for node_id in node_ids:
            if node_id in filter_ids:
                value = client_read.get_node(node_id).get_value()
                timestamp = time.time()
                new_row = {'Timestamp': timestamp, 'Node ID': node_id, 'Value': value}
                df = df.append(new_row, ignore_index=True)

        time.sleep(1)  # Wait for 1 second before the next iteration


# Create an empty DataFrame outside the function
df = pd.DataFrame(columns=['Timestamp', 'Node ID', 'Value'])

all_parameters = [
    ID_PitDensity, ID_PitTemperature, ID_PitVolume,
    ID_AnnulusPressure, ID_BitDepth, ID_BOPChokeOpening,
    ID_BOPChokePressure, ID_MPDChokeOpening, ID_MPDChokePressure,
    ID_ECDDownhole, ID_PressureDownhole, ID_PressureDownhole_WP,
    ID_FLowRateIn, ID_FLowRateOut, ID_FLowRateOut_Gas, ID_HookLoad,
    ID_HookPosition, ID_HookVelocity, ID_ROPInst, ID_SPP,
    ID_RPMSurf, ID_TorqueSurf, ID_TD, ID_WOB
]

# Write parameters you want to save in filter_ids
read_parameters = [
    ID_PitDensity, ID_PitTemperature, ID_PitVolume,
    ID_AnnulusPressure, ID_BitDepth, ID_BOPChokeOpening,
    ID_BOPChokePressure, ID_MPDChokeOpening, ID_MPDChokePressure,
    ID_ECDDownhole, ID_PressureDownhole, ID_PressureDownhole_WP,
    ID_FLowRateIn, ID_FLowRateOut, ID_FLowRateOut_Gas, ID_HookLoad,
    ID_HookPosition, ID_HookVelocity, ID_ROPInst, ID_SPP,
    ID_RPMSurf, ID_TorqueSurf, ID_TD, ID_WOB
]

# Call the function to continuously update the DataFrame
read_and_save_data(node_ids, filter_ids, df)

# Create a subplot grid with one row and one column
fig = make_subplots(rows=1, cols=1)

# Add an empty trace to the plot with the current SPP value as the initial point
bit_value = bit_node.get_value()
# convert the data
timestamp = time.time()
fig.add_trace(go.Scatter(x=[bit_value], y=[timestamp], mode="lines+markers"), row=1, col=1)

# Update the layout of the plot
fig.update_layout(title="Bit Depth", xaxis_title="SPP", yaxis_title="Time")

# Show the plot
fig.show()

# Continuously update the plot with new SPP values
while True:
    # Read the current value of the "SPP" node
    bit_value = bit_node.get_value()
    timestamp = time.time()

    # Append the new SPP value to the plot
    fig.add_trace(go.Scatter(x=[bit_value], y=[timestamp], mode="lines+markers"), row=1, col=1)

    # Update the plot
    fig.update_traces(mode="lines+markers")

    # Wait for a short amount of time before updating the plot again
    time.sleep(1)
