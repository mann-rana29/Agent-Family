from langchain.agents import create_agent
from langchain_google_genai import ChatGoogleGenerativeAI

from app.config import GEMINI_API_KEY
from app.schemas import SupportResponse

model = ChatGoogleGenerativeAI(
    model="gemini-3.1-flash-lite",
    api_key=GEMINI_API_KEY,
    temperature=0,
)

agent = create_agent(
    model = model,
    tools = [],
    response_format = SupportResponse
)

if __name__ == "__main__":
    result = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": (
                        "My order O-1021 has arrived successfully. "
                        "Tell me the result."
                    ),
                }
            ]
        }
    )

    response = result["structured_response"]

    print("Structured response:")
    print(response)

    print("\nType:")
    print(type(response))

    print("\nResolution:")
    print(response.resolution)

    print("\nStatus:")
    print(response.status)

    print("\nOrder IDs:")
    print(response.cited_order_ids)