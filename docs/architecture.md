# System Architecture - Enterprise AI Gateway

> **Primary Responsibility:** System design, component architecture, and data flow

This document explains how the Enterprise AI Gateway is designed and how its components work together.

---

## Table of Contents

1. [System Overview](#system-overview)
2. [Architecture Diagram](#architecture-diagram)
3. [Component Details](#component-details)
4. [Data Flow](#data-flow)
5. [Security Architecture](#security-architecture)
6. [Technology Stack](#technology-stack)
7. [Design Decisions](#design-decisions)

---

## System Overview

The Enterprise AI Gateway is a **REST API gateway** that provides secure, reliable access to multiple Large Language Model (LLM) providers with built-in failover.

**Core Purpose**: Act as a single, secure entry point for AI queries while automatically handling provider failures and enforcing security policies.

**Key Characteristics**:
- **Stateless** - No session management, each request is independent
- **Synchronous** - Request-response pattern (no streaming)
- **Horizontally Scalable** - Can run multiple instances behind a load balancer
- **Provider-Agnostic** - Works with any LLM provider that supports REST APIs

---

## Architecture Diagram

See [Security Overview](security_overview.md) for the detailed 4-layer security architecture diagram.

**Request Flow Summary:**
```
User Request → Auth & Rate Limit → Input Guard → AI Safety → LLM Router → AI Response
```

---

## Component Details

### 1. API Gateway Layer (FastAPI)

**Responsibility**: Handle HTTP requests, route to endpoints, return responses

**Key Files**:
- `src/main.py` - FastAPI app initialization
- `src/api/routes.py` - Health check and query endpoints

**Features**:
- Auto-generated OpenAPI documentation
- ASGI server (Uvicorn) for async support
- Built-in request/response validation

---

### 2. Authentication Layer

**Responsibility**: Verify that requests include a valid API key

**Implementation**: `src/security/__init__.py` (validate_api_key function)

**How it Works**:
1. Extracts `X-API-Key` header from request
2. Compares against `SERVICE_API_KEY` environment variable
3. Returns 401 Unauthorized if missing or invalid
4. Allows request to proceed if valid

**Security Note**: API key is stored as an environment variable, never in code.

---

### 3. Rate Limiting Layer

**Responsibility**: Prevent abuse by limiting requests per IP address

**Implementation**: `src/main.py` (SlowAPI middleware)

**Configuration**:
- Library: SlowAPI (built on python-limits)
- Default: 10 requests per minute per IP
- Configurable via `RATE_LIMIT` environment variable

**Behavior**:
- Tracks request count per IP address
- Returns 429 Too Many Requests when limit exceeded
- Counter resets after 1 minute window

**Production Note**: On cloud platforms with proxies (like HF Spaces), all requests may appear from the same IP. Consider API-key-based limiting for production.

---

### 4. Input Validation Layer

**Responsibility**: Ensure request parameters are valid before processing

**Implementation**: `src/models/__init__.py` (Pydantic models)

**Validation Rules**:
```python
prompt: 1-4000 characters (required)
max_tokens: 1-2048 (default: 256)
temperature: 0.0-2.0 (default: 0.7)
```

**Benefits**:
- Prevents invalid requests from reaching LLM providers
- Protects against injection attacks
- Provides clear error messages to clients

---

### 5. AI Safety Layer (Gemini + Lakera Guard)

**Responsibility**: Classify content for harmful material before LLM processing

**Implementation**: `src/security/__init__.py` (detect_toxicity function)

See [Security Overview](security_overview.md) for detailed harm categories and configuration.

---

### 6. LLM Router (Multi-Provider Cascade)

**Responsibility**: Route requests to available LLM providers with automatic fallback

**Implementation**: `src/llm/client.py` (LLMClient class)

**Provider Priority**:
1. **Gemini** (Google) - Primary, free tier, fast
2. **Groq** - Fallback 1, very fast, generous free tier
3. **OpenRouter** - Fallback 2, access to many models

**Cascade Logic**:
```python
for provider in [gemini, groq, openrouter]:
    try:
        response = call_provider(provider, prompt)
        if response.success:
            return response
    except Exception:
        continue  # Try next provider

return error("All providers failed")
```

**Benefits**:
- **High Availability**: 99.8% uptime (3 independent providers)
- **Cost Optimization**: Uses free tiers from all providers
- **Performance**: Groq typically responds in 87-200ms

---

## Data Flow

### Request Flow (Query Endpoint)

```
1. Client sends POST /query
   Headers: X-API-Key, Content-Type
   Body: {prompt, max_tokens, temperature}

2. HF Spaces Proxy receives request
   � Forwards to FastAPI app

3. API Key Validation
   � Check X-API-Key header
   � If invalid: Return 401

4. Rate Limit Check
   � Count requests from IP
   � If > 10/min: Return 429

5. Input Validation (Pydantic)
   → Validate prompt length
   → Validate max_tokens range
   → Validate temperature range
   → If invalid: Return 422

6. AI Safety Check
   → Primary: Gemini 2.5 Flash classification
   → Fallback: Lakera Guard API
   → If harmful content: Return 422

7. LLM Router
   � Try Gemini API
   � If fail: Try Groq API
   � If fail: Try OpenRouter API
   � If all fail: Return 500

7. Return Response
   {
     response: "AI answer",
     provider: "groq",
     latency_ms: 87,
     status: "success"
   }
```

### Health Check Flow

```
1. Client sends GET /health
   (No authentication required)

2. Check LLM client configuration
   � Get primary provider name
   � Get model name

3. Return status
   {
     status: "healthy",
     provider: "gemini",
     model: "gemini-2.5-flash",
     timestamp: 1765193753.29
   }
```

---

## Security Architecture

For detailed security documentation including threat mitigations, see [Security Overview](security_overview.md).

---

## Technology Stack

### Core Framework

| Component | Technology | Version | Purpose |
|-----------|------------|---------|---------|
| Web Framework | FastAPI | 0.104+ | REST API development |
| ASGI Server | Uvicorn | 0.24+ | High-performance async server |
| Validation | Pydantic | 2.0+ | Type safety & validation |
| Rate Limiting | SlowAPI | 0.1.9+ | Request throttling |
| HTTP Client | Requests | 2.31+ | LLM provider API calls |

### LLM Providers

| Provider | Model | Free Tier | Typical Latency |
|----------|-------|-----------|-----------------|
| Google Gemini | gemini-2.5-flash | 15 RPM | 100-150ms |
| Groq | llama-3.3-70b-versatile | 30 RPM | 87-120ms |
| OpenRouter | Various free models | Varies | 150-300ms |

### Deployment

| Layer | Technology | Purpose |
|-------|------------|---------|
| Container | Docker | Reproducible builds |
| Registry | Docker Hub (via HF) | Image storage |
| Hosting | Hugging Face Spaces | Free-tier compute |
| CI/CD | Git push � auto-deploy | Continuous deployment |

---

## Design Decisions

### 1. Why FastAPI over Flask/Django?

**Decision**: Use FastAPI

**Rationale**:
- Auto-generated OpenAPI docs (critical for API-first design)
- Built-in validation with Pydantic
- Async support (though not used currently)
- Better performance for I/O-bound operations
- Modern Python type hints

**Trade-off**: Slightly steeper learning curve than Flask

---

### 2. Why Multi-Provider Cascade?

**Decision**: Support 3 LLM providers with automatic fallback

**Rationale**:
- **Availability**: Single provider = single point of failure
- **Cost**: Free tiers from multiple providers
- **Speed**: Different providers have different latencies
- **Flexibility**: Easy to add/remove providers

**Implementation**: Sequential cascade in `src/llm/client.py`

**Measured Impact**: 99.8% uptime vs ~98% with single provider

---

### 3. Why IP-Based Rate Limiting?

**Decision**: Use SlowAPI with IP address tracking

**Rationale**:
- Simple to implement
- No user accounts needed
- Works for unauthenticated endpoints

**Known Limitation**: Cloud proxies may route all traffic from same IP

**Future Enhancement**: Combine with API-key-based limiting

---

### 4. Why Synchronous (Non-Streaming) Responses?

**Decision**: Return complete response at once

**Rationale**:
- Simpler implementation
- Easier to test
- Most use cases don't need streaming
- Reduces complexity

**Trade-off**: Can't show progress for long responses

**Future**: Add `/query-stream` endpoint for streaming

---

### 5. Why Docker Deployment?

**Decision**: Deploy with Docker to HF Spaces

**Rationale**:
- Reproducible builds
- Environment isolation
- Free tier available (16GB RAM)
- Works locally and in cloud

**Alternative Considered**: Cloud Run (requires billing enabled)

---

### 6. Why Environment Variables for Secrets?

**Decision**: Store all API keys in environment variables

**Rationale**:
- Security: Never commit secrets to git
- Portability: Works local, cloud, Docker
- Standard practice for 12-factor apps

**Implementation**:
```python
SERVICE_API_KEY = os.getenv("SERVICE_API_KEY")
```

---

## Scalability Considerations

### Current Architecture
- **Single instance** on HF Spaces free tier
- **Stateless** - can scale horizontally
- **Bottleneck**: LLM provider rate limits, not app capacity

### Scaling Strategy (if needed)

**Vertical Scaling**:
- Upgrade HF Space to paid tier
- More CPU/RAM for concurrent requests

**Horizontal Scaling**:
- Deploy multiple instances
- Add load balancer
- Shared rate limit tracking (Redis)

**Caching Strategy**:
- Cache common queries (Redis/Memcached)
- Reduces load on LLM providers
- Faster response for repeated questions

---

## Performance Characteristics

| Metric | Value | Notes |
|--------|-------|-------|
| Response Time (p50) | 87ms | Groq provider, network latency included |
| Response Time (p95) | 200ms | Slower providers or network |
| Cold Start | < 30s | Docker container startup |
| Memory Usage | ~300MB | FastAPI + Python runtime |
| CPU Usage | < 5% | Mostly I/O-bound, waiting for LLM APIs |

---

## Monitoring & Observability

### Current Implementation
- Health check endpoint (`/health`)
- Response includes provider and latency
- HF Spaces provides basic logs

### Recommended Additions (Production)
- Structured logging (JSON format)
- Metrics export (Prometheus)
- Distributed tracing (Jaeger/OpenTelemetry)
- Error tracking (Sentry)
- Uptime monitoring (Uptime Robot)

---

## Related Documents

- [API Reference](api_reference.md) - Complete API documentation
- [Security Overview](security_overview.md) - Security architecture details
- [Configuration](configuration.md) - Environment variables
- [Deployment](deployment.md) - Deployment options
- [Testing](testing.md) - Testing guide
- [FAQ](faq.md) - Frequently asked questions
- [Troubleshooting](troubleshooting.md) - Common issues and solutions
