# Configuration Guide

This document explains how to configure the LLM Secure Gateway for different environments and use cases.

## Environment Variables

The LLM Secure Gateway is configured using environment variables. These can be set in a `.env` file or in your deployment environment.

### Required Configuration

| Variable | Description | Default | Example |
|----------|-------------|---------|---------|
| `SERVICE_API_KEY` | API key for accessing the gateway | None | `sk-secure-key-12345` |

### LLM Provider Configuration

At least one LLM provider must be configured:

| Variable | Description | Default | Example |
|----------|-------------|---------|---------|
| `GEMINI_API_KEY` | Google Gemini API key | None | `AIzaSyB1234567890` |
| `GROQ_API_KEY` | Groq API key | None | `gsk_1234567890abcdef` |
| `OPENROUTER_API_KEY` | OpenRouter API key | None | `sk-or-1234567890abcdef` |

### Optional Configuration

| Variable | Description | Default | Example |
|----------|-------------|---------|---------|
| `RATE_LIMIT` | Rate limit per IP | `10/minute` | `5/minute` |
| `ALLOWED_ORIGINS` | CORS allowed origins | `*` | `https://yourapp.com` |
| `ENABLE_PROMPT_INJECTION_CHECK` | Enable prompt injection detection | `true` | `false` |
| `GEMINI_MODEL` | Gemini model to use | `gemini-2.0-flash-exp` | `gemini-pro` |
| `GROQ_MODEL` | Groq model to use | `llama-3.3-70b-versatile` | `llama3-70b-8192` |
| `OPENROUTER_MODEL` | OpenRouter model to use | `google/gemini-2.0-flash-exp:free` | `openai/gpt-3.5-turbo` |

## Configuration Files

### .env File

Create a `.env` file in the project root with the following format:

```bash
# Service Configuration
SERVICE_API_KEY=your_secure_api_key_here

# LLM Provider API Keys (at least one required)
GEMINI_API_KEY=your_gemini_api_key
GROQ_API_KEY=your_groq_api_key
OPENROUTER_API_KEY=your_openrouter_api_key

# Optional Configuration
RATE_LIMIT=10/minute
ALLOWED_ORIGINS=*
ENABLE_PROMPT_INJECTION_CHECK=true
GEMINI_MODEL=gemini-2.0-flash-exp
GROQ_MODEL=llama-3.3-70b-versatile
OPENROUTER_MODEL=google/gemini-2.0-flash-exp:free
```

### Docker Configuration

When using Docker, you can pass environment variables using the `-e` flag:

```bash
docker run -d \
  -e SERVICE_API_KEY=your_secure_api_key \
  -e GEMINI_API_KEY=your_gemini_api_key \
  -e GROQ_API_KEY=your_groq_api_key \
  -e RATE_LIMIT=5/minute \
  -p 8000:8000 \
  llm-secure-gateway
```

Or use a Docker environment file:

```bash
docker run -d \
  --env-file .env \
  -p 8000:8000 \
  llm-secure-gateway
```

## Deployment-Specific Configuration

### Hugging Face Spaces

When deploying to Hugging Face Spaces, set the environment variables in the Space settings under "Repository secrets":

1. Go to your Space settings
2. Navigate to "Repository secrets"
3. Add the following secrets:
   - `SERVICE_API_KEY`
   - `GEMINI_API_KEY`
   - `GROQ_API_KEY`
   - `OPENROUTER_API_KEY`

### Production Considerations

1. **API Key Security**: Never commit API keys to version control
2. **Rate Limiting**: Adjust rate limits based on your expected usage
3. **CORS**: Restrict allowed origins in production
4. **Logging**: Enable appropriate logging levels
5. **Monitoring**: Set up monitoring for your deployment

## Model Selection

### Default Models

The gateway uses optimized models by default:

- **Gemini**: `gemini-2.0-flash-exp` - Fast and capable model
- **Groq**: `llama-3.3-70b-versatile` - High-performance model
- **OpenRouter**: `google/gemini-2.0-flash-exp:free` - Free access to Gemini

### Changing Models

To use different models, set the corresponding environment variables:

```bash
GEMINI_MODEL=gemini-pro
GROQ_MODEL=llama3-70b-8192
OPENROUTER_MODEL=openai/gpt-4
```

Note: Different models may have different pricing, rate limits, and capabilities.

## Security Configuration

### API Key Best Practices

1. Generate a strong, random API key
2. Rotate keys periodically
3. Use different keys for different clients/environments
4. Monitor key usage

### Rate Limiting

Adjust rate limits based on your needs:

```bash
# More restrictive
RATE_LIMIT=5/hour

# Less restrictive
RATE_LIMIT=100/minute

# Multiple limits
RATE_LIMIT=10/minute;1000/day
```

### Prompt Injection Detection

Enable/disable prompt injection detection:

```bash
# Enable (recommended)
ENABLE_PROMPT_INJECTION_CHECK=true

# Disable (not recommended)
ENABLE_PROMPT_INJECTION_CHECK=false
```

## Testing Configuration

For testing purposes, you can use placeholder values:

```bash
# Test configuration
SERVICE_API_KEY=test-key-12345
GEMINI_API_KEY=test-gemini-key
GROQ_API_KEY=test-groq-key
OPENROUTER_API_KEY=test-openrouter-key
RATE_LIMIT=100/minute
```

Note: These won't work with actual LLM providers but can be useful for testing the gateway itself.