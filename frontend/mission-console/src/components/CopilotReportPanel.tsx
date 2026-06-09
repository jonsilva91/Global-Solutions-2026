import React, { useState } from "react";
import { generateCopilotReport } from "../api/client";
import type { RiskAnalysisResponse, CopilotReportResponse } from "../types/api";

interface CopilotReportPanelProps {
  riskAnalysis: RiskAnalysisResponse | null;
}

export const CopilotReportPanel: React.FC<CopilotReportPanelProps> = ({
  riskAnalysis,
}) => {
  const [report, setReport] = useState<CopilotReportResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleGenerateReport = async () => {
    if (!riskAnalysis) {
      setError("Risk analysis required. Please run risk analysis first.");
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const reportData = await generateCopilotReport(riskAnalysis);
      setReport(reportData);
    } catch (err) {
      setError(
        err instanceof Error ? err.message : "Failed to generate report",
      );
      console.error("Error generating copilot report:", err);
    } finally {
      setLoading(false);
    }
  };

  const getRiskLevelColor = (level: string): string => {
    switch (level.toUpperCase()) {
      case "CRITICAL":
        return "#dc2626";
      case "HIGH":
        return "#ea580c";
      case "MODERATE":
        return "#f59e0b";
      case "LOW":
        return "#10b981";
      default:
        return "#6b7280";
    }
  };

  return (
    <div
      style={{
        backgroundColor: "#1e293b",
        padding: "20px",
        borderRadius: "8px",
        marginBottom: "20px",
      }}
    >
      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          marginBottom: "20px",
        }}
      >
        <h2 style={{ margin: 0, color: "#f1f5f9" }}>
          🤖 Copilot Operational Briefing
        </h2>
        <button
          onClick={handleGenerateReport}
          disabled={loading || !riskAnalysis}
          style={{
            padding: "10px 20px",
            backgroundColor: riskAnalysis ? "#3b82f6" : "#475569",
            color: "white",
            border: "none",
            borderRadius: "4px",
            cursor: riskAnalysis ? "pointer" : "not-allowed",
            fontSize: "14px",
            fontWeight: "bold",
          }}
        >
          {loading ? "Generating..." : "Generate Operational Briefing"}
        </button>
      </div>

      {error && (
        <div
          style={{
            backgroundColor: "#7f1d1d",
            color: "#fecaca",
            padding: "12px",
            borderRadius: "4px",
            marginBottom: "20px",
          }}
        >
          ⚠️ {error}
        </div>
      )}

      {!riskAnalysis && !report && (
        <div
          style={{
            backgroundColor: "#1e3a8a",
            color: "#93c5fd",
            padding: "16px",
            borderRadius: "4px",
            textAlign: "center",
          }}
        >
          ℹ️ Run a risk analysis first to generate an operational briefing
        </div>
      )}

      {report && (
        <div style={{ color: "#f1f5f9" }}>
          {/* Header */}
          <div
            style={{
              backgroundColor: "#0f172a",
              padding: "16px",
              borderRadius: "4px",
              marginBottom: "16px",
            }}
          >
            <h3 style={{ margin: "0 0 8px 0", fontSize: "18px" }}>
              {report.title}
            </h3>
            <div style={{ display: "flex", gap: "20px", fontSize: "14px" }}>
              <div>
                <strong>Area:</strong> {report.area_of_interest}
              </div>
              <div>
                <strong>Risk Level:</strong>{" "}
                <span
                  style={{
                    color: getRiskLevelColor(report.risk_level),
                    fontWeight: "bold",
                  }}
                >
                  {report.risk_level}
                </span>
              </div>
              <div>
                <strong>Risk Score:</strong> {report.risk_score.toFixed(1)}/100
              </div>
            </div>
            <div
              style={{ fontSize: "12px", color: "#94a3b8", marginTop: "8px" }}
            >
              Generated: {new Date(report.generated_at).toLocaleString()}
            </div>
          </div>

          {/* Executive Summary */}
          <div
            style={{
              backgroundColor: "#0f172a",
              padding: "16px",
              borderRadius: "4px",
              marginBottom: "16px",
            }}
          >
            <h4 style={{ margin: "0 0 12px 0", color: "#60a5fa" }}>
              📋 Executive Summary
            </h4>
            <p style={{ margin: 0, lineHeight: "1.6" }}>
              {report.executive_summary}
            </p>
          </div>

          {/* Evidence Summary */}
          {report.evidence_summary.length > 0 && (
            <div
              style={{
                backgroundColor: "#0f172a",
                padding: "16px",
                borderRadius: "4px",
                marginBottom: "16px",
              }}
            >
              <h4 style={{ margin: "0 0 12px 0", color: "#60a5fa" }}>
                🔍 Evidence Summary
              </h4>
              <ul style={{ margin: 0, paddingLeft: "20px" }}>
                {report.evidence_summary.map((evidence, index) => (
                  <li key={index} style={{ marginBottom: "8px" }}>
                    {evidence}
                  </li>
                ))}
              </ul>
            </div>
          )}

          {/* Recommended Actions */}
          {report.recommended_actions.length > 0 && (
            <div
              style={{
                backgroundColor: "#0f172a",
                padding: "16px",
                borderRadius: "4px",
                marginBottom: "16px",
              }}
            >
              <h4 style={{ margin: "0 0 12px 0", color: "#60a5fa" }}>
                ✅ Recommended Actions
              </h4>
              <ol style={{ margin: 0, paddingLeft: "20px" }}>
                {report.recommended_actions.map((action, index) => (
                  <li key={index} style={{ marginBottom: "8px" }}>
                    {action}
                  </li>
                ))}
              </ol>
            </div>
          )}

          {/* Limitations */}
          {report.limitations.length > 0 && (
            <div
              style={{
                backgroundColor: "#0f172a",
                padding: "16px",
                borderRadius: "4px",
                marginBottom: "16px",
              }}
            >
              <h4 style={{ margin: "0 0 12px 0", color: "#fbbf24" }}>
                ⚠️ Limitations & Uncertainties
              </h4>
              <ul style={{ margin: 0, paddingLeft: "20px", fontSize: "14px" }}>
                {report.limitations.map((limitation, index) => (
                  <li
                    key={index}
                    style={{ marginBottom: "6px", color: "#cbd5e1" }}
                  >
                    {limitation}
                  </li>
                ))}
              </ul>
            </div>
          )}

          {/* Source Provenance */}
          <div
            style={{
              backgroundColor: "#0f172a",
              padding: "16px",
              borderRadius: "4px",
            }}
          >
            <h4 style={{ margin: "0 0 12px 0", color: "#60a5fa" }}>
              📚 Source Provenance
            </h4>
            <div style={{ fontSize: "13px", color: "#cbd5e1" }}>
              <div style={{ marginBottom: "8px" }}>
                <strong>Data Sources:</strong>
              </div>
              <ul style={{ margin: 0, paddingLeft: "20px" }}>
                <li>FIRMS: {report.source_provenance.firms_file}</li>
                <li>EONET: {report.source_provenance.eonet_file}</li>
                <li>Sensors: {report.source_provenance.sensor_file}</li>
                {report.source_provenance.alerts_file && (
                  <li>Alerts: {report.source_provenance.alerts_file}</li>
                )}
              </ul>
              {report.source_provenance.knowledge_base.length > 0 && (
                <>
                  <div style={{ marginTop: "12px", marginBottom: "8px" }}>
                    <strong>Knowledge Base:</strong>
                  </div>
                  <ul style={{ margin: 0, paddingLeft: "20px" }}>
                    {report.source_provenance.knowledge_base.map(
                      (kb, index) => (
                        <li key={index}>{kb.split("/").pop()}</li>
                      ),
                    )}
                  </ul>
                </>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

// Made with Bob
