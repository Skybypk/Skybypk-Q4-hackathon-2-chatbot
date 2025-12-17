#!/usr/bin/env python3
"""
Test script to verify the chatbot system is working
"""
import requests
import time
import sys

def test_backend_health():
    """Test if the backend is running and healthy"""
    try:
        response = requests.get("http://localhost:8000/health", timeout=10)
        if response.status_code == 200:
            print("✅ Backend is healthy")
            return True
        else:
            print(f"❌ Backend health check failed: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Backend is not accessible: {e}")
        return False

def test_backend_root():
    """Test the root endpoint"""
    try:
        response = requests.get("http://localhost:8000/", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Backend root endpoint working: {data}")
            return True
        else:
            print(f"❌ Backend root endpoint failed: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Backend root endpoint error: {e}")
        return False

def test_query_endpoint():
    """Test the query endpoint with a simple request"""
    try:
        # Test query
        payload = {
            "query": "What is humanoid robotics?",
            "user_id": "test_user",
            "language": "en"
        }
        response = requests.post("http://localhost:8000/query", json=payload, timeout=30)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Query endpoint working, got response: {data.get('answer', 'No answer field')[:100]}...")
            return True
        else:
            print(f"❌ Query endpoint failed: {response.status_code}, response: {response.text}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Query endpoint error: {e}")
        return False
    except Exception as e:
        print(f"❌ Query endpoint unexpected error: {e}")
        return False

def main():
    print("Testing Chatbot System...")
    print("="*50)

    # Wait a moment for the server to be fully ready
    print("Waiting for server to be ready...")
    time.sleep(5)

    all_tests_passed = True

    print("\n1. Testing backend health...")
    if not test_backend_health():
        all_tests_passed = False

    print("\n2. Testing backend root endpoint...")
    if not test_backend_root():
        all_tests_passed = False

    print("\n3. Testing query endpoint...")
    if not test_query_endpoint():
        all_tests_passed = False

    print("\n" + "="*50)
    if all_tests_passed:
        print("SUCCESS: All tests passed! The chatbot backend is working properly.")
        print("\nYou can now access:")
        print("   - API: http://localhost:8000")
        print("   - API Docs: http://localhost:8000/docs")
        print("   - Chat interface will work at: http://localhost:3000/chat (after starting frontend)")
    else:
        print("ERROR: Some tests failed. Please check the backend server.")

    return all_tests_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)