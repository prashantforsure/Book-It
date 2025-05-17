import requests
from typing import List, Dict, Tuple
from utils.config import get_config

class ActivitiesAPI:
    """
    Client for local activities/tours API. Returns a list of experiences.
    """
    def __init__(self, api_key: str = None):
        cfg = get_config()
        self.api_key = api_key or cfg.ACTIVITIES_API_KEY
        self.base_url = cfg.ACTIVITIES_API_URL  
        self.timeout = 10

    def search(
        self,
        location: str,
        preferences: str,
        dates: Tuple[str, str],
        limit: int = 10
    ) -> List[Dict]:
     
        params = {
            "location": location,
            "query": preferences,
            "start_date": dates[0],
            "end_date": dates[1],
            "limit": limit
        }
        headers = {"Authorization": f"Bearer {self.api_key}"}
        resp = requests.get(self.base_url, params=params, headers=headers, timeout=self.timeout)
        resp.raise_for_status()
        data = resp.json().get("results", [])

        results = []
        for item in data:
            results.append({
                "title": item.get("title"),
                "description": item.get("description"),
                "price": float(item.get("price", 0)),
                "currency": item.get("currency", "USD"),
                "url": item.get("url"),
            })
        return results
