import logging
import time
from typing import List
from datetime import datetime

from src.integrations.factory import get_translation_provider
from src.translation.schemas import (
    TranslateRequest, 
    TranslateResponse,
    BatchTranslateRequest,
    BatchTranslateResponse
)
from src.core.exceptions import (
    InvalidLanguageException,
    TranslationEngineException
)

logger = logging.getLogger(__name__)


class TranslationService:
    """Translation service"""
    
    @staticmethod
    async def translate(request: TranslateRequest) -> TranslateResponse:
        """Translate single text"""
        try:
            provider = get_translation_provider()
            
            start_time = time.time()
            translated_text = await provider.translate(
                request.text,
                request.source_language,
                request.target_language
            )
            duration = time.time() - start_time
            
            logger.info(
                f"Translation completed in {duration:.2f}s - "
                f"{request.source_language}->{request.target_language}"
            )
            
            return TranslateResponse(
                original_text=request.text,
                translated_text=translated_text,
                source_language=request.source_language,
                target_language=request.target_language,
                engine=provider.__class__.__name__,
                timestamp=datetime.utcnow()
            )
        except InvalidLanguageException:
            raise
        except TranslationEngineException:
            raise
        except Exception as e:
            logger.error(f"Translation error: {str(e)}")
            raise TranslationEngineException(str(e))
    
    @staticmethod
    async def batch_translate(request: BatchTranslateRequest) -> BatchTranslateResponse:
        """Batch translate multiple texts"""
        try:
            provider = get_translation_provider()
            
            start_time = time.time()
            translated_texts = await provider.batch_translate(
                request.texts,
                request.source_language,
                request.target_language
            )
            duration = time.time() - start_time
            
            logger.info(
                f"Batch translation completed in {duration:.2f}s - "
                f"{len(request.texts)} texts translated"
            )
            
            return BatchTranslateResponse(
                original_texts=request.texts,
                translated_texts=translated_texts,
                source_language=request.source_language,
                target_language=request.target_language,
                engine=provider.__class__.__name__,
                count=len(request.texts),
                timestamp=datetime.utcnow()
            )
        except InvalidLanguageException:
            raise
        except TranslationEngineException:
            raise
        except Exception as e:
            logger.error(f"Batch translation error: {str(e)}")
            raise TranslationEngineException(str(e))
    
    @staticmethod
    async def get_supported_languages():
        """Get supported languages"""
        try:
            provider = get_translation_provider()
            languages = await provider.get_supported_languages()
            
            return {
                "languages": languages,
                "engine": provider.__class__.__name__,
                "total": len(languages)
            }
        except Exception as e:
            logger.error(f"Error getting supported languages: {str(e)}")
            raise TranslationEngineException(str(e))
    
    @staticmethod
    async def health_check():
        """Health check translation engine"""
        try:
            provider = get_translation_provider()
            
            start_time = time.time()
            is_healthy = await provider.health_check()
            response_time = (time.time() - start_time) * 1000
            
            return {
                "healthy": is_healthy,
                "engine": provider.__class__.__name__,
                "timestamp": datetime.utcnow(),
                "response_time_ms": round(response_time, 2)
            }
        except Exception as e:
            logger.error(f"Health check error: {str(e)}")
            return {
                "healthy": False,
                "engine": "unknown",
                "timestamp": datetime.utcnow(),
                "response_time_ms": 0,
                "error": str(e)
            }
