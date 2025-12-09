from abc import ABC, abstractmethod
from typing import List, Dict, Tuple
from src.core.enums import SupportedLanguage


class TranslationProvider(ABC):
    """Abstract base class for translation providers"""
    
    @abstractmethod
    async def translate(
        self,
        text: str,
        source_language: str,
        target_language: str
    ) -> str:
        """
        Translate text from source to target language
        
        Args:
            text: Text to translate
            source_language: Source language code
            target_language: Target language code
            
        Returns:
            Translated text
        """
        pass
    
    @abstractmethod
    async def batch_translate(
        self,
        texts: List[str],
        source_language: str,
        target_language: str
    ) -> List[str]:
        """
        Translate multiple texts
        
        Args:
            texts: List of texts to translate
            source_language: Source language code
            target_language: Target language code
            
        Returns:
            List of translated texts
        """
        pass
    
    @abstractmethod
    async def get_supported_languages(self) -> Dict[str, str]:
        """
        Get list of supported languages
        
        Returns:
            Dict of language codes and names
        """
        pass
    
    @abstractmethod
    def validate_language_pair(
        self,
        source_language: str,
        target_language: str
    ) -> bool:
        """
        Validate if language pair is supported
        
        Returns:
            True if supported, False otherwise
        """
        pass
    
    @abstractmethod
    async def health_check(self) -> bool:
        """
        Check if translation engine is healthy
        
        Returns:
            True if healthy, False otherwise
        """
        pass
