"""
Space-enabled environmental risk engine for the Astra Resilience Copilot.
Integrates NASA FIRMS hotspots, NASA EONET events, and edge sensor data
to calculate comprehensive environmental risk scores.
"""
import json
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta

# Resolve project root from this file's location
PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_DATA_DIR = PROJECT_ROOT / "data" / "processed"


class SpatialRiskEngine:
    """
    Space-enabled risk scoring engine that combines:
    - NASA FIRMS hotspot data (35% weight)
    - Edge sensor readings (25% weight)
    - NASA EONET events (20% weight)
    - Smoke/fire indicators (10% weight)
    - Operational risk (10% weight)
    """
    
    def __init__(self, data_dir: Optional[Path] = None):
        """
        Initialize the spatial risk engine.
        
        Args:
            data_dir: Directory containing processed data files (defaults to PROJECT_ROOT/data/processed)
        """
        self.data_dir = data_dir if data_dir else DEFAULT_DATA_DIR
        self.firms_file = self.data_dir / "firms_hotspots.json"
        self.eonet_file = self.data_dir / "eonet_events.json"
        self.sensor_file = self.data_dir / "sensor_readings.json"
    
    def _load_json_file(self, file_path: Path) -> List[Dict[str, Any]]:
        """
        Safely load a JSON file, returning empty list if file doesn't exist.
        
        Args:
            file_path: Path to JSON file
            
        Returns:
            List of data items or empty list
        """
        if not file_path.exists():
            return []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data if isinstance(data, list) else []
        except (json.JSONDecodeError, IOError) as e:
            print(f"Warning: Error reading {file_path.name}: {e}")
            return []
    
    def _calculate_firms_risk(self, firms_data: List[Dict[str, Any]]) -> Tuple[float, List[Dict[str, Any]]]:
        """
        Calculate risk score from FIRMS hotspot data (0-35 points).
        
        Args:
            firms_data: List of FIRMS hotspot records
            
        Returns:
            Tuple of (risk_score, evidence_list)
        """
        if not firms_data:
            return 0.0, []
        
        # Count recent hotspots (last 7 days)
        recent_cutoff = datetime.utcnow() - timedelta(days=7)
        recent_hotspots = []
        high_confidence_count = 0
        total_hotspots = 0
        
        for hotspot in firms_data:
            total_hotspots += 1
            try:
                # Parse acquisition date (normalized field name)
                acq_date_str = hotspot.get('acquisition_date', '')
                if acq_date_str:
                    acq_date = datetime.strptime(acq_date_str, '%Y-%m-%d')
                    if acq_date >= recent_cutoff:
                        recent_hotspots.append(hotspot)
                        
                        # Count high confidence detections
                        confidence = hotspot.get('confidence', '').lower()
                        if confidence in ['high', 'h']:
                            high_confidence_count += 1
                else:
                    # If date cannot be parsed, count as valid sample for MVP
                    recent_hotspots.append(hotspot)
                    confidence = hotspot.get('confidence', '').lower()
                    if confidence in ['high', 'h']:
                        high_confidence_count += 1
            except (ValueError, TypeError):
                # If date parsing fails, still count as valid sample for MVP
                recent_hotspots.append(hotspot)
                confidence = hotspot.get('confidence', '').lower()
                if confidence in ['high', 'h']:
                    high_confidence_count += 1
        
        # Calculate risk based on hotspot density and confidence
        hotspot_count = len(recent_hotspots)
        
        if hotspot_count == 0:
            risk_score = 0.0
        elif hotspot_count >= 10:
            risk_score = 35.0
        elif hotspot_count >= 5:
            risk_score = 28.0
        elif hotspot_count >= 2:
            risk_score = 20.0
        else:
            risk_score = 12.0
        
        # Boost score for high confidence detections
        if high_confidence_count >= 3:
            risk_score = min(35.0, risk_score + 5.0)
        
        # Build evidence
        evidence = []
        if recent_hotspots:
            evidence.append({
                "source": "NASA FIRMS",
                "description": f"{hotspot_count} active fire hotspots detected",
                "value": hotspot_count,
                "timestamp": datetime.utcnow().isoformat() + "Z"
            })
            
            if high_confidence_count > 0:
                evidence.append({
                    "source": "NASA FIRMS",
                    "description": f"{high_confidence_count} high-confidence fire detections",
                    "value": high_confidence_count,
                    "timestamp": datetime.utcnow().isoformat() + "Z"
                })
        
        return risk_score, evidence
    
    def _calculate_sensor_risk(self, sensor_data: Optional[Dict[str, Any]]) -> Tuple[float, List[Dict[str, Any]]]:
        """
        Calculate risk score from edge sensor data (0-25 points).
        
        Args:
            sensor_data: Latest sensor reading or None
            
        Returns:
            Tuple of (risk_score, evidence_list)
        """
        if not sensor_data:
            return 0.0, []
        
        risk_score = 0.0
        evidence = []
        
        # Temperature risk (0-10 points)
        temperature = sensor_data.get('temperature')
        if temperature is not None:
            if temperature > 38:
                temp_risk = 10.0
            elif temperature > 35:
                temp_risk = 7.0
            elif temperature > 32:
                temp_risk = 4.0
            else:
                temp_risk = 0.0
            
            risk_score += temp_risk
            
            if temp_risk > 0:
                evidence.append({
                    "source": "EDGE_SENSOR",
                    "description": f"Elevated temperature detected",
                    "value": f"{temperature}°C",
                    "timestamp": sensor_data.get('timestamp', datetime.utcnow().isoformat() + "Z")
                })
        
        # Humidity risk (0-8 points)
        humidity = sensor_data.get('humidity')
        if humidity is not None:
            if humidity < 15:
                humidity_risk = 8.0
            elif humidity < 25:
                humidity_risk = 5.0
            elif humidity < 35:
                humidity_risk = 2.0
            else:
                humidity_risk = 0.0
            
            risk_score += humidity_risk
            
            if humidity_risk > 0:
                evidence.append({
                    "source": "EDGE_SENSOR",
                    "description": f"Low humidity detected",
                    "value": f"{humidity}%",
                    "timestamp": sensor_data.get('timestamp', datetime.utcnow().isoformat() + "Z")
                })
        
        # Soil moisture risk (0-7 points)
        soil_moisture = sensor_data.get('soil_moisture')
        if soil_moisture is not None:
            if soil_moisture < 15:
                soil_risk = 7.0
            elif soil_moisture < 25:
                soil_risk = 4.0
            elif soil_moisture < 35:
                soil_risk = 2.0
            else:
                soil_risk = 0.0
            
            risk_score += soil_risk
            
            if soil_risk > 0:
                evidence.append({
                    "source": "EDGE_SENSOR",
                    "description": f"Low soil moisture detected",
                    "value": f"{soil_moisture}%",
                    "timestamp": sensor_data.get('timestamp', datetime.utcnow().isoformat() + "Z")
                })
        
        return min(25.0, risk_score), evidence
    
    def _calculate_eonet_risk(self, eonet_data: List[Dict[str, Any]]) -> Tuple[float, List[Dict[str, Any]]]:
        """
        Calculate risk score from EONET events (0-20 points).
        Supports both normalized records (with 'category') and raw API records (with 'categories').
        
        Args:
            eonet_data: List of EONET event records
            
        Returns:
            Tuple of (risk_score, evidence_list)
        """
        if not eonet_data:
            return 0.0, []
        
        # Count events by category
        fire_events = 0
        severe_storm_events = 0
        drought_events = 0
        flood_events = 0
        volcano_events = 0
        other_events = 0
        
        # Risk-relevant category keywords
        fire_keywords = ['wildfire', 'wildfires', 'fire']
        storm_keywords = ['storm', 'storms', 'severe storms']
        drought_keywords = ['drought']
        flood_keywords = ['flood', 'floods']
        volcano_keywords = ['volcano', 'volcanoes']
        
        for event in eonet_data:
            # Support normalized format (single 'category' field)
            if 'category' in event:
                category = event.get('category', '').lower()
                if any(kw in category for kw in fire_keywords):
                    fire_events += 1
                elif any(kw in category for kw in storm_keywords):
                    severe_storm_events += 1
                elif any(kw in category for kw in drought_keywords):
                    drought_events += 1
                elif any(kw in category for kw in flood_keywords):
                    flood_events += 1
                elif any(kw in category for kw in volcano_keywords):
                    volcano_events += 1
                else:
                    other_events += 1
            # Support raw API format (list of 'categories')
            elif 'categories' in event:
                categories = event.get('categories', [])
                for category in categories:
                    cat_title = category.get('title', '').lower()
                    if any(kw in cat_title for kw in fire_keywords):
                        fire_events += 1
                    elif any(kw in cat_title for kw in storm_keywords):
                        severe_storm_events += 1
                    elif any(kw in cat_title for kw in drought_keywords):
                        drought_events += 1
                    elif any(kw in cat_title for kw in flood_keywords):
                        flood_events += 1
                    elif any(kw in cat_title for kw in volcano_keywords):
                        volcano_events += 1
                    else:
                        other_events += 1
        
        # Calculate risk based on event types
        risk_score = 0.0
        
        if fire_events > 0:
            risk_score += min(12.0, fire_events * 4.0)
        
        if severe_storm_events > 0:
            risk_score += min(5.0, severe_storm_events * 2.0)
        
        if drought_events > 0:
            risk_score += min(3.0, drought_events * 1.5)
        
        if flood_events > 0:
            risk_score += min(3.0, flood_events * 1.5)
        
        if volcano_events > 0:
            risk_score += min(2.0, volcano_events * 1.0)
        
        risk_score = min(20.0, risk_score)
        
        # Build evidence
        evidence = []
        if fire_events > 0:
            evidence.append({
                "source": "NASA EONET",
                "description": f"{fire_events} active wildfire event(s) detected",
                "value": fire_events,
                "timestamp": datetime.utcnow().isoformat() + "Z"
            })
        
        if severe_storm_events > 0:
            evidence.append({
                "source": "NASA EONET",
                "description": f"{severe_storm_events} severe storm event(s) detected",
                "value": severe_storm_events,
                "timestamp": datetime.utcnow().isoformat() + "Z"
            })
        
        if drought_events > 0:
            evidence.append({
                "source": "NASA EONET",
                "description": f"{drought_events} drought event(s) detected",
                "value": drought_events,
                "timestamp": datetime.utcnow().isoformat() + "Z"
            })
        
        if flood_events > 0:
            evidence.append({
                "source": "NASA EONET",
                "description": f"{flood_events} flood event(s) detected",
                "value": flood_events,
                "timestamp": datetime.utcnow().isoformat() + "Z"
            })
        
        return risk_score, evidence
    
    def _calculate_smoke_risk(self, sensor_data: Optional[Dict[str, Any]]) -> Tuple[float, List[Dict[str, Any]]]:
        """
        Calculate risk score from smoke level (0-10 points).
        
        Args:
            sensor_data: Latest sensor reading or None
            
        Returns:
            Tuple of (risk_score, evidence_list)
        """
        if not sensor_data:
            return 0.0, []
        
        smoke_level = sensor_data.get('smoke_level')
        if smoke_level is None:
            return 0.0, []
        
        if smoke_level > 30:
            risk_score = 10.0
        elif smoke_level > 20:
            risk_score = 7.0
        elif smoke_level > 10:
            risk_score = 4.0
        else:
            risk_score = 0.0
        
        evidence = []
        if risk_score > 0:
            evidence.append({
                "source": "EDGE_SENSOR",
                "description": f"Elevated smoke level detected",
                "value": smoke_level,
                "timestamp": sensor_data.get('timestamp', datetime.utcnow().isoformat() + "Z")
            })
        
        return risk_score, evidence
    
    def _calculate_operational_risk(self, sensor_data: Optional[Dict[str, Any]]) -> Tuple[float, List[Dict[str, Any]]]:
        """
        Calculate operational risk from battery and connectivity (0-10 points).
        
        Args:
            sensor_data: Latest sensor reading or None
            
        Returns:
            Tuple of (risk_score, evidence_list)
        """
        if not sensor_data:
            return 0.0, []
        
        risk_score = 0.0
        evidence = []
        
        # Battery risk (0-6 points)
        battery_level = sensor_data.get('battery_level')
        if battery_level is not None:
            if battery_level < 20:
                battery_risk = 6.0
            elif battery_level < 40:
                battery_risk = 3.0
            else:
                battery_risk = 0.0
            
            risk_score += battery_risk
            
            if battery_risk > 0:
                evidence.append({
                    "source": "EDGE_SENSOR",
                    "description": f"Low battery level",
                    "value": f"{battery_level}%",
                    "timestamp": sensor_data.get('timestamp', datetime.utcnow().isoformat() + "Z")
                })
        
        # Network risk (0-4 points)
        network_status = sensor_data.get('network_status', '').lower()
        if network_status in ['degraded', 'poor', 'offline']:
            network_risk = 4.0
            evidence.append({
                "source": "EDGE_SENSOR",
                "description": f"Network connectivity issue",
                "value": network_status,
                "timestamp": sensor_data.get('timestamp', datetime.utcnow().isoformat() + "Z")
            })
        else:
            network_risk = 0.0
        
        risk_score += network_risk
        
        return min(10.0, risk_score), evidence
    
    def _get_risk_level(self, risk_score: float) -> str:
        """
        Determine risk level from score.
        
        Args:
            risk_score: Total risk score (0-100)
            
        Returns:
            Risk level string
        """
        if risk_score >= 85:
            return "CRITICAL"
        elif risk_score >= 70:
            return "HIGH"
        elif risk_score >= 40:
            return "MODERATE"
        else:
            return "LOW"
    
    def _get_recommended_action(self, risk_level: str, risk_breakdown: Dict[str, float]) -> str:
        """
        Generate recommended action based on risk level and breakdown.
        
        Args:
            risk_level: Risk level string
            risk_breakdown: Dictionary of risk component scores
            
        Returns:
            Recommended action string
        """
        if risk_level == "CRITICAL":
            return "🚨 CRITICAL: Immediate evacuation and emergency response required. Contact authorities immediately."
        elif risk_level == "HIGH":
            actions = ["⚠️ HIGH RISK: Prepare for potential evacuation."]
            
            if risk_breakdown.get('firms_risk', 0) > 20:
                actions.append("Active fires detected nearby - monitor fire spread closely.")
            
            if risk_breakdown.get('smoke_risk', 0) > 5:
                actions.append("Elevated smoke levels - ensure air filtration and limit outdoor exposure.")
            
            return " ".join(actions)
        elif risk_level == "MODERATE":
            return "⚡ MODERATE RISK: Increase monitoring frequency. Review emergency plans and ensure readiness."
        else:
            return "✅ LOW RISK: Continue routine monitoring. Maintain situational awareness."
    
    def _ensure_firms_data(self) -> None:
        """
        Ensure FIRMS data exists by loading from local sample if needed.
        This provides automatic fallback for MVP robustness.
        """
        if not self.firms_file.exists() or self.firms_file.stat().st_size == 0:
            try:
                # Import here to avoid circular dependency
                from src.ingestion.firms_client import FIRMSClient
                
                # Use local sample mode (no API key required)
                client = FIRMSClient(use_api=False)
                client.fetch_hotspots()
                print("FIRMS data loaded from local sample for risk analysis")
            except Exception as e:
                print(f"Warning: Could not load FIRMS sample data: {e}")
    
    def analyze_spatial_risk(
        self,
        area_of_interest: str,
        sensor_data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Perform comprehensive spatial risk analysis.
        
        Args:
            area_of_interest: Geographic area being analyzed
            sensor_data: Optional sensor data (if None, will load latest from file)
            
        Returns:
            Complete risk analysis result dictionary
        """
        # Ensure FIRMS data exists (automatic fallback to local sample)
        self._ensure_firms_data()
        
        # Load data from files
        firms_data = self._load_json_file(self.firms_file)
        eonet_data = self._load_json_file(self.eonet_file)
        
        # Get sensor data
        if sensor_data is None:
            sensor_readings = self._load_json_file(self.sensor_file)
            sensor_data = sensor_readings[-1] if sensor_readings else None
        
        # Calculate risk components
        firms_risk, firms_evidence = self._calculate_firms_risk(firms_data)
        sensor_risk, sensor_evidence = self._calculate_sensor_risk(sensor_data)
        eonet_risk, eonet_evidence = self._calculate_eonet_risk(eonet_data)
        smoke_risk, smoke_evidence = self._calculate_smoke_risk(sensor_data)
        operational_risk, operational_evidence = self._calculate_operational_risk(sensor_data)
        
        # Calculate total risk score
        total_risk_score = firms_risk + sensor_risk + eonet_risk + smoke_risk + operational_risk
        
        # Determine risk level
        risk_level = self._get_risk_level(total_risk_score)
        
        # Build risk breakdown
        risk_breakdown = {
            "firms_risk": round(firms_risk, 2),
            "sensor_risk": round(sensor_risk, 2),
            "eonet_risk": round(eonet_risk, 2),
            "smoke_risk": round(smoke_risk, 2),
            "operational_risk": round(operational_risk, 2)
        }
        
        # Combine all evidence
        all_evidence = firms_evidence + sensor_evidence + eonet_evidence + smoke_evidence + operational_evidence
        
        # Get recommended action
        recommended_action = self._get_recommended_action(risk_level, risk_breakdown)
        
        # Build relative provenance paths
        firms_rel = self.firms_file.relative_to(PROJECT_ROOT).as_posix()
        eonet_rel = self.eonet_file.relative_to(PROJECT_ROOT).as_posix()
        sensor_rel = self.sensor_file.relative_to(PROJECT_ROOT).as_posix()
        
        # Build result
        result = {
            "area_of_interest": area_of_interest,
            "risk_score": round(total_risk_score, 2),
            "risk_level": risk_level,
            "risk_breakdown": risk_breakdown,
            "evidence": all_evidence,
            "recommended_action": recommended_action,
            "provenance": {
                "firms_file": firms_rel,
                "eonet_file": eonet_rel,
                "sensor_file": sensor_rel
            },
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
        
        return result


# Global spatial risk engine instance
spatial_risk_engine = SpatialRiskEngine()

# Made with Bob