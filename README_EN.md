# FIAP - Faculdade de Informática e Administração Paulista

<p align="center">
  <a href="https://www.fiap.com.br/">
    <img src="docs/assets/logo-fiap.png" alt="FIAP" width="40%">
  </a>
</p>

<br>

# Astra Resilience Copilot

## Group name

**Astra Resilience Team**

## 👨‍🎓 Team members

- **Jonas Luis da Silva** — RM561465
- **Edson Henrique Felix Batista** — RM566321

## 👩‍🏫 Professors

### Tutor

- <a href="https://www.linkedin.com/company/inova-fusca">Lucas Gomes Moreira</a>

### Coordinator

- <a href="https://www.linkedin.com/company/inova-fusca">André Godoi Chiovato</a>

---

## 📜 Description

**Astra Resilience Copilot** is a Proof of Concept (POC) developed for **FIAP Global Solution 2026.1**, focused on the new space economy. The solution demonstrates how orbital data, edge sensors, automation, data analysis, and Generative AI can support fast and explainable decisions in environmental risk scenarios.

The platform integrates space-derived data from sources such as **NASA FIRMS**, for fire hotspots, and **NASA EONET**, for global natural events, with simulated ESP32/edge sensor readings. These signals are processed by a space-enabled risk engine that calculates an environmental score from 0 to 100 using fire hotspots, temperature, humidity, smoke level, connectivity, and battery conditions.

In addition to numerical scoring, the system generates **evidence and data provenance**, making it possible to trace which sources contributed to each alert. A **React + TypeScript** dashboard provides a mission-console interface with system status, space data ingestion, sensor simulation, risk analysis, hotspot map, evidence, alerts, and operational briefing.

The project also implements a **RAG Copilot**, which uses a local Markdown knowledge base to generate operational reports based on context, evidence, and recommendations. As a result, the system not only detects risk but also explains why the alert was generated and suggests practical actions for human review.

This POC answers the GS challenge by showing how advanced AI, automation, and computing can transform space data into practical decisions for disaster prevention, environmental resilience, and intelligent monitoring.

---

## 🚀 Problem addressed

Environmental events such as wildfires, droughts, storms, and floods require fast, reliable, and explainable monitoring. Satellites and space-data platforms generate large volumes of data, but these data need to be transformed into alerts, evidence, and operational recommendations.

Astra Resilience Copilot acts as an intelligent layer between space data, local sensors, and human users, working as a copilot for environmental risk analysis.

---

## 🧠 Technologies used

### Backend and APIs

- Python 3.11
- FastAPI
- Pydantic
- Uvicorn
- Requests
- Local JSON storage for the MVP

### Frontend

- React 18
- TypeScript
- Vite
- Axios
- Recharts
- Lucide React
- Custom CSS

### Space and environmental data

- NASA FIRMS, using a local hotspot sample to guarantee offline demonstration
- NASA EONET, with optional external API access
- Simulated ESP32/edge sensor

### AI, automation, and analytics

- Explainable rule-based spatial risk engine
- RAG Copilot with local Markdown knowledge base
- Data evidence and provenance
- Automatic alerts for HIGH/CRITICAL risks

---

## 🛰️ Implemented features

- NASA FIRMS hotspot ingestion through a local CSV sample.
- Optional NASA EONET integration.
- Edge/ESP32 sensor simulation with temperature, humidity, smoke, battery, and network status.
- Space-enabled risk engine with 0-100 score.
- Risk breakdown by FIRMS, sensor, EONET, smoke, and operational risk.
- Automatic alert generation.
- React-based mission console.
- FIRMS hotspot visual map.
- Evidence and provenance cards.
- RAG Copilot for operational briefings based on local knowledge.
- Windows PowerShell execution scripts and documentation.

---

## 🧩 Solution architecture

```text
User / Evaluator
        |
        v
React Mission Console (frontend/mission-console)
        |
        v
FastAPI Backend (src/backend)
        |
        +--> NASA FIRMS Local Sample (data/sample/firms_sample.csv)
        +--> Optional NASA EONET API (src/ingestion/eonet_client.py)
        +--> Edge Sensor Simulation (POST /sensor/readings)
        +--> Spatial Risk Engine (src/intelligence/spatial_risk_engine.py)
        +--> RAG Copilot (src/rag/copilot.py + data/knowledge/*.md)
        +--> Alerts and runtime JSON files (data/processed/)
```

---

## 📁 Folder structure

The organization follows the FIAP template logic, where `docs` stores documentation and screenshots, `src` stores source code, `data` stores datasets, and `README.md` explains the project.

```text
.
├── data/
│   ├── knowledge/
│   │   ├── astra_architecture.md
│   │   ├── eonet_notes.md
│   │   ├── firms_notes.md
│   │   ├── operational_guidelines.md
│   │   └── risk_methodology.md
│   ├── processed/
│   │   └── .gitkeep
│   └── sample/
│       └── firms_sample.csv
│
├── docs/
│   ├── architecture/
│   │   └── architecture-diagram.png
│   ├── screenshots/
│   │   ├── 01-mission-status.png
│   │   ├── 02-edge-and-space-data.png
│   │   ├── 03-risk-analysis.png
│   │   ├── 04-risk-breakdown.png
│   │   ├── 05-firms-hotspot-map.png
│   │   └── 06-evidence-alerts.png
│   ├── pdf/
│   │   └── entrega-global-solution.pdf
│   └── video/
│       └── video-link.md
│
├── frontend/
│   └── mission-console/
│       ├── src/
│       │   ├── api/
│       │   ├── components/
│       │   ├── styles/
│       │   └── types/
│       ├── package.json
│       └── vite.config.ts
│
├── src/
│   ├── backend/
│   │   ├── main.py
│   │   ├── models/
│   │   ├── routes/
│   │   └── utils/
│   ├── ingestion/
│   │   ├── eonet_client.py
│   │   └── firms_client.py
│   ├── intelligence/
│   │   └── spatial_risk_engine.py
│   └── rag/
│       └── copilot.py
│
├── .env.example
├── .gitignore
├── README.md
├── TESTING.md
├── requirements.txt
├── run.ps1
├── run_frontend.ps1
├── setup.ps1
├── test_copilot.ps1
└── test_spatial_risk.ps1
```

---

## 🖼️ Application screenshots

### Mission Status

![Mission Status](docs/screenshots/01-mission-status.png)

### Edge sensor and space data ingestion

![Edge and Space Data](docs/screenshots/02-edge-and-space-data.png)

### Space-enabled risk analysis

![Risk Analysis](docs/screenshots/03-risk-analysis.png)

### Risk breakdown

![Risk Breakdown](docs/screenshots/04-risk-breakdown.png)

### FIRMS hotspot map

![FIRMS Hotspot Map](docs/screenshots/05-firms-hotspot-map.png)

### Evidence, provenance and alerts

![Evidence and Alerts](docs/screenshots/06-evidence-alerts.png)

---

## 🔧 How to run the project

### Prerequisites

- Python 3.11 recommended.
- Node.js 18 or higher.
- npm.
- Windows PowerShell.

> Note: Python 3.13 may cause `pydantic-core` installation failures with the pinned versions in `requirements.txt`. For this POC, use Python 3.11.

### 1. Clone the repository

```powershell
git clone <REPOSITORY_URL>
cd "Global Solutions 2026"
```

### 2. Create and activate the Python virtual environment

```powershell
py -3.11 -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Run the FastAPI backend

Default port:

```powershell
python -m uvicorn src.backend.main:app --host 127.0.0.1 --port 8000
```

If port 8000 is busy:

```powershell
python -m uvicorn src.backend.main:app --host 127.0.0.1 --port 8002
```

API URL:

```text
http://127.0.0.1:8000
http://127.0.0.1:8000/docs
```

### 4. Run the React frontend

In another terminal:

```powershell
cd frontend/mission-console
npm install
npm run dev
```

Frontend URL:

```text
http://localhost:5173
```

If the backend is running on another port, update the **Backend URL** field in the React interface.

---

## ✅ Demo flow

1. Start the FastAPI backend.
2. Start the React frontend.
3. Check the mission status as online.
4. Submit a high-risk edge sensor reading.
5. Load FIRMS hotspots.
6. Optionally load EONET events.
7. Run the space-enabled risk analysis.
8. View risk score, level, and breakdown.
9. View the hotspot map.
10. View evidence and provenance.
11. Generate the Copilot operational briefing.
12. Show active alerts.

---

## 🧪 Main manual tests

### Health check

```powershell
Invoke-RestMethod "http://127.0.0.1:8000/health"
```

### FIRMS

```powershell
Invoke-RestMethod "http://127.0.0.1:8000/events/firms?limit=10"
```

### Edge sensor

```powershell
$body = @{
    device_id = "esp32_001"
    temperature = 39
    humidity = 18
    soil_moisture = 15
    smoke_level = 35
    battery_level = 35
    network_status = "degraded"
} | ConvertTo-Json

Invoke-RestMethod "http://127.0.0.1:8000/sensor/readings" -Method POST -ContentType "application/json" -Body $body
```

### Risk analysis

```powershell
$riskBody = @{
    area_of_interest = "Pantanal"
    sensor_data = @{
        temperature = 39
        humidity = 18
        soil_moisture = 15
        smoke_level = 35
    }
} | ConvertTo-Json -Depth 5

$risk = Invoke-RestMethod "http://127.0.0.1:8000/risk/analyze" -Method POST -ContentType "application/json" -Body $riskBody
$risk
```

### Copilot report

```powershell
$copilotBody = @{
    risk_analysis = $risk
} | ConvertTo-Json -Depth 10

Invoke-RestMethod "http://127.0.0.1:8000/copilot/report" -Method POST -ContentType "application/json" -Body $copilotBody
```

---

## 📎 Links and notes

- **GitHub repository:** [repository link](https://github.com/jonsilva91/Global-Solutions-2026).
- **Demo video:** [Demo Video](https://youtu.be/znjxI3e4TjI).
- **Final PDF:** `docs/pdf/entrega-global-solution.pdf`.

### Technical decisions

- FIRMS uses a local CSV sample to guarantee demo execution without an API key.
- EONET is optional and may fail if the external NASA API is unavailable.
- ESP32 is represented by an edge sensor simulation in the POC.
- The risk engine is rule-based to preserve explainability.
- The RAG Copilot uses a local Markdown knowledge base and deterministic fallback, without requiring a paid LLM key.
- The frontend uses React to deliver a product-like mission console experience.

---

## 🗃 Release history

- **1.0.0 - 2026-06-09**
  - Functional MVP with FastAPI backend, React Mission Console, FIRMS, optional EONET, simulated edge sensor, spatial risk engine, alerts, and RAG Copilot.

- **0.5.0 - 2026-06-09**
  - React frontend integration and risk visualization.

- **0.4.0 - 2026-06-09**
  - Space-enabled risk engine with FIRMS, EONET and sensor data.

- **0.3.0 - 2026-06-08**
  - NASA FIRMS and EONET ingestion.

- **0.2.0 - 2026-06-08**
  - Sensor, risk and alert endpoints.

- **0.1.0 - 2026-06-08**
  - Initial FastAPI backend structure.

---

## 📋 License

This is an academic project developed for FIAP Global Solution 2026.1.

README structure based on the FIAP template. Keep the template license according to institutional guidance.
