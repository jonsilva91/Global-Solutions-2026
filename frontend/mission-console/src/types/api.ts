// API Response Types for Astra Resilience Copilot

export interface HealthResponse {
  status: string;
  timestamp: string;
  version: string;
}

export interface MissionInfo {
  project_name: string;
  version: string;
  description: string;
  main_components: string[];
  mission: string;
  target_areas: string[];
}

export interface SensorReading {
  device_id: string;
  temperature: number;
  humidity: number;
  soil_moisture: number;
  smoke_level: number;
  battery_level: number;
  network_status: string;
  timestamp: string;
}

export interface SensorReadingRequest {
  device_id: string;
  temperature: number;
  humidity: number;
  soil_moisture: number;
  smoke_level: number;
  battery_level: number;
  network_status: string;
}

export interface Evidence {
  source: string;
  description: string;
  value: number | string;
  timestamp: string;
}

export interface RiskBreakdown {
  firms_risk: number;
  sensor_risk: number;
  eonet_risk: number;
  smoke_risk: number;
  operational_risk: number;
}

export interface RiskAnalysisResponse {
  area_of_interest: string;
  risk_score: number;
  total_risk_score: number;
  risk_level: string;
  recommended_action: string;
  recommendations: string[];
  risk_breakdown: RiskBreakdown;
  evidence: Evidence[];
  provenance: {
    firms_file: string;
    eonet_file: string;
    sensor_file: string;
  };
  timestamp: string;
}

export interface RiskAnalysisRequest {
  area_of_interest: string;
  sensor_data: {
    temperature: number;
    humidity: number;
    soil_moisture: number;
    smoke_level: number;
  };
}

export interface Alert {
  alert_id: string;
  alert_type: string;
  severity: string;
  area: string;
  message: string;
  risk_score: number;
  timestamp: string;
  status: string;
  device_id: string | null;
}

export interface FIRMSHotspot {
  hotspot_id: string;
  latitude: number;
  longitude: number;
  brightness: number;
  confidence: string;
  acquisition_date: string;
  acquisition_time: string;
  satellite: string;
  instrument: string;
  source: string;
  risk_weight: number;
}

export interface FIRMSResponse {
  source: string;
  mode: string;
  total_hotspots: number;
  filters: {
    limit: number | null;
    min_confidence: string | null;
  };
  hotspots: FIRMSHotspot[];
}

export interface EONETEvent {
  event_id: string;
  title: string;
  category: string;
  status: string;
  source: string;
  geometry_type: string;
  coordinates: number[];
  event_date: string;
  api_source: string;
}

export interface EONETResponse {
  source: string;
  total_events: number;
  filters: Record<string, unknown>;
  events: EONETEvent[];
}

export interface AlertsResponse {
  total_alerts: number;
  active_alerts: number;
  alerts: Alert[];
}

export interface EONETCategory {
  id: string;
  title: string;
  link: string;
  description: string;
}

export interface SourceProvenance {
  firms_file: string;
  eonet_file: string;
  sensor_file: string;
  alerts_file?: string;
  knowledge_base: string[];
}

export interface CopilotReportResponse {
  title: string;
  area_of_interest: string;
  risk_level: string;
  risk_score: number;
  executive_summary: string;
  evidence_summary: string[];
  source_provenance: SourceProvenance;
  recommended_actions: string[];
  limitations: string[];
  generated_at: string;
}

export interface CopilotReportRequest {
  risk_analysis: RiskAnalysisResponse;
}

// Made with Bob
