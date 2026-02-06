# Quickstart Guide: Docker Containerization

**Feature**: 3-docker-containerization
**Date**: 2026-01-21

## Prerequisites

- Docker Desktop installed (with Gordon AI assistance enabled if available)
- Node.js 18+ for frontend development
- Python 3.13+ for backend development
- Minikube for local Kubernetes testing (optional)

## Setup

### 1. Clone the Repository
```bash
git clone <repository-url>
cd hac2-phase4
```

### 2. Navigate to Project Root
```bash
cd D:\learning\Quarter-4\Hackathon\hac2-phase4
```

## Building Docker Images

### 1. Build Frontend Image
```bash
# Navigate to frontend directory
cd frontend

# Build the frontend Docker image
docker build -t taskflow-frontend:0.1.0 -f Dockerfile .

# Verify image size is under 200MB
docker images taskflow-frontend:0.1.0
```

### 2. Build Backend Image
```bash
# Navigate to backend directory
cd ../backend

# Build the backend Docker image
docker build -t taskflow-backend:0.1.0 -f Dockerfile .

# Verify image size is under 300MB
docker images taskflow-backend:0.1.0
```

## Running Containers

### 1. Run Frontend Container
```bash
# Run frontend container with health check
docker run -d \
  --name taskflow-frontend \
  -p 3000:80 \
  -e API_URL=http://localhost:8000 \
  taskflow-frontend:0.1.0

# Verify container is running as non-root user
docker exec taskflow-frontend ps aux

# Test health check endpoint
curl http://localhost:3000/health
```

### 2. Run Backend Container
```bash
# Run backend container with health check
docker run -d \
  --name taskflow-backend \
  -p 8000:8000 \
  -e DATABASE_URL=sqlite:///./test.db \
  -e OPENROUTER_API_KEY=your_api_key_here \
  taskflow-backend:0.1.0

# Verify container is running as non-root user
docker exec taskflow-backend ps aux

# Test health check endpoint
curl http://localhost:8000/api/health
```

## Verification Steps

### 1. Image Size Verification
```bash
# Check frontend image size (should be < 200MB)
docker images taskflow-frontend:0.1.0

# Check backend image size (should be < 300MB)
docker images taskflow-backend:0.1.0
```

### 2. Health Check Verification
```bash
# Frontend health check
curl -v http://localhost:3000/health

# Backend health check
curl -v http://localhost:8000/api/health
```

### 3. Non-Root User Verification
```bash
# Check frontend user ID
docker exec taskflow-frontend id

# Check backend user ID
docker exec taskflow-backend id
```

### 4. Environment Variables Verification
```bash
# Check frontend environment
docker exec taskflow-frontend env | grep API_URL

# Check backend environment
docker exec taskflow-backend env | grep DATABASE_URL
```

## Kubernetes Deployment (Minikube)

### 1. Start Minikube
```bash
minikube start
```

### 2. Load Images into Minikube
```bash
# Load frontend image
minikube image load taskflow-frontend:0.1.0

# Load backend image
minikube image load taskflow-backend:0.1.0
```

### 3. Deploy to Minikube
```bash
# Apply Kubernetes manifests (to be created in next phase)
kubectl apply -f k8s/frontend-deployment.yaml
kubectl apply -f k8s/backend-deployment.yaml
```

## Troubleshooting

### Common Issues

1. **Image size too large**
   - Ensure .dockerignore is properly configured
   - Use multi-stage builds to separate build and runtime artifacts
   - Consider using alpine-based base images

2. **Health check failing**
   - Verify the health check endpoint is accessible
   - Check application logs for errors
   - Ensure the application is fully initialized before health check

3. **Non-root user issues**
   - Verify file permissions are set correctly
   - Ensure the application can write to necessary directories
   - Check that the user exists in the container

### Useful Commands

```bash
# View container logs
docker logs <container-name>

# Execute commands in running container
docker exec -it <container-name> /bin/sh

# Build with no cache if needed
docker build --no-cache -t <image-name> .
```