from typing import List, Dict
import logging
from src.integrations.base import TranslationProvider
from src.core.exceptions import OpenAITranslateException, InvalidLanguageException
from src.core.config import get_settings
from src.core.enums import SupportedLanguage

logger = logging.getLogger(__name__)
settings = get_settings()


class OpenAITranslateProvider(TranslationProvider):
    """OpenAI API-based translation provider"""
    
    SUPPORTED_LANGUAGES = {
        "en": "English",
        "es": "Spanish",
        "fr": "French",
        "de": "German",
        "zh": "Chinese",
        "ja": "Japanese",
        "ko": "Korean",
        "ru": "Russian",
        "pt": "Portuguese",
        "hi": "Hindi",
        "ar": "Arabic",
        "it": "Italian"
    }
    
    def __init__(self):
        """Initialize OpenAI client"""
        try:
            from openai import OpenAI
            
            self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
            self.model = settings.OPENAI_MODEL
            logger.info(f"OpenAI provider initialized with model: {self.model}")
        except ImportError:
            raise OpenAITranslateException("openai library not installed")
        except Exception as e:
            raise OpenAITranslateException(f"Failed to initialize: {str(e)}")
    
    async def translate(
        self,
        text: str,
        source_language: str,
        target_language: str
    ) -> str:
        """Translate text using OpenAI API"""
        try:
            if not self.validate_language_pair(source_language, target_language):
                raise InvalidLanguageException(
                    f"Language pair {source_language}->{target_language} not supported"
                )
            
            source_lang_name = self.SUPPORTED_LANGUAGES.get(
                source_language, 
                source_language
            )
            target_lang_name = self.SUPPORTED_LANGUAGES.get(
                target_language,
                target_language
            )
            
            prompt = (
                f"Translate the following text from {source_lang_name} to "
                f"{target_lang_name}. Only provide the translation, no additional text.\n\n"
                f"Text: {text}"
            )
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": f"You are a professional translator. Translate text accurately from {source_lang_name} to {target_lang_name}."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.3,
                max_tokens=2048
            )
            
            return response.choices[0].message.content.strip()
        except Exception as e:
            logger.error(f"OpenAI translation error: {str(e)}")
            raise OpenAITranslateException(str(e))
    
    async def batch_translate(
        self,
        texts: List[str],
        source_language: str,
        target_language: str
    ) -> List[str]:
        """Batch translate multiple texts"""
        results = []
        for text in texts:
            translated = await self.translate(text, source_language, target_language)
            results.append(translated)
        return results
    
    async def get_supported_languages(self) -> Dict[str, str]:
        """Get supported languages"""
        return self.SUPPORTED_LANGUAGES.copy()
    
    def validate_language_pair(
        self,
        source_language: str,
        target_language: str
    ) -> bool:
        """Validate language pair"""
        return (
            source_language in self.SUPPORTED_LANGUAGES and
            target_language in self.SUPPORTED_LANGUAGES and
            source_language != target_language
        )
    
    async def health_check(self) -> bool:
        """Check if OpenAI API is accessible"""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": "hello"}],
                max_tokens=10
            )
            return bool(response.choices[0].message.content)
        except Exception as e:
            logger.error(f"Health check failed: {str(e)}")
            return False
