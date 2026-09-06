from langchain.tools import tool, ToolRuntime
import httpx
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from app.context import RequestContext
from app.services import get_customer


@tool
def calculate_total(price : float, quantity : int) -> float:
    """Calculate the total price for a quantity of items.
    
    Args:
        price: Unit price..
        quantity : Number of units.
    
    """

    if price < 0:
        raise ValueError("price cannot be less than 0")

    if quantity < 1:
        raise ValueError("quantity must be at least 1")

    return round(price*quantity, 2)


@tool
def celsius_to_farenheit(celsius : float) -> float:
    """Convert a temperature from Celsius to Fahrenheit.

    Args:
        celsius : Temperature in degree Celsius.
    
    """

    return round((celsius * 9/5) + 32,2)

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(
        multiplier=0.25,
        min=0.25,
        max =2 
    ),
    retry= retry_if_exception_type(
        (httpx.ConnectError, httpx.ReadTimeout)
    ),
    reraise=True
)
def _fetch_weather(city: str) -> str:
    url = "https://httpbin.org/delay/10"

    with httpx.Client(timeout=5.0) as client:
        response = client.get(url)

    response.raise_for_status()

    return f"Weather lookup completed for {city}"

@tool
def get_weather(city: str) -> str:
    """ Get the curent weather of the city
    
    Args:
        city : "name of the city"
    """

    city = city.lower().strip()

    return _fetch_weather(city)


@tool
def get_current_customer(runtime : ToolRuntime[RequestContext]) -> dict:
    """Return the authenticated customer's profile"""

    user_id = runtime.context.user_id
    tenant_id = runtime.context.tenant_id

    return get_customer(user_id, tenant_id)

@tool
def save_preference(key : str, value : str, runtime : ToolRuntime[RequestContext]) -> str:
    """Save a user preference to long term memory"""

    namespace = ("users", runtime.context.user_id)

    runtime.store.put(
        namespace,
        key,
        {"value" : value}
    )

    return f"Saved preferences : {key} = {value}"

@tool
def get_preference(key: str, runtime : ToolRuntime[RequestContext] ) -> str:
    """Retrieve a saved user preference"""

    namespace = ("users", runtime.context.user_id)

    memory = runtime.store.get(namespace, key)

    if memory is None:
        return "No preference found"

    return memory.value["value"]

@tool
def search_memories(
    query: str,
    runtime : ToolRuntime[RequestContext]
) -> str:
    """Search the user's long term memories for relevant information"""

    namespace = ("users", runtime.context.user_id)

    memories = runtime.store.search(
        namespace,
        query=query,
        limit=5
    )

    if not memories:
        return "No relevant memories found"

    results = []

    for memory in memories:
        results.append(str(memory.value))

    return "\n".join(results)

@tool
def delete_preference(key :str, runtime : ToolRuntime[RequestContext])-> str:
    """Delete a saved user preference from long term memory"""

    namespace = ("users", runtime.context.user_id)

    runtime.store.delete(
        namespace,
        key
    )

    return f"Forgot preference : {key}"