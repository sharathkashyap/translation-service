import logging
from typing import Optional
from src.core.config import get_settings
from src.core.enums import TranslationEngine
from src.integrations.base import TranslationProvider
from src.integrations.google_translate import GoogleTranslateProvider
from src.integrations.openai_translate import OpenAITranslateProvider
from src.integrations.local_translate import LocalTranslateProvider
from src.core.exceptions import TranslationEngineException

logger = logging.getLogger(__name__)
settings = get_settings()

# Global provider instance
_provider: Optional[TranslationProvider] = None


def get_translation_provider() -> TranslationProvider:
    """
    Get translation provider based on configuration
    
    Returns:
        TranslationProvider instance
        
    Raises:
        TranslationEngineException: If provider cannot be initialized
    """
    global _provider
    
    if _provider is not None:
        return _provider
    
    engine = settings.TRANSLATION_ENGINE
    logger.info(f"Initializing translation engine: {engine}")
    
    try:
        if engine == TranslationEngine.GOOGLE:
            _provider = GoogleTranslateProvider()
        elif engine == TranslationEngine.OPENAI:
            _provider = OpenAITranslateProvider()
        elif engine == TranslationEngine.LOCAL:
            _provider = LocalTranslateProvider()
        else:
            raise TranslationEngineException(
                f"Unknown translation engine: {engine}"
            )
        
        logger.info(f"Translation engine initialized successfully: {engine}")
        return _provider
    except Exception as e:
        logger.error(f"Failed to initialize translation engine: {str(e)}")
        raise


def reset_translation_provider():
    """Reset the global provider instance"""
    global _provider
    
    if _provider is not None:
        # Clean up if needed
        if isinstance(_provider, LocalTranslateProvider):
            _provider.unload_model()
    
    _provider = None
    logger.info("Translation provider reset")


def switch_engine(engine: TranslationEngine):
    """
    Switch to a different translation engine
    
    Args:
        engine: TranslationEngine to switch to
    """
    global _provider
    
    logger.info(f"Switching translation engine to: {engine}")
    
    # Update settings
    settings.TRANSLATION_ENGINE = engine
    
    # Reset provider
    reset_translation_provider()
    
    # Initialize new provider
    get_translation_provider()
    
    logger.info(f"Translation engine switched successfully to: {engine}")
