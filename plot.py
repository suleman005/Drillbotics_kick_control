import plotly.graph_objs as go
from plotly.subplots import make_subplots

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