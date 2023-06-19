from opcua import Client

# set up the client
client = Client("opc.tcp://localhost:48031")
client.connect()

# find the BOP node
bop_node = client.get_node("ns=2;s=BopChokeOpening")

# set the value to 0
bop_node.set_value(False)

# close the client
client.disconnect()
