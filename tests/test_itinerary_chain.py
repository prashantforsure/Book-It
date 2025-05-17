import pytest
from agent.itinerary_chain import ItineraryChain
from services.travel_api.flights_api import FlightsAPI
from services.travel_api.hotels_api import HotelsAPI
from services.travel_api.activities_api import ActivitiesAPI

@pytest.fixture(autouse=True)
def patch_apis(monkeypatch):
    # Mock flight, hotel, and activity searches
    monkeypatch.setattr(FlightsAPI, 'search', lambda self, origin, destination, start_date, end_date, budget=None: [{'dummy': 'flight'}])
    monkeypatch.setattr(HotelsAPI, 'search', lambda self, location, checkin, checkout, min_rating=None, budget=None: [{'dummy': 'hotel'}])
    monkeypatch.setattr(ActivitiesAPI, 'search', lambda self, location, preferences, dates, limit=10: [{'dummy': 'activity'}])
    yield


def test_itinerary_chain(monkeypatch):
    # Prepare complete slot data
    slots = {
        'destination': 'TestCity',
        'start_date': '2025-10-01',
        'end_date': '2025-10-05',
        'budget': 1000.0,
        'num_travelers': 2,
        'hotel_rating': 4,
        'activities': 'sightseeing',
        'email': 'user@example.com'
    }

    chain = ItineraryChain()
    # Monkeypatch the LLMChain to return a fixed summary
    monkeypatch.setattr(chain, 'chain', type('C', (), {'run': lambda self, **kwargs: 'Generated Itinerary Summary'})())

    itinerary = chain.run(slots)

    assert itinerary.summary_text == 'Generated Itinerary Summary'
    assert itinerary.flights == [{'dummy': 'flight'}]
    assert itinerary.hotels == [{'dummy': 'hotel'}]
    assert itinerary.activities == [{'dummy': 'activity'}]
    assert itinerary.slots == slots
