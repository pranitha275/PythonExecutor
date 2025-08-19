#!/usr/bin/env python3
"""
Test Examples for Python Code Execution Service

This file contains various Python script examples that can be used to test
the /execute endpoint of the service.
"""

# Example 1: Basic function with return value
BASIC_SCRIPT = '''
def main():
    return {"message": "Hello World", "status": "success"}
'''

# Example 2: Function with print statements
PRINT_SCRIPT = '''
def main():
    print("Starting calculation...")
    result = 42 * 2
    print(f"Calculation result: {result}")
    return {"result": result, "message": "Calculation complete"}
'''

# Example 3: Data processing with pandas
PANDAS_SCRIPT = '''
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

# Example 4: Error handling example
ERROR_SCRIPT = '''
def main():
    try:
        result = 10 / 0
        return {"result": result}
    except ZeroDivisionError as e:
        return {"error": str(e), "type": "ZeroDivisionError"}
'''

# Example 5: Complex data structure
COMPLEX_SCRIPT = '''
def main():
    # Create nested data structure
    data = {
        "users": [
            {"id": 1, "name": "Alice", "age": 30},
            {"id": 2, "name": "Bob", "age": 25},
            {"id": 3, "name": "Charlie", "age": 35}
        ],
        "metadata": {
            "total_users": 3,
            "average_age": 30.0,
            "created_at": "2024-01-01"
        }
    }
    
    print(f"Processed {data['metadata']['total_users']} users")
    return data
'''

# Example 6: Mathematical calculations
MATH_SCRIPT = '''
import math

def main():
    # Calculate various mathematical values
    pi = math.pi
    e = math.e
    sqrt_2 = math.sqrt(2)
    
    calculations = {
        "pi": pi,
        "e": e,
        "sqrt_2": sqrt_2,
        "sin_pi": math.sin(pi),
        "cos_pi": math.cos(pi),
        "log_10": math.log10(100)
    }
    
    print("Mathematical calculations completed")
    return calculations
'''

# Example 7: String processing
STRING_SCRIPT = '''
def main():
    text = "Hello, World! This is a test string."
    
    # Process the string
    processed = {
        "original": text,
        "length": len(text),
        "uppercase": text.upper(),
        "lowercase": text.lower(),
        "word_count": len(text.split()),
        "reversed": text[::-1]
    }
    
    print(f"Processed string: {text}")
    return processed
'''

# Example 8: List and dictionary operations
DATA_SCRIPT = '''
def main():
    # Create sample data
    numbers = list(range(1, 11))
    squares = [x**2 for x in numbers]
    cubes = [x**3 for x in numbers]
    
    # Create dictionary
    data = {
        "numbers": numbers,
        "squares": squares,
        "cubes": cubes,
        "sum_numbers": sum(numbers),
        "sum_squares": sum(squares),
        "sum_cubes": sum(cubes)
    }
    
    print(f"Generated {len(numbers)} numbers")
    return data
'''

# Example 9: File-like operations (simulated)
FILE_SCRIPT = '''
from io import StringIO

def main():
    # Simulate file operations
    content = "Line 1\\nLine 2\\nLine 3\\nLine 4\\nLine 5"
    
    # Process content
    lines = content.split('\\n')
    line_count = len(lines)
    char_count = len(content)
    
    # Create result
    result = {
        "content": content,
        "line_count": line_count,
        "char_count": char_count,
        "lines": lines,
        "first_line": lines[0] if lines else "",
        "last_line": lines[-1] if lines else ""
    }
    
    print(f"Processed file with {line_count} lines")
    return result
'''

# Example 10: Conditional logic
CONDITIONAL_SCRIPT = '''
def main():
    import random
    
    # Generate random number
    number = random.randint(1, 100)
    
    # Apply conditional logic
    if number < 25:
        category = "low"
        message = "Number is in the low range"
    elif number < 75:
        category = "medium"
        message = "Number is in the medium range"
    else:
        category = "high"
        message = "Number is in the high range"
    
    result = {
        "number": number,
        "category": category,
        "message": message,
        "is_even": number % 2 == 0,
        "is_prime": number > 1 and all(number % i != 0 for i in range(2, int(number**0.5) + 1))
    }
    
    print(f"Generated number: {number}")
    return result
'''

# Dictionary of all examples
EXAMPLES = {
    "basic": BASIC_SCRIPT,
    "print": PRINT_SCRIPT,
    "pandas": PANDAS_SCRIPT,
    "error": ERROR_SCRIPT,
    "complex": COMPLEX_SCRIPT,
    "math": MATH_SCRIPT,
    "string": STRING_SCRIPT,
    "data": DATA_SCRIPT,
    "file": FILE_SCRIPT,
    "conditional": CONDITIONAL_SCRIPT
}

def print_examples():
    """Print all available examples."""
    print("Available test examples:")
    for name, script in EXAMPLES.items():
        print(f"  {name}: {script.split('def main():')[0].strip()}")
    print()

def get_example(name):
    """Get a specific example by name."""
    return EXAMPLES.get(name, BASIC_SCRIPT)

if __name__ == "__main__":
    print_examples()
    print("Use these examples to test your Python Code Execution Service!")
    print("Example usage:")
    print("  curl -X POST http://localhost:8080/execute \\")
    print("    -H 'Content-Type: application/json' \\")
    print("    -d '{\"script\": \"def main(): return {\\\"message\\\": \\\"Hello\\\"}\"}'") 