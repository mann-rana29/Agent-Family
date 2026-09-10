from langgraph.graph import StateGraph, START, END
from langgraph.types import interrupt, Command
from langgraph.checkpoint.memory import InMemorySaver

from typing import TypedDict

from app.refund_agent import refund_agent

class RefundState(TypedDict):
    order_id : str
    amount : float
    reason : str
    eligible : bool
    status : str
    approval_status : str


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

# def prepare_refund(state : RefundState):
    # result = refund_agent.invoke({
    #     "messages" : [
    #         {
    #             "role" : "user",
    #             "content" : (
    #                 f"Prepare a refund for order {state['order_id']}. "
    #                 f"Amount: ₹{state['amount']}. "
    #                 f"Reason: {state['reason']}."
    #             )
    #         }
    #     ]
    # })

    # return {
    #     "status" : "pending_approval",
    #     "preparation" : result["messages"][-1].text
    # }

def prepare_refund(state : RefundState):
    print("Preparing Refund")

    return {
        "status" : "pending_approval"
    }


def request_approval(state : RefundState):
    decision = interrupt({
        "action" : "refund_order",
        "order_id" : state["order_id"],
        "amount" : state["amount"],
        "reason" : state["reason"],
        "question" : "Approve this refund?"
    })

    if decision.get("approved") is True:
        return {
            "approval_status" : "approved"
        }
    
    return {
        "approval_status" : "rejected"
    }

def route_after_approval(state: RefundState):
    if state["approval_status"] == "approved":
        return "commit"

    return "reject"

def commit_refund(state : RefundState):
    print("Committing refund...")

    return {
        "status" : "refunded"
    }

def reject_refund(state : RefundState):
    return {
        "status" : "rejected",
    }


builder = StateGraph(RefundState)

builder.add_node("check_eligibility", check_eligibility)
builder.add_node("prepare", prepare_refund)
builder.add_node("approval",request_approval)
builder.add_node("commit", commit_refund) 
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
builder.add_edge("prepare","approval")
builder.add_conditional_edges(
    "approval", 
    route_after_approval, 
    {
        "commit" : "commit",
        "reject" : "reject"
    }
)
builder.add_edge("commit",END)
builder.add_edge("reject", END)

checkpointer = InMemorySaver()

graph = builder.compile(
    checkpointer=checkpointer
)

if __name__ == "__main__":

    config = {
        "configurable": {
            "thread_id": "refund-1009"
        }
    }

    result = graph.invoke(
        {
            "order_id": "O-1009",
            "amount": 500,
            "reason": "Damaged product",
            "eligible": False,
            "status": "new",
            "approval_status": "",
        },
        config=config,
    )

    print("\nWorkflow paused.")
    print(result)


    result = graph.invoke(
        Command(
            resume={
                "approved": False
            }
        ),
        config=config,
    )

    print("\nWorkflow resumed.")
    print(result)