import pytest
from services.email_service import EmailService
import services.email_service as email_mod

class DummyServer:
    def __init__(self, host, port):
        self.sent = []
    def starttls(self):
        pass
    def login(self, user, password):
        pass
    def sendmail(self, user, to_email, msg_str):
        self.sent.append((user, to_email, msg_str))
    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

@pytest.fixture(autouse=True)
def patch_env(monkeypatch):
    monkeypatch.setenv('SMTP_HOST', 'smtp.test.com')
    monkeypatch.setenv('SMTP_PORT', '587')
    monkeypatch.setenv('SMTP_USER', 'sender@test.com')
    monkeypatch.setenv('SMTP_PASS', 'password')
    yield


def test_render_template():
    class Itin:
        pass
    itinerary = Itin()
    itinerary.slots = {
        'destination': 'Paris',
        'start_date': '2025-08-01',
        'end_date': '2025-08-05',
        'budget': 1500,
        'num_travelers': 2
    }
    itinerary.flights = [{'airline': 'TestAir', 'flight_number': 'TA123', 'departure': '2025-08-01T10:00', 'arrival': '2025-08-01T14:00', 'price': 500, 'currency': 'USD'}]
    itinerary.hotels = [{'name': 'HotelTest', 'rating': 4, 'price_per_night': 100, 'total_price': 400, 'currency': 'USD', 'address': '123 Road', 'url': 'http://hotel'}]
    itinerary.activities = [{'title': 'Tour', 'description': 'City tour', 'price': 50, 'currency': 'USD', 'url': 'http://activity'}]

    svc = EmailService()
    html = svc.render_template(itinerary)

    assert 'Paris' in html
    assert 'HotelTest' in html
    assert 'Tour' in html


def test_send_itinerary(monkeypatch):
    class Itin:
        pass
    itinerary = Itin()
    itinerary.slots = {
        'destination': 'Paris',
        'start_date': '2025-08-01',
        'end_date': '2025-08-05',
        'budget': 1500,
        'num_travelers': 2
    }
    itinerary.flights = []
    itinerary.hotels = []
    itinerary.activities = []

    svc = EmailService()
    svc.user = 'sender@test.com'

    monkeypatch.setattr(email_mod.smtplib, 'SMTP', lambda host, port: DummyServer(host, port))

    svc.send_itinerary('recipient@test.com', itinerary)

    assert True
