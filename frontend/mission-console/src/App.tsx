import { useState } from "react";
import { Settings, Satellite } from "lucide-react";
import apiClient from "./api/client";
import MissionStatus from "./components/MissionStatus";
import SensorPanel from "./components/SensorPanel";
import SpaceDataPanel from "./components/SpaceDataPanel";
import RiskPanel from "./components/RiskPanel";
import RiskBreakdownChart from "./components/RiskBreakdownChart";
import HotspotMap from "./components/HotspotMap";
import EvidencePanel from "./components/EvidencePanel";
import AlertsPanel from "./components/AlertsPanel";
import { CopilotReportPanel } from "./components/CopilotReportPanel";
import type {
  FIRMSHotspot,
  EONETEvent,
  RiskAnalysisResponse,
} from "./types/api";
import "./styles/app.css";

function App() {
  const [backendUrl, setBackendUrl] = useState("http://127.0.0.1:8000");
  const [areaOfInterest, setAreaOfInterest] = useState("Pantanal");
  const [firmsHotspots, setFirmsHotspots] = useState<FIRMSHotspot[]>([]);
  const [eonetEvents, setEonetEvents] = useState<EONETEvent[]>([]);
  const [riskResult, setRiskResult] = useState<RiskAnalysisResponse | null>(
    null,
  );

  const handleBackendUrlChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const newUrl = e.target.value;
    setBackendUrl(newUrl);
    apiClient.setBaseURL(newUrl);
  };

  const handleFIRMSLoaded = (hotspots: FIRMSHotspot[]) => {
    setFirmsHotspots(hotspots);
  };

  const handleEONETLoaded = (events: EONETEvent[]) => {
    setEonetEvents(events);
  };

  const handleRiskAnalyzed = (result: RiskAnalysisResponse) => {
    setRiskResult(result);
  };

  return (
    <div className="mission-console">
      {/* Header */}
      <div className="console-header">
        <div>
          <div className="console-title">Astra Resilience Copilot</div>
          <div className="console-subtitle">
            Mission Console — Space-Enabled Risk Monitoring
          </div>
        </div>
        <div className="backend-url-control">
          <Settings size={16} />
          <label>Backend URL:</label>
          <input
            type="text"
            value={backendUrl}
            onChange={handleBackendUrlChange}
            placeholder="http://127.0.0.1:8000"
          />
        </div>
      </div>

      {/* Mission Status */}
      <div className="console-grid">
        <MissionStatus />
      </div>

      {/* Area of Interest Control */}
      <div className="console-grid">
        <div className="panel">
          <div className="panel-header">
            <div className="panel-title">Area of Interest</div>
          </div>
          <div className="panel-content">
            <div className="form-group" style={{ marginBottom: 0 }}>
              <input
                type="text"
                className="form-input"
                value={areaOfInterest}
                onChange={(e) => setAreaOfInterest(e.target.value)}
                placeholder="Enter area of interest (e.g., Pantanal, Amazon)"
              />
            </div>
            <div
              style={{
                marginTop: "8px",
                fontSize: "11px",
                color: "var(--text-muted)",
              }}
            >
              Specify the geographic area for risk analysis and monitoring
            </div>
          </div>
        </div>
      </div>

      {/* Sensor and Space Data Panels */}
      <div className="console-grid">
        <SensorPanel />
        <SpaceDataPanel
          onFIRMSLoaded={handleFIRMSLoaded}
          onEONETLoaded={handleEONETLoaded}
        />
      </div>

      {/* EONET Events Summary */}
      {eonetEvents.length > 0 && (
        <div className="console-grid">
          <div className="panel">
            <div className="panel-header">
              <div className="panel-title">
                <Satellite className="panel-icon" />
                EONET Events Summary
              </div>
            </div>
            <div className="panel-content">
              <div className="metric-grid">
                <div className="metric-card">
                  <div className="metric-label">Total Events</div>
                  <div
                    className="metric-value"
                    style={{ color: "var(--accent-blue)" }}
                  >
                    {eonetEvents.length}
                  </div>
                </div>
                <div className="metric-card">
                  <div className="metric-label">Wildfires</div>
                  <div
                    className="metric-value"
                    style={{ fontSize: "18px", color: "var(--accent-red)" }}
                  >
                    {
                      eonetEvents.filter((e) => e.category === "Wildfires")
                        .length
                    }
                  </div>
                </div>
                <div className="metric-card">
                  <div className="metric-label">Open Status</div>
                  <div
                    className="metric-value"
                    style={{ fontSize: "18px", color: "var(--accent-orange)" }}
                  >
                    {eonetEvents.filter((e) => e.status === "open").length}
                  </div>
                </div>
              </div>
              <div
                style={{
                  marginTop: "12px",
                  fontSize: "11px",
                  color: "var(--text-muted)",
                }}
              >
                NASA EONET events loaded successfully. Data includes natural
                events tracked by Earth observation satellites.
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Risk Analysis Panel */}
      <div className="console-grid">
        <RiskPanel
          areaOfInterest={areaOfInterest}
          onRiskAnalyzed={handleRiskAnalyzed}
        />
      </div>

      {/* Copilot Operational Briefing */}
      <div className="console-grid">
        <div className="console-grid-full">
          <CopilotReportPanel riskAnalysis={riskResult} />
        </div>
      </div>

      {/* Risk Breakdown Chart */}
      {riskResult && (
        <div className="console-grid">
          <div className="console-grid-full">
            <RiskBreakdownChart breakdown={riskResult.risk_breakdown} />
          </div>
        </div>
      )}

      {/* Hotspot Map */}
      <div className="console-grid">
        <div className="console-grid-full">
          <HotspotMap hotspots={firmsHotspots} />
        </div>
      </div>

      {/* Evidence and Alerts */}
      <div className="console-grid">
        {riskResult && (
          <EvidencePanel
            evidence={riskResult.evidence}
            provenance={riskResult.provenance}
          />
        )}
        <AlertsPanel />
      </div>

      {/* Footer Info */}
      <div
        style={{
          marginTop: "20px",
          padding: "16px",
          textAlign: "center",
          fontSize: "11px",
          color: "var(--text-muted)",
          borderTop: "1px solid var(--border-color)",
        }}
      >
        <p>Astra Resilience Copilot — FIAP Global Solution 2026.1</p>
        <p style={{ marginTop: "4px" }}>
          Space-enabled environmental monitoring and disaster prevention system
        </p>
      </div>
    </div>
  );
}

export default App;

// Made with Bob
