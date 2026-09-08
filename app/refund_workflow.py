from langgraph.graph import StateGraph, START, END

from typing import TypedDict

from app.refund_agent import refund_agent

class RefundState(TypedDict):
    order_id : str
    amount : float
    reason : str
    eligible : bool
    status : str
    preparation : str


def check_eligibility(state : RefundState):
    eligible = (
        state["amount"] > 0
        and state["amount"] <= 1000
    )

    return {
        "eligible" : eligible
    }

def route_refund(state : RefundState):
    if state["eligible"]:
        return "prepare"

    return "reject"

def prepare_refund(state : RefundState):
    result = refund_agent.invoke({
        "messages" : [
            {
                "role" : "user",
                "content" : (
                    f"Prepare a refund for order {state['order_id']}. "
                    f"Amount: ₹{state['amount']}. "
                    f"Reason: {state['reason']}."
                )
            }
        ]
    })

    return {
        "status" : "pending_approval",
        "preparation" : result["messages"][-1].text
    }


def reject_refund(state : RefundState):
    return {
        "status" : "rejected",
        "preparation" : "Refund is not eligible"
    }


builder = StateGraph(RefundState)

builder.add_node("check_eligibility", check_eligibility)
builder.add_node("prepare", prepare_refund)
builder.add_node("reject", reject_refund)

builder.add_edge(START,"check_eligibility")
builder.add_conditional_edges(
    "check_eligibility",
    route_refund,
    {
        "prepare" : "prepare",
        "reject" : "reject"
    },
)

builder.add_edge("prepare",END)
builder.add_edge("reject", END)

graph = builder.compile()

if __name__ == "__main__":

    print("\n--- Eligible refund ---")

    result = graph.invoke({
        "order_id": "O-1009",
        "amount": 500,
        "reason": "Damaged product",
        "eligible": False,
        "status": "new",
    })

    print(result)


    print("\n--- Ineligible refund ---")

    result = graph.invoke({
        "order_id": "O-1010",
        "amount": 1500,
        "reason": "Damaged product",
        "eligible": False,
        "status": "new",
    })

    print(result)