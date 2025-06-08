import json
from typing import List

from .tools.pandas_tools.read_data import tool_read_csv
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
   
@mcp.tool(description="Read a CSV file and return the data as a JSON object.")
async def read_csv(csv_file: str) -> json:
    return tool_read_csv(csv_file)

@mcp.tool(description="Get all tools available in the MCP server.")
async def get_all_tools():
    tool_list = []
    async with sse_client("http://localhost:8000/sse") as stream:
        async with ClientSession(*stream) as session:
            await session.initialize()
            tools = await session.list_tools()
            for tool in tools.tools:
                tool_list.append(tool.name)
    return tool_list

@mcp.tool(description="Get weather for location")
async def get_weather(location: str) -> str:
    return "It's always sunny in New York"


if __name__ == "__main__":
    mcp.run(transport="sse") # sse