from fastapi import status


class TranslationException(Exception):
    """Base translation exception"""
    def __init__(self, message: str, status_code: int = 500):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class InvalidLanguageException(TranslationException):
    """Invalid language pair"""
    def __init__(self, message: str = "Invalid language pair"):
        super().__init__(message, status.HTTP_400_BAD_REQUEST)


class TranslationEngineException(TranslationException):
    """Translation engine error"""
    def __init__(self, message: str, engine: str = "unknown"):
        super().__init__(
            f"Translation engine error ({engine}): {message}",
            status.HTTP_503_SERVICE_UNAVAILABLE
        )


class GoogleTranslateException(TranslationEngineException):
    """Google Translate specific error"""
    def __init__(self, message: str):
        super().__init__(message, "google")


class OpenAITranslateException(TranslationEngineException):
    """OpenAI API specific error"""
    def __init__(self, message: str):
        super().__init__(message, "openai")


class LocalTranslateException(TranslationEngineException):
    """Local GPU translation error"""
    def __init__(self, message: str):
        super().__init__(message, "local")


class ModelLoadException(TranslationException):
    """Model loading error"""
    def __init__(self, model_name: str):
        super().__init__(
            f"Failed to load model: {model_name}",
            status.HTTP_500_INTERNAL_SERVER_ERROR
        )


class RateLimitException(TranslationException):
    """Rate limit exceeded"""
    def __init__(self):
        super().__init__(
            "Rate limit exceeded. Please try again later.",
            status.HTTP_429_TOO_MANY_REQUESTS
        )
