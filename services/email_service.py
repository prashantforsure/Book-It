import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from jinja2 import Environment, FileSystemLoader
from utils.config import get_config

class EmailService:
    """
    Renders an itinerary into HTML via Jinja2 and sends it via SMTP.
    """
    def __init__(self):
        cfg = get_config()
        self.host = cfg.SMTP_HOST
        self.port = cfg.SMTP_PORT
        self.user = cfg.SMTP_USER
        self.password = cfg.SMTP_PASS

        templates_dir = os.path.join(
            os.path.dirname(__file__), '..', 'data', 'templates'
        )
        self.env = Environment(
            loader=FileSystemLoader(templates_dir),
            autoescape=True
        )

    def render_template(self, itinerary) -> str:
        """
        Renders the itinerary_email.html template with itinerary data.
        """
        template = self.env.get_template('itinerary_email.html')
        return template.render(
            destination=itinerary.slots['destination'],
            start_date=itinerary.slots['start_date'],
            end_date=itinerary.slots['end_date'],
            flights=itinerary.flights,
            hotels=itinerary.hotels,
            activities=itinerary.activities,
            budget=itinerary.slots['budget'],
            travelers=itinerary.slots['num_travelers']
        )

    def send_itinerary(self, to_email: str, itinerary) -> None:
        """
        Sends the rendered itinerary HTML to the given email address.
        """
        html = self.render_template(itinerary)

        msg = MIMEMultipart('alternative')
        msg['Subject'] = f"Your Trip to {itinerary.slots['destination']}"
        msg['From'] = self.user
        msg['To'] = to_email
        msg.attach(MIMEText(html, 'html'))

        with smtplib.SMTP(self.host, self.port) as server:
            server.starttls()
            server.login(self.user, self.password)
            server.sendmail(self.user, to_email, msg.as_string())
