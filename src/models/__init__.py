"""
Pydantic models for the Enterprise AI Gateway
"""

from pydantic import BaseModel, Field, validator
from typing import Optional

class QueryRequest(BaseModel):
    prompt: str = Field(..., min_length=1, max_length=4000)
    max_tokens: int = Field(256, ge=1, le=2048)
    temperature: float = Field(0.7, ge=0.0, le=2.0)

    @validator('prompt')
    def check_prompt_injection(cls, v):
        from ..security import detect_prompt_injection
        if detect_prompt_injection(v):
            raise ValueError("Security Alert: Prompt injection pattern detected.")
        return v

class CascadeStep(BaseModel):
    provider: str
    model: Optional[str] = None
    status: str  # "success", "failed", "timeout"
    reason: Optional[str] = None
    latency_ms: int

class QueryResponse(BaseModel):
    response: Optional[str]
    provider: Optional[str]
    latency_ms: int
    status: str
    error: Optional[str]
    cascade_path: Optional[list] = None
    cost_estimate_usd: Optional[float] = None

class HealthResponse(BaseModel):
    status: str
    provider: Optional[str]
    timestamp: float