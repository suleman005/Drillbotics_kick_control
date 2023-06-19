from opcua import Client


def connect_read_server():
    """
    Connect to the OPC-UA server defined by the global OPC_SERVER_URL constant
    and return the client object."""

    OPC_SERVER_read = "opc.tcp://localhost:48030"

    client_read = Client(OPC_SERVER_read)
    client_read.connect()
    return client_read


def connect_write_server():
    """
    Connect to the OPC-UA server defined by the global OPC_SERVER_URL constant
    and return the client object."""

    OPC_SERVER_Write = "opc.tcp://localhost:48031"

    client_write = Client(OPC_SERVER_Write)
    client_write.connect()
    return client_write
