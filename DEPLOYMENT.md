# 🚀 Deployment Guide

This guide covers deploying your Python Code Execution Service to various platforms.

## 📋 Prerequisites

- **GitHub Repository**: Your code should be in a GitHub repository
- **Docker**: Ensure your Dockerfile works locally
- **Platform Account**: Account on your chosen deployment platform

## 🚀 Railway.app (Recommended - Free & Easy)

### Step 1: Prepare Your Repository
1. **Ensure your repository has:**
   - `Dockerfile`
   - `requirements.txt`
   - `app.py`
   - `start.sh`

2. **Verify local build works:**
   ```bash
   docker build -t python-executor .
   docker run -p 8080:8080 python-executor
   ```

### Step 2: Deploy to Railway
1. **Visit [railway.app](https://railway.app)**
2. **Sign in with GitHub**
3. **Click "New Project"**
4. **Select "Deploy from GitHub repo"**
5. **Choose your repository**
6. **Railway will automatically detect Dockerfile and deploy**

### Step 3: Get Your URL
1. **Wait for deployment to complete**
2. **Go to "Settings" → "Networking"**
3. **Click "Generate Domain"**
4. **Copy your public URL**

### Step 4: Test Your Service
```bash
# Health check
curl https://your-app.railway.app/health

# Test execution
curl -X POST https://your-app.railway.app/execute \
  -H "Content-Type: application/json" \
  -d '{"script": "def main():\n    return {\"message\": \"Hello Railway!\"}"}'
```

## ☁️ Google Cloud Run

### Step 1: Setup Google Cloud
1. **Install Google Cloud CLI:**
   ```bash
   # macOS
   brew install google-cloud-sdk
   
   # Linux
   curl https://sdk.cloud.google.com | bash
   exec -l $SHELL
   ```

2. **Authenticate and set project:**
   ```bash
   gcloud auth login
   gcloud config set project YOUR_PROJECT_ID
   ```

3. **Enable required APIs:**
   ```bash
   gcloud services enable cloudbuild.googleapis.com
   gcloud services enable run.googleapis.com
   ```

### Step 2: Build and Deploy
1. **Build and push to Container Registry:**
   ```bash
   gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/python-executor
   ```

2. **Deploy to Cloud Run:**
   ```bash
   gcloud run deploy python-executor \
     --image gcr.io/YOUR_PROJECT_ID/python-executor \
     --platform managed \
     --region us-central1 \
     --allow-unauthenticated \
     --port 8080
   ```

3. **Get your service URL:**
   ```bash
   gcloud run services describe python-executor --region us-central1 --format 'value(status.url)'
   ```

### Step 3: Test Your Service
```bash
# Health check
curl https://your-service-url/health

# Test execution
curl -X POST https://your-service-url/execute \
  -H "Content-Type: application/json" \
  -d '{"script": "def main():\n    return {\"message\": \"Hello Cloud Run!\"}"}'
```

## 🐳 Docker Deployment

### Local Docker
```bash
# Build image
docker build -t python-executor .

# Run container
docker run -p 8080:8080 python-executor

# Test
curl http://localhost:8080/health
```

### Docker Compose
Create `docker-compose.yml`:
```yaml
version: '3.8'
services:
  python-executor:
    build: .
    ports:
      - "8080:8080"
    environment:
      - PORT=8080
    restart: unless-stopped
```

Run with:
```bash
docker-compose up -d
```

## ☁️ AWS ECS/Fargate

### Step 1: Create ECR Repository
```bash
aws ecr create-repository --repository-name python-executor
```

### Step 2: Build and Push
```bash
# Get login token
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com

# Build and tag
docker build -t python-executor .
docker tag python-executor:latest YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/python-executor:latest

# Push to ECR
docker push YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/python-executor:latest
```

### Step 3: Deploy to ECS
1. **Create ECS cluster**
2. **Create task definition** with your ECR image
3. **Create service** using the task definition
4. **Configure load balancer** for public access

## 🔧 Environment Configuration

### Railway
Railway automatically sets the `PORT` environment variable.

### Google Cloud Run
```bash
gcloud run deploy python-executor \
  --image gcr.io/YOUR_PROJECT_ID/python-executor \
  --set-env-vars PORT=8080
```

### Docker
```bash
docker run -p 8080:8080 -e PORT=8080 python-executor
```

## 📊 Monitoring and Logs

### Railway
- **Logs**: Available in the Railway dashboard
- **Metrics**: Basic usage statistics
- **Health Checks**: Automatic health monitoring

### Google Cloud Run
```bash
# View logs
gcloud logs read --service=python-executor --limit=50

# View metrics
gcloud run services describe python-executor --region us-central1
```

### Docker
```bash
# View logs
docker logs <container_id>

# View stats
docker stats <container_id>
```

## 🔒 Security Considerations

### Production Recommendations
1. **Enable HTTPS**: All platforms provide this automatically
2. **Rate Limiting**: Implement request throttling
3. **Authentication**: Add API key or OAuth protection
4. **Resource Limits**: Set CPU and memory limits
5. **Network Policies**: Restrict outbound connections

### Environment Variables
```bash
# Add these to your deployment
SECURITY_KEY=your-secret-key
MAX_EXECUTION_TIME=30
MAX_MEMORY_MB=512
```

## 🚨 Troubleshooting

### Common Issues

**Service won't start:**
- Check Dockerfile syntax
- Verify all files are copied
- Check startup script permissions

**Health checks failing:**
- Ensure `/health` endpoint works
- Check if service binds to correct port
- Verify environment variables

**Script execution errors:**
- Check Python dependencies
- Verify timeout settings
- Review subprocess configuration

### Debug Commands

**Check container logs:**
```bash
docker logs <container_id>
```

**Inspect running container:**
```bash
docker exec -it <container_id> /bin/bash
```

**Test health endpoint:**
```bash
curl -v http://localhost:8080/health
```

## 📈 Scaling

### Railway
- **Automatic scaling** based on traffic
- **Manual scaling** in project settings

### Google Cloud Run
```bash
# Set minimum instances
gcloud run services update python-executor \
  --min-instances=1 \
  --max-instances=10
```

### Docker
```bash
# Scale with docker-compose
docker-compose up --scale python-executor=3
```

## 💰 Cost Optimization

### Railway
- **Free tier**: 500 hours/month
- **Paid plans**: $5/month for additional usage

### Google Cloud Run
- **Pay per request**: ~$0.40 per million requests
- **CPU time**: ~$0.00002400 per 100ms
- **Memory**: ~$0.00000250 per GB-second

### AWS ECS
- **Fargate**: Pay per task
- **EC2**: Pay for instances

## 🔄 Continuous Deployment

### GitHub Actions
Create `.github/workflows/deploy.yml`:
```yaml
name: Deploy to Railway

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Deploy to Railway
        uses: railway/deploy@v1
        with:
          railway_token: ${{ secrets.RAILWAY_TOKEN }}
```

### Google Cloud Build
Create `cloudbuild.yaml`:
```yaml
steps:
  - name: 'gcr.io/cloud-builders/docker'
    args: ['build', '-t', 'gcr.io/$PROJECT_ID/python-executor', '.']
  - name: 'gcr.io/cloud-builders/docker'
    args: ['push', 'gcr.io/$PROJECT_ID/python-executor']
  - name: 'gcr.io/google.com/cloudsdktool/cloud-sdk'
    args:
      - run
      - deploy
      - python-executor
      - --image
      - gcr.io/$PROJECT_ID/python-executor
      - --region
      - us-central1
      - --allow-unauthenticated
```

## 🎯 Next Steps

1. **Deploy to your chosen platform**
2. **Test all endpoints thoroughly**
3. **Monitor performance and logs**
4. **Implement additional security measures**
5. **Set up monitoring and alerting**
6. **Plan for scaling and optimization**

---

**Happy deploying! 🚀**

Your Python Code Execution Service is ready to scale across the cloud! 