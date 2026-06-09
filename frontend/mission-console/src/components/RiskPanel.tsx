import { useState } from "react";
import { AlertTriangle, Play } from "lucide-react";
import apiClient from "../api/client";
import type { RiskAnalysisResponse } from "../types/api";

interface RiskPanelProps {
  areaOfInterest: string;
  onRiskAnalyzed: (result: RiskAnalysisResponse) => void;
}

export default function RiskPanel({
  areaOfInterest,
  onRiskAnalyzed,
}: RiskPanelProps) {
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState<{
    type: "success" | "error";
    text: string;
  } | null>(null);
  const [result, setResult] = useState<RiskAnalysisResponse | null>(null);

  const runAnalysis = async () => {
    setLoading(true);
    setMessage(null);

    try {
      // Get latest sensor reading for analysis
      const latestReading = await apiClient.getLatestSensorReading();

      const analysisResult = await apiClient.analyzeRisk({
        area_of_interest: areaOfInterest,
        sensor_data: {
          temperature: latestReading.temperature,
          humidity: latestReading.humidity,
          soil_moisture: latestReading.soil_moisture,
          smoke_level: latestReading.smoke_level,
        },
      });

      setResult(analysisResult);
      onRiskAnalyzed(analysisResult);
      setMessage({
        type: "success",
        text: "Risk analysis completed successfully!",
      });
    } catch (err: any) {
      setMessage({
        type: "error",
        text:
          err.response?.data?.detail ||
          "Failed to run risk analysis. Make sure you have submitted sensor data and loaded space data.",
      });
      console.error("Risk analysis error:", err);
    } finally {
      setLoading(false);
    }
  };

  const getRiskLevelClass = (level: string) => {
    const levelLower = level.toLowerCase();
    if (levelLower.includes("critical")) return "risk-critical";
    if (levelLower.includes("high")) return "risk-high";
    if (levelLower.includes("moderate")) return "risk-moderate";
    return "risk-low";
  };

  return (
    <div className="panel">
      <div className="panel-header">
        <div className="panel-title">
          <AlertTriangle className="panel-icon" />
          Space-Enabled Risk Analysis
        </div>
      </div>
      <div className="panel-content">
        <button
          className="btn btn-danger btn-full"
          onClick={runAnalysis}
          disabled={loading}
        >
          <Play size={16} />
          {loading ? "Analyzing..." : "Run Space-Enabled Risk Analysis"}
        </button>

        {message && (
          <div
            className={
              message.type === "success" ? "success-message" : "error-message"
            }
          >
            {message.text}
          </div>
        )}

        {result && (
          <div style={{ marginTop: "20px" }}>
            <div className="metric-grid">
              <div className="metric-card">
                <div className="metric-label">Risk Score</div>
                <div
                  className="metric-value"
                  style={{ color: "var(--accent-orange)" }}
                >
                  {result.risk_score.toFixed(1)}
                </div>
              </div>
              <div className="metric-card">
                <div className="metric-label">Total Risk Score</div>
                <div
                  className="metric-value"
                  style={{ color: "var(--accent-red)" }}
                >
                  {result.total_risk_score.toFixed(1)}
                </div>
              </div>
            </div>

            <div style={{ marginTop: "16px", textAlign: "center" }}>
              <div
                style={{
                  fontSize: "12px",
                  color: "var(--text-muted)",
                  marginBottom: "8px",
                }}
              >
                RISK LEVEL
              </div>
              <span
                className={`risk-badge ${getRiskLevelClass(result.risk_level)}`}
              >
                {result.risk_level}
              </span>
            </div>

            <div
              style={{
                marginTop: "16px",
                padding: "12px",
                background: "var(--bg-tertiary)",
                borderRadius: "6px",
                borderLeft: "3px solid var(--accent-yellow)",
              }}
            >
              <div
                style={{
                  fontSize: "11px",
                  color: "var(--text-muted)",
                  marginBottom: "6px",
                }}
              >
                RECOMMENDED ACTION
              </div>
              <div style={{ fontSize: "14px", color: "var(--text-primary)" }}>
                {result.recommended_action}
              </div>
            </div>

            <div style={{ marginTop: "16px" }}>
              <div
                style={{
                  fontSize: "11px",
                  color: "var(--text-muted)",
                  marginBottom: "8px",
                }}
              >
                AREA OF INTEREST
              </div>
              <div style={{ fontSize: "14px", color: "var(--accent-blue)" }}>
                {result.area_of_interest}
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

// Made with Bob
