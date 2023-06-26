import pandas as pd
import time
import matplotlib.pyplot as plt
from opcua import Client

# trend settings:
RED_LINE_START_TIME = 100  # red lines start after 100 seconds
PREDICTION_STEPS = 100  # how long to make the pred line
N_STEPS = 2  # how many steps the used to make the linear regression
WINDOW_SIZE = 100  # how many steps to make the avg from


# Fetch data from the OPC-UA server
def fetch_opcua_data(client, node_ids):
    values = {node_id: client.get_node(node_id).get_value() for node_id in node_ids}

    # Process values (e.g., convert units)

    return values


# Connect to the OPC-UA server
client_read = Client("opc.tcp://localhost:48030")
client_write = Client("opc.tcp://localhost:48031")
client_read.connect()
client_write.connect()

# Read NodeIds
node_ids = ["ns=6;s=openLAB.ActivePitDensity", "ns=6;s=openLAB.ActivePitTemperature", "ns=6;s=openLAB.ActivePitVolume",
            "ns=6;s=openLAB.AnnulusPressure", "ns=6;s=openLAB.BitDepth", "ns=6;s=openLAB.BopChokeOpening",
            "ns=6;s=openLAB.BopChokePressure", "ns=6;s=openLAB.ChokeOpening", "ns=6;s=openLAB.ChokePressure",
            "ns=6;s=openLAB.DownholeECD", "ns=6;s=openLAB.DownholePressure", "ns=6;s=openLAB.DownholePressure_WP",
            "ns=6;s=openLAB.FlowRateIn", "ns=6;s=openLAB.FlowRateOut", "ns=6;s=openLAB.GasFlowRateOut",
            "ns=6;s=openLAB.HookLoad", "ns=6;s=openLAB.HookPosition", "ns=6;s=openLAB.HookVelocity",
            "ns=6;s=openLAB.InstantaneousROP", "ns=6;s=openLAB.SPP", "ns=6;s=openLAB.SurfaceRPM",
            "ns=6;s=openLAB.SurfaceTorque", "ns=6;s=openLAB.TD", "ns=6;s=openLAB.WOB"]

# Write NodeIds
write_node_ids = ["ns=2;s=BOPOpeningSetPoint", "ns=2;s=ChokeOpeningSetPoint", "ns=6;s=openLAB.FlowRateInSetPoint",
                  "ns=6;s=openLAB.SurfaceRPMSetPoint", "ns=6;s=openLAB.TopOfStringVelocitySetPoint"]