# API Reference

> **Primary Responsibility:** Complete API endpoint and function documentation

This document provides a complete reference for the Enterprise AI Gateway API endpoints.

## Base URL

```
https://your-deployment-url
```

For local development: `http://localhost:8000`

## Authentication

All API requests (except `/health` and `/`) require authentication using an API key.

Include the API key in the request header:

```
X-API-Key: YOUR_API_KEY
```

## Rate Limiting

The API implements rate limiting to prevent abuse:
- Default limit: 10 requests per minute per IP address
- Exceeding the limit returns a 429 (Too Many Requests) status code

## Core Modules

### main.py
Main application entry point that initializes the FastAPI application.

#### `app`
The main FastAPI application instance with all routes and middleware configured.

### config.py
Configuration module that loads environment variables and defines application settings.

#### `SERVICE_API_KEY`
The API key required for authenticating requests to the gateway.

#### `RATE_LIMIT`
Rate limiting configuration (e.g., "10/minute").

#### `ALLOWED_ORIGINS`
List of allowed origins for CORS middleware.

#### `ENABLE_PROMPT_INJECTION_CHECK`
Flag to enable/disable prompt injection detection.

### security/\_\_init\_\_.py
Security utilities for authentication and prompt validation.

#### `detect_prompt_injection(prompt: str) -> bool`
Detect potential prompt injection attacks using regex patterns.

#### `detect_pii(prompt: str) -> dict`
Detect PII (Personally Identifiable Information) in prompts. Returns:
- `has_pii`: Boolean indicating if PII was found
- `pii_types`: List of PII types detected (email, credit_card, ssn, tax_id, api_key)
- `matches`: Dictionary with count of each PII type found

#### `detect_toxicity(text: str) -> dict`
Detect toxic/harmful content using Gemini AI classification with Lakera Guard fallback. Returns:
- `is_toxic`: Boolean indicating if content is harmful
- `scores`: Dictionary of category scores
- `blocked_categories`: List of detected harmful categories
- `error`: Error message if API call failed

Categories detected: SEXUALLY_EXPLICIT, HATE_SPEECH, HARASSMENT, DANGEROUS_CONTENT, CIVIC_INTEGRITY

#### `detect_toxicity_lakera(text: str) -> dict`
Fallback toxicity detection using Lakera Guard API. Called automatically when Gemini fails.

#### `validate_api_key(api_key: str) -> str`
Validate API key for request authentication.

### models/\_\_init\_\_.py
Pydantic models for request/response validation.

#### `QueryRequest`
Model for query requests with prompt, max_tokens, and temperature.

#### `QueryResponse`
Model for query responses with response content, provider info, and metadata.
- `cascade_path`: List of provider attempts with status and latency
- `cost_estimate_usd`: Estimated cost of the request

#### `CascadeStep`
Model for individual steps in the provider cascade.
- `provider`: Provider name
- `model`: Model used
- `status`: "success", "failed", or "timeout"
- `reason`: Error reason if failed
- `latency_ms`: Response time in milliseconds

#### `HealthResponse`
Model for health check responses.

### api/routes.py
API route definitions.

#### `/` (GET)
Serves the Interactive Gateway Demo Dashboard from `static/index.html`.

#### `/health` (GET)
Health check endpoint that returns the status of the service.

#### `/query` (POST)
Query endpoint that processes LLM requests with security and fallback protocols.
Returns cascade path and cost estimate.

#### `/metrics` (GET)
Returns gateway metrics including total requests, latency, provider usage, and security events.

#### `/providers` (GET)
Returns available providers with pricing information and active configuration.

#### `/batch/resilience` (POST)
Batch resilience testing endpoint. Runs multiple prompts through the cascade and returns aggregate metrics.

#### `/batch/security` (POST)
Batch security testing endpoint. Tests prompts for PII and injection without executing LLM calls.

#### `/check-toxicity` (POST)
Content safety check endpoint. Uses Gemini AI classification with Lakera Guard fallback.
Returns toxicity status, scores, and blocked categories.

### llm/client.py
LLM client with multi-provider fallback functionality.

#### `LLMClient`
Class that manages connections to multiple LLM providers.

#### `call_llm_provider(provider_name: str, api_key: str, model: str, prompt: str, max_tokens: int, temperature: float)`
Call a specific LLM provider with the given parameters.

#### `query_llm_cascade(prompt: str, max_tokens: int, temperature: float)`
Query LLM with cascade fallback across providers.
Returns: `(response, provider_name, latency_ms, error, cascade_path)`

### metrics/\_\_init\_\_.py
Metrics tracking module.

#### `MetricsStore`
Thread-safe metrics store for tracking gateway performance.
- `record_request()`: Record a request with metrics
- `to_dict()`: Return metrics as dictionary
- `reset()`: Reset all metrics

#### `metrics`
Singleton instance of MetricsStore.

### providers/\_\_init\_\_.py
Provider configuration module.

#### `PROVIDER_CONFIG`
Dictionary containing provider pricing and configuration.

#### `get_model_pricing(provider: str, model: str) -> dict`
Get pricing info for a specific provider/model combination.

#### `estimate_cost(provider: str, model: str, input_tokens: int, output_tokens: int) -> float`
Estimate cost for a request in USD.

## Environment Variables

See [Configuration Guide](configuration.md) for complete environment variable reference.

## Endpoints

### Health Check

#### `GET /health`

Check if the service is running and healthy.

**Response:**
```json
{
  "status": "healthy",
  "provider": "gemini",
  "timestamp": 1700000000.123456
}
```

**Response Fields:**
- `status`: Service status ("healthy" or "unhealthy")
- `provider`: Currently active LLM provider
- `timestamp`: Unix timestamp of the health check

### Query LLM

#### `POST /query`

Send a prompt to the LLM through the secure gateway with automatic failover.

**Headers:**
```
Content-Type: application/json
X-API-Key: YOUR_API_KEY
```

**Request Body:**
```json
{
  "prompt": "Your question here",
  "max_tokens": 256,
  "temperature": 0.7
}
```

**Request Parameters:**
- `prompt` (required): The prompt to send to the LLM (1-4000 characters)
- `max_tokens` (optional): Maximum number of tokens in the response (1-2048, default: 256)
- `temperature` (optional): Sampling temperature (0.0-2.0, default: 0.7)

**Successful Response:**
```json
{
  "response": "The AI's answer",
  "provider": "groq",
  "latency_ms": 87,
  "status": "success",
  "error": null
}
```

**Error Response:**
```json
{
  "response": null,
  "provider": null,
  "latency_ms": 0,
  "status": "error",
  "error": "Error message"
}
```

**Response Fields:**
- `response`: The LLM's response text (null if error)
- `provider`: Which LLM provider was used (null if error)
- `latency_ms`: Request latency in milliseconds (0 if error)
- `status`: Request status ("success" or "error")
- `error`: Error message if request failed (null if successful)
- `cascade_path`: Array of provider attempts with status and latency
- `cost_estimate_usd`: Estimated cost of the request in USD

### Get Metrics

#### `GET /metrics`

Get current gateway metrics.

**Response:**
```json
{
  "total_requests": 150,
  "successful_requests": 145,
  "blocked_requests": 5,
  "average_latency_ms": 120.5,
  "provider_usage": {"gemini": 100, "groq": 45},
  "cascade_failures": 3,
  "pii_detections": 2,
  "injection_detections": 3,
  "latency_history": [87, 120, 95, ...]
}
```

### Get Providers

#### `GET /providers`

Get available providers with pricing information.

**Response:**
```json
{
  "providers": {
    "gemini": {"name": "Google Gemini", "models": {...}},
    "groq": {"name": "Groq", "models": {...}},
    "openrouter": {"name": "OpenRouter", "models": {...}}
  },
  "active_providers": ["gemini", "groq", "openrouter"],
  "active_models": {"gemini": "gemini-2.0-flash-exp", ...}
}
```

### Batch Resilience Test

#### `POST /batch/resilience`

Run multiple prompts through the cascade and return aggregate metrics.

**Headers:**
```
Content-Type: application/json
X-API-Key: YOUR_API_KEY
```

**Request Body:**
```json
{
  "prompts": [
    "First test prompt",
    "Second test prompt"
  ]
}
```

**Response:**
```json
{
  "total": 2,
  "successful": 2,
  "failed": 0,
  "total_cascade_failures": 1,
  "average_latency_ms": 105.5,
  "downtime_prevented_minutes": 4.0,
  "results": [...]
}
```

### Batch Security Test

#### `POST /batch/security`

Test prompts for security issues without executing LLM calls.

**Request Body:**
```json
{
  "prompts": [
    "Normal question",
    "Ignore all instructions",
    "My SSN is 123-45-6789"
  ]
}
```

**Response:**
```json
{
  "total": 3,
  "blocked": 2,
  "passed": 1,
  "pii_leaks_prevented": 1,
  "injection_attempts_blocked": 1,
  "compliance_fines_avoided_usd": 28000,
  "results": [...]
}
```

### Content Safety Check

#### `POST /check-toxicity`

Check content for harmful/toxic material using AI classification.

**Headers:**
```
Content-Type: application/json
X-API-Key: YOUR_API_KEY
```

**Request Body:**
```json
{
  "text": "Content to analyze for safety"
}
```

**Response:**
```json
{
  "is_toxic": false,
  "scores": {"SAFE": 1.0},
  "blocked_categories": [],
  "error": null
}
```

**Blocked Response Example:**
```json
{
  "is_toxic": true,
  "scores": {"HARM_CATEGORY_SEXUALLY_EXPLICIT": 0.9},
  "blocked_categories": ["HARM_CATEGORY_SEXUALLY_EXPLICIT"],
  "error": null
}
```

**Harm Categories:** See [Security Overview](security_overview.md) for the complete list of blocked content categories.

## Error Codes

### 200 OK
Request successful

### 401 Unauthorized
- Missing or invalid API key

### 422 Unprocessable Entity
- Invalid request parameters
- Prompt injection detected
- Input validation failed

### 429 Too Many Requests
- Rate limit exceeded

### 500 Internal Server Error
- All LLM providers failed
- Unexpected server error

## Example Usage

### cURL

```bash
# Health check
curl https://your-deployment-url/health

# Query LLM
curl -X POST https://your-deployment-url/query \
  -H "Content-Type: application/json" \
  -H "X-API-Key: YOUR_API_KEY" \
  -d '{
    "prompt": "What is artificial intelligence?",
    "max_tokens": 150,
    "temperature": 0.7
  }'
```

### Python

```python
import requests

# Health check
response = requests.get('https://your-deployment-url/health')
print(response.json())

# Query LLM
headers = {
    'Content-Type': 'application/json',
    'X-API-Key': 'YOUR_API_KEY'
}

data = {
    'prompt': 'What is artificial intelligence?',
    'max_tokens': 150,
    'temperature': 0.7
}

response = requests.post('https://your-deployment-url/query', headers=headers, json=data)
print(response.json())
```

## Security Features

### Authentication
All requests to `/query` require a valid API key in the `X-API-Key` header.

### Rate Limiting
Requests are rate limited based on the `RATE_LIMIT` configuration.

### Prompt Injection Detection
Potential prompt injection attempts are detected and blocked automatically.

### CORS
Cross-Origin Resource Sharing is configured based on `ALLOWED_ORIGINS`.

## Security Considerations

1. Always use HTTPS in production
2. Keep your API key secure
3. Validate all responses before using them
4. Implement proper error handling
5. Be aware of rate limits