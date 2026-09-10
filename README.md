# Agent Family

A production-oriented Agentic AI learning project built with **LangChain, LangGraph, Gemini, and Pydantic**.

This project follows a 14-day **"1 Agent a Day"** progression focused on building production-grade agent systems rather than simple chatbot demos.

---

## Tech Stack

- Python 3.10+
- LangChain
- LangGraph
- Google Gemini
- Pydantic
- python-dotenv
- Tenacity
- HTTPX

---

## Project Goals

The project progressively implements:

- Typed tools
- Input validation
- Tool error handling
- Timeouts and retries
- Runtime authentication context
- Tenant isolation
- Short-term thread memory
- Long-term user memory
- Bounded semantic memory retrieval
- Memory correction and deletion
- Deterministic LangGraph workflows
- Human-in-the-loop approval
- PII and prompt-injection guardrails
- Structured Pydantic output
- Tool retry behavior
- Observability and audit logging
- Final production-style agent architecture

---

# Project Structure

```text
agent-family/
│
├── .venv/
│
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── main.py
│   ├── tools.py
│   ├── context.py
│   ├── services.py
│   ├── refund_workflow.py
│   ├── guardrails.py
│   ├── guarded_agent.py
│   └── schemas.py
│   └── structured_agent.py
│
├── tests/
│
├── .env
├── .gitignore
├── pyproject.toml
└── README.md