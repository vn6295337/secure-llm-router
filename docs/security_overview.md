# Security Overview

> **Primary Responsibility:** Detailed security architecture, threat model, and compliance

Multi-layer security architecture for the Enterprise AI Gateway.

## Security Layers

```
┌─────────────────────────────────────────────────────────┐
│  Layer 1: Authentication & Rate Limiting                │
│  • API Key validation (X-API-Key header)                │
│  • Rate limiting (10 req/min, configurable)             │
│  • Token limit enforcement (4096 max input)             │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│  Layer 2: Input Guard                                   │
│  • Prompt injection detection (pattern-based)           │
│  • PII detection (SSN, credit cards, emails, API keys)  │
│  • SQL/Command injection patterns                       │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│  Layer 3: AI Safety (Gemini + Lakera Guard)             │
│  Primary: Gemini 2.5 Flash content classification       │
│  Fallback: Lakera Guard API                             │
│  Categories: Sexual, Hate, Harassment, Dangerous,       │
│              Civic Integrity, Prompt Injection          │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│  Layer 4: LLM Router                                    │
│  • Provider authentication                              │
│  • Secure API communication (HTTPS)                     │
│  • Response validation                                  │
└─────────────────────────────────────────────────────────┘
```

## Authentication

### API Key Validation
- Header: `X-API-Key: YOUR_API_KEY`
- Environment variable: `SERVICE_API_KEY`
- Constant-time comparison to prevent timing attacks

## Rate Limiting

### Client-Side (Dashboard)
- 5 requests per 60 seconds
- Persisted in sessionStorage
- Reset button for demo purposes

### Server-Side
- SlowAPI rate limiting
- Configurable via `RATE_LIMIT` environment variable
- Returns 429 on limit exceeded

## Input Validation

### PII Detection
Automatically detects and blocks:
- Email addresses
- Credit card numbers (4x4 digit patterns)
- Social Security Numbers (XXX-XX-XXXX)
- Tax IDs (XX-XXXXXXX)
- API keys (sk_, pk_, api_, bearer_ prefixes)

### Prompt Injection Detection
Pattern-based detection for:
- "ignore all previous instructions"
- "disregard all previous instructions"
- "you are now"
- "system:" prefixes

## AI Safety Layer

### Primary: Gemini Classification
Uses Gemini 2.5 Flash to classify content into categories:

| Category | Description |
|----------|-------------|
| SEXUALLY_EXPLICIT | Nude, porn, explicit sexual content |
| HATE_SPEECH | Racism, discrimination, slurs |
| HARASSMENT | Threats, bullying, intimidation |
| DANGEROUS_CONTENT | Weapons, drugs, violence, self-harm |
| CIVIC_INTEGRITY | Election fraud, voter suppression |

### Fallback: Lakera Guard
When Gemini fails or times out:
- Endpoint: `https://api.lakera.ai/v2/guard`
- Detects prompt injections, jailbreaks, PII, toxicity
- Environment variable: `LAKERA_API_KEY`

## Environment Variables

See [Configuration Guide](configuration.md) for complete environment variable reference.

## Data Protection

- **No persistent storage** of user prompts or responses
- **HTTPS/TLS** for all API communications
- **Environment variables** for secrets (never in code)
- **No logging** of sensitive content by default

## Compliance

- GDPR compliant (data minimization)
- OWASP API Security Top 10 aligned
- PII auto-detection prevents data leaks
