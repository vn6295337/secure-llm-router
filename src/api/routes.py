"""
API routes for the LLM Secure Gateway
"""

import time
from fastapi import APIRouter, HTTPException, Depends, Request, status
from fastapi.responses import HTMLResponse
from slowapi import Limiter
from slowapi.util import get_remote_address

from ..models import QueryRequest, QueryResponse, HealthResponse
from ..security import validate_api_key
from ..llm.client import llm_client
from ..config import RATE_LIMIT

# --- Router Setup ---
router = APIRouter()
limiter = Limiter(key_func=get_remote_address, default_limits=[RATE_LIMIT])

@router.get("/", include_in_schema=False)
async def read_root():
    """Serves the Interactive Gateway Demo Dashboard"""
    from ..config import DASHBOARD_HTML, SERVICE_API_KEY
    # Inject the actual service API key into the HTML for the demo experience
    # In production, you would NOT do this, but for a portfolio demo, it makes the UI usable immediately.
    html_with_key = DASHBOARD_HTML.replace('value="secure-demo-ak7x9..."', f'value="{SERVICE_API_KEY}"')
    return HTMLResponse(content=html_with_key, media_type="text/html")

@router.get("/health", response_model=HealthResponse)
async def health_check(request: Request):
    """Health check endpoint"""
    active_provider = None
    if llm_client.providers:
        active_provider = llm_client.providers[0]["name"]
    return HealthResponse(
        status="healthy",
        provider=active_provider,
        timestamp=time.time()
    )

@router.post("/query", response_model=QueryResponse)
@limiter.limit(RATE_LIMIT)
async def query_llm(request: Request, query: QueryRequest, api_key: str = Depends(validate_api_key)):
    """Query LLM with security and fallback protocols"""
    
    # 1. Input Validation is handled by Pydantic models automatically before this line
    
    # 2. Execute Logic
    response_content, provider_used, latency_ms, error_message = await llm_client.query_llm_cascade(
        prompt=query.prompt,
        max_tokens=query.max_tokens,
        temperature=query.temperature
    )

    if response_content:
        return QueryResponse(
            response=response_content,
            provider=provider_used,
            latency_ms=latency_ms,
            status="success",
            error=None
        )
    else:
        # Fallback failure
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=error_message or "All LLM providers failed."
        )