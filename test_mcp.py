from mcp import ClientSession
import json
from mcp.client.sse import sse_client
import plotly.io as pio

async def check():
    async with sse_client("http://localhost:8000/sse") as stream:
        async with ClientSession(*stream) as session:
            await session.initialize()
            # tools = await session.list_tools()
            # print(tools)
            # for tool in tools.tools:
                # print(tool.name)
            response = await session.call_tool("get_weather", arguments={"location": "NY"})
            print(response)
            # response = await session.call_tool("visualize_barchart", arguments={
            #     "categories": ["A", "B", "C"],
            #     "values": [1, 2, 3]
            # })
            # figure_json = json.loads(response.content[0].text)["figure"]
            # figure = pio.from_json(figure_json)
            # pio.write_image(figure, 'plot.jpg')
            # response.plot.to_image(format="png")
            # print(response)

import asyncio
asyncio.run(check())