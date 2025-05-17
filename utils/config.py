import os
from functools import lru_cache
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI

load_dotenv()

class Config:
    """
    Application configuration loaded from environment variables.
    """
    # API Keys
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    ELEVENLABS_API_KEY: str = os.getenv("ELEVENLABS_API_KEY", "")
    SMTP_HOST: str = os.getenv("SMTP_HOST", "smtp.example.com")
    SMTP_PORT: int = int(os.getenv("SMTP_PORT", 587))
    SMTP_USER: str = os.getenv("SMTP_USER", "")
    SMTP_PASS: str = os.getenv("SMTP_PASS", "")

    # Travel API endpoints & keys
    FLIGHTS_API_URL: str = os.getenv("FLIGHTS_API_URL", "https://api.example.com/v1/flights")
    FLIGHTS_API_KEY: str = os.getenv("FLIGHTS_API_KEY", "")
    HOTELS_API_URL: str = os.getenv("HOTELS_API_URL", "https://api.example.com/v1/hotels")
    HOTELS_API_KEY: str = os.getenv("HOTELS_API_KEY", "")
    ACTIVITIES_API_URL: str = os.getenv("ACTIVITIES_API_URL", "https://api.example.com/v1/activities")
    ACTIVITIES_API_KEY: str = os.getenv("ACTIVITIES_API_KEY", "")

    # ElevenLabs default voice
    DEFAULT_VOICE_ID: str = os.getenv("DEFAULT_VOICE_ID", "Rachel")

    # LLM settings
    LLM_TEMPERATURE: float = float(os.getenv("LLM_TEMPERATURE", 0.7))
    LLM_MAX_TOKENS: int = int(os.getenv("LLM_MAX_TOKENS", 1024))

    def openai_llm(self) -> ChatOpenAI:
        """
        Returns a configured OpenAI Chat LLM instance via LangChain.
        """
        return ChatOpenAI(
            temperature=self.LLM_TEMPERATURE,
            max_tokens=self.LLM_MAX_TOKENS,
            openai_api_key=self.OPENAI_API_KEY
        )

@lru_cache(maxsize=1)
def get_config() -> Config:
    return Config()