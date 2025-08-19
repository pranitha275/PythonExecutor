#!/bin/bash

# Google Cloud Run Deployment Script
# Make sure you have gcloud CLI installed and configured

set -e

# Configuration
PROJECT_ID=$(gcloud config get-value project)
REGION="us-central1"
SERVICE_NAME="python-executor"
IMAGE_NAME="gcr.io/$PROJECT_ID/$SERVICE_NAME"

echo "🚀 Deploying Python Code Execution Service to Google Cloud Run"
echo "Project ID: $PROJECT_ID"
echo "Region: $REGION"
echo "Service Name: $SERVICE_NAME"
echo "Image: $IMAGE_NAME"
echo ""

# Check if gcloud is configured
if [ -z "$PROJECT_ID" ]; then
    echo "❌ Error: No Google Cloud project configured"
    echo "Run: gcloud config set project YOUR_PROJECT_ID"
    exit 1
fi

echo "📦 Building and pushing Docker image..."
gcloud builds submit --tag $IMAGE_NAME

echo "🚀 Deploying to Cloud Run..."
gcloud run deploy $SERVICE_NAME \
    --image $IMAGE_NAME \
    --platform managed \
    --region $REGION \
    --allow-unauthenticated \
    --port 8080 \
    --memory 1Gi \
    --cpu 1 \
    --timeout 300 \
    --max-instances 10

echo ""
echo "✅ Deployment completed successfully!"
echo ""
echo "🌐 Service URL:"
SERVICE_URL=$(gcloud run services describe $SERVICE_NAME --region=$REGION --format='value(status.url)')
echo $SERVICE_URL
echo ""

echo "🧪 Test the service with:"
echo "curl -X POST $SERVICE_URL/execute \\"
echo "  -H 'Content-Type: application/json' \\"
echo "  -d '{\"script\": \"def main():\\n    return {\\\"message\\\": \\\"Hello from Cloud Run!\\\"}\"}'"
echo ""

echo "📊 Monitor the service:"
echo "gcloud run services describe $SERVICE_NAME --region=$REGION"
echo ""

echo "🔍 View logs:"
echo "gcloud logs read --filter resource.type=cloud_run_revision --limit=50" 