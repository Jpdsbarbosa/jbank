"""
Aplicação FastAPI principal.

Ponto de entrada da API REST.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.presentation.api.routes import accounts, transfers
from src.infrastructure.config import settings


# Cria aplicação FastAPI
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Sistema bancário com Clean Architecture + DDD",
)

# CORS (permite requisições de qualquer origem)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registra rotas
app.include_router(accounts.router)
app.include_router(transfers.router)


@app.get("/")
async def root():
    """Health check."""
    return {
        "app": settings.app_name,
        "version": settings.app_version,
        "status": "running"
    }


@app.get("/health")
async def health_check():
    """Health check detalhado."""
    return {
        "status": "healthy",
        "environment": settings.environment,
    }
