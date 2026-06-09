# NASA FIRMS (Fire Information for Resource Management System)

## Overview

NASA FIRMS provides near real-time active fire data from MODIS and VIIRS satellite instruments. This data is critical for detecting and monitoring wildfires globally.

## Data Characteristics

### Spatial Resolution

- **MODIS**: 1km resolution, twice-daily coverage
- **VIIRS**: 375m resolution, higher sensitivity to smaller fires

### Key Attributes

- **Latitude/Longitude**: Geographic coordinates of detected hotspot
- **Brightness**: Temperature in Kelvin (brightness_t31)
- **Confidence**: Detection confidence (low, nominal, high)
- **FRP (Fire Radiative Power)**: Measure of fire intensity in MW
- **Acquisition Date/Time**: When the satellite detected the hotspot

## Integration in Astra

### Data Ingestion

- FIRMS data is ingested from CSV files
- Stored in `data/processed/firms_hotspots.json`
- Updated periodically to capture new detections

### Risk Contribution

FIRMS hotspots contribute to risk assessment by:

1. **Proximity Analysis**: Distance from area of interest
2. **Intensity Evaluation**: FRP values indicate fire severity
3. **Confidence Weighting**: High-confidence detections weighted more heavily
4. **Temporal Patterns**: Recent detections indicate active fire fronts

### Interpretation Guidelines

**High FRP (>100 MW)**

- Indicates intense, rapidly spreading fire
- Requires immediate attention
- High risk to nearby areas

**Medium FRP (50-100 MW)**

- Moderate fire activity
- Monitor for escalation
- Prepare response resources

**Low FRP (<50 MW)**

- Small fires or smoldering
- Continue monitoring
- May indicate controlled burns

## Limitations

- **Cloud Cover**: Satellites cannot detect fires through thick clouds
- **Canopy Fires**: Dense forest canopy may obscure smaller fires
- **Temporal Gap**: 12-hour gaps between satellite passes
- **False Positives**: Industrial heat sources, gas flares may be detected

## Operational Use

FIRMS data is most effective when:

- Combined with ground sensor data
- Validated against other satellite sources (EONET)
- Analyzed with local weather conditions
- Integrated with historical fire patterns

## Data Source

- **Provider**: NASA LANCE (Land, Atmosphere Near real-time Capability for EOS)
- **Update Frequency**: Near real-time (3-hour latency)
- **Coverage**: Global
- **Access**: Public, no authentication required for standard products
