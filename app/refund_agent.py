from langchain.agents import create_agent
from langchain_google_genai import ChatGoogleGenerativeAI

from app.config import GEMINI_API_KEY
from app.tools import prepare_refund

model = ChatGoogleGenerativeAI(
    model="gemini-3.1-flash-lite",
    google_api_key=GEMINI_API_KEY
)

refund_agent = create_agent(
    model= model,
    tools = [prepare_refund]
)