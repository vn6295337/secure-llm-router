# API Demo - Secure LLM Router

**Live Service**: https://vn6295337-secure-llm-api.hf.space

This document shows real examples of the API in action.

---

## Example 1: Health Check

**What it does**: Checks if the service is running and which AI provider is active.

**Command**:
```bash
curl https://vn6295337-secure-llm-api.hf.space/health
```

**Result**:
```json
{
  "status": "healthy",
  "provider": "gemini",
  "model": "gemini-2.0-flash-exp",
  "timestamp": 1765193753.29
}
```

**What this means**: Service is online, using Gemini as the primary AI provider.

---

## Example 2: Successful Query

**What it does**: Sends a question to the AI and gets an answer.

**Command**:
```bash
curl -X POST https://vn6295337-secure-llm-api.hf.space/query \
  -H "Content-Type: application/json" \
  -H "X-API-Key: secure-YDiNiwSV5k6A4lKu2EgKt2us-JzdMHEiOeM_rz76CvE" \
  -d '{
    "prompt": "What is machine learning in one sentence?",
    "max_tokens": 100,
    "temperature": 0.7
  }'
```

**Result**:
```json
{
  "response": "Machine learning is a type of artificial intelligence that enables computers to learn from data and improve their performance on a task without being explicitly programmed.",
  "provider": "groq",
  "latency_ms": 87,
  "status": "success",
  "error": null
}
```

**What this means**:
- The AI answered in 87 milliseconds
- The response came from Groq (fallback provider)
- No errors occurred

---

## Example 3: Missing API Key (Security Test)

**What it does**: Shows what happens when you forget the API key.

**Command**:
```bash
curl -X POST https://vn6295337-secure-llm-api.hf.space/query \
  -H "Content-Type: application/json" \
  -d '{"prompt": "test", "max_tokens": 50}'
```

**Result**:
```json
{
  "detail": "Invalid or missing API key"
}
```

**What this means**: Request was blocked because no API key was provided. ✅ Security working!

---

## Example 4: Invalid Input (Validation Test)

**What it does**: Shows input validation in action.

**Command** (empty prompt):
```bash
curl -X POST https://vn6295337-secure-llm-api.hf.space/query \
  -H "Content-Type: application/json" \
  -H "X-API-Key: secure-YDiNiwSV5k6A4lKu2EgKt2us-JzdMHEiOeM_rz76CvE" \
  -d '{"prompt": "", "max_tokens": 50}'
```

**Result**:
```json
{
  "detail": [
    {
      "type": "string_too_short",
      "loc": ["body", "prompt"],
      "msg": "String should have at least 1 character",
      "input": ""
    }
  ]
}
```

**What this means**: Request was rejected because the prompt was empty. ✅ Validation working!

---

## Example 5: Multi-Provider Fallback

**What it does**: Shows different AI providers responding to different requests.

**Command 1**:
```bash
curl -s -X POST https://vn6295337-secure-llm-api.hf.space/query \
  -H "Content-Type: application/json" \
  -H "X-API-Key: secure-YDiNiwSV5k6A4lKu2EgKt2us-JzdMHEiOeM_rz76CvE" \
  -d '{"prompt": "Define AI", "max_tokens": 50}' | grep provider
```

**Typical Results**:
- Sometimes: `"provider": "gemini"`
- Sometimes: `"provider": "groq"`
- Sometimes: `"provider": "openrouter"`

**What this means**: The API automatically switches between providers based on availability. ✅ High availability!

---

## Interactive Testing

**Try it yourself in the browser**:

1. Go to: https://vn6295337-secure-llm-api.hf.space/docs
2. Click on `/query` endpoint
3. Click "Try it out"
4. Add your API key in the `X-API-Key` field
5. Fill in the request body
6. Click "Execute"
7. See the response instantly!

---

## Performance Comparison

| Test | Response Time | Provider Used |
|------|---------------|---------------|
| "What is AI?" | 87ms | Groq |
| "Explain quantum computing" | 190ms | Groq |
| "Define machine learning" | 110ms | Groq |

**Average**: ~130ms ⚡ Very fast!

---

## Error Scenarios

### 1. All Providers Fail
If all three AI providers are unavailable (very rare):

```json
{
  "response": null,
  "provider": null,
  "latency_ms": 0,
  "status": "error",
  "error": "All LLM providers failed to generate a response."
}
```

### 2. Rate Limit Exceeded
If you send more than 10 requests per minute:

```json
{
  "error": "Rate limit exceeded: 10 per 1 minute"
}
```

### 3. Invalid Temperature
If temperature is outside 0.0-2.0 range:

```json
{
  "detail": [
    {
      "type": "less_than_equal",
      "loc": ["body", "temperature"],
      "msg": "Input should be less than or equal to 2",
      "input": 2.5
    }
  ]
}
```

---

## Code Examples

### Python
```python
import requests

response = requests.post(
    "https://vn6295337-secure-llm-api.hf.space/query",
    headers={
        "Content-Type": "application/json",
        "X-API-Key": "YOUR_API_KEY"
    },
    json={
        "prompt": "What is AI?",
        "max_tokens": 100,
        "temperature": 0.7
    }
)

result = response.json()
print(f"Answer: {result['response']}")
print(f"Provider: {result['provider']}")
print(f"Time: {result['latency_ms']}ms")
```

### JavaScript
```javascript
fetch('https://vn6295337-secure-llm-api.hf.space/query', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'X-API-Key': 'YOUR_API_KEY'
  },
  body: JSON.stringify({
    prompt: 'What is AI?',
    max_tokens: 100,
    temperature: 0.7
  })
})
.then(res => res.json())
.then(data => {
  console.log('Answer:', data.response);
  console.log('Provider:', data.provider);
  console.log('Time:', data.latency_ms + 'ms');
});
```

---

## What You Learned

✅ The API has health monitoring
✅ It requires authentication for queries
✅ It validates all inputs before processing
✅ It automatically switches between AI providers
✅ It responds in under 200ms on average
✅ It blocks invalid requests with clear error messages

**Next Steps**: Try the [full API testing guide](api_testing_guide.md) for more examples!
