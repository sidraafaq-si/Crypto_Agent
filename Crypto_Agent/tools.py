# Safe import to avoid agents module error
try:
    from agents import function_tool
except ImportError:
    def function_tool(func):
        return func

import requests

@function_tool
def get_crypto_price(coin: str = "bitcoin", currency: str = "usd") -> str:
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin.lower()}&vs_currencies={currency.lower()}"

    try:
        response = requests.get(url, timeout=10)  # Timeout added for safety
        response.raise_for_status()  # Raise HTTPError if status != 200
        data = response.json()

        # Validate response structure
        if coin.lower() in data and currency.lower() in data[coin.lower()]:
            price = data[coin.lower()][currency.lower()]
            return f"{coin.capitalize()} ki current price in {currency.upper()} is: {price}"
        else:
            return "Coin ya currency ka naam galat hai. Dubara try kren."
    except requests.exceptions.RequestException as e:
        return f"Network error aaya: {str(e)}"
    except Exception as e:
        return f"Kuch error aaya: {str(e)}"


