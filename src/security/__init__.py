"""
Security utilities for the LLM Secure Gateway
"""

import os
import re
from fastapi import HTTPException, Depends, status
from fastapi.security import APIKeyHeader

# --- Security Configuration ---
API_KEY_NAME = "X-API-Key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)
SERVICE_API_KEY = os.getenv("SERVICE_API_KEY")
ENABLE_PROMPT_INJECTION_CHECK = os.getenv("ENABLE_PROMPT_INJECTION_CHECK", "true").lower() == "true"

# --- Prompt Injection Detection ---
INJECTION_PATTERNS = [
    r"ignore\s+(all\s+)?(previous|above|prior)\s+instructions?",
    r"disregard\s+(all\s+)?(previous|above|prior)\s+instructions?",
    r"you\s+are\s+now",
    r"system\s*:\s*",
]

def detect_prompt_injection(prompt: str) -> bool:
    """Detect potential prompt injection attacks"""
    if not ENABLE_PROMPT_INJECTION_CHECK:
        return False
    prompt_lower = prompt.lower()
    for pattern in INJECTION_PATTERNS:
        if re.search(pattern, prompt_lower, re.IGNORECASE):
            return True
    return False

# --- API Key Validation ---
async def validate_api_key(api_key: str = Depends(api_key_header)):
    """Validate API key for request authentication"""
    if not SERVICE_API_KEY:
        raise HTTPException(status_code=500, detail="Server misconfiguration: API Key missing")
    if api_key != SERVICE_API_KEY:
        raise HTTPException(status_code=401, detail="Invalid or missing API key")
    return api_key