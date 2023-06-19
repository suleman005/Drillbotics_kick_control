from opcua import Client

# Define the URL of the OPC-UA server as a constant
OPC_SERVER_URL = "opc.tcp://localhost:48030"

def connect_to_server():
    """
    Connect to the OPC-UA server defined by the global OPC_SERVER_URL constant
    and return the client object.

    Returns:
        opcua.Client: The OPC-UA client object for the connected server.
    """
    client = Client(OPC_SERVER_URL)
    client.connect()
    return client
