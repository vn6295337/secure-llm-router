# API Examples

This document provides practical examples of how to use the LLM Secure Gateway API in various programming languages and scenarios.

## Table of Contents

1. [Authentication Examples](#authentication-examples)
2. [Health Check Examples](#health-check-examples)
3. [Query Examples](#query-examples)
4. [Error Handling Examples](#error-handling-examples)
5. [Language-Specific Examples](#language-specific-examples)
6. [Advanced Usage Examples](#advanced-usage-examples)

## Authentication Examples

### Setting Up Authentication

All API requests (except `/health`) require an API key in the `X-API-Key` header.

```bash
# Store your API key as an environment variable
export SERVICE_API_KEY="sk-your-secure-api-key-here"
```

## Health Check Examples

### Basic Health Check

```bash
# Using cURL
curl https://your-gateway-url/health

# Using wget
wget -qO- https://your-gateway-url/health
```

Expected response:
```json
{
  "status": "healthy",
  "provider": "gemini",
  "timestamp": 1700000000.123456
}
```

### Health Check with Programming Languages

#### Python
```python
import requests

response = requests.get("https://your-gateway-url/health")
if response.status_code == 200:
    data = response.json()
    print(f"Status: {data['status']}")
    print(f"Provider: {data['provider']}")
```

#### JavaScript (Node.js)
```javascript
fetch('https://your-gateway-url/health')
  .then(response => response.json())
  .then(data => {
    console.log(`Status: ${data.status}`);
    console.log(`Provider: ${data.provider}`);
  });
```

#### JavaScript (Browser)
```javascript
async function checkHealth() {
  try {
    const response = await fetch('https://your-gateway-url/health');
    const data = await response.json();
    console.log(`Status: ${data.status}`);
    console.log(`Provider: ${data.provider}`);
  } catch (error) {
    console.error('Health check failed:', error);
  }
}
```

## Query Examples

### Basic Query

```bash
curl -X POST https://your-gateway-url/query \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $SERVICE_API_KEY" \
  -d '{
    "prompt": "What is artificial intelligence?",
    "max_tokens": 150,
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

### Query with Minimal Parameters

```bash
curl -X POST https://your-gateway-url/query \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $SERVICE_API_KEY" \
  -d '{
    "prompt": "Hello, world!"
  }'
```

### Query with All Parameters

```bash
curl -X POST https://your-gateway-url/query \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $SERVICE_API_KEY" \
  -d '{
    "prompt": "Write a short story about a robot learning to paint.",
    "max_tokens": 500,
    "temperature": 0.9
  }'
```

## Error Handling Examples

### Handling 401 Unauthorized

```bash
curl -X POST https://your-gateway-url/query \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "This will fail without an API key"
  }'
```

Response:
```json
{
  "detail": "Invalid or missing API key"
}
```

### Handling 422 Validation Error

```bash
curl -X POST https://your-gateway-url/query \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $SERVICE_API_KEY" \
  -d '{
    "prompt": ""
  }'
```

Response:
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

### Handling 429 Rate Limit Exceeded

```bash
# Make too many requests in a short time
for i in {1..15}; do
  curl -X POST https://your-gateway-url/query \
    -H "Content-Type: application/json" \
    -H "X-API-Key: $SERVICE_API_KEY" \
    -d '{"prompt": "Test request"}'
done
```

Response (on request 11+):
```json
{
  "error": "Rate limit exceeded"
}
```

## Language-Specific Examples

### Python Examples

#### Basic Query
```python
import requests
import os

API_KEY = os.getenv("SERVICE_API_KEY")
GATEWAY_URL = "https://your-gateway-url"

def query_llm(prompt, max_tokens=256, temperature=0.7):
    headers = {
        "Content-Type": "application/json",
        "X-API-Key": API_KEY
    }
    
    data = {
        "prompt": prompt,
        "max_tokens": max_tokens,
        "temperature": temperature
    }
    
    response = requests.post(f"{GATEWAY_URL}/query", headers=headers, json=data)
    
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"API request failed: {response.status_code} - {response.text}")

# Usage
try:
    result = query_llm("What are the benefits of using an AI gateway?")
    print(f"Response: {result['response']}")
    print(f"Provider: {result['provider']}")
    print(f"Latency: {result['latency_ms']}ms")
except Exception as e:
    print(f"Error: {e}")
```

#### Batch Processing
```python
import requests
import os
from concurrent.futures import ThreadPoolExecutor

API_KEY = os.getenv("SERVICE_API_KEY")
GATEWAY_URL = "https://your-gateway-url"

def query_single_prompt(prompt):
    headers = {
        "Content-Type": "application/json",
        "X-API-Key": API_KEY
    }
    
    data = {"prompt": prompt}
    
    try:
        response = requests.post(f"{GATEWAY_URL}/query", headers=headers, json=data)
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"HTTP {response.status_code}", "prompt": prompt}
    except Exception as e:
        return {"error": str(e), "prompt": prompt}

def batch_query(prompts, max_workers=5):
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        results = list(executor.map(query_single_prompt, prompts))
    return results

# Usage
prompts = [
    "What is machine learning?",
    "Explain neural networks",
    "Describe deep learning",
    "What is natural language processing?"
]

results = batch_query(prompts)
for i, result in enumerate(results):
    if "error" in result:
        print(f"Prompt {i+1} failed: {result['error']}")
    else:
        print(f"Prompt {i+1}: {result['response'][:100]}...")
```

### JavaScript Examples

#### Node.js Basic Query
```javascript
const axios = require('axios');

const API_KEY = process.env.SERVICE_API_KEY;
const GATEWAY_URL = 'https://your-gateway-url';

async function queryLLM(prompt, maxTokens = 256, temperature = 0.7) {
  try {
    const response = await axios.post(`${GATEWAY_URL}/query`, {
      prompt: prompt,
      max_tokens: maxTokens,
      temperature: temperature
    }, {
      headers: {
        'Content-Type': 'application/json',
        'X-API-Key': API_KEY
      }
    });
    
    return response.data;
  } catch (error) {
    if (error.response) {
      throw new Error(`API Error: ${error.response.status} - ${error.response.data.detail || error.response.statusText}`);
    } else {
      throw new Error(`Network Error: ${error.message}`);
    }
  }
}

// Usage
(async () => {
  try {
    const result = await queryLLM("What are microservices?");
    console.log(`Response: ${result.response}`);
    console.log(`Provider: ${result.provider}`);
    console.log(`Latency: ${result.latency_ms}ms`);
  } catch (error) {
    console.error(`Error: ${error.message}`);
  }
})();
```

#### Browser JavaScript with Async/Await
```javascript
class LLMGatewayClient {
  constructor(baseUrl, apiKey) {
    this.baseUrl = baseUrl;
    this.apiKey = apiKey;
  }
  
  async healthCheck() {
    const response = await fetch(`${this.baseUrl}/health`);
    if (!response.ok) {
      throw new Error(`Health check failed: ${response.status}`);
    }
    return await response.json();
  }
  
  async query(prompt, options = {}) {
    const { maxTokens = 256, temperature = 0.7 } = options;
    
    const response = await fetch(`${this.baseUrl}/query`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-API-Key': this.apiKey
      },
      body: JSON.stringify({
        prompt: prompt,
        max_tokens: maxTokens,
        temperature: temperature
      })
    });
    
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(`Query failed: ${response.status} - ${errorData.detail || response.statusText}`);
    }
    
    return await response.json();
  }
}

// Usage
const client = new LLMGatewayClient('https://your-gateway-url', 'your-api-key');

async function example() {
  try {
    // Health check
    const health = await client.healthCheck();
    console.log('Health:', health);
    
    // Query
    const result = await client.query('Explain quantum computing in simple terms');
    console.log('Response:', result.response);
    console.log('Provider:', result.provider);
    console.log('Latency:', result.latency_ms, 'ms');
  } catch (error) {
    console.error('Error:', error.message);
  }
}
```

### Java Examples

#### Basic Query with OkHttp
```java
import okhttp3.*;
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import java.io.IOException;

public class LLMGatewayClient {
    private final OkHttpClient client;
    private final String baseUrl;
    private final String apiKey;
    private final ObjectMapper objectMapper;
    
    public LLMGatewayClient(String baseUrl, String apiKey) {
        this.client = new OkHttpClient();
        this.baseUrl = baseUrl;
        this.apiKey = apiKey;
        this.objectMapper = new ObjectMapper();
    }
    
    public JsonNode query(String prompt, int maxTokens, double temperature) throws IOException {
        String json = String.format(
            "{\"prompt\":\"%s\",\"max_tokens\":%d,\"temperature\":%.1f}",
            prompt, maxTokens, temperature
        );
        
        RequestBody body = RequestBody.create(
            json, MediaType.get("application/json")
        );
        
        Request request = new Request.Builder()
            .url(baseUrl + "/query")
            .post(body)
            .addHeader("X-API-Key", apiKey)
            .build();
            
        try (Response response = client.newCall(request).execute()) {
            if (!response.isSuccessful()) {
                throw new IOException("Unexpected response code: " + response);
            }
            
            String responseBody = response.body().string();
            return objectMapper.readTree(responseBody);
        }
    }
    
    public static void main(String[] args) {
        LLMGatewayClient gateway = new LLMGatewayClient(
            "https://your-gateway-url",
            System.getenv("SERVICE_API_KEY")
        );
        
        try {
            JsonNode result = gateway.query("What is blockchain?", 200, 0.7);
            System.out.println("Response: " + result.get("response").asText());
            System.out.println("Provider: " + result.get("provider").asText());
            System.out.println("Latency: " + result.get("latency_ms").asInt() + "ms");
        } catch (IOException e) {
            System.err.println("Error: " + e.getMessage());
        }
    }
}
```

## Advanced Usage Examples

### Streaming Responses (Conceptual)

While the current version doesn't support streaming, here's how it might be implemented:

```javascript
// Conceptual example for future streaming support
async function* streamQuery(prompt) {
  const response = await fetch('/query-stream', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-API-Key': API_KEY
    },
    body: JSON.stringify({ prompt })
  });
  
  const reader = response.body.getReader();
  const decoder = new TextDecoder();
  
  try {
    while (true) {
      const { done, value } = await reader.read();
      if (done) break;
      
      const chunk = decoder.decode(value);
      yield chunk;
    }
  } finally {
    reader.releaseLock();
  }
}

// Usage
for await (const chunk of streamQuery("Write a story about space exploration")) {
  process.stdout.write(chunk);
}
```

### Retry Logic with Exponential Backoff

```python
import requests
import time
import random
import os

API_KEY = os.getenv("SERVICE_API_KEY")
GATEWAY_URL = "https://your-gateway-url"

def query_with_retry(prompt, max_retries=3, base_delay=1):
    headers = {
        "Content-Type": "application/json",
        "X-API-Key": API_KEY
    }
    
    data = {"prompt": prompt}
    
    for attempt in range(max_retries + 1):
        try:
            response = requests.post(f"{GATEWAY_URL}/query", headers=headers, json=data)
            
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 429:  # Rate limited
                if attempt < max_retries:
                    delay = base_delay * (2 ** attempt) + random.uniform(0, 1)
                    print(f"Rate limited. Retrying in {delay:.2f} seconds...")
                    time.sleep(delay)
                    continue
            elif response.status_code >= 500:  # Server error
                if attempt < max_retries:
                    delay = base_delay * (2 ** attempt) + random.uniform(0, 1)
                    print(f"Server error. Retrying in {delay:.2f} seconds...")
                    time.sleep(delay)
                    continue
            
            # For other errors, don't retry
            response.raise_for_status()
            
        except requests.exceptions.RequestException as e:
            if attempt < max_retries:
                delay = base_delay * (2 ** attempt) + random.uniform(0, 1)
                print(f"Request failed: {e}. Retrying in {delay:.2f} seconds...")
                time.sleep(delay)
                continue
            else:
                raise
    
    raise Exception("Max retries exceeded")

# Usage
try:
    result = query_with_retry("Explain the theory of relativity")
    print(result["response"])
except Exception as e:
    print(f"Failed after retries: {e}")
```

### Circuit Breaker Pattern

```python
import requests
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
            else:
                raise Exception("Circuit breaker is OPEN")
        
        try:
            result = func(*args, **kwargs)
            self.on_success()
            return result
        except Exception as e:
            self.on_failure()
            raise e
    
    def on_success(self):
        self.failure_count = 0
        self.state = CircuitState.CLOSED
    
    def on_failure(self):
        self.failure_count += 1
        self.last_failure_time = time.time()
        
        if self.failure_count >= self.failure_threshold:
            self.state = CircuitState.OPEN

# Usage with LLM Gateway
API_KEY = os.getenv("SERVICE_API_KEY")
GATEWAY_URL = "https://your-gateway-url"
circuit_breaker = CircuitBreaker(failure_threshold=3, timeout=30)

def query_llm(prompt):
    headers = {
        "Content-Type": "application/json",
        "X-API-Key": API_KEY
    }
    
    data = {"prompt": prompt}
    response = requests.post(f"{GATEWAY_URL}/query", headers=headers, json=data)
    response.raise_for_status()
    return response.json()

# Usage
try:
    result = circuit_breaker.call(query_llm, "What is quantum computing?")
    print(result["response"])
except Exception as e:
    print(f"Circuit breaker prevented call: {e}")
```

## Best Practices

### Error Handling

1. Always check HTTP status codes
2. Handle network timeouts gracefully
3. Implement retry logic for transient failures
4. Log errors for debugging
5. Provide user-friendly error messages

### Security

1. Never log API keys
2. Use HTTPS in production
3. Validate all inputs
4. Implement proper authentication
5. Rotate API keys regularly

### Performance

1. Use connection pooling
2. Implement caching where appropriate
3. Set appropriate timeouts
4. Handle rate limiting gracefully
5. Monitor response times

These examples demonstrate common usage patterns for the LLM Secure Gateway API. Adapt them to your specific use case and programming language preferences.