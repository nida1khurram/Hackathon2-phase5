# Data Model: Minikube Deployment

**Feature**: 5-minikube-deployment
**Date**: 2026-01-21
**Status**: Draft

## Minikube Configuration

### Cluster Configuration
- **Name**: minikube cluster identifier
- **Driver**: Virtualization driver (virtualbox, docker, hyperv, etc.)
- **Resources**:
  - CPU cores (minimum 2 recommended)
  - Memory (minimum 4GB recommended)
  - Disk size (minimum 20GB recommended)
- **Network**: Network configuration for service access
- **Add-ons**: Enabled Minikube add-ons (ingress, metrics-server, etc.)

### Resource Allocation
- **Node Count**: Number of nodes in the cluster (typically 1 for local)
- **Pod Resources**: Resource requests and limits for application pods
- **Storage**: Persistent volume configuration for local development

## Helm Release Configuration

### Release Metadata
- **Name**: Unique identifier for the Helm release
- **Namespace**: Kubernetes namespace for deployment
- **Version**: Helm chart version being deployed
- **Values**: Custom values overriding default chart values

### Deployment Parameters
- **Image Tags**: Specific image versions for frontend and backend
- **Replica Counts**: Number of pod replicas for each service
- **Service Types**: Service configuration (NodePort for local access)
- **Environment Variables**: Configuration parameters for local deployment

## Service Exposure Configuration

### NodePort Services
- **Frontend Service**:
  - Type: NodePort
  - Port: 80 (internal), NodePort (external access)
  - Target Port: 80
- **Backend Service**:
  - Type: NodePort
  - Port: 8000 (internal), NodePort (external access)
  - Target Port: 8000

### Access Configuration
- **Local Access URL**: Combination of Minikube IP and NodePort
- **Service Mapping**: Mapping between internal service names and external access
- **DNS Configuration**: Minikube's built-in DNS settings

## Health Check Configuration

### Probe Settings
- **Liveness Probes**:
  - Path: Health check endpoint path
  - Port: Port to check
  - Initial Delay: Time before first check
  - Period: Interval between checks
  - Timeout: Time to wait for response
  - Failure Threshold: Consecutive failures before restart
- **Readiness Probes**:
  - Path: Readiness check endpoint
  - Port: Port to check
  - Initial Delay: Time before first check
  - Period: Interval between checks
  - Timeout: Time to wait for response
  - Failure Threshold: Consecutive failures before removing from service

### Monitoring Configuration
- **Metrics Collection**: Configuration for collecting application metrics
- **Log Aggregation**: Settings for accessing application logs
- **Status Indicators**: Key indicators for deployment health