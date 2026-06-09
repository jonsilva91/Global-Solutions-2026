import { useEffect, useState } from "react";
import { Bell, RefreshCw } from "lucide-react";
import apiClient from "../api/client";
import type { Alert } from "../types/api";

export default function AlertsPanel() {
  const [alerts, setAlerts] = useState<Alert[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadAlerts();
  }, []);

  const loadAlerts = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await apiClient.getAlerts();
      setAlerts(data);
    } catch (err: any) {
      setError(err.response?.data?.detail || "Failed to load alerts");
      console.error("Alerts load error:", err);
    } finally {
      setLoading(false);
    }
  };

  const getSeverityClass = (severity: string) => {
    const sev = severity.toLowerCase();
    if (sev === "critical") return "severity-critical";
    if (sev === "high") return "severity-high";
    if (sev === "medium" || sev === "moderate") return "severity-medium";
    return "severity-low";
  };

  return (
    <div className="panel">
      <div className="panel-header">
        <div className="panel-title">
          <Bell className="panel-icon" />
          Active Alerts
        </div>
        <button
          className="btn btn-primary"
          onClick={loadAlerts}
          disabled={loading}
          style={{ padding: "6px 12px", fontSize: "12px" }}
        >
          <RefreshCw size={14} />
          Refresh
        </button>
      </div>
      <div className="panel-content">
        {loading && (
          <div className="loading">
            <div className="loading-spinner"></div>
            <p>Loading alerts...</p>
          </div>
        )}

        {error && <div className="error-message">{error}</div>}

        {!loading && !error && alerts.length === 0 && (
          <div className="empty-state">
            <Bell className="empty-state-icon" />
            <p className="empty-state-text">
              No active alerts at this time. System is operating normally.
            </p>
          </div>
        )}

        {!loading && !error && alerts.length > 0 && (
          <div style={{ overflowX: "auto" }}>
            <table className="alerts-table">
              <thead>
                <tr>
                  <th>Severity</th>
                  <th>Type</th>
                  <th>Message</th>
                  <th>Area</th>
                  <th>Risk Score</th>
                  <th>Status</th>
                  <th>Timestamp</th>
                </tr>
              </thead>
              <tbody>
                {alerts.map((alert) => (
                  <tr key={alert.alert_id}>
                    <td>
                      <span className={getSeverityClass(alert.severity)}>
                        {alert.severity.toUpperCase()}
                      </span>
                    </td>
                    <td
                      style={{ fontSize: "11px", color: "var(--text-muted)" }}
                    >
                      {alert.alert_type}
                    </td>
                    <td>{alert.message}</td>
                    <td>{alert.area}</td>
                    <td
                      style={{
                        fontSize: "14px",
                        fontWeight: "bold",
                        color:
                          alert.risk_score >= 80
                            ? "var(--accent-red)"
                            : alert.risk_score >= 50
                              ? "var(--accent-orange)"
                              : "var(--accent-yellow)",
                      }}
                    >
                      {alert.risk_score.toFixed(1)}
                    </td>
                    <td>
                      <span
                        style={{
                          fontSize: "11px",
                          padding: "2px 6px",
                          borderRadius: "3px",
                          background:
                            alert.status === "active"
                              ? "var(--accent-red)"
                              : "var(--bg-tertiary)",
                          color:
                            alert.status === "active"
                              ? "white"
                              : "var(--text-muted)",
                        }}
                      >
                        {alert.status}
                      </span>
                    </td>
                    <td
                      style={{ fontSize: "11px", color: "var(--text-muted)" }}
                    >
                      {new Date(alert.timestamp).toLocaleString()}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}

        {!loading && !error && alerts.length > 0 && (
          <div
            style={{
              marginTop: "12px",
              padding: "8px 12px",
              background: "var(--bg-tertiary)",
              borderRadius: "4px",
              fontSize: "11px",
              color: "var(--text-muted)",
              display: "flex",
              justifyContent: "space-between",
              alignItems: "center",
            }}
          >
            <span>
              Total Alerts:{" "}
              <strong style={{ color: "var(--text-primary)" }}>
                {alerts.length}
              </strong>
            </span>
            <span>
              Critical:{" "}
              <strong style={{ color: "var(--accent-red)" }}>
                {
                  alerts.filter((a) => a.severity.toLowerCase() === "critical")
                    .length
                }
              </strong>
            </span>
            <span>
              High:{" "}
              <strong style={{ color: "var(--accent-orange)" }}>
                {
                  alerts.filter((a) => a.severity.toLowerCase() === "high")
                    .length
                }
              </strong>
            </span>
          </div>
        )}
      </div>
    </div>
  );
}

// Made with Bob
