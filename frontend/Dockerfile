# Frontend Dockerfile with multi-stage build pattern (node:18-alpine → nginx:alpine)
# Optimized for size < 200MB

# Build stage
FROM node:18-alpine AS builder

# Install only essential build dependencies and clean cache
RUN apk add --no-cache python3 make g++

# Set working directory
WORKDIR /app

# Copy package files
COPY package*.json ./

# Install only production dependencies and clean cache
RUN npm ci --only=production --prefer-offline --no-audit --no-fund && \
    npm cache clean --force --silent

# Copy source code
COPY . .

# Build the application with environment variable
ARG NEXT_PUBLIC_API_URL=http://localhost:8001
ENV NEXT_PUBLIC_API_URL=${NEXT_PUBLIC_API_URL}

RUN npm run build

# Remove unnecessary build tools and dependencies after build
RUN npm prune --production --silent && \
    rm -rf ~/.npm && \
    rm -rf /root/.npm

# Production stage
FROM nginx:alpine

# Install minimal packages and clean cache in single layer
RUN apk add --no-cache curl && \
    rm -rf /var/cache/apk/*

# Create non-root user with UID 1001 for file ownership
RUN addgroup -g 1001 -S appgroup && \
    adduser -u 1001 -S appuser -G appgroup

# Copy nginx configuration
COPY nginx.conf /etc/nginx/nginx.conf

# Copy built application from builder stage
COPY --from=builder --chown=appuser:appgroup /app/out /usr/share/nginx/html

# Copy environment setup script
COPY env.sh /env.sh
RUN chmod +x /env.sh

# Set minimal permissions
RUN chmod -R 755 /usr/share/nginx/html

# Create cache directories with proper permissions
RUN mkdir -p /var/cache/nginx/client_temp && \
    chown -R appuser:appgroup /var/cache/nginx && \
    chmod -R 755 /var/cache/nginx

# Expose port
EXPOSE 3001

# Health check endpoint (runs as root but checks health)
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost/health || exit 1

# Start nginx with environment variable support (as root)
CMD ["/env.sh"]