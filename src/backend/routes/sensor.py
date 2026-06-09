"""
Sensor data endpoints for the Astra Resilience Copilot API.
"""
from fastapi import APIRouter, HTTPException
from datetime import datetime
from src.backend.models.sensor_models import SensorReading, SensorReadingResponse
from src.backend.utils.storage import storage

router = APIRouter()

SENSOR_READINGS_FILE = "sensor_readings.json"


@router.post("/sensor/readings", response_model=SensorReadingResponse, tags=["Sensor"])
async def submit_sensor_reading(reading: SensorReading) -> SensorReadingResponse:
    """
    Submit a new sensor reading from ESP32/edge devices.
    
    Args:
        reading: Sensor reading data
        
    Returns:
        Confirmation response with reading ID
        
    Raises:
        HTTPException: If storage operation fails
    """
    try:
        # Ensure timestamp is set
        if reading.timestamp is None:
            reading.timestamp = datetime.utcnow()
        
        # Generate unique reading ID
        reading_id = f"{reading.device_id}_{int(reading.timestamp.timestamp())}"
        
        # Convert to dictionary for storage
        reading_dict = reading.model_dump()
        reading_dict['reading_id'] = reading_id
        reading_dict['timestamp'] = reading.timestamp.isoformat() + "Z"
        
        # Store the reading
        success = storage.append_json(SENSOR_READINGS_FILE, reading_dict)
        
        if not success:
            raise HTTPException(
                status_code=500,
                detail="Failed to store sensor reading"
            )
        
        return SensorReadingResponse(
            success=True,
            message="Sensor reading stored successfully",
            reading_id=reading_id,
            timestamp=reading.timestamp
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing sensor reading: {str(e)}"
        )


@router.get("/sensor/readings/latest", response_model=SensorReading | None, tags=["Sensor"])
async def get_latest_sensor_reading():
    """
    Get the most recent sensor reading.
    
    Returns:
        Latest sensor reading or None if no readings exist
        
    Raises:
        HTTPException: If retrieval operation fails
    """
    try:
        latest = storage.get_latest(SENSOR_READINGS_FILE)
        
        if latest is None:
            return None
        
        # Convert timestamp string back to datetime
        if isinstance(latest.get('timestamp'), str):
            latest['timestamp'] = datetime.fromisoformat(latest['timestamp'].replace('Z', '+00:00'))
        
        return SensorReading(**latest)
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving latest sensor reading: {str(e)}"
        )

# Made with Bob
