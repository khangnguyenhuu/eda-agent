from typing import List
from .mcp_interface import PlotlyChart
from mcp.server.fastmcp import FastMCP
from .tools.pandas_tools.barchart_visualize import visualize_barchart as tool_visualize_barchart

# Create an MCP server
mcp = FastMCP(
    name="eda-agent",
    version="0.9.0",
    description="EDA Agent",
    author="Khangnh",
    author_email="nskhang1@gmail.com",
)

@mcp.tool(description="Visualize a bar chart using Plotly.")
async def visualize_barchart(categories: List[str], values: List[float], title: str = 'Bar Chart', x_title: str = 'Categories', y_title: str = 'Values') -> PlotlyChart:
    return tool_visualize_barchart(categories, values, title, x_title, y_title)

if __name__ == "__main__":
    mcp.run(transport="sse") # sse