---
title: LLM Secure Gateway
emoji: 🔐
colorFrom: blue
colorTo: purple
sdk: docker
pinned: false
---

# LLM Secure Gateway

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Enterprise-grade REST API for secure, multi-provider LLM access with automatic failover.**

| Resource | Link |
|----------|------|
| Live Demo | [huggingface.co/spaces/vn6295337/Enterprise-AI-Gateway](https://huggingface.co/spaces/vn6295337/Enterprise-AI-Gateway) |
| Demo Video | [github.com/vn6295337/Enterprise-AI-Gateway/issues/2](http://github.com/vn6295337/Enterprise-AI-Gateway/issues/2) |
| Business User Guide | [BUSINESS_README.md](BUSINESS_README.md) |

---

## Quick Start

```bash
git clone https://github.com/your-username/LLM-secure-gateway.git
cd LLM-secure-gateway
pip install -r requirements.txt

# Set at least one provider API key
export GEMINI_API_KEY="your-key"      # or
export GROQ_API_KEY="your-key"        # or
export OPENROUTER_API_KEY="your-key"

./start-app.sh
```

---

## Architecture

```
Request → [Auth] → [Rate Limit] → [Input Validation] → [Injection Check] → [PII Check]
                                                                              ↓
Response ← [Provider 1: Gemini] ← fails? → [Provider 2: Groq] ← fails? → [Provider 3: OpenRouter]
```

---

## API Endpoints

| Endpoint | Method | Auth | Description |
|----------|--------|------|-------------|
| `/` | GET | No | Interactive dashboard |
| `/health` | GET | No | Health check |
| `/query` | POST | Yes | LLM query with cascade fallback |
| `/metrics` | GET | No | Gateway metrics |
| `/providers` | GET | No | Provider config and pricing |
| `/batch/resilience` | POST | Yes | Batch resilience testing |
| `/batch/security` | POST | No | Batch PII/injection testing |

### Query Example

```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -H "X-API-Key: YOUR_API_KEY" \
  -d '{"prompt": "What is machine learning?", "max_tokens": 150}'
```

**Response:**
```json
{
  "response": "Machine learning is...",
  "provider": "gemini",
  "latency_ms": 120,
  "cascade_path": [{"provider": "gemini", "status": "success", "latency_ms": 120}],
  "cost_estimate_usd": 0.000015
}
```

---

## Development

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python -m pytest tests
```

---

## Deployment

### Docker
```bash
docker build -t llm-secure-gateway .
docker run -p 8000:8000 llm-secure-gateway
```

### Hugging Face Spaces
1. Create Space at [huggingface.co/new-space](https://huggingface.co/new-space)
2. Select "Docker" SDK
3. Add repository as source
4. Configure Secrets with API keys

---

## Documentation

| Doc | Description |
|-----|-------------|
| [API Reference](docs/api_reference.md) | Complete endpoint documentation |
| [Architecture](docs/architecture.md) | System design |
| [Case Study](docs/case_study.md) | Business value analysis |

---

## License

MIT License
