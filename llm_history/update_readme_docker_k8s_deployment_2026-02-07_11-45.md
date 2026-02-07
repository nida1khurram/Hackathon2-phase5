# Update README with Docker Compose and Kubernetes Deployment Instructions

## Date
February 7, 2026

## Changes Made

### Updated README.md with comprehensive deployment instructions:

1. Added Docker Compose Configuration section:
   - Documented the Neon PostgreSQL database connection string used in docker-compose.yml
   - Explained that the Docker Compose setup connects to Neon database

2. Enhanced Running the Application section with three options:
   - Option 1: Development Mode (Individual Services) - existing method
   - Option 2: Docker Compose (Recommended for Quick Start) - new addition
     * Instructions for running `docker-compose up --build`
     * Access information for frontend (port 3002) and backend (port 8001)
     * Backend health check endpoint
   - Option 3: Kubernetes Deployment (Minikube) - detailed instructions
     * Minikube start command
     * Docker image building instructions
     * Image loading into Minikube
     * Helm deployment command with all necessary parameters
     * Service access information

3. Added note about Docker Compose connecting to Neon PostgreSQL database

## Technical Details

The Docker Compose configuration connects to:
DATABASE_URL=postgresql://neondb_owner:npg_vOQXx8w0kRed@ep-rough-king-ahuvd09s-pooler.c-3.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require

The Kubernetes deployment uses SQLite for local development with the path sqlite:////tmp/todo_app_local.db to ensure proper write permissions for the non-root container user.

## Purpose

These changes provide clear, comprehensive instructions for users to run the Todo application in three different environments:
1. Traditional development mode with separate services
2. Containerized deployment with Docker Compose
3. Kubernetes deployment with Minikube and Helm

This addresses the need for multiple deployment strategies and makes the application more accessible to users with different requirements and expertise levels.