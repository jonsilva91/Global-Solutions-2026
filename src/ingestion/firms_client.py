"""
NASA FIRMS (Fire Information for Resource Management System) Client
Fetches and processes fire hotspot data from NASA FIRMS API or local sample data.
"""
import csv
import json
import os
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict, Any
import requests


class FIRMSClient:
    """Client for interacting with NASA FIRMS API or local sample data."""
    
    # NASA FIRMS API endpoint (requires API key)
    FIRMS_API_URL = "https://firms.modaps.eosdis.nasa.gov/api/area/csv"
    
    def __init__(self, api_key: Optional[str] = None, use_api: bool = False):
        """
        Initialize the FIRMS client.
        
        Args:
            api_key: NASA FIRMS API key (optional)
            use_api: Whether to use the API or local sample data
        """
        self.api_key = api_key or os.getenv("FIRMS_API_KEY")
        self.use_api = use_api or os.getenv("FIRMS_USE_API", "false").lower() == "true"
        
        if self.use_api and not self.api_key:
            raise ValueError("FIRMS API key is required when use_api is True")
        
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Astra-Resilience-Copilot/1.0"
        })
    
    def fetch_hotspots(
        self,
        limit: Optional[int] = None,
        min_confidence: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Fetch fire hotspot data from NASA FIRMS API or local sample.
        
        Args:
            limit: Maximum number of hotspots to return
            min_confidence: Minimum confidence level ('low', 'nominal', 'high')
            
        Returns:
            Dictionary containing processed hotspots and metadata
        """
        if self.use_api and self.api_key:
            hotspots = self._fetch_from_api()
            mode = "api"
        else:
            hotspots = self._fetch_from_sample()
            mode = "local_sample"
        
        # Apply filters
        filtered_hotspots = self._apply_filters(
            hotspots,
            limit=limit,
            min_confidence=min_confidence
        )
        
        # Save processed data
        self._save_hotspots(filtered_hotspots)
        
        return {
            "source": "NASA FIRMS",
            "mode": mode,
            "total_hotspots": len(filtered_hotspots),
            "filters": {
                "limit": limit,
                "min_confidence": min_confidence
            },
            "hotspots": filtered_hotspots
        }
    
    def _fetch_from_sample(self) -> List[Dict[str, Any]]:
        """
        Fetch hotspot data from local sample CSV file.
        
        Returns:
            List of normalized hotspot dictionaries
            
        Raises:
            FileNotFoundError: If sample CSV file doesn't exist
        """
        PROJECT_ROOT = Path(__file__).resolve().parents[2]
        sample_file = PROJECT_ROOT / "data" / "sample" / "firms_sample.csv"
        
        if not sample_file.exists():
            raise FileNotFoundError(
                f"Sample CSV file not found: {sample_file}. "
                "Please ensure data/sample/firms_sample.csv exists."
            )
        
        hotspots = []
        
        try:
            with open(sample_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    try:
                        hotspot = self._normalize_hotspot(row)
                        hotspots.append(hotspot)
                    except (ValueError, KeyError) as e:
                        # Skip invalid rows but continue processing
                        print(f"Warning: Skipping invalid row: {e}")
                        continue
        
        except Exception as e:
            raise Exception(f"Failed to read sample CSV: {str(e)}")
        
        return hotspots
    
    def _fetch_from_api(self) -> List[Dict[str, Any]]:
        """
        Fetch hotspot data from NASA FIRMS API.
        
        Returns:
            List of normalized hotspot dictionaries
            
        Raises:
            requests.RequestException: If API request fails
        """
        # This is a placeholder for future API implementation
        # The actual FIRMS API requires specific parameters like area coordinates
        # For now, fall back to sample data
        try:
            # Example API call structure (not fully implemented):
            # params = {
            #     'MAP_KEY': self.api_key,
            #     'source': 'VIIRS_NOAA20_NRT',
            #     'area': '-90,-180,90,180',  # World coordinates
            #     'dayRange': 1
            # }
            # response = self.session.get(self.FIRMS_API_URL, params=params, timeout=30)
            # response.raise_for_status()
            
            # For MVP, return sample data even in API mode
            print("Warning: FIRMS API mode not fully implemented. Using sample data.")
            return self._fetch_from_sample()
            
        except Exception as e:
            raise Exception(f"Failed to fetch FIRMS data from API: {str(e)}")
    
    def _normalize_hotspot(self, row: Dict[str, str]) -> Dict[str, Any]:
        """
        Normalize FIRMS hotspot data into a clean structure.
        
        Args:
            row: Raw CSV row data
            
        Returns:
            Normalized hotspot dictionary
            
        Raises:
            ValueError: If required fields are missing or invalid
        """
        try:
            latitude = float(row['latitude'])
            longitude = float(row['longitude'])
            brightness = float(row['brightness'])
            confidence = row['confidence'].strip().lower()
            acq_date = row['acq_date'].strip()
            acq_time = row['acq_time'].strip()
            satellite = row['satellite'].strip()
            instrument = row['instrument'].strip()
            
            # Generate unique hotspot ID
            hotspot_id = f"FIRMS_{satellite}_{acq_date}_{acq_time}_{latitude}_{longitude}"
            
            # Calculate risk weight based on confidence and brightness
            risk_weight = self._calculate_risk_weight(confidence, brightness)
            
            return {
                "hotspot_id": hotspot_id,
                "latitude": latitude,
                "longitude": longitude,
                "brightness": brightness,
                "confidence": confidence,
                "acquisition_date": acq_date,
                "acquisition_time": acq_time,
                "satellite": satellite,
                "instrument": instrument,
                "source": "NASA FIRMS",
                "risk_weight": risk_weight
            }
            
        except KeyError as e:
            raise ValueError(f"Missing required field: {e}")
        except ValueError as e:
            raise ValueError(f"Invalid data format: {e}")
    
    def _calculate_risk_weight(self, confidence: str, brightness: float) -> float:
        """
        Calculate risk weight based on confidence level and brightness.
        
        Args:
            confidence: Confidence level ('low', 'nominal', 'high')
            brightness: Brightness temperature in Kelvin
            
        Returns:
            Risk weight between 0.0 and 1.0
        """
        # Base weight from confidence
        confidence_weights = {
            'low': 0.3,
            'nominal': 0.6,
            'high': 0.9
        }
        base_weight = confidence_weights.get(confidence, 0.5)
        
        # Adjust based on brightness (higher brightness = higher risk)
        # Typical fire brightness: 300-400K
        brightness_factor = min((brightness - 280) / 120, 1.0)
        brightness_factor = max(brightness_factor, 0.0)
        
        # Combine factors
        risk_weight = (base_weight * 0.7) + (brightness_factor * 0.3)
        return round(risk_weight, 3)
    
    def _apply_filters(
        self,
        hotspots: List[Dict[str, Any]],
        limit: Optional[int] = None,
        min_confidence: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Apply filters to hotspot data.
        
        Args:
            hotspots: List of hotspot dictionaries
            limit: Maximum number of hotspots to return
            min_confidence: Minimum confidence level filter
            
        Returns:
            Filtered list of hotspots
        """
        filtered = hotspots
        
        # Filter by confidence level
        if min_confidence:
            confidence_order = {'low': 0, 'nominal': 1, 'high': 2}
            min_level = confidence_order.get(min_confidence.lower(), 0)
            
            filtered = [
                h for h in filtered
                if confidence_order.get(h['confidence'], 0) >= min_level
            ]
        
        # Sort by risk weight (highest first) and acquisition date (most recent first)
        filtered.sort(
            key=lambda x: (x['risk_weight'], x['acquisition_date'], x['acquisition_time']),
            reverse=True
        )
        
        # Apply limit
        if limit and limit > 0:
            filtered = filtered[:limit]
        
        return filtered
    
    def _save_hotspots(self, hotspots: List[Dict[str, Any]]) -> None:
        """
        Save processed hotspots to JSON file.
        
        Args:
            hotspots: List of normalized hotspot dictionaries
        """
        # Create data directory if it doesn't exist
        PROJECT_ROOT = Path(__file__).resolve().parents[2]
        data_dir = PROJECT_ROOT / "data" / "processed"
        data_dir.mkdir(parents=True, exist_ok=True)
        
        # Save hotspots to file
        output_file = data_dir / "firms_hotspots.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(hotspots, f, indent=2, ensure_ascii=False)


# Convenience function for easy import
def fetch_firms_hotspots(
    limit: Optional[int] = None,
    min_confidence: Optional[str] = None
) -> Dict[str, Any]:
    """
    Convenience function to fetch FIRMS hotspots.
    
    Args:
        limit: Maximum number of hotspots to return
        min_confidence: Minimum confidence level ('low', 'nominal', 'high')
        
    Returns:
        Dictionary containing processed hotspots and metadata
    """
    client = FIRMSClient()
    return client.fetch_hotspots(limit=limit, min_confidence=min_confidence)


# Made with Bob