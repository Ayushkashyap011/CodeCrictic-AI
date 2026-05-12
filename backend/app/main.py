"""
app/main.py
FastAPI application entry point.
Run: uvicorn app.main:app --reload
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

from app.config import get_settings
from app.database.connection import connect_db, close_db
from app.routes import problems, execute, ai_review

# ── Logging ──────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(name)s  %(message)s",
)
logger = logging.getLogger(__name__)

settings = get_settings()


# ── Lifespan (startup / shutdown) ─────────────────────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("🚀 CodeCritic AI backend starting up...")
    await connect_db()
    yield
    await close_db()
    logger.info("🛑 Backend shut down cleanly")


# ── App ───────────────────────────────────────────────────────────────────────
app = FastAPI(
    title="CodeCritic AI",
    description="AI-powered coding evaluation platform — backend API",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS — allow all origins (development)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Routers ───────────────────────────────────────────────────────────────────
app.include_router(problems.router, prefix="/api/v1")
app.include_router(execute.router, prefix="/api/v1")
app.include_router(ai_review.router, prefix="/api/v1")


# ── Health check ──────────────────────────────────────────────────────────────
@app.get("/health", tags=["health"])
async def health():
    return {"status": "ok", "env": settings.app_env}


@app.get("/", tags=["health"])
async def root():
    return {
        "message": "CodeCritic AI API",
        "docs": "/docs",
        "version": "1.0.0",
    }
