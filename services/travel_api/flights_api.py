import requests
from typing import List, Dict, Optional
from utils.config import get_config

class FlightsAPI:
    """
    Client for flight search API. Returns a list of normalized flight options.
    """
    def __init__(self, api_key: str = None):
        cfg = get_config()
        self.api_key = api_key or cfg.FLIGHTS_API_KEY
        self.base_url = cfg.FLIGHTS_API_URL 
        self.timeout = 10

    def search(
        self,
        origin: str,
        destination: str,
        start_date: str,
        end_date: str,
        budget: Optional[float] = None
    ) -> List[Dict]:
        
        params = {
            "origin": origin,
            "destination": destination,
            "depart_date": start_date,
            "return_date": end_date,
            "limit": 10
        }
        headers = {"Authorization": f"Bearer {self.api_key}"}
        resp = requests.get(self.base_url, params=params, headers=headers, timeout=self.timeout)
        resp.raise_for_status()
        data = resp.json().get("data", [])

        results = []
        for item in data:
            price = float(item.get("price", 0))
            if budget and price > budget:
                continue
            results.append({
                "airline": item.get("airline_name"),
                "flight_number": item.get("flight_number"),
                "departure": item.get("departure_time"),
                "arrival": item.get("arrival_time"),
                "price": price,
                "currency": item.get("currency", "USD"),
            })
        return results
