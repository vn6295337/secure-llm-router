---
title: Enterprise-AI-Gateway
emoji: 🔐
colorFrom: blue
colorTo: purple
sdk: docker
pinned: false
short_description: "Resilient AI Mesh - Secure, Cost-Aware, Speed-Optimized"
---

# Enterprise-AI-Gateway

**Resilient AI mesh: secure, cost-aware, speed-optimized gateway for LLM applications.**

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

| Resource | Link |
|----------|------|
| Live Demo | [huggingface.co/spaces/vn6295337/Enterprise-AI-Gateway](https://huggingface.co/spaces/vn6295337/Enterprise-AI-Gateway) |
| Demo Video | [github.com/vn6295337/Enterprise-AI-Gateway/issues/4](http://github.com/vn6295337/Enterprise-AI-Gateway/issues/4) |
| Business Guide | [BUSINESS_README.md](BUSINESS_README.md) |

---

## The Problem

Enterprise AI adoption faces three critical barriers:

- **Reliability Risk** — Single-provider dependencies create unacceptable downtime. When your LLM provider goes down, operations halt.
- **Security Exposure** — LLM applications are vulnerable to prompt injection, PII leaks, and harmful content generation.
- **Compliance Uncertainty** — Regulated industries need audit trails, content moderation, and demonstrable safety controls.

## The Solution

A security-first API gateway that sits between your applications and LLM providers:

- **Multi-provider failover** — Automatic cascade through 3 providers ensures 99.8% uptime
- **4-layer security pipeline** — Auth, input validation, AI safety, and rate limiting
- **Compliance-ready** — Full audit trails with cascade paths, latency, and cost tracking

## Why This Matters

Most enterprise AI deployments fail not from bad models, but from lack of reliability and security controls. This architecture demonstrates how to build production-grade AI infrastructure—a pattern applicable to any domain requiring consistent, safe LLM access.

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER REQUEST                            │
└─────────────────────────────┬───────────────────────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  LAYER 1: AUTH & RATE LIMITING                                  │
│  • API Key validation (X-API-Key header)                        │
│  • DDoS protection (configurable rate limits)                   │
│  • Token limit enforcement (4096 max)                           │
└─────────────────────────────┬───────────────────────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  LAYER 2: INPUT GUARD                                           │
│  • Prompt injection detection (regex patterns)                  │
│  • PII detection (SSN, credit cards, emails, API keys)          │
│  • SQL/Command injection patterns                               │
└─────────────────────────────┬───────────────────────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  LAYER 3: AI SAFETY                                             │
│  Primary: Gemini 2.5 Flash classification                       │
│  Fallback: Lakera Guard API                                     │
│  Categories: Sexual, Hate, Harassment, Dangerous, Civic         │
└─────────────────────────────┬───────────────────────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  LAYER 4: LLM ROUTER (CASCADE FAILOVER)                         │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────────┐     │
│  │   Gemini    │───▶│    Groq     │───▶│   OpenRouter    │     │
│  │  (Primary)  │    │ (Fallback 1)│    │  (Fallback 2)   │     │
│  └─────────────┘    └─────────────┘    └─────────────────┘     │
└─────────────────────────────┬───────────────────────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                        AI RESPONSE                              │
│  + provider, latency_ms, cascade_path, cost_estimate_usd        │
└─────────────────────────────────────────────────────────────────┘
```

### Data Flow

```
Request → Auth → Rate Limit → Input Guard → AI Safety → LLM Router
                                                            ↓
Response ← Gemini ← fails? → Groq ← fails? → OpenRouter
```

---

## Features

| Component | Role | Implementation |
|-----------|------|----------------|
| **Auth** | API key validation | Constant-time comparison, env-based secrets |
| **Rate Limiter** | DDoS protection | SlowAPI, configurable per-minute limits |
| **Input Guard** | Injection/PII detection | Regex patterns for known attack vectors |
| **AI Safety** | Content moderation | Gemini classification + Lakera Guard fallback |
| **LLM Router** | Provider orchestration | Cascade failover with latency tracking |
| **Metrics** | Observability | Thread-safe store, real-time /metrics endpoint |

---

## Providers

| Provider | Role | Free Tier | Avg Latency | Context Window |
|----------|------|-----------|-------------|----------------|
| Gemini | Primary | 15 RPM | ~120ms | 1M tokens |
| Groq | Fallback 1 | 30 RPM | ~87ms | 128K tokens |
| OpenRouter | Fallback 2 | Varies | ~200ms | Model-dependent |

---

## API Endpoints

| Endpoint | Method | Auth | Description |
|----------|--------|------|-------------|
| `/` | GET | No | Interactive dashboard |
| `/health` | GET | No | Health check |
| `/query` | POST | Yes | LLM query with cascade fallback |
| `/check-toxicity` | POST | No | Content safety classification |
| `/metrics` | GET | No | Gateway performance metrics |
| `/providers` | GET | No | Provider config and pricing |
| `/batch/resilience` | POST | Yes | Batch resilience testing (up to 10 prompts) |
| `/batch/security` | POST | No | Batch PII/injection testing (up to 20 prompts) |

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

## Configuration

**Required:** `SERVICE_API_KEY`, `GEMINI_API_KEY`

**Optional:** `GROQ_API_KEY`, `OPENROUTER_API_KEY`, `LAKERA_API_KEY`, `TOXICITY_THRESHOLD`, `RATE_LIMIT`

Copy `.env.example` to `.env` and configure your keys. See [Configuration Guide](docs/configuration.md) for full details.

---

## Quick Start

```bash
git clone https://github.com/vn6295337/Enterprise-AI-Gateway.git
cd Enterprise-AI-Gateway
pip install -r requirements.txt

# Set at least one provider API key
export GEMINI_API_KEY="your-key"      # or
export GROQ_API_KEY="your-key"        # or
export OPENROUTER_API_KEY="your-key"

./start-app.sh
```

---

## Development

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn src.main:app --reload
```

---

## Testing

```bash
python -m pytest tests/
```

---

## Deployment

### Docker

```bash
docker build -t llm-secure-gateway .
docker run -p 8000:8000 \
  -e SERVICE_API_KEY=your-key \
  -e GEMINI_API_KEY=your-gemini-key \
  llm-secure-gateway
```

### Hugging Face Spaces

1. Create Space at [huggingface.co/new-space](https://huggingface.co/new-space)
2. Select "Docker" SDK
3. Add repository as source
4. Configure Secrets with API keys

---

## Roadmap

- [ ] Streaming responses via Server-Sent Events
- [ ] Redis-based rate limiting for horizontal scaling
- [ ] Custom safety policies per organization
- [ ] Provider performance analytics dashboard
- [ ] Webhook notifications for blocked requests

---

## Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Implement changes with tests
4. Submit a pull request

---

## Documentation

| Doc | Description |
|-----|-------------|
| [API Reference](docs/api_reference.md) | Complete endpoint documentation |
| [Architecture](docs/architecture.md) | System design deep dive |
| [Security Overview](docs/security_overview.md) | Security layers and threat model |
| [Configuration](docs/configuration.md) | Environment variables reference |
| [Deployment](docs/deployment.md) | Docker and cloud deployment |
| [FAQ](docs/faq.md) | Frequently asked questions |

---

## License

MIT License
