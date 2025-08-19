#!/usr/bin/env python3
"""
Local test script for the Flask application
Run this to test the service locally without Docker
"""

import requests
import json
import time

# Test server URL (change if needed)
BASE_URL = "http://localhost:8080"

def test_health():
    """Test the health endpoint."""
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"Health check: {response.status_code} - {response.json()}")
        return response.status_code == 200
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server. Is it running?")
        return False

def test_basic_script():
    """Test a basic script execution."""
    script = '''
def main():
    return {"message": "Hello from Python!", "status": "success"}
'''
    
    data = {"script": script}
    
    try:
        response = requests.post(f"{BASE_URL}/execute", json=data)
        print(f"Basic script: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Result: {result['result']}")
            print(f"✅ Stdout: {result['stdout']}")
            return True
        else:
            print(f"❌ Error: {response.json()}")
            return False
    except Exception as e:
        print(f"❌ Exception: {e}")
        return False

def test_data_processing():
    """Test pandas and numpy functionality."""
    script = '''
import pandas as pd
import numpy as np

def main():
    # Create sample data
    data = np.random.randn(10)
    df = pd.DataFrame({"values": data})
    
    stats = {
        "count": len(df),
        "mean": float(df["values"].mean()),
        "std": float(df["values"].std())
    }
    
    print("Data processing completed")
    return stats
'''
    
    data = {"script": script}
    
    try:
        response = requests.post(f"{BASE_URL}/execute", json=data)
        print(f"Data processing: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Result: {result['result']}")
            print(f"✅ Stdout: {result['stdout']}")
            return True
        else:
            print(f"❌ Error: {response.json()}")
            return False
    except Exception as e:
        print(f"❌ Exception: {e}")
        return False

def test_error_handling():
    """Test error handling for invalid scripts."""
    # Test missing main function
    script1 = '''
def hello():
    return "Hello"
'''
    
    data1 = {"script": script1}
    
    try:
        response = requests.post(f"{BASE_URL}/execute", json=data1)
        print(f"Missing main function: {response.status_code}")
        if response.status_code == 400:
            print(f"✅ Expected error: {response.json()}")
        else:
            print(f"❌ Unexpected status: {response.status_code}")
    except Exception as e:
        print(f"❌ Exception: {e}")
    
    # Test non-JSON return
    script2 = '''
def main():
    return "Not JSON"
'''
    
    data2 = {"script": script2}
    
    try:
        response = requests.post(f"{BASE_URL}/execute", json=data2)
        print(f"Non-JSON return: {response.status_code}")
        if response.status_code == 500:
            print(f"✅ Expected error: {response.json()}")
        else:
            print(f"❌ Unexpected status: {response.status_code}")
    except Exception as e:
        print(f"❌ Exception: {e}")

def run_all_tests():
    """Run all tests."""
    print("🧪 Running Python Code Execution Service Tests")
    print("=" * 50)
    
    tests = [
        ("Health Check", test_health),
        ("Basic Script", test_basic_script),
        ("Data Processing", test_data_processing),
        ("Error Handling", test_error_handling)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🔍 Testing: {test_name}")
        print("-" * 30)
        
        if test_func():
            passed += 1
            print(f"✅ {test_name}: PASSED")
        else:
            print(f"❌ {test_name}: FAILED")
        
        time.sleep(0.5)  # Small delay between tests
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Service is working correctly.")
    else:
        print("⚠️  Some tests failed. Check the service configuration.")

if __name__ == "__main__":
    run_all_tests() 