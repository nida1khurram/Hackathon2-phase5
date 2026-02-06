#!/usr/bin/env python3
"""
Script to run both FastAPI and MCP (Model Context Protocol) servers for the Todo AI Chatbot
"""

import asyncio
import os
import sys
from contextlib import asynccontextmanager

# Use local MCP server implementation directly
from src.mcp_server.server import Server
from src.mcp_server.types import TextContent
from sqlmodel import create_engine, Session
from src.models import Base, Task
from src.mcp_server.server import TodoMCPTools
from src.mcp_server.tools import get_mcp_tools_definitions
from src.settings import settings


# Create database engine and session using the same approach as the main app
if settings.database_url:
    DATABASE_URL = settings.database_url
else:
    DATABASE_URL = f"postgresql://{settings.db_user}:{settings.db_password}@{settings.db_host}:{settings.db_port}/{settings.db_name}"

if DATABASE_URL.startswith("sqlite"):
    # For SQLite, ensure the path is writable and create directories if needed
    import os
    import tempfile
    # Use a temporary file for SQLite database in container
    temp_db_path = os.path.join(tempfile.gettempdir(), 'todo_app.db')
    DATABASE_URL = f"sqlite:///{temp_db_path}"

    # SQLite-specific engine configuration
    engine = create_engine(
        DATABASE_URL,
        echo=settings.db_echo,
        connect_args={"check_same_thread": False}  # Required for SQLite with threading
    )
else:
    # PostgreSQL-specific engine configuration
    engine = create_engine(
        DATABASE_URL,
        echo=settings.db_echo,  # Set to True to see SQL queries in logs
        pool_pre_ping=True,  # Verify connections before use
        pool_recycle=300,  # Recycle connections after 5 minutes
    )

SessionLocal = Session


def create_db_and_tables():
    """Create database tables if they don't exist"""
    Base.metadata.create_all(bind=engine)


@asynccontextmanager
async def lifespan(server: Server):
    """Lifespan context manager for the MCP server"""
    print("Starting MCP server...")
    create_db_and_tables()
    yield
    print("Shutting down MCP server...")


async def run_mcp_server():
    """Run the MCP server"""
    print("Initializing Todo MCP Server...")

    # Create a database session
    db_session = SessionLocal(bind=engine)

    # Create tools instance
    todo_tools = TodoMCPTools(db_session)

    # Create MCP server instance
    server = Server("todo-mcp-server", version="1.0.0")

    # Register the tools with the server
    server.todo_tools = todo_tools

    print("Starting MCP server on port 8001...")

    # Start the MCP server and keep it running
    # The serve method is an async generator that needs to be properly consumed
    serve_gen = server.serve(lifespan=lifespan, host="127.0.0.1", port=8001)

    # Get the first iteration of the generator to start the server
    # This will initiate the lifespan context manager within the serve method
    await serve_gen.__anext__()

    print("MCP server is running on port 8001.")

    # Keep the server running indefinitely
    mcp_event = asyncio.Event()
    await mcp_event.wait()  # Wait indefinitely


def run_fastapi_server():
    """Run the FastAPI server"""
    print("Starting FastAPI server on port 8000...")
    import uvicorn
    from src.main import app

    # Run the FastAPI application
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")


async def main():
    """Main function to run both MCP and FastAPI servers"""
    print("Initializing Todo Application Servers...")
    print("- FastAPI server: http://localhost:8000 (for API/web access)")
    print("- MCP server: http://localhost:8001 (for AI agent communication)")

    # Create tasks for both servers
    mcp_task = asyncio.create_task(run_mcp_server())
    fastapi_task = asyncio.to_thread(run_fastapi_server)

    # Run both servers concurrently
    await asyncio.gather(mcp_task, fastapi_task)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nServers stopped by user.")
    except Exception as e:
        print(f"Error running servers: {e}")
        import traceback
        traceback.print_exc()