import { useState } from "react";
import { Cpu, Send } from "lucide-react";
import apiClient from "../api/client";
import type { SensorReadingRequest } from "../types/api";

export default function SensorPanel() {
  const [formData, setFormData] = useState<SensorReadingRequest>({
    device_id: "esp32_001",
    temperature: 39,
    humidity: 18,
    soil_moisture: 15,
    smoke_level: 35,
    battery_level: 35,
    network_status: "degraded",
  });
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState<{
    type: "success" | "error";
    text: string;
  } | null>(null);

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>,
  ) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: [
        "temperature",
        "humidity",
        "soil_moisture",
        "smoke_level",
        "battery_level",
      ].includes(name)
        ? parseFloat(value)
        : value,
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setMessage(null);

    try {
      const response = await apiClient.submitSensorReading(formData);
      setMessage({
        type: "success",
        text: response.message || "Sensor reading submitted successfully!",
      });
    } catch (err: any) {
      setMessage({
        type: "error",
        text: err.response?.data?.detail || "Failed to submit sensor reading",
      });
      console.error("Sensor submission error:", err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="panel">
      <div className="panel-header">
        <div className="panel-title">
          <Cpu className="panel-icon" />
          Edge Sensor Simulation
        </div>
      </div>
      <div className="panel-content">
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label className="form-label">Device ID</label>
            <input
              type="text"
              name="device_id"
              className="form-input"
              value={formData.device_id}
              onChange={handleChange}
              required
            />
          </div>

          <div className="form-grid">
            <div className="form-group">
              <label className="form-label">Temperature (°C)</label>
              <input
                type="number"
                name="temperature"
                className="form-input"
                value={formData.temperature}
                onChange={handleChange}
                step="0.1"
                required
              />
            </div>

            <div className="form-group">
              <label className="form-label">Humidity (%)</label>
              <input
                type="number"
                name="humidity"
                className="form-input"
                value={formData.humidity}
                onChange={handleChange}
                step="0.1"
                required
              />
            </div>

            <div className="form-group">
              <label className="form-label">Soil Moisture (%)</label>
              <input
                type="number"
                name="soil_moisture"
                className="form-input"
                value={formData.soil_moisture}
                onChange={handleChange}
                step="0.1"
                required
              />
            </div>

            <div className="form-group">
              <label className="form-label">Smoke Level (ppm)</label>
              <input
                type="number"
                name="smoke_level"
                className="form-input"
                value={formData.smoke_level}
                onChange={handleChange}
                step="0.1"
                required
              />
            </div>

            <div className="form-group">
              <label className="form-label">Battery Level (%)</label>
              <input
                type="number"
                name="battery_level"
                className="form-input"
                value={formData.battery_level}
                onChange={handleChange}
                step="1"
                min="0"
                max="100"
                required
              />
            </div>

            <div className="form-group">
              <label className="form-label">Network Status</label>
              <select
                name="network_status"
                className="form-select"
                value={formData.network_status}
                onChange={handleChange}
                required
              >
                <option value="online">Online</option>
                <option value="degraded">Degraded</option>
                <option value="offline">Offline</option>
              </select>
            </div>
          </div>

          <button
            type="submit"
            className="btn btn-success btn-full"
            disabled={loading}
          >
            <Send size={16} />
            {loading ? "Submitting..." : "Submit Sensor Reading"}
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
        </form>
      </div>
    </div>
  );
}

// Made with Bob
