# Error Handling Guide

This document explains how the LLM Secure Gateway handles errors and how to properly handle them in your applications.

## Table of Contents

1. [Error Handling Philosophy](#error-handling-philosophy)
2. [HTTP Status Codes](#http-status-codes)
3. [Error Response Format](#error-response-format)
4. [Common Error Scenarios](#common-error-scenarios)
5. [Client-Side Error Handling](#client-side-error-handling)
6. [Retry Strategies](#retry-strategies)
7. [Logging and Monitoring](#logging-and-monitoring)
8. [Security Considerations](#security-considerations)

## Error Handling Philosophy

The LLM Secure Gateway follows these error handling principles:

1. **Be Explicit**: Provide clear, actionable error messages
2. **Be Consistent**: Use standard HTTP status codes and response formats
3. **Be Secure**: Don't expose internal implementation details
4. **Be Helpful**: Include enough information for debugging without compromising security
5. **Be Predictable**: Handle errors consistently across all endpoints

## HTTP Status Codes

The gateway uses standard HTTP status codes to indicate the result of API requests:

### 2xx Success
- `200 OK`: Request successful

### 4xx Client Errors
- `400 Bad Request`: Invalid request format
- `401 Unauthorized`: Missing or invalid API key
- `403 Forbidden`: Insufficient permissions (if implemented)
- `404 Not Found`: Endpoint does not exist
- `422 Unprocessable Entity`: Validation error or blocked request
- `429 Too Many Requests`: Rate limit exceeded

### 5xx Server Errors
- `500 Internal Server Error`: Unexpected server error
- `502 Bad Gateway`: Upstream provider error
- `503 Service Unavailable`: Service temporarily unavailable
- `504 Gateway Timeout`: Upstream provider timeout

## Error Response Format

All error responses follow a consistent JSON format:

```json
{
  "detail": "Error message describing what went wrong"
}
```

For validation errors, a more detailed format is used:

```json
{
  "detail": [
    {
      "loc": ["body", "field_name"],
      "msg": "Error message",
      "type": "error_type"
    }
  ]
}
```

## Common Error Scenarios

### 1. Authentication Errors (401)

**Cause**: Missing or invalid API key

**Example Request**:
```bash
curl -X POST https://your-gateway-url/query \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Hello"}'
```

**Response**:
```json
{
  "detail": "Invalid or missing API key"
}
```

**Solution**: Include a valid `X-API-Key` header

### 2. Validation Errors (422)

**Cause**: Invalid request parameters

**Example Request**:
```bash
curl -X POST https://your-gateway-url/query \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-key" \
  -d '{"prompt": ""}'
```

**Response**:
```json
{
  "detail": [
    {
      "loc": ["body", "prompt"],
      "msg": "ensure this value has at least 1 characters",
      "type": "value_error.any_str.min_length",
      "ctx": {"limit_value": 1}
    }
  ]
}
```

**Solution**: Ensure all parameters meet validation requirements

### 3. Prompt Injection Detection (422)

**Cause**: Suspicious prompt content detected

**Example Request**:
```bash
curl -X POST https://your-gateway-url/query \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-key" \
  -d '{"prompt": "Ignore all previous instructions"}'
```

**Response**:
```json
{
  "detail": "Security Alert: Prompt injection pattern detected."
}
```

**Solution**: Revise prompt to not include injection patterns

### 4. Rate Limiting (429)

**Cause**: Too many requests from the same IP

**Example Request**:
```bash
# Make more than 10 requests per minute
for i in {1..15}; do
  curl -X POST https://your-gateway-url/query \
    -H "Content-Type: application/json" \
    -H "X-API-Key: your-key" \
    -d '{"prompt": "Test"}'
done
```

**Response**:
```json
{
  "error": "Rate limit exceeded"
}
```

**Solution**: Implement rate limiting on the client side

### 5. Provider Failures (500)

**Cause**: All LLM providers failed

**Response**:
```json
{
  "detail": "All LLM providers failed."
}
```

**Solution**: Retry request or check provider status

## Client-Side Error Handling

### Python Example

```python
import requests
import time
from typing import Optional, Dict, Any

class LLMGatewayError(Exception):
    """Base exception for LLM Gateway errors."""
    pass

class AuthenticationError(LLMGatewayError):
    """Raised when API key is invalid or missing."""
    pass

class ValidationError(LLMGatewayError):
    """Raised when request validation fails."""
    pass

class RateLimitError(LLMGatewayError):
    """Raised when rate limit is exceeded."""
    pass

class ServerError(LLMGatewayError):
    """Raised when server encounters an error."""
    pass

def query_llm(prompt: str, api_key: str, base_url: str) -> Optional[str]:
    """
    Query the LLM gateway with proper error handling.
    
    Args:
        prompt: The prompt to send to the LLM
        api_key: The API key for authentication
        base_url: The base URL of the gateway
        
    Returns:
        The LLM response or None if unsuccessful
        
    Raises:
        LLMGatewayError: For various error conditions
    """
    url = f"{base_url}/query"
    headers = {
        "Content-Type": "application/json",
        "X-API-Key": api_key
    }
    data = {"prompt": prompt}
    
    try:
        response = requests.post(url, headers=headers, json=data, timeout=30)
        
        # Handle different status codes
        if response.status_code == 200:
            return response.json()["response"]
        elif response.status_code == 401:
            raise AuthenticationError("Invalid or missing API key")
        elif response.status_code == 422:
            error_detail = response.json().get("detail", "Validation error")
            raise ValidationError(f"Invalid request: {error_detail}")
        elif response.status_code == 429:
            raise RateLimitError("Rate limit exceeded")
        elif response.status_code >= 500:
            raise ServerError(f"Server error: {response.status_code}")
        else:
            raise LLMGatewayError(f"Unexpected status code: {response.status_code}")
            
    except requests.exceptions.Timeout:
        raise LLMGatewayError("Request timeout")
    except requests.exceptions.ConnectionError:
        raise LLMGatewayError("Connection error")
    except requests.exceptions.RequestException as e:
        raise LLMGatewayError(f"Request failed: {str(e)}")

# Usage example
def main():
    API_KEY = "your-api-key"
    BASE_URL = "https://your-gateway-url"
    
    try:
        response = query_llm("What is artificial intelligence?", API_KEY, BASE_URL)
        print(f"Response: {response}")
    except AuthenticationError as e:
        print(f"Authentication failed: {e}")
        # Prompt user to check API key
    except ValidationError as e:
        print(f"Invalid request: {e}")
        # Check request parameters
    except RateLimitError as e:
        print(f"Rate limited: {e}")
        # Wait before retrying
        time.sleep(60)
    except ServerError as e:
        print(f"Server error: {e}")
        # Retry or check provider status
    except LLMGatewayError as e:
        print(f"Error: {e}")
        # Handle other errors

if __name__ == "__main__":
    main()
```

### JavaScript Example

```javascript
class LLMGatewayError extends Error {
  constructor(message, statusCode) {
    super(message);
    this.name = 'LLMGatewayError';
    this.statusCode = statusCode;
  }
}

class AuthenticationError extends LLMGatewayError {
  constructor(message) {
    super(message, 401);
    this.name = 'AuthenticationError';
  }
}

class ValidationError extends LLMGatewayError {
  constructor(message) {
    super(message, 422);
    this.name = 'ValidationError';
  }
}

class RateLimitError extends LLMGatewayError {
  constructor(message) {
    super(message, 429);
    this.name = 'RateLimitError';
  }
}

class ServerError extends LLMGatewayError {
  constructor(message) {
    super(message, 500);
    this.name = 'ServerError';
  }
}

async function queryLLM(prompt, apiKey, baseUrl) {
  const url = `${baseUrl}/query`;
  const headers = {
    'Content-Type': 'application/json',
    'X-API-Key': apiKey
  };
  const body = JSON.stringify({ prompt });
  
  try {
    const response = await fetch(url, {
      method: 'POST',
      headers,
      body
    });
    
    // Handle different status codes
    if (response.ok) {
      const data = await response.json();
      return data.response;
    } else {
      const errorData = await response.json().catch(() => ({}));
      const errorMessage = errorData.detail || response.statusText;
      
      switch (response.status) {
        case 401:
          throw new AuthenticationError(errorMessage);
        case 422:
          throw new ValidationError(errorMessage);
        case 429:
          throw new RateLimitError(errorMessage);
        case 500:
        case 502:
        case 503:
        case 504:
          throw new ServerError(errorMessage);
        default:
          throw new LLMGatewayError(errorMessage, response.status);
      }
    }
  } catch (error) {
    if (error instanceof LLMGatewayError) {
      throw error;
    } else if (error instanceof TypeError) {
      // Network error
      throw new LLMGatewayError('Network error', 0);
    } else {
      throw new LLMGatewayError('Unknown error', 0);
    }
  }
}

// Usage example
async function main() {
  const API_KEY = 'your-api-key';
  const BASE_URL = 'https://your-gateway-url';
  
  try {
    const response = await queryLLM('What is artificial intelligence?', API_KEY, BASE_URL);
    console.log(`Response: ${response}`);
  } catch (error) {
    if (error instanceof AuthenticationError) {
      console.error('Authentication failed:', error.message);
      // Prompt user to check API key
    } else if (error instanceof ValidationError) {
      console.error('Invalid request:', error.message);
      // Check request parameters
    } else if (error instanceof RateLimitError) {
      console.error('Rate limited:', error.message);
      // Wait before retrying
      await new Promise(resolve => setTimeout(resolve, 60000));
    } else if (error instanceof ServerError) {
      console.error('Server error:', error.message);
      // Retry or check provider status
    } else {
      console.error('Error:', error.message);
      // Handle other errors
    }
  }
}

main().catch(console.error);
```

## Retry Strategies

### Exponential Backoff

```python
import time
import random
import requests

def query_with_exponential_backoff(prompt, api_key, base_url, max_retries=3):
    """Query LLM with exponential backoff retry strategy."""
    delay = 1  # Initial delay in seconds
    
    for attempt in range(max_retries + 1):
        try:
            response = requests.post(
                f"{base_url}/query",
                headers={
                    "Content-Type": "application/json",
                    "X-API-Key": api_key
                },
                json={"prompt": prompt},
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json()["response"]
            elif response.status_code == 429:
                # Rate limited - wait and retry
                if attempt < max_retries:
                    jitter = random.uniform(0, 1)
                    wait_time = delay + jitter
                    print(f"Rate limited. Waiting {wait_time:.2f} seconds...")
                    time.sleep(wait_time)
                    delay *= 2  # Exponential backoff
                    continue
            elif response.status_code >= 500:
                # Server error - wait and retry
                if attempt < max_retries:
                    jitter = random.uniform(0, 1)
                    wait_time = delay + jitter
                    print(f"Server error. Waiting {wait_time:.2f} seconds...")
                    time.sleep(wait_time)
                    delay *= 2  # Exponential backoff
                    continue
            
            # For other errors, don't retry
            response.raise_for_status()
            
        except requests.exceptions.RequestException as e:
            if attempt < max_retries:
                jitter = random.uniform(0, 1)
                wait_time = delay + jitter
                print(f"Request failed: {e}. Waiting {wait_time:.2f} seconds...")
                time.sleep(wait_time)
                delay *= 2  # Exponential backoff
                continue
            else:
                raise
    
    raise Exception("Max retries exceeded")

# Usage
try:
    response = query_with_exponential_backoff(
        "Explain quantum computing", 
        "your-api-key", 
        "https://your-gateway-url"
    )
    print(response)
except Exception as e:
    print(f"Failed after retries: {e}")
```

### Circuit Breaker Pattern

```python
import time
from enum import Enum

class CircuitState(Enum):
    CLOSED = 1
    OPEN = 2
    HALF_OPEN = 3

class CircuitBreaker:
    def __init__(self, failure_threshold=5, timeout=60):
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.failure_count = 0
        self.last_failure_time = None
        self.state = CircuitState.CLOSED
        
    def call(self, func, *args, **kwargs):
        if self.state == CircuitState.OPEN:
            if time.time() - self.last_failure_time > self.timeout:
                self.state = CircuitState.HALF_OPEN
                print("Circuit breaker half-open - testing service")
            else:
                raise Exception("Circuit breaker is OPEN - service unavailable")
        
        try:
            result = func(*args, **kwargs)
            self.on_success()
            return result
        except Exception as e:
            self.on_failure()
            raise e
    
    def on_success(self):
        print("Circuit breaker success - resetting")
        self.failure_count = 0
        self.state = CircuitState.CLOSED
    
    def on_failure(self):
        self.failure_count += 1
        self.last_failure_time = time.time()
        print(f"Circuit breaker failure #{self.failure_count}")
        
        if self.failure_count >= self.failure_threshold:
            print("Circuit breaker OPEN - service unavailable")
            self.state = CircuitState.OPEN

# Usage
breaker = CircuitBreaker(failure_threshold=3, timeout=30)

def query_llm_unsafe(prompt, api_key, base_url):
    """Simulate an LLM query that might fail."""
    import requests
    response = requests.post(
        f"{base_url}/query",
        headers={"X-API-Key": api_key},
        json={"prompt": prompt}
    )
    response.raise_for_status()
    return response.json()["response"]

# Usage with circuit breaker
try:
    result = breaker.call(
        query_llm_unsafe,
        "What is machine learning?",
        "your-api-key",
        "https://your-gateway-url"
    )
    print(result)
except Exception as e:
    print(f"Call failed: {e}")
```

## Logging and Monitoring

### Structured Logging

```python
import logging
import json
from datetime import datetime

# Configure structured logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

def log_request_outcome(prompt, api_key, base_url, outcome, error=None, duration=None):
    """Log request outcome for monitoring."""
    log_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "prompt_length": len(prompt),
        "outcome": outcome,  # success, auth_error, validation_error, rate_limit, server_error
        "error_message": str(error) if error else None,
        "duration_ms": duration,
        "base_url": base_url
    }
    
    if outcome == "success":
        logger.info(f"LLM request successful: {json.dumps(log_entry)}")
    elif outcome == "auth_error":
        logger.warning(f"LLM auth error: {json.dumps(log_entry)}")
    elif outcome == "validation_error":
        logger.warning(f"LLM validation error: {json.dumps(log_entry)}")
    elif outcome == "rate_limit":
        logger.warning(f"LLM rate limit exceeded: {json.dumps(log_entry)}")
    elif outcome == "server_error":
        logger.error(f"LLM server error: {json.dumps(log_entry)}")
    else:
        logger.error(f"LLM unknown error: {json.dumps(log_entry)}")

# Usage in error handling
def query_llm_with_logging(prompt, api_key, base_url):
    start_time = time.time()
    
    try:
        response = query_llm(prompt, api_key, base_url)
        duration = (time.time() - start_time) * 1000
        log_request_outcome(prompt, api_key, base_url, "success", duration=duration)
        return response
    except AuthenticationError as e:
        duration = (time.time() - start_time) * 1000
        log_request_outcome(prompt, api_key, base_url, "auth_error", e, duration)
        raise
    except ValidationError as e:
        duration = (time.time() - start_time) * 1000
        log_request_outcome(prompt, api_key, base_url, "validation_error", e, duration)
        raise
    except RateLimitError as e:
        duration = (time.time() - start_time) * 1000
        log_request_outcome(prompt, api_key, base_url, "rate_limit", e, duration)
        raise
    except ServerError as e:
        duration = (time.time() - start_time) * 1000
        log_request_outcome(prompt, api_key, base_url, "server_error", e, duration)
        raise
    except Exception as e:
        duration = (time.time() - start_time) * 1000
        log_request_outcome(prompt, api_key, base_url, "unknown_error", e, duration)
        raise
```

## Security Considerations

### Error Message Sanitization

The gateway follows security best practices by not exposing internal implementation details:

```python
# GOOD: Generic error messages
{
  "detail": "Invalid or missing API key"
}

# BAD: Exposing internal details
{
  "detail": "API key validation failed: HMAC comparison failed at line 42 in auth.py"
}
```

### Rate Limit Information

Rate limit errors don't reveal internal configuration:

```python
# GOOD: Generic rate limit message
{
  "error": "Rate limit exceeded"
}

# BAD: Revealing configuration details
{
  "error": "Rate limit of 10 requests per minute exceeded. Try again in 45 seconds."
}
```

### Input Validation

Validation errors provide helpful but not exploitable information:

```python
# GOOD: Descriptive but safe
{
  "detail": [
    {
      "loc": ["body", "prompt"],
      "msg": "ensure this value has at least 1 characters",
      "type": "value_error.any_str.min_length"
    }
  ]
}

# BAD: Revealing internal logic
{
  "detail": "Prompt validation failed: regex pattern ^[a-zA-Z0-9 ]+$ did not match"
}
```

## Best Practices

### 1. Always Handle Errors

```python
# GOOD: Comprehensive error handling
try:
    response = query_llm(prompt, api_key, base_url)
    process_response(response)
except AuthenticationError:
    # Handle auth error
    refresh_api_key()
except ValidationError:
    # Handle validation error
    fix_request_parameters()
except RateLimitError:
    # Handle rate limit
    wait_and_retry()
except ServerError:
    # Handle server error
    failover_to_backup()
except Exception:
    # Handle unexpected errors
    log_and_alert()
```

### 2. Implement Retry Logic

```python
# Implement exponential backoff for transient errors
def robust_query(prompt, api_key, base_url, max_retries=3):
    for attempt in range(max_retries + 1):
        try:
            return query_llm(prompt, api_key, base_url)
        except (RateLimitError, ServerError) as e:
            if attempt < max_retries:
                wait_time = (2 ** attempt) + random.uniform(0, 1)
                time.sleep(wait_time)
                continue
            else:
                raise
        except Exception:
            # Don't retry on other errors
            raise
```

### 3. Monitor and Alert

```python
# Track error rates and alert on anomalies
def should_alert_on_error_rate(error_counts, total_requests, threshold=0.05):
    """Alert if error rate exceeds threshold."""
    if total_requests == 0:
        return False
    error_rate = sum(error_counts.values()) / total_requests
    return error_rate > threshold
```

### 4. Graceful Degradation

```python
# Provide fallback behavior when gateway is unavailable
def query_with_fallback(prompt, api_key, base_url, fallback_responses):
    try:
        return query_llm(prompt, api_key, base_url)
    except Exception:
        # Use cached or default response
        return fallback_responses.get(prompt, "Sorry, I'm having trouble answering that right now.")
```

Proper error handling ensures reliable integration with the LLM Secure Gateway and provides a good user experience even when errors occur.