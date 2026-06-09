import axios, { AxiosInstance } from "axios";
import type {
  HealthResponse,
  MissionInfo,
  SensorReading,
  SensorReadingRequest,
  RiskAnalysisResponse,
  RiskAnalysisRequest,
  Alert,
  FIRMSHotspot,
  EONETEvent,
  EONETCategory,
  FIRMSResponse,
  EONETResponse,
  AlertsResponse,
  CopilotReportRequest,
  CopilotReportResponse,
} from "../types/api";

class ApiClient {
  private client: AxiosInstance;
  private baseURL: string;

  constructor(baseURL: string = "http://127.0.0.1:8000") {
    this.baseURL = baseURL;
    this.client = axios.create({
      baseURL: this.baseURL,
      timeout: 30000,
      headers: {
        "Content-Type": "application/json",
      },
    });
  }

  // Update base URL dynamically
  setBaseURL(url: string) {
    this.baseURL = url;
    this.client = axios.create({
      baseURL: this.baseURL,
      timeout: 30000,
      headers: {
        "Content-Type": "application/json",
      },
    });
  }

  getBaseURL(): string {
    return this.baseURL;
  }

  // Health endpoint
  async getHealth(): Promise<HealthResponse> {
    const response = await this.client.get<HealthResponse>("/health");
    return response.data;
  }

  // Mission info endpoint
  async getMissionInfo(): Promise<MissionInfo> {
    const response = await this.client.get<MissionInfo>("/mission/info");
    return response.data;
  }

  // Sensor readings endpoints
  async submitSensorReading(
    data: SensorReadingRequest,
  ): Promise<{ message: string; reading: SensorReading }> {
    const response = await this.client.post("/sensor/readings", data);
    return response.data;
  }

  async getLatestSensorReading(): Promise<SensorReading> {
    const response = await this.client.get<SensorReading>(
      "/sensor/readings/latest",
    );
    return response.data;
  }

  // Risk analysis endpoint
  async analyzeRisk(data: RiskAnalysisRequest): Promise<RiskAnalysisResponse> {
    const response = await this.client.post<RiskAnalysisResponse>(
      "/risk/analyze",
      data,
    );
    return response.data;
  }

  // Alerts endpoint - unwrap the response to return just the alerts array
  async getAlerts(): Promise<Alert[]> {
    const response = await this.client.get<AlertsResponse>("/alerts");
    return response.data.alerts;
  }

  // EONET events endpoints - unwrap the response to return just the events array
  async getEONETEvents(
    status: string = "open",
    limit: number = 10,
    days: number = 30,
  ): Promise<EONETEvent[]> {
    const response = await this.client.get<EONETResponse>("/events/eonet", {
      params: { status, limit, days },
    });
    return response.data.events;
  }

  async getEONETCategories(): Promise<EONETCategory[]> {
    const response = await this.client.get<EONETCategory[]>(
      "/events/eonet/categories",
    );
    return response.data;
  }

  // FIRMS hotspots endpoint - unwrap the response to return just the hotspots array
  async getFIRMSHotspots(limit: number = 50): Promise<FIRMSHotspot[]> {
    const response = await this.client.get<FIRMSResponse>("/events/firms", {
      params: { limit },
    });
    return response.data.hotspots;
  }

  // Copilot report endpoint
  async generateCopilotReport(
    riskAnalysis: RiskAnalysisResponse,
  ): Promise<CopilotReportResponse> {
    const requestData: CopilotReportRequest = {
      risk_analysis: riskAnalysis,
    };
    const response = await this.client.post<CopilotReportResponse>(
      "/copilot/report",
      requestData,
    );
    return response.data;
  }
}

// Create singleton instance
const apiClient = new ApiClient();

export default apiClient;

// Export individual methods for convenience with proper binding
export const getHealth = () => apiClient.getHealth();
export const getMissionInfo = () => apiClient.getMissionInfo();
export const submitSensorReading = (data: SensorReadingRequest) =>
  apiClient.submitSensorReading(data);
export const getLatestSensorReading = () => apiClient.getLatestSensorReading();
export const analyzeRisk = (data: RiskAnalysisRequest) =>
  apiClient.analyzeRisk(data);
export const getAlerts = () => apiClient.getAlerts();
export const getEONETEvents = (
  status: string = "open",
  limit: number = 10,
  days: number = 30,
) => apiClient.getEONETEvents(status, limit, days);
export const getEONETCategories = () => apiClient.getEONETCategories();
export const getFIRMSHotspots = (limit: number = 50) =>
  apiClient.getFIRMSHotspots(limit);
export const generateCopilotReport = (riskAnalysis: RiskAnalysisResponse) =>
  apiClient.generateCopilotReport(riskAnalysis);

// Made with Bob
