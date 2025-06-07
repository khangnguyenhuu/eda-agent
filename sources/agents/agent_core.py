import os
from langgraph.prebuilt import create_react_agent
os.environ["OPENAI_API_KEY"] = ''
def get_weather(city: str) -> str:  
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"

agent = create_react_agent(
    model="openai:o4-mini",  
    tools=[get_weather],  
    prompt="You are a helpful assistant"  
)

