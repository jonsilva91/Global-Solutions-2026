"""
Rule-based risk scoring engine for the Astra Resilience Copilot.
Calculates environmental risk scores based on sensor data.
"""
from typing import Dict, List, Tuple
from src.backend.models.risk_models import SensorDataInput, RiskBreakdown


class RiskEngine:
    """Simple rule-based risk scoring engine."""
    
    @staticmethod
    def calculate_temperature_risk(temperature: float | None) -> float:
        """
        Calculate risk score based on temperature.
        
        Args:
            temperature: Temperature in Celsius
            
        Returns:
            Risk score from 0 to 30
        """
        if temperature is None:
            return 0.0
        
        if temperature > 35:
            return 30.0
        elif temperature > 30:
            return 20.0
        elif temperature > 25:
            return 10.0
        else:
            return 0.0
    
    @staticmethod
    def calculate_humidity_risk(humidity: float | None) -> float:
        """
        Calculate risk score based on humidity.
        
        Args:
            humidity: Humidity percentage
            
        Returns:
            Risk score from 0 to 25
        """
        if humidity is None:
            return 0.0
        
        if humidity < 20:
            return 25.0
        elif humidity < 40:
            return 15.0
        elif humidity < 60:
            return 5.0
        else:
            return 0.0
    
    @staticmethod
    def calculate_smoke_risk(smoke_level: float | None) -> float:
        """
        Calculate risk score based on smoke level.
        
        Args:
            smoke_level: Smoke level (0-100 scale)
            
        Returns:
            Risk score from 0 to 35
        """
        if smoke_level is None:
            return 0.0
        
        if smoke_level > 20:
            return 35.0
        elif smoke_level > 10:
            return 25.0
        elif smoke_level > 5:
            return 15.0
        else:
            return 0.0
    
    @staticmethod
    def calculate_soil_moisture_risk(soil_moisture: float | None) -> float:
        """
        Calculate risk score based on soil moisture.
        
        Args:
            soil_moisture: Soil moisture percentage
            
        Returns:
            Risk score from 0 to 10
        """
        if soil_moisture is None:
            return 0.0
        
        if soil_moisture < 20:
            return 10.0
        elif soil_moisture < 40:
            return 5.0
        else:
            return 0.0
    
    def analyze_risk(self, sensor_data: SensorDataInput | None) -> Tuple[float, RiskBreakdown]:
        """
        Analyze overall environmental risk based on sensor data.
        
        Args:
            sensor_data: Optional sensor data input
            
        Returns:
            Tuple of (total_risk_score, risk_breakdown)
        """
        if sensor_data is None:
            # Return default low risk if no sensor data provided
            breakdown = RiskBreakdown(
                temperature_risk=0.0,
                humidity_risk=0.0,
                smoke_risk=0.0,
                soil_moisture_risk=0.0
            )
            return 0.0, breakdown
        
        # Calculate individual risk components
        temp_risk = self.calculate_temperature_risk(sensor_data.temperature)
        humidity_risk = self.calculate_humidity_risk(sensor_data.humidity)
        smoke_risk = self.calculate_smoke_risk(sensor_data.smoke_level)
        soil_risk = self.calculate_soil_moisture_risk(sensor_data.soil_moisture)
        
        # Create breakdown
        breakdown = RiskBreakdown(
            temperature_risk=temp_risk,
            humidity_risk=humidity_risk,
            smoke_risk=smoke_risk,
            soil_moisture_risk=soil_risk
        )
        
        # Calculate total risk score
        total_risk = temp_risk + humidity_risk + smoke_risk + soil_risk
        
        return total_risk, breakdown
    
    @staticmethod
    def get_risk_level(risk_score: float) -> str:
        """
        Determine risk level based on total risk score.
        
        Args:
            risk_score: Total risk score (0-100)
            
        Returns:
            Risk level: "Low", "Medium", or "High"
        """
        if risk_score >= 61:
            return "High"
        elif risk_score >= 31:
            return "Medium"
        else:
            return "Low"
    
    @staticmethod
    def get_recommendations(risk_score: float, breakdown: RiskBreakdown) -> List[str]:
        """
        Generate recommendations based on risk analysis.
        
        Args:
            risk_score: Total risk score
            breakdown: Risk breakdown by component
            
        Returns:
            List of recommendation strings
        """
        recommendations = []
        
        # Overall risk recommendations
        if risk_score >= 61:
            recommendations.append("⚠️ High risk detected - immediate action recommended")
        elif risk_score >= 31:
            recommendations.append("⚡ Medium risk detected - monitor situation closely")
        else:
            recommendations.append("✅ Low risk - continue normal monitoring")
        
        # Temperature-specific recommendations
        if breakdown.temperature_risk >= 20:
            recommendations.append("🌡️ High temperature detected - implement cooling measures and fire prevention")
        
        # Humidity-specific recommendations
        if breakdown.humidity_risk >= 15:
            recommendations.append("💧 Low humidity detected - increase fire monitoring and water availability")
        
        # Smoke-specific recommendations
        if breakdown.smoke_risk >= 25:
            recommendations.append("🔥 Elevated smoke levels - check for fire sources and evacuate if necessary")
        elif breakdown.smoke_risk >= 15:
            recommendations.append("👃 Smoke detected - investigate potential fire hazards")
        
        # Soil moisture-specific recommendations
        if breakdown.soil_moisture_risk >= 5:
            recommendations.append("🌱 Low soil moisture - consider irrigation and drought prevention measures")
        
        return recommendations


# Global risk engine instance
risk_engine = RiskEngine()

# Made with Bob
