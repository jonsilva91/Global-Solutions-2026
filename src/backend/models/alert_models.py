"""
Pydantic models for alerts in the Astra Resilience Copilot.
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class Alert(BaseModel):
    """Model for environmental alerts."""
    
    alert_id: str = Field(..., description="Unique identifier for the alert")
    alert_type: str = Field(..., description="Type of alert (fire, flood, drought, etc.)")
    severity: str = Field(..., description="Alert severity: Low, Medium, High, Critical")
    area: str = Field(..., description="Geographic area affected")
    message: str = Field(..., description="Alert message")
    risk_score: float = Field(..., ge=0, le=100, description="Associated risk score")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Alert creation timestamp")
    status: str = Field(default="active", description="Alert status: active, resolved, expired")
    device_id: Optional[str] = Field(None, description="Source device ID if applicable")
    
    class Config:
        json_schema_extra = {
            "example": {
                "alert_id": "alert_20260602_001",
                "alert_type": "fire",
                "severity": "High",
                "area": "São Paulo - Zona Leste",
                "message": "High fire risk detected due to elevated temperature and low humidity",
                "risk_score": 75.0,
                "timestamp": "2026-06-02T14:00:00Z",
                "status": "active",
                "device_id": "esp32_001"
            }
        }


class AlertsResponse(BaseModel):
    """Response model for alerts list."""
    
    total_alerts: int
    active_alerts: int
    alerts: list[Alert]
    
    class Config:
        json_schema_extra = {
            "example": {
                "total_alerts": 2,
                "active_alerts": 1,
                "alerts": [
                    {
                        "alert_id": "alert_20260602_001",
                        "alert_type": "fire",
                        "severity": "High",
                        "area": "São Paulo - Zona Leste",
                        "message": "High fire risk detected",
                        "risk_score": 75.0,
                        "timestamp": "2026-06-02T14:00:00Z",
                        "status": "active"
                    }
                ]
            }
        }

# Made with Bob
