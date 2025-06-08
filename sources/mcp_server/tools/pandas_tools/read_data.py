import pandas as pd
from io import StringIO
from typing import List
import json

import plotly.express as px
import plotly.graph_objects as go

from sources.mcp_server.mcp_interface import PlotlyChart

def tool_read_csv(csv_file: str) -> json:
    """
    """
    # Create a bar chart
    data = pd.read_csv(StringIO(csv_file))
    return data
    