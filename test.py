import dash
from dash.dependencies import Output, Input
from dash import dcc
from dash import html
import plotly.graph_objs as go
from plotly.subplots import make_subplots
from collections import deque
from connect_server import connect_read_server,connect_write_server

client_read = connect_read_server()
client_write = connect_write_server()

X = deque(maxlen=100)
X.append(1)

Y1 = deque(maxlen=100)
Y1.append(1)

Y2 = deque(maxlen=100)
Y2.append(1)

Y3 = deque(maxlen=100)
Y3.append(1)

app = dash.Dash(__name__)

app.layout = html.Div(
    [
        dcc.Graph(id='live-graph', animate=True),
        dcc.Interval(
            id='graph-update',
            interval=1000,
            n_intervals=0
        ),
    ]
)

@app.callback(
    Output('live-graph', 'figure'),
    [Input('graph-update', 'n_intervals')]
)
def update_graph_scatter(n):
    X.appendleft(X[0] - 1)
    bit_node = bit_node = client.get_node("ns=2;s=BitDepth")
    bit_value = bit_node.get_value()

    timestamp_node = client.get_node("ns=6;s=openLAB.BitDepth")
    timestamp = timestamp_node.get_value()
    Y1.append(bit_value)
    Y2.append(bit_value*2)
    Y3.append(bit_value*3)

    fig = make_subplots(rows=1, cols=3, shared_yaxes=True)

    fig.add_trace(
        go.Scatter(x=list(Y1), y=list(X), name='Plot 1', mode='lines+markers'),
        row=1, col=1
    )

    fig.add_trace(
        go.Scatter(x=list(Y2), y=list(X), name='Plot 2', mode='lines+markers'),
        row=1, col=2
    )

    fig.add_trace(
        go.Scatter(x=list(Y3), y=list(X), name='Plot 3', mode='lines+markers'),
        row=1, col=3
    )

    fig.update_xaxes(title_text='Bit Depth', row=1, col=1)
    fig.update_xaxes(title_text='Bit Depth', row=1, col=2)
    fig.update_xaxes(title_text='Bit Depth', row=1, col=3)

    fig.update_yaxes(title_text='Time', autorange='reversed')

    fig.update_layout(
        margin=dict(l=40, r=0, t=30, b=20),
    )

    return fig

if __name__ == '__main__':
    app.run_server()
