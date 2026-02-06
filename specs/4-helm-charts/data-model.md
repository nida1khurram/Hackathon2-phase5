# Data Model: Helm Chart Packaging

**Feature**: 4-helm-charts
**Date**: 2026-01-21
**Status**: Draft

## Helm Chart Structure

### Chart Metadata (Chart.yaml)
- **Name**: todo-app
- **Version**: 0.1.0 (semantic versioning)
- **AppVersion**: 1.0.0 (application version)
- **Description**: Helm chart for Todo application with frontend and backend services
- **Home**: Link to project documentation
- **Maintainers**: List of maintainers with contact information
- **Keywords**: Relevant keywords for chart discovery

### Default Values (values.yaml)
- **Global Configuration**:
  - imagePullSecrets: List of secrets for image repositories
  - storageClass: Default storage class for persistent volumes
  - namespaceOverride: Override namespace for deployment

- **Frontend Configuration**:
  - frontend.image.repository: Image repository for frontend
  - frontend.image.tag: Image tag for frontend (default: latest)
  - frontend.image.pullPolicy: Image pull policy (default: IfNotPresent)
  - frontend.replicaCount: Number of frontend replicas (default: 1)
  - frontend.service.type: Service type for frontend (default: ClusterIP)
  - frontend.service.port: Port for frontend service (default: 80)
  - frontend.resources.limits.cpu: CPU limit for frontend
  - frontend.resources.limits.memory: Memory limit for frontend
  - frontend.resources.requests.cpu: CPU request for frontend
  - frontend.resources.requests.memory: Memory request for frontend
  - frontend.env.API_URL: API URL for backend service

- **Backend Configuration**:
  - backend.image.repository: Image repository for backend
  - backend.image.tag: Image tag for backend (default: latest)
  - backend.image.pullPolicy: Image pull policy (default: IfNotPresent)
  - backend.replicaCount: Number of backend replicas (default: 1)
  - backend.service.type: Service type for backend (default: ClusterIP)
  - backend.service.port: Port for backend service (default: 8000)
  - backend.resources.limits.cpu: CPU limit for backend
  - backend.resources.limits.memory: Memory limit for backend
  - backend.resources.requests.cpu: CPU request for backend
  - backend.resources.requests.memory: Memory request for backend

- **Database Configuration**:
  - database.url: Database connection URL
  - database.secretName: Name of secret containing database credentials

- **Ingress Configuration**:
  - ingress.enabled: Whether to enable ingress (default: false)
  - ingress.className: Name of ingress class
  - ingress.annotations: Annotations for ingress controller
  - ingress.hosts: List of hostnames for ingress
  - ingress.tls: TLS configuration for ingress

## Deployment Configuration

### Frontend Deployment
- **Labels**: App-specific labels for identification
- **Selectors**: Match labels for pod selection
- **Containers**: Single container with frontend image
- **Ports**: Expose appropriate ports for service
- **Environment Variables**: Configuration via environment
- **Resource Requirements**: CPU and memory limits/requests
- **Health Checks**: Liveness and readiness probes

### Backend Deployment
- **Labels**: App-specific labels for identification
- **Selectors**: Match labels for pod selection
- **Containers**: Single container with backend image
- **Ports**: Expose appropriate ports for service
- **Environment Variables**: Configuration via environment
- **Resource Requirements**: CPU and memory limits/requests
- **Health Checks**: Liveness and readiness probes

## Service Configuration

### Frontend Service
- **Type**: Service type (ClusterIP, LoadBalancer, NodePort)
- **Ports**: Port mapping from service to pod
- **Selector**: Match labels to select backend pods
- **Annotations**: Service-specific annotations

### Backend Service
- **Type**: Service type (ClusterIP, LoadBalancer, NodePort)
- **Ports**: Port mapping from service to pod
- **Selector**: Match labels to select backend pods
- **Annotations**: Service-specific annotations

## Configuration Management

### ConfigMap
- **Application Configuration**: Non-sensitive configuration values
- **Feature Flags**: Configuration for feature toggles
- **External Service URLs**: URLs for external dependencies

### Secrets
- **Database Credentials**: Username, password, connection details
- **API Keys**: Third-party API keys and tokens
- **Encryption Keys**: Keys for encryption and security