import requests
from typing import List, Dict, Optional
from utils.config import get_config

class HotelsAPI:
    
    def __init__(self, api_key: str = None):
        cfg = get_config()
        self.api_key = api_key or cfg.HOTELS_API_KEY
        self.base_url = cfg.HOTELS_API_URL 

    def search(
        self,
        location: str,
        checkin: str,
        checkout: str,
        min_rating: Optional[int] = None,
        budget: Optional[float] = None
    ) -> List[Dict]:
      
        params = {
            "location": location,
            "checkin_date": checkin,
            "checkout_date": checkout,
            "limit": 10
        }
        headers = {"Authorization": f"Bearer {self.api_key}"}
        resp = requests.get(self.base_url, params=params, headers=headers, timeout=self.timeout)
        resp.raise_for_status()
        data = resp.json().get("hotels", [])

        results = []
        for item in data:
            rating = float(item.get("star_rating", 0))
            price = float(item.get("price_per_night", 0))
            total = price * ( 
                date_parser.parse(checkout).date() - date_parser.parse(checkin).date()
            ).days
            if min_rating and rating < min_rating:
                continue
            if budget and total > budget:
                continue
            results.append({
                "name": item.get("name"),
                "rating": rating,
                "price_per_night": price,
                "total_price": total,
                "currency": item.get("currency", "USD"),
                "address": item.get("address"),
                "url": item.get("booking_url"),
            })
        return results