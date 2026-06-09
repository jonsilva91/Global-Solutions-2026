"""
Pydantic models for sensor data in the Astra Resilience Copilot.
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, field_validator


class SensorReading(BaseModel):
    """Model for sensor readings from ESP32/edge devices."""
    
    device_id: str = Field(..., description="Unique identifier for the sensor device")
    timestamp: Optional[datetime] = Field(default_factory=datetime.utcnow, description="Reading timestamp")
    temperature: float = Field(..., ge=-50, le=100, description="Temperature in Celsius")
    humidity: float = Field(..., ge=0, le=100, description="Humidity percentage")
    soil_moisture: float = Field(..., ge=0, le=100, description="Soil moisture percentage")
    smoke_level: float = Field(..., ge=0, le=100, description="Smoke level (0-100 scale)")
    battery_level: float = Field(..., ge=0, le=100, description="Battery level percentage")
    network_status: str = Field(..., description="Network connection status")
    
    @field_validator('network_status')
    @classmethod
    def validate_network_status(cls, v: str) -> str:
        """Validate and normalize network status values."""
        allowed_statuses = [
            'connected', 'disconnected', 'weak', 'strong',
            'online', 'offline', 'degraded'
        ]
        normalized = v.lower()
        if normalized not in allowed_statuses:
            raise ValueError(f"Network status must be one of: {', '.join(allowed_statuses)}")
        return normalized
    
    class Config:
        json_schema_extra = {
            "example": {
                "device_id": "esp32_001",
                "timestamp": "2026-06-02T14:00:00Z",
                "temperature": 28.5,
                "humidity": 65.0,
                "soil_moisture": 45.0,
                "smoke_level": 0.0,
                "battery_level": 85.0,
                "network_status": "connected"
            }
        }


class SensorReadingResponse(BaseModel):
    """Response model for sensor reading submission."""
    
    success: bool
    message: str
    reading_id: str
    timestamp: datetime
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "Sensor reading stored successfully",
                "reading_id": "esp32_001_1717340400",
                "timestamp": "2026-06-02T14:00:00Z"
            }
        }

# Made with Bob
