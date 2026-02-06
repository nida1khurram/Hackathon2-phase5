# Quickstart Guide: Minikube Deployment

**Feature**: 5-minikube-deployment
**Date**: 2026-01-21

## Prerequisites

- Minikube installed (v1.28 or higher)
- kubectl installed (v1.25 or higher)
- Helm 3.x installed
- Docker installed and running
- kubectl-ai wrapper installed (for natural language operations)
- Kubernetes agent configured (.claude/agents/kubernetes-agent.md)

## Setup Instructions

### 1. Start Minikube Cluster

```bash
# Start Minikube with adequate resources for the application
minikube start --driver=docker --memory=4g --cpus=2

# Enable necessary addons
minikube addons enable ingress
minikube addons enable metrics-server
```

### 2. Verify Environment

```bash
# Check Minikube status
minikube status

# Verify kubectl can connect to cluster
kubectl cluster-info

# Verify Helm is available
helm version
```

### 3. Build and Load Docker Images

```bash
# Ensure you're in the project root directory
cd hac2-phase4

# Build frontend image
cd frontend
docker build -t taskflow-frontend:0.1.0 .
cd ..

# Build backend image
cd backend
docker build -t taskflow-backend:0.1.0 .
cd ..

# Load images into Minikube
minikube image load taskflow-frontend:0.1.0
minikube image load taskflow-backend:0.1.0
```

## Installation Instructions

### 1. Deploy Using Helm

```bash
# Navigate to the helm chart directory
cd charts/todo-app

# Install the application using Helm
helm install taskflow . --values values.yaml

# Or install with custom values for Minikube
helm install taskflow . \
  --set frontend.service.type=NodePort \
  --set backend.service.type=NodePort \
  --set frontend.resources.requests.memory=128Mi \
  --set backend.resources.requests.memory=256Mi
```

### 2. Verify Deployment

```bash
# Check if all pods are running
kubectl get pods

# Check services
kubectl get services

# Wait for all pods to be in Running state
kubectl wait --for=condition=Ready pods --all --timeout=120s
```

## Configuration Guide

### Minikube-Specific Values

Create a `values-minikube.yaml` file with the following configuration:

```yaml
frontend:
  replicaCount: 1
  image:
    repository: taskflow-frontend
    tag: "0.1.0"
  service:
    type: NodePort
    port: 80
  resources:
    limits:
      cpu: "500m"
      memory: "256Mi"
    requests:
      cpu: "100m"
      memory: "128Mi"

backend:
  replicaCount: 1
  image:
    repository: taskflow-backend
    tag: "0.1.0"
  service:
    type: NodePort
    port: 8000
  resources:
    limits:
      cpu: "1000m"
      memory: "512Mi"
    requests:
      cpu: "250m"
      memory: "256Mi"

# Database configuration (external Neon DB)
database:
  url: "your-neon-db-url-here"
  secretName: "todo-db-secret"

# Secrets for API keys
secrets:
  openrouterApiKey: "your-openrouter-api-key"
  jwtSecret: "your-jwt-secret"
  encryptionKey: "your-encryption-key"
```

Deploy with these values:

```bash
helm install taskflow . -f values-minikube.yaml
```

## Verification Steps

### 1. Check Pod Status

```bash
# Verify all pods are running
kubectl get pods -o wide

# Check pod logs for any issues
kubectl logs -l app.kubernetes.io/component=frontend
kubectl logs -l app.kubernetes.io/component=backend
```

### 2. Verify Health Checks

```bash
# Check if health endpoints are responding
kubectl port-forward svc/taskflow-frontend 8080:80 &
curl http://localhost:8080/health

kubectl port-forward svc/taskflow-backend 8081:8000 &
curl http://localhost:8081/api/health
```

### 3. Access the Application

```bash
# Get the service URLs
minikube service taskflow-frontend --url
minikube service taskflow-backend --url

# Or open in browser directly
minikube service taskflow-frontend
```

## Natural Language Kubernetes Operations

Using the kubectl-ai wrapper (if installed):

```bash
# Deploy with natural language
kubectl ai "deploy taskflow app from helm chart in current directory"

# Check status with natural language
kubectl ai "show me the status of all pods in the default namespace"

# Scale services with natural language
kubectl ai "scale frontend deployment to 2 replicas"

# Debug issues with natural language
kubectl ai "what's wrong with the backend pods that are not starting?"
```

## Troubleshooting

### Common Issues

1. **Minikube won't start**
   - Ensure virtualization is enabled in BIOS
   - Try with different driver: `minikube start --driver=hyperv` (Windows) or `--driver=virtualbox`

2. **Images not loading**
   - Verify Docker images exist locally: `docker images | grep taskflow`
   - Retry with: `minikube image load taskflow-frontend:0.1.0 --daemon`

3. **Services not accessible**
   - Check if NodePort services are properly exposed: `kubectl get svc`
   - Use `minikube service` command to access services

4. **Health checks failing**
   - Verify backend can connect to external database
   - Check if frontend can communicate with backend service

### Kubernetes Agent Usage

If encountering deployment issues, you can engage the Kubernetes agent:

1. **Activation**: Use the Kubernetes agent from `.claude/agents/kubernetes-agent.md`
2. **Troubleshooting**: Follow the agent's troubleshooting workflow for deployment issues
3. **Natural Language Operations**: Use the kubectl-ai wrapper for simplified operations
4. **Workflow**: Follow the Phase IV deployment workflow in `.claude/workflows/phase-iv-deployment.md`

## Cleanup

To remove the deployment:

```bash
# Uninstall the Helm release
helm uninstall taskflow

# Stop Minikube
minikube stop

# Optionally delete the Minikube cluster
minikube delete
```