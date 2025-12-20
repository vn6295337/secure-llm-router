# API Reference

This document provides a complete reference for the LLM Secure Gateway API endpoints.

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

#### `DASHBOARD_HTML`
HTML content for the interactive dashboard.

### security/\_\_init\_\_.py
Security utilities for authentication and prompt validation.

#### `detect_prompt_injection(prompt: str) -> bool`
Detect potential prompt injection attacks using regex patterns.

#### `validate_api_key(api_key: str) -> str`
Validate API key for request authentication.

### models/\_\_init\_\_.py
Pydantic models for request/response validation.

#### `QueryRequest`
Model for query requests with prompt, max_tokens, and temperature.

#### `QueryResponse`
Model for query responses with response content, provider info, and metadata.

#### `HealthResponse`
Model for health check responses.

### api/routes.py
API route definitions.

#### `/` (GET)
Serves the Interactive Gateway Demo Dashboard.

#### `/health` (GET)
Health check endpoint that returns the status of the service.

#### `/query` (POST)
Query endpoint that processes LLM requests with security and fallback protocols.

### llm/client.py
LLM client with multi-provider fallback functionality.

#### `LLMClient`
Class that manages connections to multiple LLM providers.

#### `call_llm_provider(provider_name: str, api_key: str, model: str, prompt: str, max_tokens: int, temperature: float)`
Call a specific LLM provider with the given parameters.

#### `query_llm_cascade(prompt: str, max_tokens: int, temperature: float)`
Query LLM with cascade fallback across providers.

## Environment Variables

### Required
- `SERVICE_API_KEY`: API key for authenticating requests

### Optional LLM Provider Keys
- `GEMINI_API_KEY`: API key for Google Gemini
- `GROQ_API_KEY`: API key for Groq
- `OPENROUTER_API_KEY`: API key for OpenRouter

### Configuration
- `RATE_LIMIT`: Rate limiting configuration (default: "10/minute")
- `ALLOWED_ORIGINS`: Comma-separated list of allowed origins (default: "*")
- `ENABLE_PROMPT_INJECTION_CHECK`: Enable prompt injection detection (default: "true")

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