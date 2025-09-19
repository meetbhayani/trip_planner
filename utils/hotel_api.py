# utils/hotel_api.py
import os
import requests

def get_hotel_prices(city_name: str):
    """
    Minimal hotel price fetcher. Uses RapidAPI booking endpoint if configured.
    Falls back to a default average nightly rate.
    """
    api_key = os.environ.get("BOOKING_API_KEY")
    if not api_key:
        return 100.0

    try:
        url = "https://booking-com15.p.rapidapi.com/api/v1/hotels/search"
        headers = {
            "X-RapidAPI-Key": api_key,
            "X-RapidAPI-Host": "booking-com15.p.rapidapi.com"
        }
        params = {
            "checkin_date": "2024-08-10",
            "checkout_date": "2024-08-11",
            "units": "metric",
            "order_by": "price",
            "locale": "en-us",
            "dest_type": "city",
            "name": city_name,
            "adults_number": 1
        }
        resp = requests.get(url, headers=headers, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        # find a typical nightly rate
        prices = []
        for r in data.get("result", [])[:5]:
            price = r.get("min_total_price")
            if price:
                try:
                    prices.append(float(price))
                except Exception:
                    continue
        if prices:
            return round(sum(prices)/len(prices), 2)
        return 100.0
    except Exception:
        return 100.0
