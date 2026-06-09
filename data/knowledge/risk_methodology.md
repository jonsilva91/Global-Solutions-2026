# Risk Assessment Methodology

## Overview

Astra Resilience Copilot uses a multi-source risk scoring system that combines satellite data, ground sensors, and spatial analysis to produce actionable risk assessments.

## Risk Score Calculation

Risk scores range from **0 to 100** and are calculated using weighted contributions from multiple data sources.

### Component Weights

1. **Sensor Data (40%)**
   - Temperature readings
   - Humidity levels
   - Soil moisture
   - Smoke detection

2. **FIRMS Hotspots (30%)**
   - Proximity to detected fires
   - Fire intensity (FRP)
   - Detection confidence
   - Number of nearby hotspots

3. **EONET Events (20%)**
   - Active wildfire events
   - Severe weather events
   - Event proximity and severity

4. **Spatial Context (10%)**
   - Terrain characteristics
   - Vegetation density
   - Historical fire patterns
   - Accessibility for response

## Risk Classification

### LOW (0-25)

**Conditions**: Normal environmental parameters, no immediate threats
**Indicators**:

- Temperature < 30°C
- Humidity > 40%
- Soil moisture > 30%
- No nearby fire detections
- No active EONET events

**Actions**:

- Continue routine monitoring
- Maintain standard readiness
- Update baseline measurements

### MODERATE (26-50)

**Conditions**: Elevated environmental stress, potential for escalation
**Indicators**:

- Temperature 30-35°C
- Humidity 25-40%
- Soil moisture 20-30%
- Distant fire detections (>50km)
- Minor EONET events

**Actions**:

- Increase monitoring frequency
- Review response plans
- Check equipment readiness
- Brief response teams

### HIGH (51-75)

**Conditions**: Significant risk factors present, prepare for response
**Indicators**:

- Temperature 35-40°C
- Humidity 15-25%
- Soil moisture 10-20%
- Nearby fire detections (10-50km)
- Active EONET wildfire events
- Smoke detection

**Actions**:

- Activate response teams
- Pre-position resources
- Establish communication protocols
- Coordinate with authorities
- Prepare evacuation plans

### CRITICAL (76-100)

**Conditions**: Immediate threat, action required now
**Indicators**:

- Temperature > 40°C
- Humidity < 15%
- Soil moisture < 10%
- Fire detections < 10km
- High FRP values (>100 MW)
- Multiple EONET events
- High smoke levels

**Actions**:

- Execute emergency response
- Initiate evacuations if needed
- Deploy all available resources
- Continuous monitoring
- Real-time coordination

## Evidence-Based Assessment

Every risk assessment includes:

### Evidence Collection

- Specific sensor readings that contributed to the score
- FIRMS hotspot detections with coordinates and FRP
- EONET events with categories and distances
- Timestamp of each data point

### Provenance Tracking

- Source files for all data
- Data ingestion timestamps
- Processing pipeline version
- API endpoints used

### Transparency

- Clear explanation of score components
- Breakdown by data source
- Confidence levels for each input
- Known limitations and uncertainties

## Temporal Considerations

Risk scores are **point-in-time assessments** and should be:

- Updated frequently (every 15-30 minutes)
- Compared to historical trends
- Validated against ground truth
- Adjusted for time-of-day patterns

## Spatial Considerations

Risk is **location-specific** and considers:

- Distance to threats (inverse square law)
- Terrain and wind patterns
- Vegetation fuel loads
- Water body proximity
- Infrastructure density

## Limitations and Uncertainties

### Data Gaps

- Satellite revisit times (12-hour gaps)
- Cloud cover obscuring detections
- Sensor network coverage
- Communication latencies

### Model Limitations

- Simplified weight assignments
- Linear scoring assumptions
- Limited historical calibration
- No predictive modeling (yet)

### Operational Constraints

- Response time requirements
- Resource availability
- Weather conditions
- Accessibility challenges

## Continuous Improvement

The risk methodology is designed to evolve:

- Incorporate feedback from field operations
- Refine weights based on outcomes
- Add new data sources as available
- Integrate machine learning models
- Validate against historical events

## Quality Assurance

Risk assessments undergo:

- Automated sanity checks
- Cross-validation between sources
- Outlier detection
- Confidence scoring
- Human review for critical alerts
