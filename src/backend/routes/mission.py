"""
Mission information endpoint for the Astra Resilience Copilot API.
"""
from fastapi import APIRouter
from typing import Dict, List

router = APIRouter()


@router.get("/mission/info", tags=["Mission"])
async def get_mission_info() -> Dict[str, str | List[str]]:
    """
    Get project information and metadata.
    
    Returns:
        Dictionary with project name, description, version, and main components
    """
    return {
        "project_name": "Astra Resilience Copilot",
        "description": "AI-powered environmental monitoring and disaster prevention system for resilient communities",
        "version": "1.0.0-MVP",
        "main_components": [
            "FastAPI Backend - Real-time sensor data processing and risk analysis",
            "ESP32/Edge Devices - Environmental sensor network for data collection",
            "Risk Analysis Engine - Rule-based environmental risk scoring system",
            "Alert System - Automated alert generation and notification",
            "RAG System - Intelligent recommendations (planned)",
            "Web Dashboard - Real-time monitoring interface (planned)",
            "Mobile App - Field access and notifications (planned)"
        ],
        "mission": "Empower communities with real-time environmental intelligence to prevent disasters and build resilience",
        "target_areas": [
            "Fire prevention and early detection",
            "Flood monitoring and prediction",
            "Drought assessment and water management",
            "Air quality monitoring",
            "Agricultural resilience"
        ]
    }

# Made with Bob
