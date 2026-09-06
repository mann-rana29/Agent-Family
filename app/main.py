from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_agent
from langchain.messages import ToolMessage
from langchain.agents.middleware import wrap_tool_call

from langgraph.checkpoint.memory import InMemorySaver
from langgraph.store.memory import InMemoryStore

from app.config import GEMINI_API_KEY
from app.context import RequestContext
from app.tools import get_current_customer,search_memories , get_preference, save_preference, calculate_total, celsius_to_farenheit, get_weather

@wrap_tool_call
def handle_tool_errors(request, handler):
    try: 
        return handler(request) #this means try to execute the tool normally
    except ValueError as exc:
        return ToolMessage(
            content=f"Invalid tool input: {exc}",
            tool_call_id = request.tool_call["id"]
        )

store = InMemoryStore()    
checkpointer = InMemorySaver()

model = ChatGoogleGenerativeAI(
    model="gemini-3.1-flash-lite",
    api_key=GEMINI_API_KEY
)

tools = [
    calculate_total,
    celsius_to_farenheit,
    get_weather,
    get_current_customer,
    save_preference,
    get_preference,
    search_memories
]

config = {
    "configurable" : {
        "thread_id" : "thread-123"
    }
}

agent = create_agent(
    model = model,
    tools = tools,
    middleware=[handle_tool_errors],
    store=store,
    checkpointer=checkpointer
)

context = RequestContext(
    user_id="user_123",
    tenant_id="tenant_abc",
    role="customer"
)

result = agent.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": ( "I like short answers", "I use python for backend", "i am looking for ai jobs"),
            }
        ]
    },
    context=context, config=config,
)

print(result["messages"][-1].text)

result = agent.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": "What job am i looking for?",
            }
        ]
    },
    context=context, config=config,
)

print(result["messages"][-1].text)