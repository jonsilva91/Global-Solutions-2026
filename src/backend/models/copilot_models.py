"""
Pydantic models for Copilot RAG operational report endpoints.
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class SourceProvenance(BaseModel):
    """Source provenance tracking for report generation."""
    firms_file: str = Field(..., description="Path to FIRMS hotspots data file")
    eonet_file: str = Field(..., description="Path to EONET events data file")
    sensor_file: str = Field(..., description="Path to sensor readings data file")
    alerts_file: Optional[str] = Field(None, description="Path to alerts data file")
    knowledge_base: List[str] = Field(
        default_factory=list,
        description="List of knowledge base files used"
    )


class CopilotReportRequest(BaseModel):
    """Request model for generating operational briefing report."""
    risk_analysis: Dict[str, Any] = Field(
        ...,
        description="Risk analysis payload from /risk/analyze endpoint"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "risk_analysis": {
                    "area_of_interest": "Pantanal",
                    "risk_score": 78.0,
                    "risk_level": "HIGH",
                    "risk_breakdown": {
                        "sensor_score": 65.0,
                        "firms_score": 85.0,
                        "eonet_score": 70.0,
                        "spatial_score": 75.0
                    },
                    "evidence": [
                        "High temperature detected: 39°C",
                        "Low humidity: 18%",
                        "FIRMS hotspot detected within 5km"
                    ],
                    "recommended_action": "Activate response teams and pre-position resources",
                    "recommendations": [
                        "Increase monitoring frequency",
                        "Coordinate with local authorities"
                    ],
                    "provenance": {
                        "timestamp": "2026-06-09T12:00:00Z",
                        "data_sources": ["sensor", "firms", "eonet"]
                    }
                }
            }
        }


class CopilotReportResponse(BaseModel):
    """Response model for operational briefing report."""
    title: str = Field(
        ...,
        description="Report title"
    )
    area_of_interest: str = Field(
        ...,
        description="Geographic area being assessed"
    )
    risk_level: str = Field(
        ...,
        description="Risk classification (LOW, MODERATE, HIGH, CRITICAL)"
    )
    risk_score: float = Field(
        ...,
        ge=0.0,
        le=100.0,
        description="Composite risk score (0-100)"
    )
    executive_summary: str = Field(
        ...,
        description="High-level summary of the situation"
    )
    evidence_summary: List[str] = Field(
        default_factory=list,
        description="List of key evidence items"
    )
    source_provenance: SourceProvenance = Field(
        ...,
        description="Data source tracking and provenance"
    )
    recommended_actions: List[str] = Field(
        default_factory=list,
        description="Recommended operational actions"
    )
    limitations: List[str] = Field(
        default_factory=list,
        description="Known limitations and uncertainties"
    )
    generated_at: str = Field(
        ...,
        description="ISO 8601 timestamp of report generation"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "title": "Astra Resilience Copilot — Operational Briefing",
                "area_of_interest": "Pantanal",
                "risk_level": "HIGH",
                "risk_score": 78.0,
                "executive_summary": "The Pantanal region is currently assessed at HIGH risk with a composite score of 78.0/100. This assessment is based on 3 FIRMS fire hotspot(s), 2 EONET event(s), 5 sensor reading(s). Significant risk factors are present. Response teams should be activated and resources pre-positioned for rapid deployment.",
                "evidence_summary": [
                    "High temperature detected: 39°C",
                    "Low humidity: 18%",
                    "FIRMS hotspot detected within 5km",
                    "Active wildfire event in EONET"
                ],
                "source_provenance": {
                    "firms_file": "data/processed/firms_hotspots.json",
                    "eonet_file": "data/processed/eonet_events.json",
                    "sensor_file": "data/processed/sensor_readings.json",
                    "alerts_file": "data/processed/alerts.json",
                    "knowledge_base": [
                        "data/knowledge/astra_architecture.md",
                        "data/knowledge/risk_methodology.md",
                        "data/knowledge/firms_notes.md"
                    ]
                },
                "recommended_actions": [
                    "Activate response teams",
                    "Pre-position resources at staging areas",
                    "Establish command post and communication protocols",
                    "Coordinate with local authorities",
                    "Increase monitoring frequency to every 15-30 minutes"
                ],
                "limitations": [
                    "Satellite data subject to 12-hour revisit gaps and cloud cover interference",
                    "Risk assessment is point-in-time and should be updated every 15-30 minutes",
                    "Ground conditions may vary significantly from satellite observations",
                    "Model uses simplified weight assignments pending historical calibration"
                ],
                "generated_at": "2026-06-09T12:00:00Z"
            }
        }

# Made with Bob
