from pydantic import BaseModel
from typing import Any
from plotly.graph_objects import Figure


class PlotlyChart(BaseModel):
    figure: Any

    class Config:
        arbitrary_types_allowed = True