import os
from dotenv import load_dotenv
import requests
import json
import time

# Load environment variables
load_dotenv()

class LLMClient:
    def __init__(self):
        self.gemini_api_key = os.getenv("GEMINI_API_KEY")
        self.groq_api_key = os.getenv("GROQ_API_KEY")
        self.openrouter_api_key = os.getenv("OPENROUTER_API_KEY")

        self.gemini_model = os.getenv("GEMINI_MODEL", "gemini-2.0-flash-exp")
        self.groq_model = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
        self.openrouter_model = os.getenv("OPENROUTER_MODEL", "google/gemini-2.0-flash-exp:free")

        self.providers = []
        if self.gemini_api_key:
            self.providers.append({"name": "gemini", "key": self.gemini_api_key, "model": self.gemini_model})
        if self.groq_api_key:
            self.providers.append({"name": "groq", "key": self.groq_api_key, "model": self.groq_model})
        if self.openrouter_api_key:
            self.providers.append({"name": "openrouter", "key": self.openrouter_api_key, "model": self.openrouter_model})

    async def call_llm_provider(self, provider_name: str, api_key: str, model: str, prompt: str, max_tokens: int, temperature: float):
        headers = {"Content-Type": "application/json"}
        payload = {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": max_tokens,
            "temperature": temperature,
        }

        if provider_name == "gemini":
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
            # Gemini API expects 'contents' not 'messages'
            payload["contents"] = payload.pop("messages")
            # Gemini content structure is slightly different
            payload["contents"] = [{
                "parts": [{
                    "text": prompt
                }]
            }]
            try:
                response = requests.post(url, headers=headers, json=payload)
                response.raise_for_status()
                data = response.json()
                if data and "candidates" in data and data["candidates"]:
                    # Gemini's response structure for text is complex, often in 'parts' of 'content'
                    first_candidate = data["candidates"][0]
                    if "content" in first_candidate and "parts" in first_candidate["content"]:
                        for part in first_candidate["content"]["parts"]:
                            if "text" in part:
                                return part["text"], None
                return None, "No text content found in Gemini response."
            except requests.exceptions.RequestException as e:
                return None, str(e)

        elif provider_name == "groq":
            url = "https://api.groq.com/openai/v1/chat/completions"
            headers["Authorization"] = f"Bearer {api_key}"
            try:
                response = requests.post(url, headers=headers, json=payload)
                response.raise_for_status()
                data = response.json()
                if data and "choices" in data and data["choices"]:
                    return data["choices"][0]["message"]["content"], None
                return None, "No content found in Groq response."
            except requests.exceptions.RequestException as e:
                return None, str(e)

        elif provider_name == "openrouter":
            url = "https://openrouter.ai/api/v1/chat/completions"
            headers["Authorization"] = f"Bearer {api_key}"
            headers["HTTP-Referer"] = "http://localhost:8000"  # Replace with your app URL
            headers["X-Title"] = "Secure LLM Router PoC"
            try:
                response = requests.post(url, headers=headers, json=payload)
                response.raise_for_status()
                data = response.json()
                if data and "choices" in data and data["choices"]:
                    return data["choices"][0]["message"]["content"], None
                return None, "No content found in OpenRouter response."
            except requests.exceptions.RequestException as e:
                return None, str(e)
        else:
            return None, f"Unknown LLM provider: {provider_name}"

    async def query_llm_cascade(self, prompt: str, max_tokens: int, temperature: float):
        for provider in self.providers:
            print(f"Attempting with {provider['name']}...")
            start_time = time.perf_counter()
            response_content, error = await self.call_llm_provider(
                provider_name=provider["name"],
                api_key=provider["key"],
                model=provider["model"],
                prompt=prompt,
                max_tokens=max_tokens,
                temperature=temperature
            )
            latency_ms = int((time.perf_counter() - start_time) * 1000)

            if response_content:
                return response_content, provider["name"], latency_ms, None
            else:
                print(f"Provider {provider['name']} failed: {error}")
        return None, None, 0, "All LLM providers failed."

# Instantiate the client (can be imported and used in app.py)
llm_client = LLMClient()