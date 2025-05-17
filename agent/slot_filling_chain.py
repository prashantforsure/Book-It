from typing import Tuple, Dict, Any, Optional
from dateutil import parser as date_parser
import re


class SlotFillingChain:
   
    REQUIRED_SLOTS = [
        "destination",
        "start_date",
        "end_date",
        "budget",
        "num_travelers",
        "hotel_rating",
        "activities",
        "email",
    ]

    PROMPT_TEMPLATES: Dict[str, str] = {
        "destination": "Where would you like to travel?",
        "start_date": "What is your desired departure date? (YYYY-MM-DD)",
        "end_date": "What is your return date? (YYYY-MM-DD)",
        "budget": "What is your total budget for the trip (in USD)?",
        "num_travelers": "How many people are traveling?",
        "hotel_rating": "What minimum hotel star rating do you prefer? (1-5)?",
        "activities": (
            "Any specific activities or experiences you'd like "
            "(e.g., sightseeing, adventure, relaxation)?"
        ),
        "email": "Please provide your email address to send the itinerary.",
    }

    def run(
        self, slots: Dict[str, Any], user_input: str
    ) -> Tuple[str, Dict[str, Any], bool]:
        
        updated_slots: Dict[str, Any] = {}

        if "awaiting_slot" in slots:
            current = slots["awaiting_slot"]
            valid, parsed, error_msg = self._validate_slot(current, user_input)
            if not valid:
                return error_msg, {}, False
            updated_slots[current] = parsed
            slots.pop("awaiting_slot", None)

        merged = {**slots, **updated_slots}
        next_slot: Optional[str] = self._get_next_slot(merged)
        if next_slot:
            prompt = self.PROMPT_TEMPLATES[next_slot]
            updated_slots["awaiting_slot"] = next_slot
            return prompt, updated_slots, False

        return "All set! Let me craft your itinerary…", {}, True

    def _get_next_slot(self, slots: Dict[str, Any]) -> Optional[str]:
        for s in self.REQUIRED_SLOTS:
            if s not in slots:
                return s
        return None

    def _validate_slot(
        self, slot: str, user_input: str
    ) -> Tuple[bool, Any, str]:
        """
        Validates and transforms the user input for a given slot.
        Returns: (is_valid, cleaned_value, error_message)
        """
        inp = user_input.strip()

        if slot in ("start_date", "end_date"):
            try:
                dt = date_parser.parse(inp).date()
                return True, dt.isoformat(), ""
            except Exception:
                return False, None, (
                    "I couldn't understand that date. "
                    "Please use YYYY-MM-DD format."
                )

        if slot == "budget":
            num = re.sub(r"[^\d.]", "", inp)
            try:
                b = float(num)
                if b <= 0:
                    raise ValueError
                return True, b, ""
            except Exception:
                return False, None, (
                    "Please enter a positive number for your budget."
                )

        if slot == "num_travelers":
            if inp.isdigit() and int(inp) > 0:
                return True, int(inp), ""
            return False, None, (
                "Enter a valid number of travelers (integer > 0)."
            )

        if slot == "hotel_rating":
            if inp.isdigit() and 1 <= int(inp) <= 5:
                return True, int(inp), ""
            return False, None, (
                "Provide a hotel rating between 1 and 5 stars."
            )

        if slot == "email":
            pattern = r"[^@]+@[^@]+\.[^@]+"
            if re.match(pattern, inp):
                return True, inp, ""
            return False, None, (
                "That doesn't look like a valid email. Please try again."
            )

        return True, inp, ""
