from typing import Tuple


class ConfirmationChain:
    
    def confirmation_prompt(self) -> str:
        return (
            "Here is your itinerary draft. "
            "Does this look good? Please reply 'yes' to confirm or 'no' to make changes."
        )

    def parse_confirmation(self, user_input: str) -> Tuple[bool, bool]:
       
        resp = user_input.strip().lower()
        if resp in ("yes", "y", "confirm", "sure", "looks good"):
            return True, False
        if resp in ("no", "n", "change", "edit", "regenerate", "redo"):
            return False, True
        return False, False
