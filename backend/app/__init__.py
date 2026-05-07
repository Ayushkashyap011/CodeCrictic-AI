# Set Windows event loop policy BEFORE any async code or Uvicorn initialization
import sys
import asyncio

if sys.platform.startswith("win"):
    try:
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    except Exception:
        pass
