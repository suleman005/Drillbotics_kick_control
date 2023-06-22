import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.graph_objects as go


def dash_plot(selected_parameters, data):
    # Create the Dash application
    app = dash.Dash(__name__)

    # Create a figure object for each parameter
    figures = {}

    # Create the graph components and store their names
    graph_components = []

    for parameter in selected_parameters:
        parameter_name = parameter[0]
        figures[parameter_name] = go.Figure()

        # Create the graph component with parameter name
        graph_component = dcc.Graph(
            id=f"graph-{parameter_name}",
            figure=figures[parameter_name]
        )
        graph_components.append(
            html.Div(
                children=[
                    html.H2(f"Parameter: {parameter_name}"),
                    graph_component
                ]
            )
        )

    # Define the layout of the application
    app.layout = html.Div(
        children=[
            html.H1("Live Plot"),
            html.Div(id="graph-container", children=graph_components),
            dcc.Interval(
                id="interval-component",
                interval=10000,  # Update interval in milliseconds
                n_intervals=0
            )
        ]
    )

    # Define the callbacks to update each plot
    for parameter in selected_parameters:
        parameter_name = parameter[0]

        @app.callback(
            Output(f"graph-{parameter_name}", "figure"),
            [Input("interval-component", "n_intervals")]
        )
        def update_live_plot(n):
            # Get the figure for the parameter
            fig = figures[parameter_name]

            # Update the data in the figure
            fig.data[0].x = data["timestamp"]
            fig.data[0].y = data[parameter_name]

            # Update layout
            fig.update_layout(
                xaxis_title="Timestamp",
                yaxis_title="Value",
                title=f"Live Plot of {parameter_name}"
            )

            return fig

    # Run the Dash application
    app.run_server(debug=True, port=3050)


import pandas as pd
from datetime import datetime
import random
para = [
    ["parameter1", random.randint(1, 100)],
    ["parameter2", random.randint(1, 100)],
    ["parameter3", random.randint(1, 100)]
]

df = pd.DataFrame({
    "timestamp": [datetime.now()],
    "parameter1": [random.randint(1, 100)],
    "parameter2": [random.randint(1, 100)],
    "parameter3": [random.randint(1, 100)]
})

dash_plot(para, data=df)