"""
Integration tests for the LLM Secure Gateway
"""

import unittest
import requests
import time

class TestGatewayIntegration(unittest.TestCase):
    
    BASE_URL = "http://localhost:8000"
    
    def test_health_endpoint(self):
        """Test the health check endpoint"""
        try:
            response = requests.get(f"{self.BASE_URL}/health", timeout=5)
            
            self.assertEqual(response.status_code, 200)
            
            data = response.json()
            self.assertIn("status", data)
            self.assertIn("timestamp", data)
            self.assertEqual(data["status"], "healthy")
            
        except requests.exceptions.ConnectionError:
            self.skipTest("Gateway not running - skipping integration test")
        except requests.exceptions.Timeout:
            self.fail("Health check timed out")
    
    def test_docs_endpoint(self):
        """Test the documentation endpoint"""
        try:
            response = requests.get(f"{self.BASE_URL}/docs", timeout=5)
            
            self.assertEqual(response.status_code, 200)
            self.assertIn("text/html", response.headers.get("content-type", ""))
            
        except requests.exceptions.ConnectionError:
            self.skipTest("Gateway not running - skipping integration test")
        except requests.exceptions.Timeout:
            self.fail("Docs endpoint timed out")
    
    def test_missing_api_key(self):
        """Test that requests without API key are rejected"""
        try:
            payload = {
                "prompt": "Test prompt",
                "max_tokens": 128,
                "temperature": 0.7
            }
            
            response = requests.post(
                f"{self.BASE_URL}/query",
                json=payload,
                timeout=5
            )
            
            # Should be rejected with 401 or 422
            self.assertIn(response.status_code, [401, 422])
            
        except requests.exceptions.ConnectionError:
            self.skipTest("Gateway not running - skipping integration test")
        except requests.exceptions.Timeout:
            self.fail("Query endpoint timed out")

if __name__ == '__main__':
    unittest.main()