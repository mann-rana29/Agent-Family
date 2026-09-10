from langchain.tools import tool

from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential
import httpx

@retry(
    stop= stop_after_attempt(3),
    wait= wait_exponential(
        multiplier=0.2,
        min=0.2,
        max=2
    ),
    retry = retry_if_exception_type((
        httpx.ConnectError,
        httpx.ReadTimeout
    )),
    reraise=True
)
def fetch_order_from_service(order_id : str) -> dict:
    """
    Simulate calling an external order service.
    """

    return {
        "order_id" : order_id,
        "status" : "delivered",
        "amount" : 500
    }

@tool
def get_order_with_retry(order_id: str) -> dict:
    """Get an order from the order service with retry handling"""
    # raise ValueError("Invalid order ID")
    if not order_id.strip():
        raise ValueError("order_id cannot be empty")

    return fetch_order_from_service(order_id)

if __name__ == "__main__":
    result = get_order_with_retry.invoke(
        {
            "order_id": "O-1021"
        }
    )

    print(result)