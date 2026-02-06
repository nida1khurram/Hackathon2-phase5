# Quickstart Guide: Helm Chart Deployment

**Feature**: 4-helm-charts
**Date**: 2026-01-21

## Prerequisites

- Helm 3 installed (https://helm.sh/docs/intro/install/)
- Kubernetes cluster (Minikube, Kind, or cloud-based)
- kubectl configured to access the cluster
- Docker images for frontend and backend already pushed to registry

## Setup

### 1. Clone the Repository
```bash
git clone <repository-url>
cd hac2-phase4
```

### 2. Navigate to Helm Chart Directory
```bash
cd charts/todo-app  # Or wherever the Helm chart is located
```

## Installing the Helm Chart

### 1. Add Helm Repository (if using published chart)
```bash
helm repo add todo-repo <repository-url>
helm repo update
```

### 2. Install the Chart
```bash
# Install with default values
helm install todo-app .

# Install with custom release name
helm install my-todo-app .

# Install with custom values file
helm install todo-app . -f my-values.yaml

# Install with specific values override
helm install todo-app . --set frontend.replicaCount=2 --set backend.resources.limits.memory=2Gi
```

### 3. Verify Installation
```bash
# Check release status
helm status todo-app

# List releases
helm list

# Check deployed resources
kubectl get pods,services,deployments -l app.kubernetes.io/name=todo-app
```

## Configuration Options

### 1. Custom Values File
Create a `my-values.yaml` file to customize the deployment:

```yaml
frontend:
  image:
    tag: "v1.2.0"
  replicaCount: 2
  resources:
    limits:
      memory: "512Mi"
      cpu: "500m"
    requests:
      memory: "256Mi"
      cpu: "250m"

backend:
  image:
    tag: "v1.2.0"
  replicaCount: 2
  resources:
    limits:
      memory: "1Gi"
      cpu: "1000m"
    requests:
      memory: "512Mi"
      cpu: "500m"

ingress:
  enabled: true
  hosts:
    - host: todo.example.com
      paths:
        - path: /
          pathType: Prefix
```

### 2. Environment-Specific Configurations

#### Development
```bash
helm install todo-dev . -f values-dev.yaml
```

#### Staging
```bash
helm install todo-staging . -f values-staging.yaml
```

#### Production
```bash
helm install todo-prod . -f values-prod.yaml
```

## Upgrading the Chart

### 1. Upgrade to New Version
```bash
# Upgrade with new chart version
helm upgrade todo-app . --reuse-values

# Upgrade with specific values
helm upgrade todo-app . -f my-values.yaml

# Dry run to see changes
helm upgrade todo-app . --dry-run
```

### 2. Rollback
```bash
# List revisions
helm history todo-app

# Rollback to previous revision
helm rollback todo-app 1
```

## Verification Steps

### 1. Check Resources
```bash
# Check deployments
kubectl get deployments

# Check services
kubectl get services

# Check pods
kubectl get pods

# Check ingress (if enabled)
kubectl get ingress
```

### 2. Test Application Access
```bash
# Get service information
kubectl get svc todo-frontend-svc

# Port forward to test locally
kubectl port-forward svc/todo-frontend-svc 8080:80

# Access the application at http://localhost:8080
```

### 3. Check Health
```bash
# Check pod status
kubectl get pods -l app.kubernetes.io/name=todo-app

# Check logs
kubectl logs -l app.kubernetes.io/name=todo-app

# Check events
kubectl get events --sort-by='.lastTimestamp'
```

## Uninstalling

### 1. Remove Release
```bash
# Uninstall the release
helm uninstall todo-app

# Verify removal
helm status todo-app
```

## Troubleshooting

### Common Issues

1. **Chart fails validation**
   ```bash
   # Run lint to check for issues
   helm lint .
   ```

2. **Pods stuck in Pending state**
   ```bash
   # Check events for scheduling issues
   kubectl get events

   # Check resource requests
   kubectl describe nodes
   ```

3. **Image pull errors**
   ```bash
   # Check if image pull secrets are configured
   kubectl get secrets

   # Verify image exists in registry
   kubectl describe pod <pod-name>
   ```

### Useful Commands

```bash
# Template values locally
helm template todo-app . --debug

# Check dependencies
helm dependency list .

# Show values from release
helm get values todo-app

# Show manifest from release
helm get manifest todo-app
```