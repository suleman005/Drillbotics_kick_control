from collections import deque
from opcua import Client
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def plot_parameters(selected_parameters):

    X = deque(maxlen=1000)
    X.append(1)

    Y = {}
    for parameter in selected_parameters:
        name = parameter[0]
        Y[name] = deque(maxlen=1000)
        Y[name].append(1)

    app = dash.Dash(__name__)

    app.layout = html.Div(
        [
            dcc.Graph(id='live-graph', animate=True),
            dcc.Interval(
                id='graph-update',
                interval=500,
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

        for parameter in selected_parameters:
            parameter_name = parameter[0]
            value = eval(parameter[1])
            Y[parameter_name].append(value)

        fig = make_subplots(rows=1, cols=len(selected_parameters), shared_yaxes=True)

        for i, parameter in enumerate(selected_parameters):
            parameter_name = parameter[0]
            fig.add_trace(
                go.Scatter(x=list(Y[parameter_name]), y=list(X), name=parameter_name, mode='lines+markers'),
                row=1, col=i+1
            )
            fig.update_xaxes(title_text=parameter_name, row=1, col=i+1)

        fig.update_yaxes(title_text='Time', autorange='reversed')

        fig.update_layout(
            margin=dict(l=40, r=0, t=30, b=20),
        )

        return fig

    if __name__ == '__main__':
        app.run_server(debug=False, port=3050)


from dwis import *
selected_parameters = [
    pit_volume,
    bit_depth,
    BOP_ChokeOpening,
    BOP_ChokePressure,
    MPD_ChokeOpening,
    MPD_ChokePressure,
    ECD_Downhole,
    Pressure_Downhole,
    FlowRateIn,
    FlowRateOut
]

plot_parameters(selected_parameters)
