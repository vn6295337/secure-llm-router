"""
Basic usage examples for the LLM Secure Gateway
"""

import requests
import json
import time

# Configuration
BASE_URL = "http://localhost:8000"
API_KEY = "your-api-key-here"  # Replace with your actual API key

def example_health_check():
    """Example of health check endpoint usage"""
    print("=== Health Check Example ===")
    
    response = requests.get(f"{BASE_URL}/health")
    
    if response.status_code == 200:
        data = response.json()
        print(f"Status: {data['status']}")
        print(f"Provider: {data['provider']}")
        print(f"Timestamp: {data['timestamp']}")
    else:
        print(f"Health check failed with status code: {response.status_code}")

def example_single_query():
    """Example of single query to the LLM"""
    print("\n=== Single Query Example ===")
    
    headers = {
        "Content-Type": "application/json",
        "X-API-Key": API_KEY
    }
    
    payload = {
        "prompt": "Explain the benefits of using a secure LLM gateway in enterprise applications.",
        "max_tokens": 256,
        "temperature": 0.7
    }
    
    response = requests.post(f"{BASE_URL}/query", headers=headers, json=payload)
    
    if response.status_code == 200:
        data = response.json()
        print(f"Response: {data['response']}")
        print(f"Provider: {data['provider']}")
        print(f"Latency: {data['latency_ms']} ms")
        print(f"Status: {data['status']}")
    else:
        print(f"Query failed with status code: {response.status_code}")
        print(f"Response: {response.text}")

def example_batch_queries():
    """Example of batch queries to the LLM"""
    print("\n=== Batch Queries Example ===")
    
    queries = [
        "What is artificial intelligence?",
        "Explain machine learning in simple terms",
        "What are the benefits of cloud computing?",
        "How does blockchain technology work?",
        "What is the difference between HTTP and HTTPS?"
    ]
    
    headers = {
        "Content-Type": "application/json",
        "X-API-Key": API_KEY
    }
    
    results = []
    
    for i, query in enumerate(queries, 1):
        print(f"\nProcessing query {i}/{len(queries)}: {query[:50]}...")
        
        payload = {
            "prompt": query,
            "max_tokens": 128,
            "temperature": 0.7
        }
        
        response = requests.post(f"{BASE_URL}/query", headers=headers, json=payload)
        
        if response.status_code == 200:
            data = response.json()
            results.append({
                "query": query,
                "response": data["response"],
                "provider": data["provider"],
                "latency_ms": data["latency_ms"]
            })
            print(f"  ✓ Success - {data['provider']} ({data['latency_ms']} ms)")
        else:
            print(f"  ✗ Failed - Status {response.status_code}")
        
        # Small delay to avoid rate limiting
        time.sleep(0.5)
    
    # Print summary
    print(f"\n=== Batch Results Summary ===")
    total_latency = sum(result["latency_ms"] for result in results if "latency_ms" in result)
    avg_latency = total_latency / len(results) if results else 0
    
    print(f"Successful queries: {len(results)}/{len(queries)}")
    print(f"Average latency: {avg_latency:.2f} ms")
    print(f"Providers used: {set(result['provider'] for result in results if 'provider' in result)}")

if __name__ == "__main__":
    # Note: Make sure the LLM Secure Gateway is running before executing these examples
    example_health_check()
    example_single_query()
    example_batch_queries()