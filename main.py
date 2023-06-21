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



pit_density = ["pit_density", round(client_read.get_node(ID_PitDensity).get_value() / 1000, 2)]# Convert from Kg/m^3 to sg
pit_temperature = ["pit_temperature", round(client_read.get_node(ID_PitTemperature).get_value()-273.15,1)]
pit_volume = ["pit_volume", round(client_read.get_node(ID_PitVolume).get_value()*1000,1)] #convert from cubic meters to litres
#Why are we getting 4 values?????
Annulus_Pressure = ["Annulus_Pressure", round(client_read.get_node(ID_AnnulusPressure).get_value()[0] / 100000, 1)]  # Pascals to bars
bit_depth = ["bit_depth", round(client_read.get_node(ID_BitDepth).get_value(), 1)]
BOP_ChokeOpening = ["BOP_ChokeOpening", client_read.get_node(ID_BOPChokeOpening).get_value()]
BOP_ChokePressure = ["BOP_ChokePressure", round(client_read.get_node(ID_BOPChokePressure).get_value() / 100000, 1)]
MPD_ChokeOpening = ["MPD_ChokeOpening", client_read.get_node(ID_MPDChokeOpening).get_value()]
MPD_ChokePressure = ["MPD_ChokePressure", round(client_read.get_node(ID_MPDChokePressure).get_value() / 100000, 1)]
ECD_Downhole = ["ECD_Downhole", round(client_read.get_node(ID_ECDDownhole).get_value() / 1000, 2)]
Pressure_Downhole = ["Pressure_Downhole", round(client_read.get_node(ID_PressureDownhole).get_value() / 100000, 1)]
Pressure_Downhole_WP = ["Pressure_Downhole_WP", round(client_read.get_node(ID_PressureDownhole_WP).get_value() / 100000, 1)]
FLowRateIn = ["FLowRateIn", round(client_read.get_node(ID_FLowRateIn).get_value() * 60000, 1)]
FLowRateOut = ["FLowRateOut", round(client_read.get_node(ID_FLowRateOut).get_value() * 60000, 1)]
FLowRateOut_Gas = ["FLowRateOut_Gas", round(client_read.get_node(ID_FLowRateOut_Gas).get_value() * 60000, 1)]
HookLoad = ["HookLoad", round(client_read.get_node(ID_HookLoad).get_value() / 1000, 1)]
HookPosition = ["HookPosition", client_read.get_node(ID_HookPosition).get_value()]
HookVelocity = ["HookVelocity", client_read.get_node(ID_HookVelocity).get_value()]
ROP_Inst = ["ROP_Inst", round(client_read.get_node(ID_ROPInst).get_value() * 3600, 1)]
SPP = ["SPP", round(client_read.get_node(ID_SPP).get_value() / 100000, 1)]
RPM_Surf = ["RPM_Surf", round(client_read.get_node(ID_RPMSurf).get_value() * 60, 1)]
Torque_Surf = ["Torque_Surf", round(client_read.get_node(ID_TorqueSurf).get_value() / 1000, 1)]
TD = ["TD", round(client_read.get_node(ID_TD).get_value(), 1)]
WOB = ["WOB", round(client_read.get_node(ID_WOB).get_value() / 1000, 1)]


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

# Create an empty DataFrame
df = pd.DataFrame()
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

    # Wait for 1 second before reading the next set of data
    time.sleep(1)


import plotly.graph_objs as go
from plotly.subplots import make_subplots
import pandas as pd

# Function to plot selected parameters
def plot_parameters(df):
    # Create subplot grid based on the number of selected parameters
    num_params = len(df.columns) - 1  # Exclude the timestamp column
    fig = make_subplots(rows=num_params, cols=1, shared_xaxes=True)

    # Iterate over the selected parameters
    for i, col in enumerate(df.columns[1:]):  # Exclude the timestamp column
        # Create a scatter plot for each parameter
        fig.add_trace(
            go.Scatter(
                x=df['timestamp'],
                y=df[col],
                name=col
            ),
            row=i + 1, col=1
        )

    # Update layout and display the figure
    fig.update_layout(height=600*num_params, showlegend=True)
    fig.show()

# Function to update plots when DataFrame is updated
def update_plots(df, fig):
    # Iterate over the selected parameters
    for i, col in enumerate(df.columns[1:]):  # Exclude the timestamp column
        # Update the y-axis data for each scatter plot
        fig.data[i].y = df[col]

    # Redraw the figure
    fig.show()


# Example usage
df = pd.DataFrame({'timestamp': [], 'param1': [], 'param2': []})  # Replace with your actual DataFrame

# Initial plot
plot_parameters(df)

# Update DataFrame and plots
df = df.append({'timestamp': pd.Timestamp.now(), 'param1': 1, 'param2': 2}, ignore_index=True)
update_plots(df, fig)
