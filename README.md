# Python Code Execution Service

A secure, containerized service that executes arbitrary Python code in a sandboxed environment and returns the result of the `main()` function. Perfect for building code execution platforms, educational tools, or API services that need to run Python code safely.

## 🌟 Features

- **Secure Execution**: Code runs in isolated subprocess environment with resource limits
- **Smart Output Capture**: Separates function return values from print statements
- **Library Support**: Built-in support for pandas, numpy, and other Python libraries
- **JSON Validation**: Ensures all return values are JSON-serializable
- **Error Handling**: Comprehensive error reporting and validation
- **Docker Ready**: Lightweight container for easy deployment
- **Cloud Native**: Designed for deployment on Railway, Google Cloud Run, or any container platform

## 🚀 Live Service

The service is now deployed and available at: **`https://pythonexecutor-production.up.railway.app`**

### Quick Test
```bash
# Health check
curl https://pythonexecutor-production.up.railway.app/health

# Basic execution
curl -X POST https://pythonexecutor-production.up.railway.app/execute \
  -H "Content-Type: application/json" \
  -d '{"script": "def main():\n    return {\"message\": \"Hello World!\"}"}'
```

## 🏗️ Architecture

### How It Works
1. **Request Validation**: Checks for valid JSON and required script field
2. **Script Validation**: Ensures script contains `main()` function and valid Python syntax
3. **Safe Execution**: Runs script in isolated subprocess with timeout protection
4. **Output Processing**: Captures stdout separately from function return value
5. **JSON Conversion**: Handles numpy/pandas types and validates JSON serialization
6. **Response**: Returns structured JSON with result and stdout

### Security Features
- **Process Isolation**: Each script runs in separate subprocess
- **Resource Limits**: 30-second execution timeout
- **Non-root Execution**: Container runs as unprivileged user
- **Input Validation**: Strict validation of script content and return values
- **Error Containment**: Script errors don't affect the main service

## 📋 Prerequisites

- **Docker** (for containerized deployment)
- **Python 3.11+** (for local development)
- **curl** (for testing)

## 🚀 Quick Start

### Option 1: Use the Live Service
The service is already deployed and ready to use at:
```
https://pythonexecutor-production.up.railway.app
```

### Option 2: Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/pranitha275/PythonExecutor.git
   cd PythonExecutor
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run locally**
   ```bash
   python app.py
   ```

4. **Test the service**
   ```bash
   curl -X POST http://localhost:8080/execute \
     -H "Content-Type: application/json" \
     -d '{"script": "def main():\n    return {\"message\": \"Hello Local!\"}"}'
   ```

### Option 3: Docker Deployment

1. **Build the image**
   ```bash
   docker build -t python-executor .
   ```

2. **Run the container**
   ```bash
   docker run -p 8080:8080 python-executor
   ```

3. **Test the service**
   ```bash
   curl -X POST http://localhost:8080/execute \
     -H "Content-Type: application/json" \
     -d '{"script": "def main():\n    return {\"message\": \"Hello Docker!\"}"}'
   ```

## 🎯 API Reference

### POST /execute

Executes a Python script and returns the result of the `main()` function.

**Request Body:**
```json
{
  "script": "def main():\n    return {\"message\": \"Hello World\"}"
}
```

**Response:**
```json
{
  "result": {"message": "Hello World"},
  "stdout": ""
}
```

**Error Response:**
```json
{
  "error": "Script must contain a 'main()' function"
}
```

### GET /health

Health check endpoint.

**Response:**
```json
{
  "status": "healthy"
}
```

## 📝 Script Requirements

### Required Structure
1. **Must contain a `main()` function**
2. **`main()` function must return JSON-serializable data**
3. **Valid Python syntax**

### Valid Examples

**Basic Return:**
```python
def main():
    return {"message": "Hello World"}
```

**With Print Statements:**
```python
def main():
    print("Processing data...")
    result = {"status": "success", "count": 42}
    print(f"Returning {result}")
    return result
```

**Using Libraries:**
```python
import pandas as pd
import numpy as np

def main():
    df = pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6]})
    print(f"DataFrame shape: {df.shape}")
    return {
        "shape": df.shape,
        "sum": df.sum().to_dict(),
        "mean": df.mean().to_dict()
    }
```

### Invalid Examples

**Missing main() function:**
```python
print("Hello World")
# ❌ No main() function
```

**Non-JSON return:**
```python
def main():
    return lambda x: x  # ❌ Lambda functions aren't JSON serializable
```

**Syntax Error:**
```python
def main():
    return {"message": "Hello"  # ❌ Missing closing brace
```

## 🧪 Testing Examples

### Test 1: Basic Functionality
```bash
curl -X POST https://pythonexecutor-production.up.railway.app/execute \
  -H "Content-Type: application/json" \
  -d '{"script": "def main():\n    print(\"Hello from Railway!\")\n    return {\"message\": \"Success!\", \"timestamp\": \"2024-01-01\"}"}'
```

**Expected Response:**
```json
{
  "result": {
    "message": "Success!",
    "timestamp": "2024-01-01"
  },
  "stdout": "Hello from Railway!"
}
```

### Test 2: Data Processing with Pandas
```bash
curl -X POST https://pythonexecutor-production.up.railway.app/execute \
  -H "Content-Type: application/json" \
  -d '{"script": "import pandas as pd\nimport numpy as np\ndef main():\n    df = pd.DataFrame({\"A\": [1, 2, 3], \"B\": [4, 5, 6]})\n    print(f\"DataFrame shape: {df.shape}\")\n    return {\"shape\": df.shape, \"sum\": df.sum().to_dict()}"}'
```

**Expected Response:**
```json
{
  "result": {
    "shape": [3, 2],
    "sum": {"A": 6, "B": 15}
  },
  "stdout": "DataFrame shape: (3, 2)"
}
```

### Test 3: Error Handling
```bash
curl -X POST https://pythonexecutor-production.up.railway.app/execute \
  -H "Content-Type: application/json" \
  -d '{"script": "def main():\n    return lambda x: x"}'
```

**Expected Response:**
```json
{
  "error": "Execution error: main() function must return valid JSON"
}
```

## 🚀 Deployment

### Railway.app (Recommended for Quick Start)

1. **Fork this repository** to your GitHub account
2. **Connect Railway** to your GitHub repository
3. **Deploy automatically** - Railway will detect the Dockerfile and deploy
4. **Get your public URL** from the Railway dashboard

### Google Cloud Run

1. **Build and push to Google Container Registry**
   ```bash
   gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/python-executor
   ```

2. **Deploy to Cloud Run**
   ```bash
   gcloud run deploy python-executor \
     --image gcr.io/YOUR_PROJECT_ID/python-executor \
     --platform managed \
     --region us-central1 \
     --allow-unauthenticated
   ```

### Other Platforms

- **AWS ECS/Fargate**: Use the Dockerfile with ECS task definition
- **Azure Container Instances**: Deploy directly from Docker image
- **DigitalOcean App Platform**: Connect GitHub repository for auto-deployment

## 🔧 Configuration

### Environment Variables

- **PORT**: Port to bind to (default: 8080)
- **WORKERS**: Number of Gunicorn workers (default: 1)
- **TIMEOUT**: Request timeout in seconds (default: 60)

### Customization

**Modify timeout in start.sh:**
```bash
exec gunicorn --bind 0.0.0.0:$PORT --workers 1 --timeout 120 app:app
```

**Add more workers for production:**
```bash
exec gunicorn --bind 0.0.0.0:$PORT --workers 4 --timeout 60 app:app
```

## 🛠️ Development

### Project Structure
```
PythonExecutor/
├── app.py              # Main Flask application
├── start.sh            # Startup script for production
├── Dockerfile          # Container configuration
├── requirements.txt    # Python dependencies
├── railway.json        # Railway deployment config
├── README.md           # This file
└── test_examples.py    # Example scripts for testing
```

### Adding New Features

1. **New Endpoints**: Add routes to `app.py`
2. **Enhanced Security**: Implement nsjail or similar sandboxing
3. **Additional Libraries**: Update `requirements.txt` and Dockerfile
4. **Custom Validation**: Extend `validate_script()` function

### Testing

**Run local tests:**
```bash
python test_examples.py
```

**Test with custom scripts:**
```bash
curl -X POST http://localhost:8080/execute \
  -H "Content-Type: application/json" \
  -d '{"script": "YOUR_PYTHON_SCRIPT_HERE"}'
```

## 🔒 Security Considerations

### Current Implementation
- **Process Isolation**: Each script runs in separate subprocess
- **Resource Limits**: Execution timeout prevents infinite loops
- **Input Validation**: Script content and return value validation
- **Non-root Execution**: Container runs as unprivileged user

### Production Enhancements
- **nsjail Integration**: Advanced sandboxing for better isolation
- **Resource Quotas**: CPU and memory limits per execution
- **Network Isolation**: Prevent outbound network calls
- **File System Restrictions**: Limit file access and creation
- **Rate Limiting**: Prevent abuse through request throttling

## 🐛 Troubleshooting

### Common Issues

**Service won't start:**
- Check if port 8080 is available
- Verify Docker container is running
- Check logs: `docker logs <container_id>`

**Script execution fails:**
- Ensure script contains `main()` function
- Check Python syntax is valid
- Verify return value is JSON-serializable

**Permission denied errors:**
- Ensure startup script is executable: `chmod +x start.sh`
- Check file ownership in container

**Timeout errors:**
- Increase timeout in `start.sh` if needed
- Check if script has infinite loops

### Debug Mode

**Enable Flask debug mode locally:**
```python
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
```

**Check container logs:**
```bash
docker logs <container_id>
```

## 🤝 Contributing

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature-name`
3. **Make your changes**
4. **Test thoroughly**
5. **Submit a pull request**

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🙏 Acknowledgments

- **Flask**: Web framework for the API
- **Gunicorn**: WSGI server for production
- **Railway**: Free hosting platform
- **Docker**: Containerization technology

## 📞 Support

- **Issues**: Report bugs on GitHub Issues
- **Discussions**: Ask questions on GitHub Discussions
- **Documentation**: Check this README for common solutions

---

**Happy coding! 🚀**

Your Python Code Execution Service is ready to power the next generation of code execution platforms! 