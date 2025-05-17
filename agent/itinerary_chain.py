from typing import Dict, Any
from dataclasses import dataclass

from services.travel_api.flights_api import FlightsAPI
from services.travel_api.hotels_api import HotelsAPI
from services.travel_api.activities_api import ActivitiesAPI
from langchain import LLMChain, PromptTemplate
from utils.config import get_config


@dataclass
class Itinerary:
    summary_text: str
    flights: Any
    hotels: Any
    activities: Any
    slots: Dict[str, Any]


class ItineraryChain:
    """
    Once all slots are collected, fetch travel options via APIs,
    then prompt the LLM to draft a day-by-day plan.
    """
    def __init__(self):
        cfg = get_config()
        self.flights_api = FlightsAPI(api_key=cfg.FLIGHTS_API_KEY)
        self.hotels_api = HotelsAPI(api_key=cfg.HOTELS_API_KEY)
        self.activities_api = ActivitiesAPI(api_key=cfg.ACTIVITIES_API_KEY)
        template = (
            "You are a travel planner. Given the following options, "
            "draft a concise day-by-day itinerary including flights, hotels, "
            "and suggested activities. Be mindful of budget and preferences.\n"
            "Slots: {slots}\n"
            "Flights: {flights}\n"
            "Hotels: {hotels}\n"
            "Activities: {activities}\n"
        )
        self.prompt = PromptTemplate(
            input_variables=["slots", "flights", "hotels", "activities"],
            template=template
        )
        self.chain = LLMChain(
            llm=get_config().openai_llm(),
            prompt=self.prompt
        )
        self.last_itinerary: Itinerary

    def run(self, slots: Dict[str, Any]) -> Itinerary:
        # 1. Fetch options
        flights = self.flights_api.search(
            origin=slots.get("origin", None),
            destination=slots["destination"],
            start_date=slots["start_date"],
            end_date=slots["end_date"],
            budget=slots["budget"]
        )
        hotels = self.hotels_api.search(
            location=slots["destination"],
            checkin=slots["start_date"],
            checkout=slots["end_date"],
            min_rating=slots["hotel_rating"],
            budget=slots["budget"]
        )
        activities = self.activities_api.search(
            location=slots["destination"],
            preferences=slots["activities"],
            dates=(slots["start_date"], slots["end_date"])
        )

        # 2. Generate via LLM
        llm_input = {
            "slots": slots,
            "flights": flights,
            "hotels": hotels,
            "activities": activities,
        }
        summary = self.chain.run(**llm_input)

        # 3. Package result
        itinerary = Itinerary(
            summary_text=summary,
            flights=flights,
            hotels=hotels,
            activities=activities,
            slots=slots
        )
        self.last_itinerary = itinerary
        return itinerary
