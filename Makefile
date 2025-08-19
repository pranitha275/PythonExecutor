.PHONY: help build run test clean deploy local-test

# Default target
help:
	@echo "Python Code Execution Service - Available Commands:"
	@echo ""
	@echo "Development:"
	@echo "  build          Build Docker image"
	@echo "  run            Run Docker container locally"
	@echo "  test           Run local tests (requires Flask app running)"
	@echo "  clean          Clean up Docker images and containers"
	@echo ""
	@echo "Deployment:"
	@echo "  deploy         Deploy to Google Cloud Run"
	@echo ""
	@echo "Local Development:"
	@echo "  local-test     Test Flask app locally (without Docker)"
	@echo "  install-dev    Install development dependencies"
	@echo "  run-flask      Run Flask app locally for development"

# Build Docker image
build:
	@echo "🔨 Building Docker image..."
	docker build -t python-executor .
	@echo "✅ Build completed!"

# Run Docker container locally
run:
	@echo "🚀 Running Docker container..."
	docker run -p 8080:8080 python-executor

# Run local tests
test:
	@echo "🧪 Running tests..."
	python test_local.py

# Clean up Docker resources
clean:
	@echo "🧹 Cleaning up Docker resources..."
	docker stop $$(docker ps -q --filter ancestor=python-executor) 2>/dev/null || true
	docker rm $$(docker ps -aq --filter ancestor=python-executor) 2>/dev/null || true
	docker rmi python-executor 2>/dev/null || true
	@echo "✅ Cleanup completed!"

# Deploy to Google Cloud Run
deploy:
	@echo "🚀 Deploying to Google Cloud Run..."
	./deploy.sh

# Install development dependencies
install-dev:
	@echo "📦 Installing development dependencies..."
	pip install -r requirements.txt
	pip install requests  # For testing

# Run Flask app locally for development
run-flask:
	@echo "🔥 Running Flask app locally..."
	python app.py

# Show project structure
tree:
	@echo "📁 Project Structure:"
	@find . -type f -name "*.py" -o -name "*.md" -o -name "*.txt" -o -name "*.sh" -o -name "*.config" -o -name "Dockerfile" -o -name "Makefile" | grep -v __pycache__ | sort

# Quick start - build and run
quickstart: build run 