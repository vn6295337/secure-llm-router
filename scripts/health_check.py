#!/usr/bin/env python3
"""
Health check script for Enterprise AI Gateway
"""

import requests
import sys

def health_check():
    """Perform a basic health check of the Enterprise AI Gateway"""
    print("Enterprise AI Gateway - Health Check")
    print("=" * 35)
    
    try:
        # Test health endpoint
        response = requests.get("http://localhost:8000/health", timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            print("✓ Health endpoint accessible")
            print(f"✓ Status: {data.get('status', 'N/A')}")
            print(f"✓ Active provider: {data.get('provider', 'N/A')}")
        else:
            print(f"⚠ Health endpoint returned status {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("✗ Could not connect to the Enterprise AI Gateway")
        print("  Make sure the service is running on http://localhost:8000")
        return False
    except requests.exceptions.Timeout:
        print("✗ Health check timed out")
        return False
    except Exception as e:
        print(f"✗ Health check failed: {e}")
        return False
    
    print("\nHealth check completed successfully!")
    return True

if __name__ == "__main__":
    success = health_check()
    sys.exit(0 if success else 1)