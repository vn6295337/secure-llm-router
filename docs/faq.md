# Frequently Asked Questions (FAQ)

> **Primary Responsibility:** Q&A format help with cross-references to detailed docs

This document answers common questions about the Enterprise AI Gateway.

## Table of Contents

1. [General Questions](#general-questions)
2. [Technical Questions](#technical-questions)
3. [Security Questions](#security-questions)
4. [Deployment Questions](#deployment-questions)
5. [Usage Questions](#usage-questions)
6. [Troubleshooting](#troubleshooting)

## General Questions

### What is the Enterprise AI Gateway?

The Enterprise AI Gateway is a production-ready API gateway that provides secure, reliable access to multiple Large Language Model (LLM) providers with built-in failover, security controls, and governance features. It acts as an intelligent intermediary between your applications and LLM providers.

### Why should I use the Enterprise AI Gateway instead of calling LLM providers directly?

The Enterprise AI Gateway provides several advantages over direct LLM calls:

1. **High Availability**: Automatic failover between multiple providers ensures 99.8% uptime
2. **Security**: Built-in authentication, rate limiting, input validation, and prompt injection protection
3. **Cost Optimization**: Intelligent routing and token budget enforcement reduce costs
4. **Simplified Integration**: Single API endpoint instead of managing multiple provider APIs
5. **Governance**: Centralized control over AI access and usage
6. **Performance**: Optimized response times and caching capabilities

### Is the Enterprise AI Gateway free to use?

Yes, the Enterprise AI Gateway is open-source and free to use. You only pay for the LLM provider APIs you use through the gateway. The gateway itself can be deployed on free-tier infrastructure like Hugging Face Spaces.

### Which LLM providers does the gateway support?

The gateway currently supports:
- **Google Gemini** (primary provider)
- **Groq** (secondary fallback)
- **OpenRouter** (tertiary fallback)

Additional providers can be added through custom integration.

## Technical Questions

### What programming language and framework are used?

The Enterprise AI Gateway is built with:
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

Configuration is done through environment variables. See [Configuration Guide](configuration.md) for the complete list of required and optional settings.

### What APIs does the gateway provide?

See [API Reference](api_reference.md) for complete documentation.

**Main endpoints:**
- `POST /query` - LLM query with security checks
- `POST /check-toxicity` - Content safety check
- `GET /health` - Service health status
- `GET /metrics` - Performance metrics

## Security Questions

For detailed security documentation, see [Security Overview](security_overview.md).

### How secure is the Enterprise AI Gateway?

The gateway implements 4 security layers (Authentication, Input Guard, AI Safety, Transport Security). See [Security Overview](security_overview.md) for the complete security architecture.

### How are API keys protected?

- Stored as environment variables (never in code)
- Constant-time comparison (prevents timing attacks)
- Easy rotation process

### What prompt injection attacks are detected?

The gateway uses a dual-layer detection system:

**Pattern-Based Detection** (Layer 2 - Input Guard):
- `ignore all previous instructions`
- `disregard all prior instructions`
- `you are now`
- `system:`

**AI-Based Detection** (Layer 3 - AI Safety):
- Gemini 2.5 Flash content classification
- Lakera Guard fallback for advanced jailbreak attempts

### What harmful content is blocked?

The AI Safety layer blocks sexually explicit content, hate speech, harassment, dangerous content, and civic integrity violations. See [Security Overview](security_overview.md) for the complete list of harm categories and how the Gemini + Lakera Guard fallback works.

### How does rate limiting work?

By default, the gateway implements IP-based rate limiting:
- 10 requests per minute per IP address
- Configurable through `RATE_LIMIT` environment variable
- Returns 429 status code when limit exceeded

Note: In cloud environments with proxies, all requests may appear from the same IP.

## Deployment Questions

### Where can I deploy the Enterprise AI Gateway?

The gateway can be deployed on:

1. **Hugging Face Spaces** (recommended for getting started)
2. **Docker Containers** (any cloud platform)
3. **Traditional Cloud Providers** (AWS, GCP, Azure)
4. **On-premises Servers**
5. **Kubernetes Clusters**

### How do I deploy to Hugging Face Spaces?

See [Deployment Guide - Hugging Face Spaces](deployment.md#hugging-face-spaces) for step-by-step instructions.

### Can I run the gateway in a serverless environment?

Yes, the gateway can be adapted for serverless deployment, though it works best with stateful deployments due to rate limiting requirements. For serverless, consider:
- Using API key-based rate limiting instead of IP-based
- Implementing external state management for rate limiting
- Adapting the cascade logic for short-lived executions

### How do I build a Docker image?

Build the Docker image from source:
```bash
git clone https://github.com/vn6295337/Enterprise-AI-Gateway.git
cd Enterprise-AI-Gateway
docker build -t enterprise-ai-gateway .
```

See [Deployment Guide](deployment.md) for complete Docker deployment instructions.

## Usage Questions

### How do I get started quickly?

See the [Quick Start](README.md#quick-start) in the documentation index.

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

For detailed troubleshooting, see [Troubleshooting Guide](troubleshooting.md).

**Quick fixes:**
- 401 errors → Check `X-API-Key` header and `SERVICE_API_KEY` env var
- 422 errors → Check prompt length (1-4000 chars) and injection patterns
- 500 errors → Check provider API keys and quotas
- Slow responses → Check provider status and network latency

## Getting More Help

1. Check the [Troubleshooting Guide](troubleshooting.md)
2. Review [GitHub Issues](https://github.com/vn6295337/Enterprise-AI-Gateway/issues)
3. Open a new issue with your question