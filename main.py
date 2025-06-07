import chainlit as cl
from langchain_core.messages.ai import AIMessage
from sources.agents.agent_core import agent

@cl.on_chat_start
async def start():
    await cl.Message(content="Hello, how can I help you today?").send()


@cl.on_message
async def on_message(message: cl.Message):
    # Run the agent
    response = agent.invoke(
        {"messages": [{"role": "user", "content": f'{message.content}'}]}
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
    response_content = "i do not know how to answer that"
    if isinstance(response["messages"][-1], AIMessage):
        response_content = response["messages"][-1].content
    await cl.Message(content=response_content).send()
    # else:
    #     await cl.Message(content="I'm sorry, I don't know how to answer that.").send()