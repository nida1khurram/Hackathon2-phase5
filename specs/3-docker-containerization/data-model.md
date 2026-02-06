# Data Model: Docker Containerization

**Feature**: 3-docker-containerization
**Date**: 2026-01-21
**Status**: Draft

## Docker Image Configuration

### Frontend Image
- **Name**: taskflow-frontend
- **Base Image**: node:18-alpine (build stage), nginx:alpine (production stage)
- **Size Constraint**: < 200MB
- **Build Context**: ./frontend
- **Build Args**: NODE_ENV=production
- **Layers**:
  - Dependencies installation layer
  - Build assets layer
  - Production serving layer

### Backend Image
- **Name**: taskflow-backend
- **Base Image**: python:3.13-slim (build stage), python:3.13-slim (runtime stage)
- **Size Constraint**: < 300MB
- **Build Context**: ./backend
- **Build Args**: PYTHONUNBUFFERED=1
- **Layers**:
  - System dependencies layer
  - Python packages layer
  - Application code layer

## Container Configuration

### User Configuration
- **UID**: 1001 (non-root user)
- **Username**: appuser
- **Permissions**: Read/write access to application directories
- **Groups**: appgroup

### Environment Variables
- **Frontend**:
  - API_URL: URL for backend API endpoint
  - NODE_ENV: Environment indicator (production/staging)

- **Backend**:
  - DATABASE_URL: Connection string for database
  - OPENROUTER_API_KEY: API key for OpenRouter service
  - PYTHONPATH: Python module search path

### Health Check Configuration
- **Endpoint Path**: /health (frontend), /api/health (backend)
- **Response Code**: 200 OK
- **Response Format**: JSON object with status information
- **Timeout**: 5 seconds
- **Interval**: 10 seconds (for Kubernetes probes)

## Build Artifacts

### Frontend Build Artifacts
- **Source Location**: ./frontend/out (Next.js build output)
- **Destination**: /usr/share/nginx/html in production image
- **Asset Types**: HTML, CSS, JavaScript, static assets
- **Compression**: Gzipped for production

### Backend Build Artifacts
- **Source Location**: ./backend/src (application code)
- **Destination**: /app in runtime image
- **Dependencies**: Python packages installed via pip
- **Virtual Environment**: Not required (using system Python in container)

## Volume Mounts (if needed)
- **Logs**: /app/logs (backend), /var/log/nginx (frontend)
- **Configuration**: /app/config (runtime configuration files)
- **Temporary Storage**: /tmp/app (temporary file storage)