from typing import List, Dict
import logging
from src.integrations.base import TranslationProvider
from src.core.exceptions import GoogleTranslateException, InvalidLanguageException
from src.core.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


class GoogleTranslateProvider(TranslationProvider):
    """Google Cloud Translate API provider"""
    
    def __init__(self):
        """Initialize Google Translate client"""
        try:
            from google.cloud import translate_v2
            
            # Initialize with credentials path
            if settings.GOOGLE_CREDENTIALS_PATH:
                import os
                os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = settings.GOOGLE_CREDENTIALS_PATH
            
            self.client = translate_v2.Client(project_id=settings.GOOGLE_PROJECT_ID)
            self.supported_langs = None
            logger.info("Google Translate provider initialized")
        except ImportError:
            raise GoogleTranslateException("google-cloud-translate not installed")
        except Exception as e:
            raise GoogleTranslateException(f"Failed to initialize: {str(e)}")
    
    async def translate(
        self,
        text: str,
        source_language: str,
        target_language: str
    ) -> str:
        """Translate text using Google Translate API"""
        try:
            if not self.validate_language_pair(source_language, target_language):
                raise InvalidLanguageException(
                    f"Language pair {source_language}->{target_language} not supported"
                )
            
            result = self.client.translate_text(
                text,
                source_language_code=source_language,
                target_language_code=target_language
            )
            
            return result['translatedText']
        except Exception as e:
            logger.error(f"Google Translate error: {str(e)}")
            raise GoogleTranslateException(str(e))
    
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
        """Get supported languages from Google Translate"""
        try:
            if self.supported_langs is None:
                langs = self.client.get_languages()
                self.supported_langs = {
                    lang['language']: lang.get('name', lang['language'])
                    for lang in langs.get('languages', [])
                }
            return self.supported_langs
        except Exception as e:
            logger.error(f"Failed to get supported languages: {str(e)}")
            raise GoogleTranslateException(str(e))
    
    def validate_language_pair(
        self,
        source_language: str,
        target_language: str
    ) -> bool:
        """Validate language pair"""
        # Google Translate supports most language pairs
        # Basic validation
        return (
            isinstance(source_language, str) and 
            isinstance(target_language, str) and
            len(source_language) == 2 and 
            len(target_language) == 2
        )
    
    async def health_check(self) -> bool:
        """Check if Google Translate is accessible"""
        try:
            # Try a simple translation
            result = self.client.translate_text(
                "hello",
                source_language_code="en",
                target_language_code="es"
            )
            return 'translatedText' in result
        except Exception as e:
            logger.error(f"Health check failed: {str(e)}")
            return False
