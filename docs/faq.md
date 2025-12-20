# Frequently Asked Questions (FAQ)

This document answers common questions about the LLM Secure Gateway.

## Table of Contents

1. [General Questions](#general-questions)
2. [Technical Questions](#technical-questions)
3. [Security Questions](#security-questions)
4. [Deployment Questions](#deployment-questions)
5. [Usage Questions](#usage-questions)
6. [Troubleshooting](#troubleshooting)

## General Questions

### What is the LLM Secure Gateway?

The LLM Secure Gateway is a production-ready API gateway that provides secure, reliable access to multiple Large Language Model (LLM) providers with built-in failover, security controls, and governance features. It acts as an intelligent intermediary between your applications and LLM providers.

### Why should I use the LLM Secure Gateway instead of calling LLM providers directly?

The LLM Secure Gateway provides several advantages over direct LLM calls:

1. **High Availability**: Automatic failover between multiple providers ensures 99.8% uptime
2. **Security**: Built-in authentication, rate limiting, input validation, and prompt injection protection
3. **Cost Optimization**: Intelligent routing and token budget enforcement reduce costs
4. **Simplified Integration**: Single API endpoint instead of managing multiple provider APIs
5. **Governance**: Centralized control over AI access and usage
6. **Performance**: Optimized response times and caching capabilities

### Is the LLM Secure Gateway free to use?

Yes, the LLM Secure Gateway is open-source and free to use. You only pay for the LLM provider APIs you use through the gateway. The gateway itself can be deployed on free-tier infrastructure like Hugging Face Spaces.

### Which LLM providers does the gateway support?

The gateway currently supports:
- **Google Gemini** (primary provider)
- **Groq** (secondary fallback)
- **OpenRouter** (tertiary fallback)

Additional providers can be added through custom integration.

## Technical Questions

### What programming language and framework are used?

The LLM Secure Gateway is built with:
- **Python 3.8+** as the primary language
- **FastAPI** as the web framework
- **Uvicorn** as the ASGI server
- **Pydantic** for data validation
- **SlowAPI** for rate limiting

### How does the multi-provider failover work?

The gateway implements a sequential cascade approach:

1. Try primary provider (Gemini)
2. If failed, try secondary provider (Groq)
3. If failed, try tertiary provider (OpenRouter)
4. Return error if all providers fail

Each provider attempt includes timeout handling and error recovery.

### What are the system requirements?

Minimum requirements:
- Python 3.8 or higher
- 512 MB RAM
- 100 MB disk space
- Internet connectivity

Recommended for production:
- Python 3.11+
- 1 GB RAM
- 500 MB disk space
- Stable broadband connection

### How is the gateway configured?

Configuration is done through environment variables:

```bash
SERVICE_API_KEY=your_secure_api_key
GEMINI_API_KEY=your_gemini_api_key
GROQ_API_KEY=your_groq_api_key
OPENROUTER_API_KEY=your_openrouter_api_key
RATE_LIMIT=10/minute
ALLOWED_ORIGINS=*
```

### What APIs does the gateway provide?

The gateway exposes three main endpoints:
- `GET /health` - Health check endpoint
- `POST /query` - Main LLM query endpoint
- `GET /` - Interactive dashboard (UI only)

See the [API Reference](api_reference.md) for detailed documentation.

## Security Questions

### How secure is the LLM Secure Gateway?

The gateway implements multiple security layers:

1. **Authentication**: API key validation with constant-time comparison
2. **Rate Limiting**: IP-based request throttling
3. **Input Validation**: Strict validation of all request parameters
4. **Prompt Injection Protection**: Pattern-based detection of malicious prompts
5. **Transport Security**: HTTPS encryption (provided by deployment platform)
6. **Environment Isolation**: API keys stored as environment variables

### How are API keys protected?

API keys are protected through:

1. **Environment Variables**: Never stored in code or version control
2. **Constant-Time Comparison**: Prevents timing attacks
3. **Secure Generation**: Recommendations for strong, random keys
4. **Easy Rotation**: Simple process for changing keys

### What prompt injection attacks are detected?

The gateway detects common prompt injection patterns including:
- `ignore all previous instructions`
- `disregard all prior instructions`
- `you are now`
- `system:`

The detection system can be extended with additional patterns as needed.

### How does rate limiting work?

By default, the gateway implements IP-based rate limiting:
- 10 requests per minute per IP address
- Configurable through `RATE_LIMIT` environment variable
- Returns 429 status code when limit exceeded

Note: In cloud environments with proxies, all requests may appear from the same IP.

## Deployment Questions

### Where can I deploy the LLM Secure Gateway?

The gateway can be deployed on:

1. **Hugging Face Spaces** (recommended for getting started)
2. **Docker Containers** (any cloud platform)
3. **Traditional Cloud Providers** (AWS, GCP, Azure)
4. **On-premises Servers**
5. **Kubernetes Clusters**

### How do I deploy to Hugging Face Spaces?

1. Create a new Space at [https://huggingface.co/new-space](https://huggingface.co/new-space)
2. Choose "Docker" as the SDK
3. Select a Docker image (e.g., `python:3.11-slim`)
4. Add your repository URL
5. In Space settings, add the required secrets:
   - `SERVICE_API_KEY`
   - `GEMINI_API_KEY`
   - `GROQ_API_KEY`
   - `OPENROUTER_API_KEY`

### Can I run the gateway in a serverless environment?

Yes, the gateway can be adapted for serverless deployment, though it works best with stateful deployments due to rate limiting requirements. For serverless, consider:
- Using API key-based rate limiting instead of IP-based
- Implementing external state management for rate limiting
- Adapting the cascade logic for short-lived executions

### What Docker images are available?

Official Docker images are available on Docker Hub:
- `llm-secure-gateway:latest` - Latest stable release
- `llm-secure-gateway:1.0` - Specific version tags
- `llm-secure-gateway:dev` - Development builds

You can also build from source:
```bash
docker build -t llm-secure-gateway .
```

## Usage Questions

### How do I get started quickly?

1. Obtain API keys from at least one LLM provider
2. Clone the repository: `git clone https://github.com/vn6295337/LLM-secure-gateway.git`
3. Install dependencies: `pip install -r requirements.txt`
4. Configure environment variables
5. Run the server: `uvicorn src.main:app --host 0.0.0.0 --port 8000`
6. Test with: `curl http://localhost:8000/health`

### What's the format for querying the LLM?

Send a POST request to `/query` with this JSON format:

```json
{
  "prompt": "Your question here",
  "max_tokens": 256,
  "temperature": 0.7
}
```

Include your API key in the `X-API-Key` header.

### How do I handle errors from the gateway?

The gateway returns standard HTTP status codes:
- `200`: Success
- `401`: Invalid or missing API key
- `422`: Invalid request parameters or blocked prompt
- `429`: Rate limit exceeded
- `500`: All LLM providers failed

Check the response body for detailed error messages.

### Can I customize the prompt injection detection patterns?

Yes, the injection patterns are defined in `src/main.py`:

```python
INJECTION_PATTERNS = [
    r"ignore\s+(all\s+)?(previous|above|prior)\s+instructions?",
    r"disregard\s+(all\s+)?(previous|above|prior)\s+instructions?",
    r"you\s+are\s+now",
    r"system\s*:\s*",
]
```

You can modify these patterns or add new ones as needed.

## Troubleshooting

### I'm getting a 401 Unauthorized error

Check that:
1. You're including the `X-API-Key` header
2. Your API key is correctly configured in the environment
3. Your API key matches exactly (no extra spaces)

### I'm getting a 422 Validation Error

Check that:
1. Your prompt is between 1-4000 characters
2. `max_tokens` is between 1-2048
3. `temperature` is between 0.0-2.0
4. Your prompt doesn't contain injection patterns

### I'm getting a 500 Internal Server Error

This indicates all LLM providers failed. Check:
1. That your provider API keys are valid
2. That you have sufficient quotas with your providers
3. Provider status pages for service outages
4. Network connectivity to provider endpoints

### The gateway won't start

Check that:
1. All required environment variables are set
2. Python dependencies are installed
3. Port is not already in use
4. Sufficient system resources are available

### Performance seems slow

Consider:
1. Provider response times (some providers are naturally slower)
2. Network latency between gateway and providers
3. Request complexity and token count
4. Concurrent request load

### How do I monitor the gateway?

The gateway provides:
1. Health check endpoint (`/health`)
2. Response metadata (provider, latency)
3. Structured logging (when enabled)
4. Dashboard UI for interactive monitoring

For production, consider implementing:
- Prometheus metrics endpoint
- Log aggregation
- Performance monitoring
- Alerting for errors and performance issues

## Getting More Help

If your question isn't answered here:

1. Check the [Documentation](README.md)
2. Review the [GitHub Issues](https://github.com/vn6295337/LLM-secure-gateway/issues)
3. Open a new issue with your question
4. Join community discussions (when available)