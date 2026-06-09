"""
Pydantic models for risk analysis in the Astra Resilience Copilot.
"""
from typing import Optional, Dict, List, Any
from pydantic import BaseModel, Field, field_validator


class SensorDataInput(BaseModel):
    """Optional sensor data for risk analysis."""
    
    temperature: Optional[float] = Field(None, ge=-50, le=100, description="Temperature in Celsius")
    humidity: Optional[float] = Field(None, ge=0, le=100, description="Humidity percentage")
    soil_moisture: Optional[float] = Field(None, ge=0, le=100, description="Soil moisture percentage")
    smoke_level: Optional[float] = Field(None, ge=0, le=100, description="Smoke level (0-100 scale)")
    battery_level: Optional[float] = Field(None, ge=0, le=100, description="Battery level percentage")
    network_status: Optional[str] = Field(None, description="Network status (connected, disconnected, weak, strong, online, offline, degraded)")
    device_id: Optional[str] = Field(None, description="Device identifier")
    
    @field_validator('network_status')
    @classmethod
    def normalize_network_status(cls, v: Optional[str]) -> Optional[str]:
        """Normalize network status to lowercase."""
        if v is not None:
            normalized = v.lower()
            valid_statuses = ['connected', 'disconnected', 'weak', 'strong', 'online', 'offline', 'degraded']
            if normalized not in valid_statuses:
                raise ValueError(f"network_status must be one of: {', '.join(valid_statuses)}")
            return normalized
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "temperature": 35.0,
                "humidity": 20.0,
                "smoke_level": 15.0,
                "soil_moisture": 25.0,
                "battery_level": 85.0,
                "network_status": "connected",
                "device_id": "esp32_001"
            }
        }


class RiskAnalysisRequest(BaseModel):
    """Request model for risk analysis."""
    
    area_of_interest: str = Field(..., description="Geographic area or location to analyze")
    sensor_data: Optional[SensorDataInput] = Field(None, description="Optional sensor data for analysis")
    
    class Config:
        json_schema_extra = {
            "example": {
                "area_of_interest": "Pantanal",
                "sensor_data": {
                    "temperature": 39.0,
                    "humidity": 18.0,
                    "soil_moisture": 15.0,
                    "smoke_level": 35.0
                }
            }
        }


class RiskBreakdown(BaseModel):
    """Breakdown of risk components (backward compatible)."""
    
    temperature_risk: float = Field(..., ge=0, le=30, description="Risk score from temperature (0-30)")
    humidity_risk: float = Field(..., ge=0, le=25, description="Risk score from humidity (0-25)")
    smoke_risk: float = Field(..., ge=0, le=35, description="Risk score from smoke level (0-35)")
    soil_moisture_risk: float = Field(..., ge=0, le=10, description="Risk score from soil moisture (0-10)")


class SpatialRiskBreakdown(BaseModel):
    """Space-enabled risk breakdown with NASA data integration."""
    
    firms_risk: float = Field(..., ge=0, le=35, description="Risk from NASA FIRMS hotspots (0-35)")
    sensor_risk: float = Field(..., ge=0, le=25, description="Risk from edge sensors (0-25)")
    eonet_risk: float = Field(..., ge=0, le=20, description="Risk from NASA EONET events (0-20)")
    smoke_risk: float = Field(..., ge=0, le=10, description="Risk from smoke indicators (0-10)")
    operational_risk: float = Field(..., ge=0, le=10, description="Risk from operational status (0-10)")


class Evidence(BaseModel):
    """Evidence item from risk analysis."""
    
    source: str = Field(..., description="Data source (NASA FIRMS, NASA EONET, EDGE_SENSOR)")
    description: str = Field(..., description="Human-readable description")
    value: Any = Field(..., description="Evidence value (number, string, etc.)")
    timestamp: str = Field(..., description="ISO 8601 timestamp")


class Provenance(BaseModel):
    """Data provenance information."""
    
    firms_file: str = Field(..., description="Path to FIRMS data file")
    eonet_file: str = Field(..., description="Path to EONET data file")
    sensor_file: str = Field(..., description="Path to sensor data file")


class RiskAnalysisResponse(BaseModel):
    """Response model for risk analysis (backward compatible with spatial enhancements)."""
    
    area_of_interest: str
    risk_score: float = Field(..., ge=0, le=100, description="Total risk score (0-100)")
    total_risk_score: float = Field(..., ge=0, le=100, description="Total risk score (backward compatible)")
    risk_level: str = Field(..., description="Risk level: LOW, MODERATE, HIGH, or CRITICAL")
    risk_breakdown: RiskBreakdown
    recommendations: List[str] = Field(..., description="List of recommendations based on risk level")
    timestamp: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "area_of_interest": "Pantanal",
                "risk_score": 75.0,
                "total_risk_score": 75.0,
                "risk_level": "HIGH",
                "risk_breakdown": {
                    "temperature_risk": 30.0,
                    "humidity_risk": 25.0,
                    "smoke_risk": 15.0,
                    "soil_moisture_risk": 5.0
                },
                "recommendations": [
                    "High fire risk detected - implement fire prevention measures",
                    "Monitor smoke levels continuously"
                ],
                "timestamp": "2026-06-02T14:00:00Z"
            }
        }


class SpatialRiskAnalysisResponse(BaseModel):
    """Space-enabled risk analysis response with full NASA data integration."""
    
    area_of_interest: str
    risk_score: float = Field(..., ge=0, le=100, description="Total risk score (0-100)")
    total_risk_score: float = Field(..., ge=0, le=100, description="Total risk score (backward compatible)")
    risk_level: str = Field(..., description="Risk level: LOW, MODERATE, HIGH, or CRITICAL")
    risk_breakdown: SpatialRiskBreakdown
    evidence: List[Evidence] = Field(..., description="Evidence from multiple data sources")
    recommended_action: str = Field(..., description="Primary recommended action")
    recommendations: List[str] = Field(..., description="List of recommendations")
    provenance: Provenance = Field(..., description="Data source provenance")
    timestamp: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "area_of_interest": "Pantanal",
                "risk_score": 78.0,
                "total_risk_score": 78.0,
                "risk_level": "HIGH",
                "risk_breakdown": {
                    "firms_risk": 35.0,
                    "sensor_risk": 20.0,
                    "eonet_risk": 10.0,
                    "smoke_risk": 8.0,
                    "operational_risk": 5.0
                },
                "evidence": [
                    {
                        "source": "NASA FIRMS",
                        "description": "10 active fire hotspots detected",
                        "value": 10,
                        "timestamp": "2026-06-08T18:00:00Z"
                    }
                ],
                "recommended_action": "⚠️ HIGH RISK: Prepare for potential evacuation.",
                "recommendations": [
                    "⚠️ HIGH RISK: Prepare for potential evacuation.",
                    "🔥 Active fires detected - implement fire prevention measures"
                ],
                "provenance": {
                    "firms_file": "data/processed/firms_hotspots.json",
                    "eonet_file": "data/processed/eonet_events.json",
                    "sensor_file": "data/processed/sensor_readings.json"
                },
                "timestamp": "2026-06-08T18:00:00Z"
            }
        }

# Made with Bob
