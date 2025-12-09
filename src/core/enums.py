from enum import Enum
from typing import Literal


class TranslationEngine(str, Enum):
    """Translation engine options"""
    GOOGLE = "google"
    OPENAI = "openai"
    LOCAL = "local"  # GPU-based local translation


class SupportedLanguage(str, Enum):
    """Supported languages for translation"""
    ENGLISH = "en"
    SPANISH = "es"
    FRENCH = "fr"
    GERMAN = "de"
    CHINESE = "zh"
    JAPANESE = "ja"
    KOREAN = "ko"
    RUSSIAN = "ru"
    PORTUGUESE = "pt"
    HINDI = "hi"
    ARABIC = "ar"
    ITALIAN = "it"


class LocalModelType(str, Enum):
    """Local model types"""
    MARIAN_MT = "Helsinki-NLP/Tatoeba-MT"  # MarianMT models
    M2M100 = "facebook/m2m100_418M"  # M2M100 multilingual
    NLLB = "facebook/nllb-200-distilled-600M"  # No Language Left Behind


EngineType = Literal["google", "openai", "local"]
