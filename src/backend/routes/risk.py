"""
Risk analysis endpoint for the Astra Resilience Copilot API.
"""
from fastapi import APIRouter, HTTPException
from datetime import datetime
from src.backend.models.risk_models import (
    RiskAnalysisRequest,
    SpatialRiskAnalysisResponse,
    SpatialRiskBreakdown,
    Evidence,
    Provenance
)
from src.backend.models.alert_models import Alert
from src.backend.utils.storage import storage
from src.intelligence.spatial_risk_engine import spatial_risk_engine

router = APIRouter()

ALERTS_FILE = "alerts.json"


@router.post("/risk/analyze", response_model=SpatialRiskAnalysisResponse, tags=["Risk Analysis"])
async def analyze_risk(request: RiskAnalysisRequest) -> SpatialRiskAnalysisResponse:
    """
    Analyze environmental risk for a given area using space-enabled risk engine.
    
    Integrates:
    - NASA FIRMS hotspot data (35% weight)
    - Edge sensor readings (25% weight)
    - NASA EONET events (20% weight)
    - Smoke/fire indicators (10% weight)
    - Operational risk (10% weight)
    
    Args:
        request: Risk analysis request with area and optional sensor data
        
    Returns:
        Spatial risk analysis response with score, level, breakdown, evidence, and recommendations
        
    Raises:
        HTTPException: If analysis fails
    """
    try:
        # Load latest stored sensor reading for operational fields
        latest_sensor = storage.get_latest("sensor_readings.json")
        
        # Build merged sensor data
        sensor_dict = None
        if request.sensor_data or latest_sensor:
            # Start with latest stored sensor (if available)
            sensor_dict = latest_sensor.copy() if latest_sensor else {}
            
            # Override/add fields from request if provided
            if request.sensor_data:
                if request.sensor_data.temperature is not None:
                    sensor_dict["temperature"] = request.sensor_data.temperature
                if request.sensor_data.humidity is not None:
                    sensor_dict["humidity"] = request.sensor_data.humidity
                if request.sensor_data.soil_moisture is not None:
                    sensor_dict["soil_moisture"] = request.sensor_data.soil_moisture
                if request.sensor_data.smoke_level is not None:
                    sensor_dict["smoke_level"] = request.sensor_data.smoke_level
                if request.sensor_data.battery_level is not None:
                    sensor_dict["battery_level"] = request.sensor_data.battery_level
                if request.sensor_data.network_status is not None:
                    sensor_dict["network_status"] = request.sensor_data.network_status
                if request.sensor_data.device_id is not None:
                    sensor_dict["device_id"] = request.sensor_data.device_id
        
        # Perform spatial risk analysis using new engine
        spatial_result = spatial_risk_engine.analyze_spatial_risk(
            area_of_interest=request.area_of_interest,
            sensor_data=sensor_dict
        )
        
        # Extract values from spatial result
        risk_score = spatial_result["risk_score"]
        risk_level = spatial_result["risk_level"]
        
        # Build spatial risk breakdown
        risk_breakdown = SpatialRiskBreakdown(
            firms_risk=spatial_result["risk_breakdown"]["firms_risk"],
            sensor_risk=spatial_result["risk_breakdown"]["sensor_risk"],
            eonet_risk=spatial_result["risk_breakdown"]["eonet_risk"],
            smoke_risk=spatial_result["risk_breakdown"]["smoke_risk"],
            operational_risk=spatial_result["risk_breakdown"]["operational_risk"]
        )
        
        # Build evidence list
        evidence_list = [
            Evidence(
                source=ev["source"],
                description=ev["description"],
                value=ev["value"],
                timestamp=ev["timestamp"]
            )
            for ev in spatial_result["evidence"]
        ]
        
        # Build provenance
        provenance = Provenance(
            firms_file=spatial_result["provenance"]["firms_file"],
            eonet_file=spatial_result["provenance"]["eonet_file"],
            sensor_file=spatial_result["provenance"]["sensor_file"]
        )
        
        # Get recommended action
        recommended_action = spatial_result["recommended_action"]
        
        # Generate recommendations list (includes main action + evidence-based)
        recommendations = [recommended_action]
        
        # Add evidence-based recommendations
        for evidence in spatial_result["evidence"]:
            if evidence["source"] == "NASA FIRMS" and "fire" in evidence["description"].lower():
                rec = "🔥 Active fires detected - implement fire prevention measures"
                if rec not in recommendations:
                    recommendations.append(rec)
            elif evidence["source"] == "NASA EONET" and "wildfire" in evidence["description"].lower():
                rec = "🌍 Satellite monitoring shows wildfire activity in region"
                if rec not in recommendations:
                    recommendations.append(rec)
            elif "smoke" in evidence["description"].lower():
                rec = "💨 Elevated smoke levels - monitor air quality"
                if rec not in recommendations:
                    recommendations.append(rec)
        
        # Use timestamp from spatial result
        timestamp = spatial_result["timestamp"]
        
        # Generate alert if risk is HIGH or CRITICAL
        if risk_level in ["HIGH", "CRITICAL"]:
            await _create_alert(
                area=request.area_of_interest,
                risk_score=risk_score,
                risk_level=risk_level,
                sensor_data=request.sensor_data
            )
        
        # Return full spatial analysis response
        return SpatialRiskAnalysisResponse(
            area_of_interest=request.area_of_interest,
            risk_score=risk_score,
            total_risk_score=risk_score,  # Backward compatibility
            risk_level=risk_level,
            risk_breakdown=risk_breakdown,
            evidence=evidence_list,
            recommended_action=recommended_action,
            recommendations=recommendations,
            provenance=provenance,
            timestamp=timestamp
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error performing risk analysis: {str(e)}"
        )


async def _create_alert(area: str, risk_score: float, risk_level: str, sensor_data) -> None:
    """
    Create and store an alert based on risk analysis.
    
    Args:
        area: Area of interest
        risk_score: Calculated risk score
        risk_level: Risk level (Medium or High)
        sensor_data: Sensor data used in analysis
    """
    try:
        # Generate alert ID
        timestamp = datetime.utcnow()
        alert_id = f"alert_{timestamp.strftime('%Y%m%d_%H%M%S')}"
        
        # Determine alert type based on sensor data
        alert_type = "environmental"
        if sensor_data:
            if sensor_data.smoke_level and sensor_data.smoke_level > 10:
                alert_type = "fire"
            elif sensor_data.soil_moisture and sensor_data.soil_moisture < 20:
                alert_type = "drought"
            elif sensor_data.temperature and sensor_data.temperature > 35:
                alert_type = "heat"
        
        # Create alert message
        message = f"{risk_level} risk detected in {area}"
        if alert_type == "fire":
            message = f"Fire risk alert: {risk_level} risk detected in {area}"
        elif alert_type == "drought":
            message = f"Drought alert: {risk_level} risk detected in {area}"
        elif alert_type == "heat":
            message = f"Heat alert: {risk_level} risk detected in {area}"
        
        # Create alert object
        alert = Alert(
            alert_id=alert_id,
            alert_type=alert_type,
            severity=risk_level,
            area=area,
            message=message,
            risk_score=risk_score,
            timestamp=timestamp,
            status="active",
            device_id=None
        )
        
        # Store alert
        alert_dict = alert.model_dump()
        alert_dict['timestamp'] = timestamp.isoformat() + "Z"
        storage.append_json(ALERTS_FILE, alert_dict)
        
    except Exception as e:
        # Log error but don't fail the risk analysis
        print(f"Error creating alert: {e}")

# Made with Bob
