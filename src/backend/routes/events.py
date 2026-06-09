"""
Events Router - NASA EONET and FIRMS Integration
Provides endpoints for fetching natural event data from NASA EONET API and FIRMS fire hotspots.
"""
from fastapi import APIRouter, Query, HTTPException
from typing import Optional

from src.ingestion.eonet_client import fetch_eonet_events
from src.ingestion.firms_client import fetch_firms_hotspots

router = APIRouter(prefix="/events", tags=["Events"])

# Force reload marker


@router.get("/eonet")
async def get_eonet_events(
    category: Optional[str] = Query(
        None,
        description="Event category filter (e.g., 'wildfires', 'floods', 'storms', 'volcanoes', 'severeStorms')"
    ),
    status: Optional[str] = Query(
        None,
        description="Event status filter: 'open' or 'closed'"
    ),
    limit: Optional[int] = Query(
        None,
        ge=1,
        le=100,
        description="Maximum number of events to return (1-100)"
    ),
    days: Optional[int] = Query(
        None,
        ge=1,
        le=365,
        description="Number of days to look back from today (1-365)"
    )
):
    """
    Fetch natural events from NASA EONET (Earth Observatory Natural Event Tracker) API.
    
    This endpoint retrieves real-time data about natural events happening around the world,
    including wildfires, floods, storms, volcanoes, and other environmental phenomena.
    
    **Available Categories:**
    - wildfires
    - floods
    - severeStorms
    - volcanoes
    - drought
    - dustHaze
    - earthquakes
    - landslides
    - manmade
    - seaLakeIce
    - snow
    - tempExtremes
    - waterColor
    
    **Example Requests:**
    - Get all open events: `/events/eonet?status=open`
    - Get recent wildfires: `/events/eonet?category=wildfires&status=open&days=30`
    - Get limited results: `/events/eonet?limit=10`
    
    **Response Format:**
    ```json
    {
      "source": "NASA EONET v3",
      "total_events": 10,
      "filters": {
        "category": "wildfires",
        "status": "open",
        "limit": 10,
        "days": 30
      },
      "events": [
        {
          "event_id": "EONET_12345",
          "title": "Wildfire - California",
          "category": "Wildfires",
          "status": "open",
          "source": "InciWeb",
          "geometry_type": "Point",
          "coordinates": [-120.5, 38.5],
          "event_date": "2026-06-01T00:00:00Z",
          "api_source": "NASA EONET v3"
        }
      ]
    }
    ```
    
    Args:
        category: Filter by event category
        status: Filter by event status ('open' or 'closed')
        limit: Maximum number of events to return
        days: Number of days to look back from today
        
    Returns:
        Dictionary containing event data and metadata
        
    Raises:
        HTTPException: If NASA EONET API is unavailable or returns an error
    """
    try:
        # Fetch events from NASA EONET API
        result = fetch_eonet_events(
            category=category,
            status=status,
            limit=limit,
            days=days
        )
        
        return result
        
    except Exception as e:
        # Handle API errors gracefully
        raise HTTPException(
            status_code=503,
            detail={
                "error": "NASA EONET API unavailable",
                "message": str(e),
                "suggestion": "Please try again later or check your internet connection"
            }
        )


@router.get("/eonet/categories")
async def get_eonet_categories():
    """
    Get available event categories from NASA EONET API.
    
    Returns a list of all available event categories that can be used
    to filter events in the `/events/eonet` endpoint.
    
    **Example Response:**
    ```json
    {
      "categories": [
        {
          "id": "wildfires",
          "title": "Wildfires",
          "description": "Wildfires includes all nature of fire, including forest and plains fires, as well as urban and industrial fire events."
        }
      ]
    }
    ```
    
    Returns:
        Dictionary containing available categories
        
    Raises:
        HTTPException: If NASA EONET API is unavailable
    """
    try:
        from src.ingestion.eonet_client import EONETClient
        
        client = EONETClient()
        categories = client.get_available_categories()
        
        return {
            "source": "NASA EONET v3",
            "total_categories": len(categories),
            "categories": categories
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=503,
            detail={
                "error": "NASA EONET API unavailable",
                "message": str(e),
                "suggestion": "Please try again later or check your internet connection"
            }
        )


@router.get("/firms")
async def get_firms_hotspots(
    limit: Optional[int] = Query(
        None,
        ge=1,
        le=100,
        description="Maximum number of hotspots to return (1-100)"
    ),
    min_confidence: Optional[str] = Query(
        None,
        description="Minimum confidence level: 'low', 'nominal', or 'high'"
    )
):
    """
    Fetch fire hotspot data from NASA FIRMS (Fire Information for Resource Management System).
    
    This endpoint retrieves fire hotspot data detected by NASA satellites (MODIS and VIIRS).
    For the MVP, it uses local sample data from Brazilian regions (Pantanal, Amazônia, Cerrado).
    
    **Confidence Levels:**
    - **low**: Lower confidence detection
    - **nominal**: Standard confidence detection
    - **high**: High confidence detection
    
    **Data Sources:**
    - **local_sample**: Uses sample CSV data (default for MVP)
    - **api**: Uses NASA FIRMS API (requires API key, not implemented in MVP)
    
    **Example Requests:**
    - Get all hotspots: `/events/firms`
    - Get top 10 hotspots: `/events/firms?limit=10`
    - Get high confidence only: `/events/firms?min_confidence=high`
    - Combined filters: `/events/firms?limit=5&min_confidence=nominal`
    
    **Response Format:**
    ```json
    {
      "source": "NASA FIRMS",
      "mode": "local_sample",
      "total_hotspots": 15,
      "filters": {
        "limit": 10,
        "min_confidence": "high"
      },
      "hotspots": [
        {
          "hotspot_id": "FIRMS_NOAA-20_2026-06-07_1530_-22.3456_-48.9876",
          "latitude": -22.3456,
          "longitude": -48.9876,
          "brightness": 345.6,
          "confidence": "high",
          "acquisition_date": "2026-06-07",
          "acquisition_time": "1530",
          "satellite": "NOAA-20",
          "instrument": "VIIRS",
          "source": "NASA FIRMS",
          "risk_weight": 0.875
        }
      ]
    }
    ```
    
    Args:
        limit: Maximum number of hotspots to return
        min_confidence: Minimum confidence level filter
        
    Returns:
        Dictionary containing hotspot data and metadata
        
    Raises:
        HTTPException: If sample data is unavailable or invalid
    """
    try:
        # Validate min_confidence parameter
        if min_confidence and min_confidence.lower() not in ['low', 'nominal', 'high']:
            raise HTTPException(
                status_code=400,
                detail={
                    "error": "Invalid confidence level",
                    "message": f"'{min_confidence}' is not a valid confidence level",
                    "valid_values": ["low", "nominal", "high"]
                }
            )
        
        # Fetch hotspots from FIRMS client
        result = fetch_firms_hotspots(
            limit=limit,
            min_confidence=min_confidence
        )
        
        return result
    
    except HTTPException:
        # Re-raise HTTPException to preserve status code
        raise
    except FileNotFoundError as e:
        # Handle missing sample CSV file
        raise HTTPException(
            status_code=503,
            detail={
                "error": "FIRMS sample data unavailable",
                "message": str(e),
                "suggestion": "Please ensure data/sample/firms_sample.csv exists in the project root"
            }
        )
    except ValueError as e:
        # Handle invalid data format
        raise HTTPException(
            status_code=400,
            detail={
                "error": "Invalid request parameters",
                "message": str(e)
            }
        )
    except Exception as e:
        # Handle other errors
        raise HTTPException(
            status_code=500,
            detail={
                "error": "Failed to fetch FIRMS data",
                "message": str(e),
                "suggestion": "Please check the server logs for more details"
            }
        )


# Made with Bob
