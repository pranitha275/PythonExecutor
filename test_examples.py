#!/usr/bin/env python3
"""
Test examples for the Python Code Execution Service
These scripts can be sent to the /execute endpoint for testing.
"""

# Basic example - simple return
BASIC_SCRIPT = '''
def main():
    return {"message": "Hello from Python!", "status": "success"}
'''

# Data processing example with pandas and numpy
DATA_PROCESSING_SCRIPT = '''
import pandas as pd
import numpy as np

def main():
    # Create sample data
    data = np.random.randn(100)
    df = pd.DataFrame({"values": data})
    
    # Calculate statistics
    stats = {
        "count": len(df),
        "mean": float(df["values"].mean()),
        "std": float(df["values"].std()),
        "min": float(df["values"].min()),
        "max": float(df["values"].max())
    }
    
    print("Data analysis complete!")
    print(f"Processed {len(df)} data points")
    return stats
'''

# File system example (limited access)
FILE_SYSTEM_SCRIPT = '''
import os

def main():
    try:
        # Only /tmp directory is accessible
        files = os.listdir("/tmp")
        return {"files_in_tmp": files, "access": "limited"}
    except Exception as e:
        return {"error": str(e), "access": "denied"}
'''

# Mathematical computation example
MATH_SCRIPT = '''
import math

def main():
    # Calculate some mathematical constants
    pi = math.pi
    e = math.e
    
    # Generate some calculations
    calculations = {
        "pi": pi,
        "e": e,
        "pi_squared": pi ** 2,
        "e_pi": e ** pi,
        "factorial_10": math.factorial(10),
        "sqrt_2": math.sqrt(2)
    }
    
    print("Mathematical calculations completed")
    return calculations
'''

# Error handling example (will cause an error)
ERROR_SCRIPT = '''
def main():
    # This will cause a division by zero error
    result = 1 / 0
    return {"result": result}
'''

# Missing main function (will cause validation error)
INVALID_SCRIPT = '''
def hello():
    return "Hello World"
'''

# Non-JSON return (will cause error)
NON_JSON_SCRIPT = '''
def main():
    return "This is not JSON"
'''

# Test scripts dictionary
TEST_SCRIPTS = {
    "basic": BASIC_SCRIPT,
    "data_processing": DATA_PROCESSING_SCRIPT,
    "file_system": FILE_SYSTEM_SCRIPT,
    "math": MATH_SCRIPT,
    "error": ERROR_SCRIPT,
    "invalid": INVALID_SCRIPT,
    "non_json": NON_JSON_SCRIPT
}

def print_test_script(name, script):
    """Print a test script with its name."""
    print(f"\n{'='*50}")
    print(f"TEST SCRIPT: {name.upper()}")
    print(f"{'='*50}")
    print(script.strip())
    print(f"{'='*50}")

if __name__ == "__main__":
    print("Python Code Execution Service - Test Scripts")
    print("Use these scripts to test the /execute endpoint")
    
    for name, script in TEST_SCRIPTS.items():
        print_test_script(name, script)
    
    print("\nTo test with curl:")
    print("curl -X POST http://localhost:8080/execute \\")
    print("  -H 'Content-Type: application/json' \\")
    print("  -d '{\"script\": \"def main():\\n    return {\\\"test\\\": \\\"value\\\"}\"}'") 