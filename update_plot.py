import plotly.graph_objs as go
from plotly.subplots import make_subplots

def update_plots(df, fig):
    # Iterate over the selected parameters
    for i, col in enumerate(df.columns[1:]):  # Exclude the timestamp column
        # Update the y-axis data for each scatter plot
        fig.data[i].y = df[col]

    # Redraw the figure
    fig.show()