# Python Code Execution Service

A secure, containerized service that executes arbitrary Python code in a sandboxed environment and returns the result of the `main()` function.

## Features

- **Secure Execution**: Uses nsjail for sandboxed code execution
- **Resource Limits**: CPU, memory, and file size restrictions
- **Input Validation**: Ensures scripts contain valid `main()` function
- **JSON Output**: Returns both function result and stdout separately
- **Docker Ready**: Lightweight container for easy deployment

## Security Features

- **Basic Sandboxing**: Script execution in isolated subprocess environment
- **Resource Limits**: 
  - 30 second execution timeout
  - Process isolation from main service
- **Non-root Execution**: Runs as unprivileged user
- **Input Validation**: Strict validation of script content and return values
- **Note**: This is a simplified version for demonstration. For production use, implement nsjail or similar sandboxing.

## Prerequisites

- Docker
- curl (for testing)

## Quick Start

### Local Development

1. **Build the Docker image:**
   ```bash
   docker build -t python-executor .
   ```

2. **Run the service:**
   ```bash
   docker run -p 8080:8080 python-executor
   ```

**Note**: The service is currently running on port 8081 to avoid conflicts with other services. Adjust the port mapping as needed.

3. **Test the service:**
   ```bash
   curl -X POST http://localhost:8080/execute \
     -H "Content-Type: application/json" \
     -d '{
       "script": "import pandas as pd\nimport numpy as np\ndef main():\n    df = pd.DataFrame({\"A\": [1, 2, 3], \"B\": [4, 5, 6]})\n    result = {\"sum\": df[\"A\"].sum(), \"mean\": df[\"B\"].mean()}\n    print(\"Processing data...\")\n    return result"
     }'
   ```

### Expected Response

```json
{
  "result": {
    "sum": 6,
    "mean": 5.0
  },
  "stdout": "Processing data..."
}
```

## API Endpoints

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

### GET /health

Health check endpoint.

**Response:**
```json
{
  "status": "healthy"
}
```

## Script Requirements

1. **Must contain a `main()` function**
2. **`main()` function must return JSON-serializable data**
3. **Valid Python syntax**
4. **Access to standard libraries: `os`, `pandas`, `numpy`**

## Example Scripts

### Basic Example
```python
def main():
    return {"message": "Hello from Python!"}
```

### Data Processing Example
```python
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
    return stats
```

### File System Example (Limited Access)
```python
import os

def main():
    # Only /tmp directory is accessible
    files = os.listdir("/tmp")
    return {"files_in_tmp": files}
```

## Error Handling

The service returns appropriate HTTP status codes and error messages:

- **400 Bad Request**: Invalid script format or syntax
- **500 Internal Server Error**: Execution failures or timeouts

### Common Error Scenarios

1. **Missing main() function:**
   ```json
   {"error": "Script must contain a 'main()' function"}
   ```

2. **Invalid Python syntax:**
   ```json
   {"error": "Invalid Python syntax: invalid syntax (<string>, line 1)"}
   ```

3. **Non-JSON return value:**
   ```json
   {"error": "main() function must return valid JSON"}
   ```

4. **Execution timeout:**
   ```json
   {"error": "Script execution timed out"}
   ```

## Deployment

### Google Cloud Run

1. **Build and push to Google Container Registry:**
   ```bash
   gcloud builds submit --tag gcr.io/PROJECT_ID/python-executor
   ```

2. **Deploy to Cloud Run:**
   ```bash
   gcloud run deploy python-executor \
     --image gcr.io/PROJECT_ID/python-executor \
     --platform managed \
     --region us-central1 \
     --allow-unauthenticated \
     --port 8080
   ```

3. **Test with Cloud Run URL:**
   ```bash
   curl -X POST https://YOUR_SERVICE_URL/execute \
     -H "Content-Type: application/json" \
     -d '{"script": "def main():\n    return {\"deployed\": true}"}'
   ```

### Docker Compose (Optional)

```yaml
version: '3.8'
services:
  python-executor:
    build: .
    ports:
      - "8080:8080"
    environment:
      - FLASK_ENV=production
```

## Security Considerations

- **Code Isolation**: User scripts run in completely isolated containers
- **Resource Limits**: Strict limits prevent resource exhaustion attacks
- **File System Access**: Only essential directories are mounted
- **Network Isolation**: No external network access from scripts
- **Process Limits**: Single process execution with timeout

## Performance

- **Lightweight Image**: Based on Python slim image
- **Fast Startup**: Optimized for Cloud Run deployment
- **Efficient Execution**: Single worker process for security

## Troubleshooting

### Common Issues

1. **nsjail not found**: Ensure Docker image built correctly
2. **Permission denied**: Check file ownership in container
3. **Import errors**: Verify package paths in nsjail config

### Debug Mode

For local development, you can run Flask in debug mode:

```bash
docker run -p 8080:8080 -e FLASK_ENV=development python-executor
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License. 