from jinja2 import Template, Environment, FileSystemLoader
import os
from typing import Dict, Any

ITINERARY_SUMMARY_TEMPLATE = """
Trip to {{ destination }} from {{ start_date }} to {{ end_date }} for {{ travelers }} traveler(s).
Budget: {{ budget }} USD.

Flights:
{% for f in flights %}
- {{ f.airline }} {{ f.flight_number }}: {{ f.departure }} -> {{ f.arrival }} ({{ f.price }} {{ f.currency }})
{% endfor %}

Hotels:
{% for h in hotels %}
- {{ h.name }} ({{ h.rating }}⭐): {{ h.price_per_night }}/night, total {{ h.total_price }} {{ h.currency }}. {{ h.url }}
{% endfor %}

Activities:
{% for a in activities %}
- {{ a.title }}: {{ a.description }} Price: {{ a.price }} {{ a.currency }}. {{ a.url }}
{% endfor %}
"""

def render_text_summary(data: Dict[str, Any]) -> str:
    """
    Renders a plain-text itinerary summary.
    """
    template = Template(ITINERARY_SUMMARY_TEMPLATE)
    return template.render(**data)

def get_html_env() -> Environment:
    """
    Returns a Jinja2 Environment pointed at data/templates.
    """
    templates_dir = os.path.join(
        os.path.dirname(__file__), '..', 'data', 'templates'
    )
    return Environment(loader=FileSystemLoader(templates_dir), autoescape=True)
