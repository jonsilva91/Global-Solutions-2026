import { MapPin } from "lucide-react";
import type { FIRMSHotspot } from "../types/api";

interface HotspotMapProps {
  hotspots: FIRMSHotspot[];
}

export default function HotspotMap({ hotspots }: HotspotMapProps) {
  if (hotspots.length === 0) {
    return (
      <div className="panel">
        <div className="panel-header">
          <div className="panel-title">
            <MapPin className="panel-icon" />
            FIRMS Hotspot Map
          </div>
        </div>
        <div className="panel-content">
          <div className="empty-state">
            <MapPin className="empty-state-icon" />
            <p className="empty-state-text">
              No hotspot data loaded yet. Load FIRMS data to visualize fire
              hotspots.
            </p>
          </div>
        </div>
      </div>
    );
  }

  // Calculate bounds for normalization
  const lats = hotspots.map((h) => h.latitude);
  const lons = hotspots.map((h) => h.longitude);
  const minLat = Math.min(...lats);
  const maxLat = Math.max(...lats);
  const minLon = Math.min(...lons);
  const maxLon = Math.max(...lons);

  // Normalize coordinates to 0-100% range for positioning
  const normalizeX = (lon: number) => {
    if (maxLon === minLon) return 50;
    return ((lon - minLon) / (maxLon - minLon)) * 90 + 5; // 5-95% range
  };

  const normalizeY = (lat: number) => {
    if (maxLat === minLat) return 50;
    return (1 - (lat - minLat) / (maxLat - minLat)) * 90 + 5; // Inverted for screen coords
  };

  // Get confidence color
  const getConfidenceColor = (confidence: string) => {
    const conf = confidence.toLowerCase();
    if (conf.includes("high") || conf === "h") return "#ea4335";
    if (conf.includes("nominal") || conf === "n") return "#ff9800";
    return "#fbbc04";
  };

  // Get brightness size
  const getBrightnessSize = (brightness: number) => {
    if (brightness > 350) return 12;
    if (brightness > 330) return 10;
    return 8;
  };

  return (
    <div className="panel">
      <div className="panel-header">
        <div className="panel-title">
          <MapPin className="panel-icon" />
          FIRMS Hotspot Map
        </div>
        <div style={{ fontSize: "12px", color: "var(--text-secondary)" }}>
          {hotspots.length} hotspots
        </div>
      </div>
      <div className="panel-content">
        <div className="hotspot-map">
          <div className="map-container">
            {hotspots.map((hotspot, idx) => {
              const x = normalizeX(hotspot.longitude);
              const y = normalizeY(hotspot.latitude);
              const size = getBrightnessSize(hotspot.brightness);
              const color = getConfidenceColor(hotspot.confidence);

              return (
                <div
                  key={idx}
                  className="hotspot-point"
                  style={{
                    left: `${x}%`,
                    top: `${y}%`,
                    width: `${size}px`,
                    height: `${size}px`,
                    background: color,
                    boxShadow: `0 0 ${size * 2}px ${color}`,
                  }}
                  title={`Lat: ${hotspot.latitude}, Lon: ${hotspot.longitude}, Brightness: ${hotspot.brightness}K, Confidence: ${hotspot.confidence}, Satellite: ${hotspot.satellite}`}
                />
              );
            })}
          </div>

          <div className="hotspot-legend">
            <div className="legend-item">
              <div
                className="legend-color"
                style={{ background: "#ea4335" }}
              ></div>
              <span>High Confidence</span>
            </div>
            <div className="legend-item">
              <div
                className="legend-color"
                style={{ background: "#ff9800" }}
              ></div>
              <span>Nominal Confidence</span>
            </div>
            <div className="legend-item">
              <div
                className="legend-color"
                style={{ background: "#fbbc04" }}
              ></div>
              <span>Low Confidence</span>
            </div>
          </div>
        </div>

        <div className="metric-grid" style={{ marginTop: "16px" }}>
          <div className="metric-card">
            <div className="metric-label">Total Hotspots</div>
            <div
              className="metric-value"
              style={{ color: "var(--accent-orange)" }}
            >
              {hotspots.length}
            </div>
          </div>
          <div className="metric-card">
            <div className="metric-label">Avg Brightness</div>
            <div
              className="metric-value"
              style={{ fontSize: "18px", color: "var(--accent-red)" }}
            >
              {(
                hotspots.reduce((sum, h) => sum + h.brightness, 0) /
                hotspots.length
              ).toFixed(0)}
              <span className="metric-unit">K</span>
            </div>
          </div>
          <div className="metric-card">
            <div className="metric-label">High Confidence</div>
            <div
              className="metric-value"
              style={{ fontSize: "18px", color: "var(--accent-red)" }}
            >
              {
                hotspots.filter(
                  (h) =>
                    h.confidence.toLowerCase().includes("high") ||
                    h.confidence === "h",
                ).length
              }
            </div>
          </div>
          <div className="metric-card">
            <div className="metric-label">Lat Range</div>
            <div className="metric-value" style={{ fontSize: "14px" }}>
              {minLat.toFixed(2)} to {maxLat.toFixed(2)}
            </div>
          </div>
          <div className="metric-card">
            <div className="metric-label">Lon Range</div>
            <div className="metric-value" style={{ fontSize: "14px" }}>
              {minLon.toFixed(2)} to {maxLon.toFixed(2)}
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
          <p>
            Hotspot visualization based on FIRMS satellite data. Point size
            indicates brightness temperature, color indicates detection
            confidence.
          </p>
        </div>
      </div>
    </div>
  );
}

// Made with Bob
