# Helm Chart Approach for Todo Application

## Overview

This document outlines the approach for packaging the Todo application using Helm charts for Kubernetes deployment.

## Chart Structure

### Directory Layout
```
charts/
└── todo-app/
    ├── Chart.yaml
    ├── values.yaml
    ├── templates/
    │   ├── frontend-deployment.yaml
    │   ├── frontend-service.yaml
    │   ├── backend-deployment.yaml
    │   ├── backend-service.yaml
    │   ├── configmap.yaml
    │   ├── secret.yaml
    │   ├── ingress.yaml
    │   └── NOTES.txt
    └── README.md
```

### Chart.yaml
- Defines the chart metadata including name, version, description, and dependencies
- Follows Helm v2 API specification
- Uses semantic versioning for chart versioning

### values.yaml
- Contains default configuration values for the entire application
- Organized by service (frontend, backend, database, ingress)
- Provides sensible defaults for development while allowing customization for production

## Multi-Service Architecture

### Frontend Service
- **Deployment**: Scalable frontend pods running the Next.js application
- **Service**: Internal service for cluster access
- **Configuration**: Image repository, tag, resource limits, environment variables

### Backend Service
- **Deployment**: Scalable backend pods running the FastAPI application
- **Service**: Internal service for cluster access
- **Configuration**: Image repository, tag, resource limits, environment variables

## Configuration Management

### Values Structure
```
frontend:
  replicaCount: 1
  image:
    repository: "taskflow-frontend"
    tag: "latest"
    pullPolicy: "IfNotPresent"
  service:
    type: ClusterIP
    port: 80
  resources:
    limits:
      cpu: "500m"
      memory: "512Mi"
    requests:
      cpu: "100m"
      memory: "128Mi"

backend:
  replicaCount: 1
  image:
    repository: "taskflow-backend"
    tag: "latest"
    pullPolicy: "IfNotPresent"
  service:
    type: ClusterIP
    port: 8000
  resources:
    limits:
      cpu: "1000m"
      memory: "1Gi"
    requests:
      cpu: "250m"
      memory: "256Mi"
```

## Environment-Specific Deployments

The chart supports different environments through value overrides:
- Development: Lower resource limits, debug configurations
- Staging: Production-like configurations with test data
- Production: Optimized resource limits, security configurations

## Security Considerations

- Sensitive data stored in Kubernetes Secrets
- Non-root user execution in containers
- Resource limits to prevent resource exhaustion
- Network policies for inter-service communication