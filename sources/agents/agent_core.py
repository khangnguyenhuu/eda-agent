import json
import os
import asyncio

from dotenv import load_dotenv

from mcp import ClientSession
from mcp.client.sse import sse_client

from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import InMemorySaver

from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_mcp_adapters.tools import load_mcp_tools

from .prompts_constants import SYSTEM_PROMPT
load_dotenv()
os.environ["OPENAI_API_KEY"] = os.environ.get("OPENAI_API_KEY")
os.environ["GROQ_API_KEY"] = os.environ.get("GROQ_API_KEY")
MCP_HOST = os.environ.get("MCP_HOST")

checkpointer = InMemorySaver()
print(f'{MCP_HOST}/sse')

async def get_mcp_tools():
    tools = []
    async with sse_client(f'{MCP_HOST}/sse') as stream:
        async with ClientSession(*stream) as session:
            await session.initialize()
            tools = await load_mcp_tools(session)
    return tools

agent = create_react_agent(
    model="groq:qwen-qwq-32b",
    tools=asyncio.run(get_mcp_tools()),  
    checkpointer=checkpointer,
    prompt=SYSTEM_PROMPT
)

