# Quickstart Guide

Get up and running with the LLM Secure Gateway in minutes.

## Prerequisites

- Python 3.8 or higher
- Git
- At least one LLM provider API key (Google Gemini, Groq, or OpenRouter)

## Step 1: Get API Keys

Obtain API keys from at least one provider:

1. **Google Gemini**: [https://ai.google.dev/](https://ai.google.dev/)
2. **Groq**: [https://console.groq.com/](https://console.groq.com/)
3. **OpenRouter**: [https://openrouter.ai/](https://openrouter.ai/)

## Step 2: Clone and Setup

```bash
# Clone the repository
git clone https://github.com/vn6295337/LLM-secure-gateway.git
cd LLM-secure-gateway

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Step 3: Configure

```bash
# Copy example configuration
cp .env.example .env

# Edit .env with your API keys
nano .env
```

Add at least one API key:
```bash
SERVICE_API_KEY=sk-your-secure-api-key-here
GEMINI_API_KEY=your-gemini-api-key  # Optional
GROQ_API_KEY=your-groq-api-key      # Optional
OPENROUTER_API_KEY=your-openrouter-api-key  # Optional
```

## Step 4: Run

```bash
# Start the server
uvicorn src.main:app --host 0.0.0.0 --port 8000
```

## Step 5: Test

### Health Check

```bash
curl http://localhost:8000/health
```

Expected response:
```json
{
  "status": "healthy",
  "provider": "gemini",
  "timestamp": 1700000000.123456
}
```

### Query the LLM

```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -H "X-API-Key: sk-your-secure-api-key-here" \
  -d '{
    "prompt": "What is artificial intelligence?",
    "max_tokens": 100,
    "temperature": 0.7
  }'
```

Expected response:
```json
{
  "response": "Artificial Intelligence (AI) refers to...",
  "provider": "groq",
  "latency_ms": 87,
  "status": "success",
  "error": null
}
```

## Step 6: Explore

### API Documentation

Visit `http://localhost:8000/docs` for interactive API documentation.

### Dashboard

Visit `http://localhost:8000` to access the interactive dashboard.

## Next Steps

1. **Configure for Production**: 
   - Set specific `ALLOWED_ORIGINS`
   - Adjust `RATE_LIMIT` as needed
   - Use strong, random API keys

2. **Deploy**: 
   - See [Deployment Guide](deployment.md) for deployment options
   - Consider cloud platforms like Hugging Face Spaces

3. **Customize**:
   - Modify prompt injection patterns in `src/main.py`
   - Add new LLM providers in `src/config.py`
   - Adjust validation rules in the Pydantic models

## Troubleshooting

### Common Issues

1. **401 Unauthorized**: Check that your `SERVICE_API_KEY` is set correctly and used in requests.

2. **422 Validation Error**: Ensure your prompt is between 1-4000 characters and other parameters are within valid ranges.

3. **500 Internal Server Error**: Verify your LLM provider API keys are valid and have sufficient quotas.

### Get Help

- Check the [Troubleshooting Guide](troubleshooting.md)
- Review application logs for detailed error messages
- Visit the [GitHub Issues](https://github.com/vn6295337/LLM-secure-gateway/issues) page

## Example Use Cases

### Customer Support Bot

```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -H "X-API-Key: sk-your-secure-api-key-here" \
  -d '{
    "prompt": "How do I reset my password?",
    "max_tokens": 150,
    "temperature": 0.5
  }'
```

### Content Generation

```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -H "X-API-Key: sk-your-secure-api-key-here" \
  -d '{
    "prompt": "Write a short blog post about the benefits of AI in healthcare",
    "max_tokens": 500,
    "temperature": 0.8
  }'
```

## Security Notes

- Never commit API keys to version control
- Use HTTPS in production environments
- Regularly rotate your API keys
- Monitor usage for unusual patterns
- Review the [Security Overview](security_overview.md) for more details

## Feedback

Have questions or feedback? 

- Open an issue on [GitHub](https://github.com/vn6295337/LLM-secure-gateway/issues)
- Contact the maintainers
- Contribute improvements via pull requests

Enjoy using the LLM Secure Gateway!