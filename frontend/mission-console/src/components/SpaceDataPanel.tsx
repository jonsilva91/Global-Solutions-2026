import { useState } from "react";
import { Satellite, Download } from "lucide-react";
import apiClient from "../api/client";
import type { FIRMSHotspot, EONETEvent } from "../types/api";

interface SpaceDataPanelProps {
  onFIRMSLoaded: (hotspots: FIRMSHotspot[]) => void;
  onEONETLoaded: (events: EONETEvent[]) => void;
}

export default function SpaceDataPanel({
  onFIRMSLoaded,
  onEONETLoaded,
}: SpaceDataPanelProps) {
  const [firmsLoading, setFirmsLoading] = useState(false);
  const [eonetLoading, setEonetLoading] = useState(false);
  const [firmsMessage, setFirmsMessage] = useState<{
    type: "success" | "error";
    text: string;
  } | null>(null);
  const [eonetMessage, setEonetMessage] = useState<{
    type: "success" | "error";
    text: string;
  } | null>(null);
  const [firmsCount, setFirmsCount] = useState<number>(0);
  const [eonetCount, setEonetCount] = useState<number>(0);

  const loadFIRMS = async () => {
    setFirmsLoading(true);
    setFirmsMessage(null);

    try {
      const hotspots = await apiClient.getFIRMSHotspots(50);
      setFirmsCount(hotspots.length);
      onFIRMSLoaded(hotspots);
      setFirmsMessage({
        type: "success",
        text: `Loaded ${hotspots.length} FIRMS hotspots successfully!`,
      });
    } catch (err: any) {
      setFirmsMessage({
        type: "error",
        text: err.response?.data?.detail || "Failed to load FIRMS hotspots",
      });
      console.error("FIRMS load error:", err);
    } finally {
      setFirmsLoading(false);
    }
  };

  const loadEONET = async () => {
    setEonetLoading(true);
    setEonetMessage(null);

    try {
      const events = await apiClient.getEONETEvents("open", 10, 30);
      setEonetCount(events.length);
      onEONETLoaded(events);
      setEonetMessage({
        type: "success",
        text: `Loaded ${events.length} EONET events successfully!`,
      });
    } catch (err: any) {
      // EONET might fail due to internet/API issues - show friendly warning
      const errorMsg =
        err.response?.data?.detail ||
        err.message ||
        "Failed to load EONET events";
      setEonetMessage({
        type: "error",
        text: `⚠️ ${errorMsg}. This is expected if NASA EONET API is unavailable. You can continue with FIRMS data.`,
      });
      console.warn("EONET load error (expected if offline):", err);
    } finally {
      setEonetLoading(false);
    }
  };

  return (
    <div className="panel">
      <div className="panel-header">
        <div className="panel-title">
          <Satellite className="panel-icon" />
          Space Data Ingestion
        </div>
      </div>
      <div className="panel-content">
        <div className="metric-grid" style={{ marginBottom: "16px" }}>
          <div className="metric-card">
            <div className="metric-label">FIRMS Hotspots</div>
            <div
              className="metric-value"
              style={{
                color:
                  firmsCount > 0 ? "var(--accent-orange)" : "var(--text-muted)",
              }}
            >
              {firmsCount}
            </div>
          </div>
          <div className="metric-card">
            <div className="metric-label">EONET Events</div>
            <div
              className="metric-value"
              style={{
                color:
                  eonetCount > 0 ? "var(--accent-blue)" : "var(--text-muted)",
              }}
            >
              {eonetCount}
            </div>
          </div>
        </div>

        <div className="btn-group">
          <button
            className="btn btn-warning"
            onClick={loadFIRMS}
            disabled={firmsLoading}
            style={{ flex: 1 }}
          >
            <Download size={16} />
            {firmsLoading ? "Loading..." : "Load FIRMS Hotspots"}
          </button>

          <button
            className="btn btn-primary"
            onClick={loadEONET}
            disabled={eonetLoading}
            style={{ flex: 1 }}
          >
            <Download size={16} />
            {eonetLoading ? "Loading..." : "Load EONET Events"}
          </button>
        </div>

        {firmsMessage && (
          <div
            className={
              firmsMessage.type === "success"
                ? "success-message"
                : "error-message"
            }
          >
            {firmsMessage.text}
          </div>
        )}

        {eonetMessage && (
          <div
            className={
              eonetMessage.type === "success"
                ? "success-message"
                : "error-message"
            }
          >
            {eonetMessage.text}
          </div>
        )}

        <div
          style={{
            marginTop: "16px",
            fontSize: "12px",
            color: "var(--text-muted)",
          }}
        >
          <p>
            <strong>FIRMS:</strong> NASA Fire Information for Resource
            Management System - Active fire hotspots from MODIS/VIIRS satellites
          </p>
          <p style={{ marginTop: "6px" }}>
            <strong>EONET:</strong> Earth Observatory Natural Event Tracker -
            Global natural events including wildfires, storms, and volcanic
            activity
          </p>
        </div>
      </div>
    </div>
  );
}

// Made with Bob
