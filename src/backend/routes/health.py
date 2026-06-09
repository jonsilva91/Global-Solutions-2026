"""
Health check endpoint for the Astra Resilience Copilot API.
"""
from fastapi import APIRouter
from datetime import datetime
from typing import Dict

router = APIRouter()


@router.get("/health", tags=["Health"])
async def health_check() -> Dict[str, str]:
    """
    Health check endpoint to verify API is running.
    
    Returns:
        Dictionary with status and timestamp
    """
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }

# Made with Bob
