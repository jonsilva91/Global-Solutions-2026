import { FileText, Database } from "lucide-react";
import type { Evidence } from "../types/api";

interface EvidencePanelProps {
  evidence: Evidence[];
  provenance: {
    firms_file: string;
    eonet_file: string;
    sensor_file: string;
  };
}

export default function EvidencePanel({
  evidence,
  provenance,
}: EvidencePanelProps) {
  const hasProvenance =
    provenance &&
    (provenance.firms_file || provenance.eonet_file || provenance.sensor_file);

  if (evidence.length === 0 && !hasProvenance) {
    return (
      <div className="panel">
        <div className="panel-header">
          <div className="panel-title">
            <FileText className="panel-icon" />
            Evidence & Provenance
          </div>
        </div>
        <div className="panel-content">
          <div className="empty-state">
            <FileText className="empty-state-icon" />
            <p className="empty-state-text">
              No evidence data available yet. Run a risk analysis to see
              evidence and data provenance.
            </p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="panel">
      <div className="panel-header">
        <div className="panel-title">
          <FileText className="panel-icon" />
          Evidence & Provenance
        </div>
      </div>
      <div className="panel-content">
        {evidence.length > 0 && (
          <div>
            <div
              style={{
                fontSize: "12px",
                color: "var(--text-muted)",
                marginBottom: "12px",
                textTransform: "uppercase",
                letterSpacing: "0.5px",
              }}
            >
              Evidence ({evidence.length})
            </div>
            <div className="evidence-grid">
              {evidence.map((item, idx) => (
                <div key={idx} className="evidence-card">
                  <div className="evidence-source">{item.source}</div>
                  <div className="evidence-description">{item.description}</div>
                  <div className="evidence-value">
                    {typeof item.value === "number"
                      ? item.value.toFixed(2)
                      : item.value}
                  </div>
                  <div className="evidence-timestamp">
                    {new Date(item.timestamp).toLocaleString()}
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {hasProvenance && (
          <div style={{ marginTop: evidence.length > 0 ? "24px" : "0" }}>
            <div
              style={{
                fontSize: "12px",
                color: "var(--text-muted)",
                marginBottom: "12px",
                textTransform: "uppercase",
                letterSpacing: "0.5px",
                display: "flex",
                alignItems: "center",
                gap: "6px",
              }}
            >
              <Database size={14} />
              Data Provenance
            </div>
            <ul className="provenance-list">
              {Object.entries(provenance).map(([key, value]) => {
                if (!value) return null;
                return (
                  <li key={key} className="provenance-item">
                    <strong>{key.replace(/_/g, " ").toUpperCase()}:</strong>{" "}
                    {value}
                  </li>
                );
              })}
            </ul>
          </div>
        )}

        <div
          style={{
            marginTop: "16px",
            padding: "12px",
            background: "var(--bg-tertiary)",
            borderRadius: "6px",
            fontSize: "11px",
            color: "var(--text-muted)",
          }}
        >
          <p>
            <strong>Evidence:</strong> Individual data points and observations
            that contribute to the risk assessment.
          </p>
          <p style={{ marginTop: "6px" }}>
            <strong>Provenance:</strong> Data lineage showing the source files
            and processing steps used in the analysis.
          </p>
        </div>
      </div>
    </div>
  );
}

// Made with Bob
