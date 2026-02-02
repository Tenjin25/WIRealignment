# Wisconsin Realignment Map - Retrofit Notes

## Overview
This project has been retrofitted from a Florida Political Realignment Map to a Wisconsin Political Realignment Map.

## Changes Made

### 1. **Page Title and Metadata**
- Changed title from "Florida Political Realignment Map (1978-2024)" to "Wisconsin Political Realignment Map (1978-2024)"
- Updated meta tags:
  - `og:title`: "FL Political Realignment Map" → "WI Political Realignment Map"
  - `og:description`: Updated to reference Wisconsin's political trends

### 2. **UI Text Updates**
- Main controls header: "Florida Election Contests" → "Wisconsin Election Contests"
- Statewide section: "Florida Statewide" → "Wisconsin Statewide"
- Comments updated to remove Florida-specific references (e.g., Miami-Dade)

### 3. **Research Findings Section**
Replaced Florida-specific findings with Wisconsin placeholders:
- **Milwaukee County** - Urban Democratic Stronghold
- **WOW Counties** (Waukesha, Ozaukee, Washington) - Republican Suburbs
- **Dane County** (Madison) - Growing Progressive Base
- **Statewide Patterns** - Highlighting Wisconsin swing counties:
  - Kenosha, Rock, Eau Claire, La Crosse, Brown (Green Bay), Racine

### 4. **Data File Paths**
Updated CONFIG object paths from Florida (FL/12) to Wisconsin (WI/55):
```javascript
counties: './data/tl_2020_55_county20.geojson'  // FIPS 55 = Wisconsin
districts: './data/wi_congressional_districts.geojson'
state_house: './data/wi_state_assembly_districts.geojson'  // Note: Assembly, not House
state_senate: './data/wi_state_senate_districts.geojson'
election: './data/wi_elections_aggregated.json'
// Similar updates for CSV files
```

### 5. **Map Configuration**
Updated map center and bounds for Wisconsin:
```javascript
center: [-89.5, 44.5]  // Central Wisconsin
zoom: 6.5
fitBounds: [[-92.9, 42.5], [-86.8, 47.1]]  // Wisconsin state boundaries
```

## Required Data Files
The following data files need to be created/obtained and placed in the `./data/` directory:

### GeoJSON Files (Boundaries)
- `tl_2020_55_county20.geojson` - Wisconsin county boundaries (TIGER/Line 2020)
- `wi_congressional_districts.geojson` - Wisconsin's 8 congressional districts
- `wi_state_assembly_districts.geojson` - Wisconsin's 99 State Assembly districts
- `wi_state_senate_districts.geojson` - Wisconsin's 33 State Senate districts

### Election Data
- `wi_elections_aggregated.json` - Historical election results (1978-2024)
  - Format should match the Florida JSON structure
  - Include: Presidential, Governor, US Senate, and state-level races

### District Information (CSV)
- `wi_congressional_districts.csv` - Congressional district metadata
- `wi_state_assembly_districts.csv` - Assembly district metadata
- `wi_state_senate_districts.csv` - Senate district metadata

## Data Sources

### Suggested Sources:
1. **County Boundaries**: [US Census TIGER/Line Shapefiles](https://www.census.gov/geographies/mapping-files/time-series/geo/tiger-line-file.html)
   - Filter for Wisconsin (FIPS 55), Counties 2020
   
2. **Congressional Districts**: [US Census Congressional District Shapefiles](https://www.census.gov/geographies/mapping-files/time-series/geo/carto-boundary-file.html)

3. **State Legislative Districts**: Wisconsin State Legislature or Wisconsin Elections Commission

4. **Election Results**: 
   - [Wisconsin Elections Commission](https://elections.wi.gov/)
   - Historical data may require compiling from multiple sources
   - MIT Election Data + Science Lab

## Wisconsin-Specific Notes

### Political Geography
- **72 counties** (vs Florida's 67)
- **8 congressional districts** (vs Florida's 28)
- **99 State Assembly districts** (vs Florida's 120 House districts)
- **33 State Senate districts** (vs Florida's 40 Senate districts)

### Key Regions
- **Southeast**: Milwaukee metro + WOW counties
- **Southwest**: Madison (Dane County) + college towns
- **Northeast**: Green Bay area (Brown County)
- **North**: Rural, sparsely populated
- **West**: Mississippi River counties (La Crosse, Eau Claire)

### Electoral Characteristics
- **No party registration** in Wisconsin (unlike Florida)
- **Same-day registration** affects turnout patterns
- **Swing state** - very competitive in presidential/statewide races
- Strong regional polarization (urban vs. rural)

## Next Steps

1. **Obtain Data Files**: Download/create all required GeoJSON, JSON, and CSV files
2. **Validate Data**: Ensure county names match between files
3. **Test Map**: Load index.html and verify boundaries display correctly
4. **Populate Election Data**: Add historical Wisconsin election results
5. **Refine Research Findings**: Replace placeholder text with actual Wisconsin data
6. **Update Styling**: Consider Wisconsin-specific color schemes if desired

## Folder Structure
```
WIRealignment/
├── index.html          (retrofitted main file)
├── data/               (needs to be populated)
│   ├── tl_2020_55_county20.geojson
│   ├── wi_congressional_districts.geojson
│   ├── wi_state_assembly_districts.geojson
│   ├── wi_state_senate_districts.geojson
│   ├── wi_elections_aggregated.json
│   ├── wi_congressional_districts.csv
│   ├── wi_state_assembly_districts.csv
│   └── wi_state_senate_districts.csv
├── script/             (for future scripts)
├── tools/              (for data processing tools)
└── RETROFIT_NOTES.md   (this file)
```

## Author
Retrofitted by: GitHub Copilot
Original Created by: Shamar Davis
Date: February 1, 2026
