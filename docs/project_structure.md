# Project Structure

> **Primary Responsibility:** Directory layout and codebase organization

Directory layout for the Enterprise AI Gateway.

```
Enterprise-AI-Gateway/
├── src/                        # Source code
│   ├── __init__.py
│   ├── main.py                 # FastAPI application entry point
│   ├── config.py               # Configuration and LLM client
│   ├── api/
│   │   └── routes.py           # API route definitions
│   ├── llm/
│   │   └── client.py           # LLM provider client
│   ├── metrics/
│   │   └── __init__.py         # Metrics tracking
│   ├── models/
│   │   └── __init__.py         # Pydantic models
│   ├── providers/
│   │   └── __init__.py         # Provider configuration
│   └── security/
│       └── __init__.py         # Security utilities (auth, PII, toxicity)
│
├── static/
│   └── index.html              # Interactive demo dashboard
│
├── tests/
│   ├── __init__.py
│   ├── unit/
│   │   └── test_security_models.py
│   └── integration/
│       └── test_gateway.py
│
├── docs/                       # Documentation (MECE structure)
│   ├── README.md               # Index + Quick Start
│   ├── api_reference.md        # API endpoints & functions
│   ├── architecture.md         # System design & data flow
│   ├── configuration.md        # Environment variables
│   ├── deployment.md           # Deployment procedures
│   ├── faq.md                  # Q&A format help
│   ├── project_structure.md    # This file
│   ├── security_overview.md    # Security architecture
│   ├── testing.md              # Testing procedures
│   └── troubleshooting.md      # Problem resolution
│
├── examples/
│   └── basic_usage.py          # Usage examples
│
├── scripts/
│   └── health_check.py         # Health check script
│
├── Dockerfile                  # Docker build configuration
├── requirements.txt            # Python dependencies
├── README.md                   # Project overview (root)
└── BUSINESS_README.md          # HuggingFace Spaces README
```

## Key Directories

### `src/` - Source Code

| Module | Purpose |
|--------|---------|
| `main.py` | FastAPI app initialization, middleware setup |
| `config.py` | Environment config, LLM client initialization |
| `api/routes.py` | HTTP endpoint handlers |
| `llm/client.py` | Multi-provider LLM client with cascade |
| `security/__init__.py` | Auth, PII detection, AI safety (Gemini + Lakera) |
| `models/__init__.py` | Request/response Pydantic models |
| `metrics/__init__.py` | Performance metrics tracking |
| `providers/__init__.py` | Provider pricing and configuration |

### `static/` - Frontend

Single-page interactive dashboard with:
- Real-time pipeline visualization
- Security gate status indicators
- Rate limiting controls
- Test scenario selector

### `tests/` - Test Suite

| Directory | Purpose |
|-----------|---------|
| `unit/` | Unit tests for individual functions |
| `integration/` | API endpoint integration tests |

### `docs/` - Documentation

See [Documentation Index](README.md) for the complete MECE documentation structure.

## Data Flow

```
Request → src/main.py
           ↓
         src/security/ (auth, PII, toxicity check)
           ↓
         src/llm/client.py (provider cascade)
           ↓
         Response
```

## Related Docs

- [Architecture](architecture.md) - Detailed system design
- [API Reference](api_reference.md) - Endpoint documentation
- [Configuration](configuration.md) - Environment setup
