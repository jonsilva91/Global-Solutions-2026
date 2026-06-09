# Astra Resilience Copilot Architecture

## Overview

Astra Resilience Copilot is a Proof of Concept for the FIAP Global Solution 2026.1, designed to provide real-time environmental risk assessment and operational intelligence for critical areas like the Pantanal wetlands.

## System Components

### Backend (FastAPI)

- **Mission Control API**: Core endpoints for system health, mission info, and operational status
- **Sensor Integration**: Real-time edge sensor data ingestion and storage
- **Risk Analysis Engine**: Multi-source risk scoring and classification
- **Alert System**: Automated alert generation based on risk thresholds
- **Space Data Integration**: NASA EONET and FIRMS data ingestion

### Frontend (React/Vite/TypeScript)

- **Mission Console**: Real-time operational dashboard
- **Risk Visualization**: Interactive risk breakdown charts and maps
- **Evidence Display**: Transparent provenance and evidence tracking
- **Alert Monitoring**: Real-time alert notifications

### Intelligence Layer

- **Spatial Risk Engine**: Geospatial analysis combining multiple data sources
- **RAG Copilot**: Operational report generation with knowledge retrieval

## Data Sources

1. **NASA FIRMS**: Fire hotspot detection from satellite thermal sensors
2. **NASA EONET**: Natural event tracking (wildfires, storms, floods)
3. **Edge Sensors**: Ground-truth environmental measurements (temperature, humidity, soil moisture, smoke)

## Risk Assessment Methodology

The system combines:

- Satellite-detected fire hotspots (FIRMS)
- Natural event proximity (EONET)
- Real-time sensor readings
- Historical patterns and knowledge base

Risk scores range from 0-100 and are classified as:

- **LOW** (0-25): Normal conditions
- **MODERATE** (26-50): Increased monitoring
- **HIGH** (51-75): Prepare response
- **CRITICAL** (76-100): Immediate action required

## Evidence and Provenance

All risk assessments include:

- **Evidence**: Specific data points contributing to the risk score
- **Provenance**: Source files, timestamps, and data lineage
- **Transparency**: Full traceability of decision-making process

## Operational Use

Designed for:

- Environmental monitoring agencies
- Emergency response teams
- Conservation organizations
- Agricultural operations in high-risk areas
