import plotly.graph_objs as go
from plotly.subplots import make_subplots
from opcua import Client
import time

# Connect to the OPC-UA server
url = "opc.tcp://localhost:48030"
client = Client(url)
client.connect()

# Get the "SPP" node from the server using its NodeId
bit_node = client.get_node("ns=6;s=openLAB.BitDepth")

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
