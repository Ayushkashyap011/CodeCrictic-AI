#!/usr/bin/env python3
"""
Entry point that sets Windows event loop policy before Uvicorn starts.
Run: python run.py
"""
import sys
import asyncio
import os

# Set policy BEFORE Uvicorn creates the event loop
if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

import uvicorn

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    config = uvicorn.Config(
        "app.main:app",
        host="0.0.0.0",
        port=port,
        reload=False,
        log_level="info"
    )
    server = uvicorn.Server(config)
    asyncio.run(server.serve())
