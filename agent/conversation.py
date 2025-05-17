import logging
from typing import Optional, Tuple, Dict, Any

from agent.slot_filling_chain import SlotFillingChain
from agent.itinerary_chain import ItineraryChain
from agent.confirmation_chain import ConfirmationChain
from services.email_service import EmailService


class Agent:
  
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.slots: Dict[str, Any] = {}
        self.history: list[Tuple[str, str]] = []
        self.stage: str = "slot_filling"
        self.slot_chain = SlotFillingChain()
        self.itinerary_chain = ItineraryChain()
        self.confirm_chain = ConfirmationChain()
        self.email_service = EmailService()

    def process_input(self, user_input: str) -> str:
        """
        Process a user utterance and return the agent's response.
        """
     
        self.history.append(("user", user_input))

        if self.stage == "slot_filling":
            response, updated_slots, done = self.slot_chain.run(self.slots, user_input)

            for k, v in updated_slots.items():
                if k != "awaiting_slot":
                    self.slots[k] = v
            if "awaiting_slot" in updated_slots:
                self.slots["awaiting_slot"] = updated_slots["awaiting_slot"]

            if done:
                self.stage = "itinerary"
                itinerary = self.itinerary_chain.run(self.slots)
                response = itinerary.summary_text
                self.history.append(("agent", response))
                self.stage = "confirmation"
            else:
                self.history.append(("agent", response))
            return response

        # Stage: Confirmation
        if self.stage == "confirmation":
            confirmed, edit_requested = self.confirm_chain.parse_confirmation(user_input)
            if confirmed:
                user_email = self.slots.get("email")
                itinerary = self.itinerary_chain.last_itinerary
                self.email_service.send_itinerary(user_email, itinerary)
                self.stage = "completed"
                response = (
                    "Great! I've emailed your personalized itinerary. "
                    "Let me know if you need anything else."
                )
            elif edit_requested:
                self.stage = "slot_filling"
                self.slots.clear()
                prompt, new_slots, _ = self.slot_chain.run(self.slots, "")
                response = prompt
            else:
                response = (
                    "Sorry, I didn't catch that. "
                    + self.confirm_chain.confirmation_prompt()
                )
            self.history.append(("agent", response))
            return response

        return (
            "This session is complete. To plan another trip, please start a new session."
        )
