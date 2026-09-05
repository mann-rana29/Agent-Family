from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_agent
from langchain.messages import ToolMessage
from langchain.agents.middleware import wrap_tool_call

from app.config import GEMINI_API_KEY
from app.tools import calculate_total, celsius_to_farenheit, get_weather

@wrap_tool_call
def handle_tool_errors(request, handler):
    try: 
        return handler(request) #this means try to execute the tool normally
    except ValueError as exc:
        return ToolMessage(
            content=f"Invalid tool input: {exc}",
            tool_call_id = request.tool_call["id"]
        )
    

model = ChatGoogleGenerativeAI(
    model="gemini-3.8-flash",
    api_key=GEMINI_API_KEY
)

tools = [
    calculate_total,
    celsius_to_farenheit,
    get_weather
]

agent = create_agent(
    model = model,
    tools = tools,
    middleware=[handle_tool_errors]
)

result = agent.invoke({
    "messages" : [
        {
            "role" : "user",
            "content" : "What is the weather in Paris and what is 45 celsius in farenheit?"
        }
    ]
})

print(result["messages"][-1].text)