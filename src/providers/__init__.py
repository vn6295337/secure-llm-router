"""
Provider configuration with pricing and performance data
"""

PROVIDER_CONFIG = {
    "gemini": {
        "name": "Google Gemini",
        "models": {
            "gemini-2.0-flash-exp": {
                "price_per_1m_input": 0.075,
                "price_per_1m_output": 0.30,
                "avg_latency_ms": 120,
                "context_window": 1048576,
            },
            "gemini-1.5-pro": {
                "price_per_1m_input": 1.25,
                "price_per_1m_output": 5.00,
                "avg_latency_ms": 150,
                "context_window": 2097152,
            },
            "gemini-1.0-pro": {
                "price_per_1m_input": 0.50,
                "price_per_1m_output": 1.50,
                "avg_latency_ms": 130,
                "context_window": 32760,
            }
        }
    },
    "groq": {
        "name": "Groq",
        "models": {
            "llama-3.3-70b-versatile": {
                "price_per_1m_input": 0.59,
                "price_per_1m_output": 0.79,
                "avg_latency_ms": 87,
                "context_window": 128000,
            },
            "llama3-70b": {
                "price_per_1m_input": 0.59,
                "price_per_1m_output": 0.79,
                "avg_latency_ms": 90,
                "context_window": 8192,
            },
            "mixtral-8x7b": {
                "price_per_1m_input": 0.24,
                "price_per_1m_output": 0.24,
                "avg_latency_ms": 95,
                "context_window": 32768,
            }
        }
    },
    "openrouter": {
        "name": "OpenRouter",
        "models": {
            "google/gemini-2.0-flash-exp:free": {
                "price_per_1m_input": 0.0,
                "price_per_1m_output": 0.0,
                "avg_latency_ms": 200,
                "context_window": 1048576,
            },
            "gpt-4": {
                "price_per_1m_input": 30.0,
                "price_per_1m_output": 60.0,
                "avg_latency_ms": 250,
                "context_window": 128000,
            },
            "gpt-3.5-turbo": {
                "price_per_1m_input": 0.50,
                "price_per_1m_output": 1.50,
                "avg_latency_ms": 180,
                "context_window": 16385,
            },
            "claude-3-opus": {
                "price_per_1m_input": 15.0,
                "price_per_1m_output": 75.0,
                "avg_latency_ms": 300,
                "context_window": 200000,
            }
        }
    }
}


def get_model_pricing(provider: str, model: str) -> dict:
    """Get pricing info for a specific provider/model combination"""
    if provider in PROVIDER_CONFIG:
        models = PROVIDER_CONFIG[provider].get("models", {})
        if model in models:
            return models[model]
    return None


def estimate_cost(provider: str, model: str, input_tokens: int, output_tokens: int) -> float:
    """Estimate cost for a request in USD"""
    pricing = get_model_pricing(provider, model)
    if not pricing:
        return 0.0

    input_cost = (input_tokens / 1_000_000) * pricing.get("price_per_1m_input", 0)
    output_cost = (output_tokens / 1_000_000) * pricing.get("price_per_1m_output", 0)
    return round(input_cost + output_cost, 6)
