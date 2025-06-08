import os
import json
import uuid
import chainlit as cl

from mcp import ClientSession
from mcp.client.sse import sse_client
from langchain_mcp_adapters.tools import load_mcp_tools

from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import InMemorySaver

from langchain_core.runnables import RunnableConfig
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage, ToolMessage
from langchain_core.messages.ai import AIMessage
import plotly.graph_objects as go

from sources.agents.agent_core import agent
from sources.agents.prompts_constants import SYSTEM_PROMPT
RECURSION_LIMIT = 100
MCP_HOST = os.environ.get("MCP_HOST")
checkpointer = InMemorySaver()

@cl.on_chat_start
async def start():
    config = RunnableConfig(
        recursion_limit = RECURSION_LIMIT,
        configurable = {
            "thread_id": str(uuid.uuid4()),
        },

    )
    cl.user_session.set("invoke_config", config)
    await cl.Message(content="Hello, how can I help you today?").send()

@cl.on_message
async def on_message(message: cl.Message):
    # Run the agent

    async with sse_client(f'{MCP_HOST}/sse') as stream:
        async with ClientSession(*stream) as session:
            await session.initialize()
            tools = await load_mcp_tools(session)
            agent = create_react_agent(
                # model="groq:meta-llama/llama-4-scout-17b-16e-instruct",
                model="groq:meta-llama/llama-4-maverick-17b-128e-instruct",
                # model="groq:gemma2-9b-it",
                tools=tools,  
                checkpointer=checkpointer
            )
            invoke_config = cl.user_session.get("invoke_config")
            initial_messages = [
                SystemMessage(content=SYSTEM_PROMPT),
                HumanMessage(content=message.content),
            ]

            inputs = {"messages": initial_messages}
            response = await agent.ainvoke(
                inputs,
                invoke_config
            )
            '''
            agent response content
            [HumanMessage(content="hello", additional_kwargs={}, response_metadata={}, id="1d33fc07-5070-4e84-b679-41f500458494"),
                AIMessage(content="Hello! How can I help you today?", 
                        additional_kwargs={
                        "refusal": None
                    }, 
                        response_metadata={
                        "token_usage": {
                            "completion_tokens": 27,
                            "prompt_tokens": 54,
                            "total_tokens": 81,
                            "completion_tokens_details": {
                                "accepted_prediction_tokens": 0,
                                "audio_tokens": 0,
                                "reasoning_tokens": 0,
                                "rejected_prediction_tokens": 0
                            },
                            "prompt_tokens_details": {
                                "audio_tokens": 0,
                                "cached_tokens": 0
                            }
                        },
                        "model_name": "o4-mini-2025-04-16",
                        "system_fingerprint": None,
                        "id": "chatcmpl-BfiMacwCTvn7gnvydhLmtmZSgKtxI",
                        "service_tier": "default",
                        "finish_reason": "stop",
                        "logprobs": None
                    }, id="run--da32def3-e954-42a0-9ef7-a585c0d72408-0", usage_metadata={
                        "input_tokens": 54,
                        "output_tokens": 27,
                        "total_tokens": 81,
                        "input_token_details": {
                            "audio": 0,
                            "cache_read": 0
                        },
                        "output_token_details": {
                            "audio": 0,
                            "reasoning": 0
                        }
                    })
                ]
            '''
            element = []
            response_content = "i do not know how to answer that"
            if isinstance(response["messages"][-1], AIMessage):
                response_content = response["messages"][-1].content
                if isinstance(response["messages"][-2], ToolMessage) or isinstance(response["messages"][-2], AIMessage):
                    tool_metadata = response["messages"][-2].content
                    data = json.loads(tool_metadata)   
                    fig = go.Figure(data=json.loads(data['figure']),
                                    layout_title_text="An example figure")
                    element = [cl.Plotly(figure=fig, display="inline")]
    
            await cl.Message(content=response_content, elements=element).send()

            # await cl.Message(content=response_content).send()



    # else:
    #     await cl.Message(content="I'm sorry, I don't know how to answer that.").send()


# import plotly.graph_objects as go
# import chainlit as cl


# @cl.on_chat_start
# async def start():
#     fig = go.Figure(
#         data=[go.Bar(y=[2, 1, 3])],
#         layout_title_text="An example figure",
#     )
#     elements = [cl.Plotly(name="chart", figure=fig, display="inline")]

#     await cl.Message(content="This message has a chart", elements=elements).send()