"""
RAG Copilot for Astra Resilience - Operational Report Generator

This module provides a lightweight RAG-style operational report generator that:
1. Loads markdown knowledge base files
2. Retrieves relevant context using keyword matching
3. Loads runtime data from processed files
4. Generates operational briefings

For MVP: Uses template-based generation with optional LLM enhancement.
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
import re


class AstraCopilot:
    """RAG-based operational report generator for Astra Resilience Copilot."""
    
    def __init__(self, knowledge_base_dir: str = "data/knowledge"):
        """
        Initialize the copilot with knowledge base directory.
        
        Args:
            knowledge_base_dir: Path to directory containing markdown knowledge files
        """
        self.knowledge_base_dir = Path(knowledge_base_dir)
        self.knowledge_base = {}
        self._load_knowledge_base()
    
    def _load_knowledge_base(self):
        """Load all markdown files from the knowledge base directory."""
        if not self.knowledge_base_dir.exists():
            print(f"Warning: Knowledge base directory {self.knowledge_base_dir} does not exist")
            return
        
        for md_file in self.knowledge_base_dir.glob("*.md"):
            try:
                with open(md_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    self.knowledge_base[md_file.stem] = {
                        'path': str(md_file),
                        'content': content
                    }
            except Exception as e:
                print(f"Error loading {md_file}: {e}")
    
    def _load_json_file(self, filepath: str) -> Optional[Any]:
        """Load a JSON file if it exists."""
        path = Path(filepath)
        if not path.exists():
            return None
        
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading {filepath}: {e}")
            return None
    
    def _retrieve_relevant_context(self, risk_analysis: Dict[str, Any]) -> List[str]:
        """
        Retrieve relevant knowledge base sections based on risk analysis.
        Uses simple keyword matching for MVP.
        
        Args:
            risk_analysis: The risk analysis payload
            
        Returns:
            List of relevant knowledge base file names
        """
        relevant_docs = []
        
        # Always include architecture and risk methodology
        relevant_docs.append('astra_architecture')
        relevant_docs.append('risk_methodology')
        
        # Check for specific keywords in evidence
        evidence = risk_analysis.get('evidence', [])
        evidence_text = ' '.join(str(e) for e in evidence).lower()
        
        if 'firms' in evidence_text or 'hotspot' in evidence_text or 'fire' in evidence_text:
            relevant_docs.append('firms_notes')
        
        if 'eonet' in evidence_text or 'event' in evidence_text:
            relevant_docs.append('eonet_notes')
        
        # Include operational guidelines for HIGH and CRITICAL risks
        risk_level = risk_analysis.get('risk_level', '').upper()
        if risk_level in ['HIGH', 'CRITICAL']:
            relevant_docs.append('operational_guidelines')
        
        return list(set(relevant_docs))  # Remove duplicates
    
    def _extract_risk_level_guidance(self, risk_level: str) -> Dict[str, Any]:
        """
        Extract specific guidance for the given risk level from knowledge base.
        
        Args:
            risk_level: Risk level (LOW, MODERATE, HIGH, CRITICAL)
            
        Returns:
            Dictionary with actions, indicators, and conditions
        """
        risk_methodology = self.knowledge_base.get('risk_methodology', {}).get('content', '')
        
        # Extract section for this risk level
        pattern = rf"### {risk_level.upper()} \([\d-]+\)(.*?)(?=###|\Z)"
        match = re.search(pattern, risk_methodology, re.DOTALL)
        
        if not match:
            return {
                'actions': [],
                'indicators': [],
                'conditions': ''
            }
        
        section = match.group(1)
        
        # Extract actions
        actions = []
        actions_match = re.search(r'\*\*Actions\*\*:(.*?)(?=\*\*|\Z)', section, re.DOTALL)
        if actions_match:
            actions_text = actions_match.group(1)
            actions = [line.strip('- ').strip() for line in actions_text.split('\n') 
                      if line.strip().startswith('-')]
        
        # Extract indicators
        indicators = []
        indicators_match = re.search(r'\*\*Indicators\*\*:(.*?)(?=\*\*|\Z)', section, re.DOTALL)
        if indicators_match:
            indicators_text = indicators_match.group(1)
            indicators = [line.strip('- ').strip() for line in indicators_text.split('\n') 
                         if line.strip().startswith('-')]
        
        # Extract conditions
        conditions = ''
        conditions_match = re.search(r'\*\*Conditions\*\*:(.*?)(?=\*\*)', section, re.DOTALL)
        if conditions_match:
            conditions = conditions_match.group(1).strip()
        
        return {
            'actions': actions,
            'indicators': indicators,
            'conditions': conditions
        }
    
    def _generate_executive_summary(self, risk_analysis: Dict[str, Any], 
                                   runtime_data: Dict[str, Any]) -> str:
        """
        Generate executive summary based on risk analysis and runtime data.
        
        Args:
            risk_analysis: Risk analysis payload
            runtime_data: Runtime data from processed files
            
        Returns:
            Executive summary text
        """
        area = risk_analysis.get('area_of_interest', 'Unknown Area')
        risk_level = risk_analysis.get('risk_level', 'UNKNOWN')
        risk_score = risk_analysis.get('risk_score', 0)
        
        # Get risk level guidance
        guidance = self._extract_risk_level_guidance(risk_level)
        
        # Count data sources
        firms_count = len(runtime_data.get('firms_hotspots', []))
        eonet_count = len(runtime_data.get('eonet_events', []))
        sensor_count = len(runtime_data.get('sensor_readings', []))
        
        summary_parts = []
        
        # Opening statement
        summary_parts.append(
            f"The {area} region is currently assessed at {risk_level} risk "
            f"with a composite score of {risk_score:.1f}/100."
        )
        
        # Data sources summary
        data_summary = []
        if firms_count > 0:
            data_summary.append(f"{firms_count} FIRMS fire hotspot(s)")
        if eonet_count > 0:
            data_summary.append(f"{eonet_count} EONET event(s)")
        if sensor_count > 0:
            data_summary.append(f"{sensor_count} sensor reading(s)")
        
        if data_summary:
            summary_parts.append(
                f"This assessment is based on {', '.join(data_summary)}."
            )
        
        # Risk-specific context
        if risk_level == 'CRITICAL':
            summary_parts.append(
                "IMMEDIATE ACTION REQUIRED. Multiple high-severity indicators detected. "
                "Emergency response protocols should be activated immediately."
            )
        elif risk_level == 'HIGH':
            summary_parts.append(
                "Significant risk factors are present. Response teams should be activated "
                "and resources pre-positioned for rapid deployment."
            )
        elif risk_level == 'MODERATE':
            summary_parts.append(
                "Elevated environmental stress detected. Enhanced monitoring and "
                "response readiness recommended."
            )
        else:  # LOW
            summary_parts.append(
                "Conditions are within normal parameters. Continue routine monitoring."
            )
        
        return ' '.join(summary_parts)
    
    def _generate_evidence_summary(self, risk_analysis: Dict[str, Any]) -> List[str]:
        """
        Generate evidence summary from risk analysis.
        
        Args:
            risk_analysis: Risk analysis payload
            
        Returns:
            List of evidence statements
        """
        evidence = risk_analysis.get('evidence', [])
        
        if not evidence:
            return ["No specific evidence items available in this assessment."]
        
        # Format evidence items
        formatted_evidence = []
        for item in evidence:
            if isinstance(item, dict):
                # Extract key information from structured evidence
                source = item.get('source', 'Unknown')
                value = item.get('value', '')
                description = item.get('description', '')
                formatted_evidence.append(f"{source}: {description or value}")
            else:
                # Handle string evidence
                formatted_evidence.append(str(item))
        
        return formatted_evidence
    
    def _generate_recommended_actions(self, risk_analysis: Dict[str, Any]) -> List[str]:
        """
        Generate recommended actions based on risk level and analysis.
        
        Args:
            risk_analysis: Risk analysis payload
            
        Returns:
            List of recommended actions
        """
        risk_level = risk_analysis.get('risk_level', 'UNKNOWN')
        
        # Get actions from knowledge base
        guidance = self._extract_risk_level_guidance(risk_level)
        actions = guidance.get('actions', [])
        
        if not actions:
            # Fallback actions if knowledge base extraction fails
            if risk_level == 'CRITICAL':
                actions = [
                    "Execute emergency response plan immediately",
                    "Initiate evacuations if required",
                    "Deploy all available resources",
                    "Establish incident command structure",
                    "Maintain continuous real-time monitoring"
                ]
            elif risk_level == 'HIGH':
                actions = [
                    "Activate response teams",
                    "Pre-position resources at staging areas",
                    "Establish command post and communication protocols",
                    "Coordinate with local authorities",
                    "Increase monitoring frequency to every 15-30 minutes"
                ]
            elif risk_level == 'MODERATE':
                actions = [
                    "Increase monitoring frequency to every 1-2 hours",
                    "Review and update response plans",
                    "Brief response teams on current situation",
                    "Check equipment and supply readiness",
                    "Establish enhanced communication protocols"
                ]
            else:  # LOW
                actions = [
                    "Continue routine monitoring every 2-4 hours",
                    "Maintain standard equipment readiness",
                    "Update baseline measurements",
                    "Conduct training and drills as scheduled"
                ]
        
        # Add any specific recommendations from the risk analysis
        specific_recommendations = risk_analysis.get('recommendations', [])
        if specific_recommendations:
            actions.extend(specific_recommendations)
        
        return actions
    
    def _generate_limitations(self, runtime_data: Dict[str, Any]) -> List[str]:
        """
        Generate list of limitations and uncertainties.
        
        Args:
            runtime_data: Runtime data from processed files
            
        Returns:
            List of limitation statements
        """
        limitations = []
        
        # Check data availability
        if not runtime_data.get('firms_hotspots'):
            limitations.append(
                "No FIRMS hotspot data available - satellite fire detection limited"
            )
        
        if not runtime_data.get('eonet_events'):
            limitations.append(
                "No EONET event data available - broader event context unavailable"
            )
        
        if not runtime_data.get('sensor_readings'):
            limitations.append(
                "No ground sensor data available - local conditions not verified"
            )
        
        # Standard limitations
        limitations.extend([
            "Satellite data subject to 12-hour revisit gaps and cloud cover interference",
            "Risk assessment is point-in-time and should be updated every 15-30 minutes",
            "Ground conditions may vary significantly from satellite observations",
            "Model uses simplified weight assignments pending historical calibration"
        ])
        
        return limitations
    
    def generate_report(self, risk_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate operational briefing report.
        
        Args:
            risk_analysis: Risk analysis payload from /risk/analyze endpoint
            
        Returns:
            Operational briefing report dictionary
        """
        # Load runtime data
        runtime_data = {
            'firms_hotspots': self._load_json_file('data/processed/firms_hotspots.json') or [],
            'eonet_events': self._load_json_file('data/processed/eonet_events.json') or [],
            'sensor_readings': self._load_json_file('data/processed/sensor_readings.json') or [],
            'alerts': self._load_json_file('data/processed/alerts.json') or []
        }
        
        # Retrieve relevant knowledge base documents
        relevant_docs = self._retrieve_relevant_context(risk_analysis)
        
        # Generate report components
        executive_summary = self._generate_executive_summary(risk_analysis, runtime_data)
        evidence_summary = self._generate_evidence_summary(risk_analysis)
        recommended_actions = self._generate_recommended_actions(risk_analysis)
        limitations = self._generate_limitations(runtime_data)
        
        # Build source provenance
        source_provenance = {
            'firms_file': 'data/processed/firms_hotspots.json',
            'eonet_file': 'data/processed/eonet_events.json',
            'sensor_file': 'data/processed/sensor_readings.json',
            'alerts_file': 'data/processed/alerts.json',
            'knowledge_base': [
                self.knowledge_base[doc]['path'] 
                for doc in relevant_docs 
                if doc in self.knowledge_base
            ]
        }
        
        # Construct final report
        report = {
            'title': 'Astra Resilience Copilot — Operational Briefing',
            'area_of_interest': risk_analysis.get('area_of_interest', 'Unknown Area'),
            'risk_level': risk_analysis.get('risk_level', 'UNKNOWN'),
            'risk_score': float(risk_analysis.get('risk_score', 0)),
            'executive_summary': executive_summary,
            'evidence_summary': evidence_summary,
            'source_provenance': source_provenance,
            'recommended_actions': recommended_actions,
            'limitations': limitations,
            'generated_at': datetime.utcnow().isoformat() + 'Z'
        }
        
        return report


# Singleton instance
_copilot_instance = None


def get_copilot() -> AstraCopilot:
    """Get or create the singleton copilot instance."""
    global _copilot_instance
    if _copilot_instance is None:
        _copilot_instance = AstraCopilot()
    return _copilot_instance

# Made with Bob
