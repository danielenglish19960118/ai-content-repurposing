"""
Global Configuration Management for InsightEngine Enterprise
"""
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    DEFAULT_MODEL: str = os.getenv("GEMINI_MODEL", "gemini-3.6-flash")
    DEFAULT_TEMPERATURE: float = float(os.getenv("DEFAULT_TEMPERATURE", "0.1"))
    MAX_TOKENS_PER_MIN: int = int(os.getenv("MAX_TOKENS_PER_MIN", "60000"))
    ESTIMATED_COST_PER_1K_TOKENS: float = 0.00015  # USD per 1k input tokens
    SUPPORTED_LANGUAGES = [
        "English",
        "Traditional Chinese (繁體中文)",
        "Japanese (日本語)",
        "Spanish (Español)"
    ]

config = Config()
