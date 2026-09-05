from langchain.tools import tool

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


@tool
def get_weather(city: str) -> str:
    """ Get the curent weather of the city
    
    Args:
        city : "name of the city"
    """

    weather_data = {
        "delhi" : "32 C, sunny",
        "mumbai" : "29 C, cloudy",
        "bangalore" : "24 C, rainy "
    }

    city = city.lower().strip()

    if city not in weather_data:
        raise ValueError(f"Weather data not available for {city}")

    return weather_data[city]