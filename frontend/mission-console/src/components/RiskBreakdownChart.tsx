import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";
import { BarChart3 } from "lucide-react";
import type { RiskBreakdown } from "../types/api";

interface RiskBreakdownChartProps {
  breakdown: RiskBreakdown | null;
}

export default function RiskBreakdownChart({
  breakdown,
}: RiskBreakdownChartProps) {
  if (!breakdown) {
    return (
      <div className="panel">
        <div className="panel-header">
          <div className="panel-title">
            <BarChart3 className="panel-icon" />
            Risk Breakdown Analysis
          </div>
        </div>
        <div className="panel-content">
          <div className="empty-state">
            <BarChart3 className="empty-state-icon" />
            <p className="empty-state-text">
              No risk analysis data available yet. Run a risk analysis to see
              the breakdown.
            </p>
          </div>
        </div>
      </div>
    );
  }

  const data = [
    { name: "FIRMS Risk", value: breakdown.firms_risk, fill: "#ff9800" },
    { name: "Sensor Risk", value: breakdown.sensor_risk, fill: "#ea4335" },
    { name: "EONET Risk", value: breakdown.eonet_risk, fill: "#4a9eff" },
    { name: "Smoke Risk", value: breakdown.smoke_risk, fill: "#fbbc04" },
    {
      name: "Operational Risk",
      value: breakdown.operational_risk,
      fill: "#34a853",
    },
  ];

  return (
    <div className="panel">
      <div className="panel-header">
        <div className="panel-title">
          <BarChart3 className="panel-icon" />
          Risk Breakdown Analysis
        </div>
      </div>
      <div className="panel-content">
        <div className="chart-container">
          <ResponsiveContainer width="100%" height={300}>
            <BarChart
              data={data}
              margin={{ top: 20, right: 30, left: 20, bottom: 5 }}
            >
              <CartesianGrid strokeDasharray="3 3" stroke="#2a3142" />
              <XAxis
                dataKey="name"
                stroke="#9aa0a6"
                tick={{ fill: "#9aa0a6", fontSize: 12 }}
                angle={-15}
                textAnchor="end"
                height={80}
              />
              <YAxis
                stroke="#9aa0a6"
                tick={{ fill: "#9aa0a6", fontSize: 12 }}
                label={{
                  value: "Risk Score",
                  angle: -90,
                  position: "insideLeft",
                  fill: "#9aa0a6",
                }}
              />
              <Tooltip
                contentStyle={{
                  backgroundColor: "#1e2433",
                  border: "1px solid #2a3142",
                  borderRadius: "4px",
                  color: "#e8eaed",
                }}
                cursor={{ fill: "rgba(74, 158, 255, 0.1)" }}
              />
              <Legend wrapperStyle={{ color: "#9aa0a6", fontSize: "12px" }} />
              <Bar dataKey="value" fill="#4a9eff" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>

        <div className="metric-grid" style={{ marginTop: "16px" }}>
          <div className="metric-card">
            <div className="metric-label">FIRMS Risk</div>
            <div
              className="metric-value"
              style={{ fontSize: "18px", color: "#ff9800" }}
            >
              {breakdown.firms_risk.toFixed(1)}
            </div>
          </div>
          <div className="metric-card">
            <div className="metric-label">Sensor Risk</div>
            <div
              className="metric-value"
              style={{ fontSize: "18px", color: "#ea4335" }}
            >
              {breakdown.sensor_risk.toFixed(1)}
            </div>
          </div>
          <div className="metric-card">
            <div className="metric-label">EONET Risk</div>
            <div
              className="metric-value"
              style={{ fontSize: "18px", color: "#4a9eff" }}
            >
              {breakdown.eonet_risk.toFixed(1)}
            </div>
          </div>
          <div className="metric-card">
            <div className="metric-label">Smoke Risk</div>
            <div
              className="metric-value"
              style={{ fontSize: "18px", color: "#fbbc04" }}
            >
              {breakdown.smoke_risk.toFixed(1)}
            </div>
          </div>
          <div className="metric-card">
            <div className="metric-label">Operational Risk</div>
            <div
              className="metric-value"
              style={{ fontSize: "18px", color: "#34a853" }}
            >
              {breakdown.operational_risk.toFixed(1)}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

// Made with Bob
