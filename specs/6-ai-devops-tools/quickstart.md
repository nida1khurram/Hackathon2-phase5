# Quickstart Guide: AI DevOps Tools Integration

**Feature**: 6-ai-devops-tools
**Date**: 2026-01-21

## Prerequisites

- kubectl-ai wrapper installed and configured
- kagent (or equivalent cluster analysis tool) available
- Gordon (Docker AI assistant) available (if using Docker Desktop with AI features)
- Kubernetes cluster (Minikube) running
- Existing Docker images built for frontend and backend
- Helm chart available for deployment

## Setup Instructions

### 1. Install AI DevOps Tools

```bash
# Install kubectl-ai plugin (if not already installed)
kubectl krew install ai

# Verify kubectl-ai is working
kubectl ai --help

# Check if Gordon (Docker AI) is available in Docker Desktop
docker version
# Look for AI features in the output
```

### 2. Verify Tool Availability

```bash
# Check kubectl-ai availability
kubectl ai version

# Test a simple natural language command
kubectl ai "show me all pods in default namespace"

# If Gordon is available, verify Docker AI functionality
docker ai --help  # This command may vary depending on Docker AI implementation
```

## Natural Language Kubernetes Operations

### 1. Basic Operations with kubectl-ai

```bash
# Deploy an application with natural language
kubectl ai "create deployment frontend --image=taskflow-frontend:latest --replicas=2"

# Scale an existing deployment
kubectl ai "scale deployment frontend --replicas=3"

# Expose a service
kubectl ai "expose deployment frontend --port=80 --type=NodePort"

# Check resource status
kubectl ai "show me the status of all deployments in the todo-app namespace"
```

### 2. Advanced Operations

```bash
# Apply a configuration change
kubectl ai "set environment variable API_URL=http://backend:8000 in frontend deployment"

# Check resource utilization
kubectl ai "show me memory usage by pods in todo-app namespace"

# Troubleshoot issues
kubectl ai "describe pods that are not running in todo-app namespace"
```

## Cluster Diagnostics with kagent

### 1. Run Cluster Health Analysis

```bash
# Perform comprehensive cluster analysis
kubectl ai "analyze cluster health and report issues"

# Check resource allocation
kubectl ai "report resource allocation across all namespaces"

# Identify performance bottlenecks
kubectl ai "find performance issues in the cluster"
```

### 2. Review Diagnostic Reports

```bash
# Save diagnostic report to file
kubectl ai "analyze cluster and save report to cluster-report.json"

# Review recommendations
cat cluster-report.json | jq '.recommendations'
```

## Dockerfile Generation with Gordon (if available)

### 1. Generate Frontend Dockerfile

```bash
# If Gordon is available, generate Dockerfile for frontend
# Note: This is typically done through Docker Desktop AI features or specific Gordon commands
# The exact command may vary depending on the implementation

# Example approach (commands may differ):
# Navigate to frontend directory
cd frontend

# If Gordon provides a command-line interface:
# gordon generate dockerfile --context . --output Dockerfile.optimized

# Or use Docker Desktop AI features if available
```

### 2. Generate Backend Dockerfile

```bash
# Navigate to backend directory
cd backend

# Generate optimized Dockerfile for backend
# gordon generate dockerfile --context . --output Dockerfile.optimized
```

## Verification Steps

### 1. Test Natural Language Commands

```bash
# Test basic deployment command
kubectl ai "create a deployment named test-app with image nginx:alpine"
kubectl get deployment test-app
kubectl delete deployment test-app

# Test service exposure
kubectl ai "expose deployment nginx --port=80 --type=NodePort"
kubectl get service nginx
kubectl delete service nginx
```

### 2. Verify Diagnostic Capabilities

```bash
# Run a basic cluster analysis
kubectl ai "check cluster status"

# Verify output format and content
kubectl ai "show nodes and their resource usage"
```

### 3. Validate Generated Artifacts

```bash
# If using AI to generate YAML, verify the output before applying:
kubectl ai "generate deployment frontend --image=taskflow-frontend:latest" > temp-deployment.yaml

# Review the generated YAML
cat temp-deployment.yaml

# Validate syntax
kubectl apply --dry-run=client -f temp-deployment.yaml

# Clean up
rm temp-deployment.yaml
```

## AI-Assisted Deployment Workflow

### 1. Deploy Application Using Natural Language

```bash
# Deploy frontend with specific configuration
kubectl ai "create deployment todo-frontend --image=taskflow-frontend:latest --replicas=2 --port=80"

# Deploy backend with specific configuration
kubectl ai "create deployment todo-backend --image=taskflow-backend:latest --replicas=2 --port=8000"

# Expose services
kubectl ai "expose deployment todo-frontend --port=80 --target-port=80 --type=NodePort"
kubectl ai "expose deployment todo-backend --port=8000 --target-port=8000 --type=ClusterIP"

# Verify deployment
kubectl ai "show me all pods in default namespace"
```

### 2. Monitor with AI Assistance

```bash
# Check application health
kubectl ai "check if all pods in deployment todo-frontend are running"

# Monitor resource usage
kubectl ai "show me CPU and memory usage for todo-frontend deployment"

# Troubleshoot if issues arise
kubectl ai "describe any pods in error state in default namespace"
```

## Quality Assurance Process

### 1. AI Artifact Review Workflow

```bash
# When AI generates an artifact, always verify before applying:

# 1. Generate with dry-run to see what would be created
kubectl ai "generate deployment test --image=nginx:alpine" | kubectl apply --dry-run=server -f -

# 2. Save to file for review if needed
kubectl ai "generate deployment test --image=nginx:alpine" > generated-artifact.yaml
cat generated-artifact.yaml  # Review manually
kubectl apply -f generated-artifact.yaml  # Apply if acceptable
rm generated-artifact.yaml  # Clean up

# 3. Document the AI interaction in a PHR
# Record the natural language command used, the generated artifact, and any review notes
```

### 2. Documentation Requirements

For each AI interaction that generates artifacts for the cluster:

1. Record the exact natural language command used
2. Save the generated artifact (if not applied directly)
3. Document the review process and approval decision
4. Note any modifications made to the AI-generated content
5. Track the outcome after applying to the cluster