# Documentation

> **Primary Responsibility:** Documentation index and quick start guide

Essential documentation for the Enterprise AI Gateway.

## Quick Start

```bash
# 1. Clone and install
git clone https://github.com/vn6295337/Enterprise-AI-Gateway.git
cd Enterprise-AI-Gateway
pip install -r requirements.txt

# 2. Configure (create .env file)
SERVICE_API_KEY=your_secure_key
GEMINI_API_KEY=your_gemini_key

# 3. Run
uvicorn src.main:app --host 0.0.0.0 --port 8000

# 4. Test
curl http://localhost:8000/health
```

See [Deployment Guide](deployment.md) for Docker and cloud deployment options.

---

## Documentation Index (MECE)

| Document | Primary Responsibility |
|----------|------------------------|
| [Project Structure](project_structure.md) | Directory layout and codebase organization |
| [API Reference](api_reference.md) | Complete API endpoint and function documentation |
| [Architecture](architecture.md) | System design, component architecture, data flow |
| [Configuration](configuration.md) | All environment variables and settings |
| [Security Overview](security_overview.md) | Security architecture, threat model, compliance |
| [Deployment](deployment.md) | Deployment procedures (local, Docker, cloud) |
| [Testing](testing.md) | Testing strategy and test examples |
| [FAQ](faq.md) | Q&A format help with cross-references |
| [Troubleshooting](troubleshooting.md) | Problem diagnosis and resolution |

## Security Layers

The gateway implements 4 security layers. See [Security Overview](security_overview.md) for detailed architecture.

## Key Features

- **Multi-provider failover**: Gemini → Groq → OpenRouter
- **AI content moderation**: Harmful content detection and blocking
- **PII protection**: Automatic detection of SSN, credit cards, emails, API keys
- **Rate limiting**: Configurable per-minute limits

## Configuration

**Required:** `SERVICE_API_KEY`, `GEMINI_API_KEY`

**Optional:** `GROQ_API_KEY`, `OPENROUTER_API_KEY`, `LAKERA_API_KEY`, `TOXICITY_THRESHOLD`, `RATE_LIMIT`

See [Configuration Guide](configuration.md) for complete details.
