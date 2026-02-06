# Docker Containerization Approach

## Overview

This document outlines the approach for containerizing the frontend and backend services of the Todo application using Docker multi-stage builds.

## Architecture

### Frontend Container
- **Base Images**: node:18-alpine (build) → nginx:alpine (production)
- **Purpose**: Serve the Next.js frontend application
- **Port**: 80 (exposed as 80)
- **User**: Non-root user (UID 1001) for security
- **Health Check**: GET /health endpoint returning 200 OK

### Backend Container
- **Base Images**: python:3.13-slim (build) → python:3.13-slim (runtime)
- **Purpose**: Run the FastAPI backend application
- **Port**: 8000 (exposed as 8000)
- **User**: Non-root user (UID 1001) for security
- **Health Check**: GET /api/health endpoint returning 200 OK

## Multi-Stage Build Pattern

### Frontend Build Process
1. **Build Stage**: node:18-alpine
   - Install Node.js dependencies
   - Build Next.js application
   - Output to `/app/out` directory

2. **Production Stage**: nginx:alpine
   - Copy built assets from build stage
   - Configure nginx to serve static files
   - Set up health check endpoint
   - Run as non-root user

### Backend Build Process
1. **Build Stage**: python:3.13-slim
   - Install system dependencies for building Python packages
   - Install Python dependencies using uv
   - Create virtual environment

2. **Runtime Stage**: python:3.13-slim
   - Copy Python runtime and dependencies from build stage
   - Copy application code
   - Set up non-root user
   - Configure health check
   - Run application as non-root user

## Security Considerations

- **Non-Root Users**: Both containers run as UID 1001 to reduce security risks
- **Minimal Base Images**: Using Alpine and slim images to reduce attack surface
- **Separation of Concerns**: Build and runtime environments separated
- **Proper Permissions**: File permissions set correctly for non-root users

## Size Optimization

- **Layer Caching**: Optimized Dockerfile structure for effective layer caching
- **Alpine Images**: Using Alpine Linux for smaller base images
- **Clean Installations**: Removing build dependencies after installation
- **Multi-Stage Builds**: Discarding build artifacts in final image

## Environment Variables

### Frontend
- `API_URL`: URL for backend API endpoint
- `NODE_ENV`: Environment indicator (production/staging)

### Backend
- `DATABASE_URL`: Connection string for database
- `OPENROUTER_API_KEY`: API key for OpenRouter service
- `PYTHONPATH`: Python module search path

## Kubernetes Compatibility

- **Health Checks**: Ready for Kubernetes liveness/readiness probes
- **Resource Limits**: Prepared for CPU/memory constraints
- **Environment Configuration**: Compatible with ConfigMaps/Secrets
- **Service Discovery**: Designed for internal service communication