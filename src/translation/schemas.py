from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from datetime import datetime


class TranslateRequest(BaseModel):
    """Translation request"""
    text: str = Field(..., min_length=1, max_length=5000)
    source_language: str = Field(..., description="Source language code (e.g., 'en')")
    target_language: str = Field(..., description="Target language code (e.g., 'es')")


class BatchTranslateRequest(BaseModel):
    """Batch translation request"""
    texts: List[str] = Field(..., min_items=1, max_items=100)
    source_language: str
    target_language: str


class TranslateResponse(BaseModel):
    """Translation response"""
    original_text: str
    translated_text: str
    source_language: str
    target_language: str
    engine: str
    timestamp: datetime


class BatchTranslateResponse(BaseModel):
    """Batch translation response"""
    original_texts: List[str]
    translated_texts: List[str]
    source_language: str
    target_language: str
    engine: str
    count: int
    timestamp: datetime


class LanguageInfo(BaseModel):
    """Language information"""
    code: str
    name: str


class SupportedLanguagesResponse(BaseModel):
    """Supported languages response"""
    languages: Dict[str, str]
    engine: str
    total: int


class EngineStatusResponse(BaseModel):
    """Translation engine status"""
    engine: str
    status: str
    healthy: bool
    message: str


class EngineHealthResponse(BaseModel):
    """Engine health check response"""
    healthy: bool
    engine: str
    timestamp: datetime
    response_time_ms: float


class EngineConfigResponse(BaseModel):
    """Current engine configuration"""
    current_engine: str
    available_engines: List[str]
    google_configured: bool
    openai_configured: bool
    local_model: str
    local_device: str


class ErrorResponse(BaseModel):
    """Error response"""
    error: str
    detail: str
    timestamp: datetime
