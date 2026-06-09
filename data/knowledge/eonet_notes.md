# NASA EONET (Earth Observatory Natural Event Tracker)

## Overview

NASA EONET is a repository of natural events detected by various Earth-observing satellites and instruments. It provides a comprehensive view of ongoing environmental events worldwide.

## Event Categories

EONET tracks multiple event types:

- **Wildfires**: Active fire events
- **Severe Storms**: Hurricanes, cyclones, typhoons
- **Floods**: River flooding, coastal flooding
- **Volcanoes**: Volcanic eruptions and activity
- **Drought**: Extended dry periods
- **Dust and Haze**: Atmospheric particulate events
- **Sea and Lake Ice**: Ice coverage changes
- **Snow**: Significant snowfall events
- **Water Color**: Algal blooms, sediment plumes
- **Landslides**: Ground movement events
- **Manmade**: Oil spills, industrial incidents

## Data Structure

### Event Attributes

- **Event ID**: Unique identifier
- **Title**: Human-readable event name
- **Category**: Event type classification
- **Geometry**: Geographic coordinates (point or polygon)
- **Date**: Event start and end dates
- **Sources**: Contributing data sources (MODIS, VIIRS, etc.)

## Integration in Astra

### Data Ingestion

- EONET data fetched via REST API
- Stored in `data/processed/eonet_events.json`
- Filtered for relevant event categories (wildfires, storms, floods)

### Risk Contribution

EONET events contribute to risk assessment through:

1. **Event Proximity**: Distance from area of interest
2. **Event Category**: Different weights for different event types
3. **Event Status**: Active vs. closed events
4. **Multi-Source Validation**: Events confirmed by multiple satellites

### Event Interpretation

**Wildfire Events**

- Corroborate FIRMS hotspot detections
- Provide broader context of fire extent
- Track fire progression over time

**Severe Storm Events**

- Indicate potential for lightning-caused fires
- Affect fire behavior and spread
- Impact response operations

**Flood Events**

- May reduce immediate fire risk
- Affect accessibility for response teams
- Create secondary hazards

## Advantages Over FIRMS

- **Event-Level Tracking**: Groups related detections into coherent events
- **Multi-Source Integration**: Combines data from multiple satellites
- **Historical Context**: Tracks events from start to closure
- **Broader Coverage**: Includes non-fire environmental hazards

## Limitations

- **Coarser Temporal Resolution**: Not as real-time as FIRMS
- **Event Boundaries**: May not capture exact fire perimeter
- **Update Latency**: Events updated less frequently than raw detections
- **Category Overlap**: Some events may fit multiple categories

## Operational Use

EONET data is most valuable for:

- **Strategic Planning**: Understanding broader event context
- **Resource Allocation**: Identifying multiple concurrent threats
- **Trend Analysis**: Tracking event evolution over days/weeks
- **Situational Awareness**: Comprehensive environmental picture

## Data Source

- **Provider**: NASA Earth Science Division
- **API Endpoint**: https://eonet.gsfc.nasa.gov/api/v3/events
- **Update Frequency**: Variable by event type (hours to days)
- **Coverage**: Global
- **Access**: Public, no authentication required
