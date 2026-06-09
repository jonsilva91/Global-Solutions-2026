"""
Astra Resilience Copilot - FastAPI Backend MVP
Main application entry point for the environmental monitoring and disaster prevention system.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.backend.routes import health, mission, sensor, risk, alerts, events, copilot

# Create FastAPI application
app = FastAPI(
    title="Astra Resilience Copilot API",
    description="AI-powered environmental monitoring and disaster prevention system for resilient communities",
    version="1.0.0-MVP",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS for React frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5174",
        "http://localhost:5175",
        "http://127.0.0.1:5175",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router)
app.include_router(mission.router)
app.include_router(sensor.router)
app.include_router(risk.router)
app.include_router(alerts.router)
app.include_router(events.router)
app.include_router(copilot.router)


@app.get("/", tags=["Root"])
async def root():
    """
    Root endpoint with API information.
    
    Returns:
        Welcome message and API documentation links
    """
    return {
        "message": "Welcome to Astra Resilience Copilot API",
        "version": "1.0.0-MVP",
        "documentation": {
            "swagger_ui": "/docs",
            "redoc": "/redoc"
        },
        "endpoints": {
            "health": "/health",
            "mission_info": "/mission/info",
            "sensor_readings": "/sensor/readings",
            "latest_reading": "/sensor/readings/latest",
            "risk_analysis": "/risk/analyze",
            "alerts": "/alerts",
            "eonet_events": "/events/eonet",
            "eonet_categories": "/events/eonet/categories",
            "firms_hotspots": "/events/firms",
            "copilot_report": "/copilot/report"
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

# Made with Bob
# Hotfix: Spatial risk engine integration complete

