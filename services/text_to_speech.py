from elevenlabs import generate, play, set_api_key
from utils.config import get_config

class TextToSpeech:
    """
    Converts text to speech using ElevenLabs and plays it.
    """
    def __init__(self, voice: str = None):
        cfg = get_config()
        set_api_key(cfg.ELEVENLABS_API_KEY)
        self.voice = voice or cfg.DEFAULT_VOICE_ID

    def speak(self, text: str) -> None:
        """
        Generates and plays audio for the given text.
        """
        audio = generate(text=text, voice=self.voice)
        play(audio)
