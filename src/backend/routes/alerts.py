"""
Alerts endpoint for the Astra Resilience Copilot API.
"""
from fastapi import APIRouter, HTTPException
from datetime import datetime
from src.backend.models.alert_models import AlertsResponse, Alert
from src.backend.utils.storage import storage

router = APIRouter()

ALERTS_FILE = "alerts.json"


@router.get("/alerts", response_model=AlertsResponse, tags=["Alerts"])
async def get_alerts() -> AlertsResponse:
    """
    Get all alerts from the system.
    
    Returns:
        Response containing total alerts, active alerts count, and list of all alerts
        
    Raises:
        HTTPException: If retrieval operation fails
    """
    try:
        # Retrieve all alerts
        alerts_data = storage.read_json(ALERTS_FILE)
        
        # Convert timestamp strings back to datetime objects
        alerts = []
        for alert_dict in alerts_data:
            if isinstance(alert_dict.get('timestamp'), str):
                alert_dict['timestamp'] = datetime.fromisoformat(
                    alert_dict['timestamp'].replace('Z', '+00:00')
                )
            alerts.append(Alert(**alert_dict))
        
        # Count active alerts
        active_count = sum(1 for alert in alerts if alert.status == "active")
        
        return AlertsResponse(
            total_alerts=len(alerts),
            active_alerts=active_count,
            alerts=alerts
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving alerts: {str(e)}"
        )

# Made with Bob
