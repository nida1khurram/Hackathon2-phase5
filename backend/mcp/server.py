"""
Mock MCP server module to satisfy imports
"""
class Server:
    def __init__(self, name, version):
        self.name = name
        self.version = version

    async def serve(self, lifespan, host, port):
        # Placeholder for actual server logic
        async with lifespan(self):
            yield

async def asynccontextmanager(func):
    """Simple async context manager wrapper"""
    class AsyncContextManager:
        def __init__(self, func, *args, **kwargs):
            self.gen = func(*args, **kwargs)

        async def __aenter__(self):
            return await self.gen.__anext__()

        async def __aexit__(self, exc_type, exc_val, exc_tb):
            try:
                await self.gen.__anext__()
            except StopAsyncIteration:
                pass
    return AsyncContextManager(func)