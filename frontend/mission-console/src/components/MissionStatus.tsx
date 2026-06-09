import { useEffect, useState } from "react";
import { Activity, CheckCircle, XCircle } from "lucide-react";
import apiClient from "../api/client";
import type { HealthResponse, MissionInfo } from "../types/api";

export default function MissionStatus() {
  const [health, setHealth] = useState<HealthResponse | null>(null);
  const [missionInfo, setMissionInfo] = useState<MissionInfo | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadStatus();
  }, []);

  const loadStatus = async () => {
    setLoading(true);
    setError(null);
    try {
      const [healthData, infoData] = await Promise.all([
        apiClient.getHealth(),
        apiClient.getMissionInfo(),
      ]);
      setHealth(healthData);
      setMissionInfo(infoData);
    } catch (err) {
      setError("Failed to connect to backend API");
      console.error("Status load error:", err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="panel">
        <div className="panel-header">
          <div className="panel-title">
            <Activity className="panel-icon" />
            Mission Status
          </div>
        </div>
        <div className="panel-content">
          <div className="loading">
            <div className="loading-spinner"></div>
            <p>Loading mission status...</p>
          </div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="panel">
        <div className="panel-header">
          <div className="panel-title">
            <Activity className="panel-icon" />
            Mission Status
          </div>
        </div>
        <div className="panel-content">
          <div className="error-message">{error}</div>
          <button
            className="btn btn-primary btn-full"
            onClick={loadStatus}
            style={{ marginTop: "12px" }}
          >
            Retry Connection
          </button>
        </div>
      </div>
    );
  }

  const isOnline = health?.status === "healthy";

  return (
    <div className="panel">
      <div className="panel-header">
        <div className="panel-title">
          <Activity className="panel-icon" />
          Mission Status
        </div>
        <span
          className={`status-indicator ${isOnline ? "status-online" : "status-offline"}`}
        >
          {isOnline ? <CheckCircle size={14} /> : <XCircle size={14} />}
          {isOnline ? "Online" : "Offline"}
        </span>
      </div>
      <div className="panel-content">
        <div className="metric-grid">
          <div className="metric-card">
            <div className="metric-label">API Status</div>
            <div
              className="metric-value"
              style={{
                color: isOnline ? "var(--accent-green)" : "var(--accent-red)",
              }}
            >
              {health?.status || "Unknown"}
            </div>
          </div>
          <div className="metric-card">
            <div className="metric-label">Version</div>
            <div className="metric-value" style={{ fontSize: "18px" }}>
              {health?.version || missionInfo?.version || "N/A"}
            </div>
          </div>
          <div className="metric-card">
            <div className="metric-label">Backend URL</div>
            <div
              className="metric-value"
              style={{ fontSize: "12px", wordBreak: "break-all" }}
            >
              {apiClient.getBaseURL()}
            </div>
          </div>
        </div>
        {missionInfo && (
          <div style={{ marginTop: "16px" }}>
            <h4
              style={{
                fontSize: "14px",
                color: "var(--text-primary)",
                marginBottom: "8px",
              }}
            >
              {missionInfo.project_name}
            </h4>
            <p
              style={{
                fontSize: "13px",
                color: "var(--text-secondary)",
                marginBottom: "12px",
              }}
            >
              {missionInfo.description}
            </p>
            {missionInfo.mission && (
              <p
                style={{
                  fontSize: "12px",
                  color: "var(--text-secondary)",
                  marginBottom: "12px",
                  fontStyle: "italic",
                }}
              >
                <strong>Mission:</strong> {missionInfo.mission}
              </p>
            )}
            {missionInfo.target_areas &&
              missionInfo.target_areas.length > 0 && (
                <p
                  style={{
                    fontSize: "12px",
                    color: "var(--text-secondary)",
                    marginBottom: "12px",
                  }}
                >
                  <strong>Target Areas:</strong>{" "}
                  {missionInfo.target_areas.join(", ")}
                </p>
              )}
            {missionInfo.main_components &&
              missionInfo.main_components.length > 0 && (
                <div>
                  <div
                    style={{
                      fontSize: "11px",
                      color: "var(--text-muted)",
                      textTransform: "uppercase",
                      marginBottom: "6px",
                    }}
                  >
                    Main Components
                  </div>
                  <div
                    style={{ display: "flex", flexWrap: "wrap", gap: "6px" }}
                  >
                    {missionInfo.main_components.map((component, idx) => (
                      <span
                        key={idx}
                        style={{
                          background: "var(--bg-tertiary)",
                          border: "1px solid var(--border-color)",
                          borderRadius: "4px",
                          padding: "4px 8px",
                          fontSize: "11px",
                          color: "var(--text-secondary)",
                        }}
                      >
                        {component}
                      </span>
                    ))}
                  </div>
                </div>
              )}
          </div>
        )}
        <button
          className="btn btn-primary btn-full"
          onClick={loadStatus}
          style={{ marginTop: "16px" }}
        >
          Refresh Status
        </button>
      </div>
    </div>
  );
}

// Made with Bob
