#!/usr/bin/env python3
"""
Script to run the FastAPI server for the Todo application
"""

import subprocess
import sys
import uvicorn
from src.main import app

if __name__ == "__main__":
    print("Running database migrations...")
    try:
        # Run alembic migrations
        result = subprocess.run([
            sys.executable, "-c",
            "from alembic.config import Config; from alembic import command; "
            "alembic_cfg = Config('alembic.ini'); command.upgrade(alembic_cfg, 'head')"
        ], cwd="/app", capture_output=True, text=True)

        if result.returncode != 0:
            print(f"Alembic migration output: {result.stdout}")
            print(f"Alembic migration error: {result.stderr}")
            # Continue even if migration fails (might be due to columns already existing)
            print("Continuing with server startup...")
        else:
            print("Database migrations completed successfully!")
    except Exception as e:
        print(f"Error running migrations: {e}")
        print("Continuing with server startup...")

    print("Starting FastAPI server on port 8000...")
    print("FastAPI server: http://localhost:8000 (for API/web access)")
    print("Health check: http://localhost:8000/health")
    print("API health check: http://localhost:8000/api/health")

    # Run the FastAPI application
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")