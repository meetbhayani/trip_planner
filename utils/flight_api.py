# utils/flight_api.py
import os
import requests

def get_flight_price(origin: str, destination: str, date: str, timeout: int = 10):
    """
    Minimal wrapper around a flight-quote endpoint.
    Replace RapidAPI endpoint & params with the ones you have access to.
    Returns a dict or a simple fallback structure if the API is not configured.
    """
    api_key = os.environ.get("SKYSCANNER_API_KEY")
    if not api_key:
        # Return sensible fallback structure expected by your code.
        return {"Quotes": [{"MinPrice": 300}], "Note": "No API key: using fallback price 300"}

    # Example: using a hypothetical RapidAPI flight endpoint (adjust to your actual one).
    try:
        url = "https://example-flight-api.p.rapidapi.com/getFlightPrices"
        headers = {
            "X-RapidAPI-Key": api_key,
            "X-RapidAPI-Host": "example-flight-api.p.rapidapi.com",
            "Accept": "application/json"
        }
        params = {"origin": origin, "destination": destination, "date": date, "adults": 1}
        resp = requests.get(url, headers=headers, params=params, timeout=timeout)
        resp.raise_for_status()
        data = resp.json()
        return data
    except Exception as e:
        # If API fails, return fallback
        return {"Quotes": [{"MinPrice": 300}], "Error": str(e)}
