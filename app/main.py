from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_agent

from app.config import GEMINI_API_KEY
from app.tools import calculate_total, celsius_to_farenheit

model = ChatGoogleGenerativeAI(
    model="gemini-3.8-flash",
    api_key=GEMINI_API_KEY
)

tools = [
    calculate_total,
    celsius_to_farenheit
]

agent = create_agent(
    model = model,
    tools = tools
)

result = agent.invoke(
    {
        "messages" : [
            {
                "role" : "user",
                "content" : "What is the total price if an item costs 49.99 and I buy 3?"
            }
        ]
    }
)


print(result["messages"][-1].text)