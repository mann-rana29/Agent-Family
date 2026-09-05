from langchain.tools import tool
import httpx
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type



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