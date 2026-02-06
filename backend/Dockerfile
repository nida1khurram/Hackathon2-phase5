# Backend Dockerfile with single-stage build for reliability
# Ensures all dependencies are properly installed

FROM python:3.13-slim

# Install system dependencies needed for building Python packages and clean in same layer
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && rm -rf /usr/share/doc/* \
    && rm -rf /usr/share/man/*

# Create non-root user with UID 1001
RUN groupadd -g 1001 appgroup && \
    useradd -u 1001 -g appgroup -m -s /bin/bash appuser

# Set working directory
WORKDIR /app

# Copy requirements file first for better caching
COPY pyproject.toml ./

# Install uv and create virtual environment with cleanup
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir uv && \
    uv venv && \
    rm -rf /root/.cache

# Install dependencies using uv with size optimization
RUN . .venv/bin/activate && \
    uv pip install --only-binary=all --compile-bytecode --no-cache-dir -e . && \
    rm -rf /root/.cache

# Copy application code
COPY --chown=appuser:appgroup . .

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 8000

# Note: MCP server doesn't have a standard HTTP health endpoint
# The server runs on port 8000 but uses MCP protocol, not standard HTTP
# HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
#   CMD curl -f http://localhost/api/health || exit 1

# Environment variables
ENV DATABASE_URL=${DATABASE_URL:-sqlite:///./todo_app.db}
ENV OPENROUTER_API_KEY=${OPENROUTER_API_KEY:-""}

# Activate virtual environment and start the application
ENV PATH="/app/.venv/bin:$PATH"
CMD ["python", "run_server.py"]