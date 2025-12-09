from typing import List, Dict, Optional
import logging
import torch
from src.integrations.base import TranslationProvider
from src.core.exceptions import LocalTranslateException, ModelLoadException, InvalidLanguageException
from src.core.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


class LocalTranslateProvider(TranslationProvider):
    """Local GPU-based translation provider using transformers"""
    
    SUPPORTED_MODELS = {
        "facebook/nllb-200-distilled-600M": {
            "name": "NLLB-200 Distilled 600M",
            "languages": [
                "en", "es", "fr", "de", "zh", "ja", "ko", "ru", "pt", "hi", "ar", "it"
            ]
        },
        "facebook/m2m100_418M": {
            "name": "M2M-100 418M",
            "languages": [
                "en", "es", "fr", "de", "zh", "ja", "ko", "ru", "pt", "hi", "ar", "it"
            ]
        },
        "Helsinki-NLP/Tatoeba-MT": {
            "name": "MarianMT",
            "languages": ["en", "es", "fr", "de", "zh", "ja"]
        }
    }
    
    def __init__(self):
        """Initialize local translation model"""
        try:
            from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
            
            self.model_name = settings.LOCAL_MODEL_NAME
            self.device = settings.LOCAL_DEVICE
            self.batch_size = settings.LOCAL_BATCH_SIZE
            
            # Check device availability
            if self.device == "cuda" and not torch.cuda.is_available():
                logger.warning("CUDA not available, falling back to CPU")
                self.device = "cpu"
            
            logger.info(f"Loading model: {self.model_name} on device: {self.device}")
            
            # Load model and tokenizer
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            self.model = AutoModelForSeq2SeqLM.from_pretrained(self.model_name)
            self.model = self.model.to(self.device)
            
            # Set model to evaluation mode
            self.model.eval()
            
            logger.info(f"Model loaded successfully: {self.model_name}")
        except ImportError as e:
            raise LocalTranslateException(f"Required library not installed: {str(e)}")
        except Exception as e:
            logger.error(f"Failed to load model: {str(e)}")
            raise ModelLoadException(settings.LOCAL_MODEL_NAME)
    
    async def translate(
        self,
        text: str,
        source_language: str,
        target_language: str
    ) -> str:
        """Translate text using local model"""
        try:
            if not self.validate_language_pair(source_language, target_language):
                raise InvalidLanguageException(
                    f"Language pair {source_language}->{target_language} not supported"
                )
            
            translated = self._translate_internal(
                text,
                source_language,
                target_language
            )
            return translated
        except Exception as e:
            logger.error(f"Local translation error: {str(e)}")
            raise LocalTranslateException(str(e))
    
    async def batch_translate(
        self,
        texts: List[str],
        source_language: str,
        target_language: str
    ) -> List[str]:
        """Batch translate multiple texts"""
        try:
            if not self.validate_language_pair(source_language, target_language):
                raise InvalidLanguageException(
                    f"Language pair {source_language}->{target_language} not supported"
                )
            
            results = []
            # Process in batches
            for i in range(0, len(texts), self.batch_size):
                batch = texts[i:i + self.batch_size]
                batch_results = self._batch_translate_internal(
                    batch,
                    source_language,
                    target_language
                )
                results.extend(batch_results)
            
            return results
        except Exception as e:
            logger.error(f"Batch translation error: {str(e)}")
            raise LocalTranslateException(str(e))
    
    def _translate_internal(
        self,
        text: str,
        source_language: str,
        target_language: str
    ) -> str:
        """Internal translation method"""
        # Prepare input
        inputs = self.tokenizer(
            text,
            return_tensors="pt",
            padding=True,
            truncation=True,
            max_length=settings.LOCAL_MAX_LENGTH
        ).to(self.device)
        
        # Translate
        with torch.no_grad():
            translated_tokens = self.model.generate(
                **inputs,
                forced_bos_token_id=self.tokenizer.get_lang_id(target_language),
                max_length=settings.LOCAL_MAX_LENGTH
            )
        
        # Decode
        translated_text = self.tokenizer.batch_decode(
            translated_tokens,
            skip_special_tokens=True
        )
        
        return translated_text[0] if translated_text else text
    
    def _batch_translate_internal(
        self,
        texts: List[str],
        source_language: str,
        target_language: str
    ) -> List[str]:
        """Internal batch translation method"""
        # Prepare inputs
        inputs = self.tokenizer(
            texts,
            return_tensors="pt",
            padding=True,
            truncation=True,
            max_length=settings.LOCAL_MAX_LENGTH
        ).to(self.device)
        
        # Translate
        with torch.no_grad():
            translated_tokens = self.model.generate(
                **inputs,
                forced_bos_token_id=self.tokenizer.get_lang_id(target_language),
                max_length=settings.LOCAL_MAX_LENGTH
            )
        
        # Decode
        translated_texts = self.tokenizer.batch_decode(
            translated_tokens,
            skip_special_tokens=True
        )
        
        return translated_texts
    
    async def get_supported_languages(self) -> Dict[str, str]:
        """Get supported languages for loaded model"""
        model_info = self.SUPPORTED_MODELS.get(
            self.model_name,
            {"languages": ["en", "es", "fr"]}
        )
        return {
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
    
    def validate_language_pair(
        self,
        source_language: str,
        target_language: str
    ) -> bool:
        """Validate language pair"""
        model_info = self.SUPPORTED_MODELS.get(self.model_name)
        if not model_info:
            return True  # Unknown model, allow any pair
        
        supported = model_info.get("languages", [])
        return (
            source_language in supported and
            target_language in supported and
            source_language != target_language
        )
    
    async def health_check(self) -> bool:
        """Check if model is loaded and working"""
        try:
            # Try a simple translation
            result = self._translate_internal(
                "hello",
                "en",
                "es"
            )
            return bool(result)
        except Exception as e:
            logger.error(f"Health check failed: {str(e)}")
            return False
    
    def unload_model(self):
        """Unload model to free memory"""
        try:
            if self.model:
                del self.model
            if self.tokenizer:
                del self.tokenizer
            torch.cuda.empty_cache()
            logger.info("Model unloaded successfully")
        except Exception as e:
            logger.error(f"Failed to unload model: {str(e)}")
