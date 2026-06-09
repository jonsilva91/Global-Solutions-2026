"""
NASA EONET (Earth Observatory Natural Event Tracker) Client
Fetches and processes natural event data from NASA's EONET v3 API.
"""
import requests
import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, List, Dict, Any


class EONETClient:
    """Client for interacting with NASA EONET v3 API."""
    
    BASE_URL = "https://eonet.gsfc.nasa.gov/api/v3"
    
    def __init__(self):
        """Initialize the EONET client."""
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Astra-Resilience-Copilot/1.0"
        })
    
    def fetch_events(
        self,
        category: Optional[str] = None,
        status: Optional[str] = None,
        limit: Optional[int] = None,
        days: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Fetch natural events from NASA EONET API.
        
        Args:
            category: Event category filter (e.g., 'wildfires', 'floods', 'storms')
            status: Event status filter ('open' or 'closed')
            limit: Maximum number of events to return
            days: Number of days to look back from today
            
        Returns:
            Dictionary containing processed events and metadata
            
        Raises:
            requests.RequestException: If API request fails
        """
        try:
            # Build query parameters
            params = {}
            if status:
                params['status'] = status
            if limit:
                params['limit'] = limit
            if days:
                start_date = (datetime.utcnow() - timedelta(days=days)).strftime('%Y-%m-%d')
                params['start'] = start_date
            
            # Determine endpoint based on category filter
            if category:
                endpoint = f"{self.BASE_URL}/categories/{category}"
            else:
                endpoint = f"{self.BASE_URL}/events"
            
            # Make API request
            response = self.session.get(endpoint, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            # Process and normalize events
            events = data.get('events', [])
            processed_events = [self._normalize_event(event) for event in events]
            
            # Save to file
            self._save_events(processed_events)
            
            return {
                "source": "NASA EONET v3",
                "total_events": len(processed_events),
                "filters": {
                    "category": category,
                    "status": status,
                    "limit": limit,
                    "days": days
                },
                "events": processed_events
            }
            
        except requests.RequestException as e:
            raise Exception(f"Failed to fetch EONET data: {str(e)}")
    
    def _normalize_event(self, event: Dict[str, Any]) -> Dict[str, Any]:
        """
        Normalize EONET event data into a clean structure.
        
        Args:
            event: Raw event data from EONET API
            
        Returns:
            Normalized event dictionary
        """
        # Extract geometry information
        geometries = event.get('geometry', [])
        geometry_type = None
        coordinates = []
        event_date = None
        
        if geometries:
            latest_geometry = geometries[-1]  # Get most recent geometry
            geometry_type = latest_geometry.get('type', 'Point')
            coordinates = latest_geometry.get('coordinates', [])
            event_date = latest_geometry.get('date', '')
        
        # Extract category information
        categories = event.get('categories', [])
        category = categories[0].get('title', 'Unknown') if categories else 'Unknown'
        
        # Extract source information
        sources = event.get('sources', [])
        source = sources[0].get('id', 'Unknown') if sources else 'Unknown'
        
        return {
            "event_id": event.get('id', ''),
            "title": event.get('title', ''),
            "category": category,
            "status": event.get('closed', None) is None and 'open' or 'closed',
            "source": source,
            "geometry_type": geometry_type,
            "coordinates": coordinates,
            "event_date": event_date or event.get('geometry', [{}])[0].get('date', ''),
            "api_source": "NASA EONET v3"
        }
    
    def _save_events(self, events: List[Dict[str, Any]]) -> None:
        """
        Save processed events to JSON file.
        
        Args:
            events: List of normalized event dictionaries
        """
        # Create data directory if it doesn't exist
        PROJECT_ROOT = Path(__file__).resolve().parents[2]
        data_dir = PROJECT_ROOT / "data" / "processed"
        data_dir.mkdir(parents=True, exist_ok=True)
        
        # Save events to file
        output_file = data_dir / "eonet_events.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(events, f, indent=2, ensure_ascii=False)
    
    def get_available_categories(self) -> List[Dict[str, Any]]:
        """
        Fetch available event categories from EONET API.
        
        Returns:
            List of available categories
        """
        try:
            response = self.session.get(f"{self.BASE_URL}/categories", timeout=10)
            response.raise_for_status()
            data = response.json()
            return data.get('categories', [])
        except requests.RequestException as e:
            raise Exception(f"Failed to fetch EONET categories: {str(e)}")


# Convenience function for easy import
def fetch_eonet_events(
    category: Optional[str] = None,
    status: Optional[str] = None,
    limit: Optional[int] = None,
    days: Optional[int] = None
) -> Dict[str, Any]:
    """
    Convenience function to fetch EONET events.
    
    Args:
        category: Event category filter
        status: Event status filter ('open' or 'closed')
        limit: Maximum number of events to return
        days: Number of days to look back from today
        
    Returns:
        Dictionary containing processed events and metadata
    """
    client = EONETClient()
    return client.fetch_events(category=category, status=status, limit=limit, days=days)


# Made with Bob