import json
import subprocess
import tempfile
import os
import sys
from flask import Flask, request, jsonify
import traceback

app = Flask(__name__)

def validate_script(script):
    """Validate that the script contains a main() function and is valid Python."""
    if not script or not isinstance(script, str):
        raise ValueError("Script must be a non-empty string")
    
    if "def main()" not in script:
        raise ValueError("Script must contain a 'main()' function")
    
    # Basic Python syntax validation
    try:
        compile(script, '<string>', 'exec')
    except SyntaxError as e:
        raise ValueError(f"Invalid Python syntax: {str(e)}")

def execute_script_safely(script):
    """Execute the Python script in a secure environment."""
    
    try:
        # Escape quotes and newlines for the wrapper script
        script_escaped = script.replace('"', '\\"').replace('\n', '\\n')
        
        # Create wrapper script that executes user code and captures output
        wrapper_script = f'''import sys
import json
import traceback
from io import StringIO

# Create namespace for user code
user_globals = {{}}

try:
    # Execute user script in namespace
    exec("{script_escaped}", user_globals)
    
    # Check if main function exists
    if 'main' not in user_globals:
        print("Error: main() function not found", file=sys.stderr)
        sys.exit(1)
    
    # Capture stdout during main() execution
    original_stdout = sys.stdout
    stdout_capture = StringIO()
    sys.stdout = stdout_capture
    
    try:
        # Call main function
        result = user_globals['main']()
        
        # Convert numpy types to Python native types for JSON serialization
        try:
            import numpy as np
            
            # Custom JSON encoder for numpy types
            class NumpyEncoder(json.JSONEncoder):
                def default(self, obj):
                    if isinstance(obj, np.integer):
                        return int(obj)
                    elif isinstance(obj, np.floating):
                        return float(obj)
                    elif isinstance(obj, np.ndarray):
                        return obj.tolist()
                    return super().default(obj)
            
            # Convert result using custom encoder
            result = json.loads(json.dumps(result, cls=NumpyEncoder))
        except:
            pass  # Continue if numpy is not available
        
        # Restore stdout and print captured output
        sys.stdout = original_stdout
        print(stdout_capture.getvalue(), end='')
        
        # Validate JSON serializability
        try:
            json.dumps(result)
        except (TypeError, ValueError) as e:
            print(f"Error: main() function must return valid JSON: {{str(e)}}", file=sys.stderr)
            sys.exit(1)
        
        # Print result as JSON on last line
        print(json.dumps(result))
        
    finally:
        # Ensure stdout is restored
        sys.stdout = original_stdout
        
except Exception as e:
    print(f"Error: {{str(e)}}", file=sys.stderr)
    traceback.print_exc(file=sys.stderr)
    sys.exit(1)'''
        
        # Create temporary file for wrapper
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(wrapper_script)
            wrapper_file = f.name
        
        # Execute with timeout
        result = subprocess.run(
            ['python3', wrapper_file],
            capture_output=True,
            text=True,
            timeout=30,  # 30 second timeout
            cwd='/tmp'
        )
        
        # Check execution success
        if result.returncode != 0:
            raise RuntimeError(f"Script execution failed: {result.stderr}")
        
        # Parse output to separate stdout from return value
        lines = result.stdout.strip().split('\n')
        
        if not lines:
            raise ValueError("Script execution produced no output")
        
        # Last line contains return value (JSON)
        try:
            return_value = json.loads(lines[-1])
        except json.JSONDecodeError:
            raise ValueError("main() function must return valid JSON")
        
        # Everything except last line is stdout
        stdout_output = '\n'.join(lines[:-1]) if len(lines) > 1 else ""
        
        return {
            "result": return_value,
            "stdout": stdout_output
        }
        
    except subprocess.TimeoutExpired:
        raise RuntimeError("Script execution timed out")
    except Exception as e:
        raise RuntimeError(f"Execution error: {str(e)}")
    finally:
        # Clean up temporary file
        try:
            os.unlink(wrapper_file)
        except:
            pass

@app.route('/execute', methods=['POST'])
def execute():
    """Execute Python script and return main() function result."""
    try:
        # Validate request
        if not request.is_json:
            return jsonify({"error": "Request must be JSON"}), 400
        
        data = request.get_json()
        if not data or 'script' not in data:
            return jsonify({"error": "Request must contain 'script' field"}), 400
        
        script = data['script']
        
        # Validate script
        try:
            validate_script(script)
        except ValueError as e:
            return jsonify({"error": str(e)}), 400
        
        # Execute script safely
        try:
            result = execute_script_safely(script)
            return jsonify(result)
        except Exception as e:
            return jsonify({"error": str(e)}), 500
            
    except Exception as e:
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({"status": "healthy"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=False) 