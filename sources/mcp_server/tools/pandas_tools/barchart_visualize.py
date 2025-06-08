import pandas as pd
from typing import List
from sources.mcp_server.mcp_interface import PlotlyChart
import plotly.express as px
import plotly.graph_objects as go
import logging

def visualize_barchart(categories: List[str], 
                    values: List[float], 
                    title: str = 'Bar Chart', 
                    x_title: str = 'Categories',
                    y_title: str = 'Values') -> PlotlyChart:
    """
    Visualize a bar chart using Plotly.

    Parameters:
    - categories: List of category names (x-axis).
    - values: List of corresponding values (y-axis).
    - title: Title of the chart.
    - x_title: Title for the x-axis.
    - y_title: Title for the y-axis.
    """
    # Create a bar chart
    fig = go.Figure(data=[go.Bar(x=categories, y=values)])

    # Customize layout
    fig.update_layout(
        title=title,
        xaxis_title=x_title,
        yaxis_title=y_title,
        template='plotly'
    )
    # Show the figure
    # return PlotlyChart(figure=fig.to_json())
    return fig.to_json()