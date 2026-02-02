# Wisconsin Political Realignment Interactive Map

> An interactive geospatial visualization exploring Wisconsin's dramatic political transformation from 2000-2024, featuring county-level presidential election results, demographic shifts, and regional realignment patterns.

![Wisconsin Election Map](https://img.shields.io/badge/Elections-2000--2024-blue) ![Data Source](https://img.shields.io/badge/Data-OpenElections-green) ![Status](https://img.shields.io/badge/Status-Active-success)

## 🎯 Project Overview

This project provides an interactive choropleth map and comprehensive analysis of Wisconsin's political realignment over 13 presidential election cycles (2000-2024). The visualization reveals how counties shifted between Democratic and Republican support, highlighting key regional patterns like the suburban WOW counties moderating, the Fox Valley BOW counties flipping Republican, and the Driftless Area's dramatic 40+ point swings.

### Key Features

- **Interactive County-Level Visualization**: Click any of Wisconsin's 72 counties to see detailed vote breakdowns across all years
- **Temporal Analysis**: Year-by-year slider to track political shifts over 24 years
- **Comprehensive Research Findings**: Curated narratives on Milwaukee County, WOW suburbs, Dane County, BOW industrial counties, and the Driftless Area
- **Accurate Margin Calculations**: Includes third-party votes in all margin calculations for precision matching between map and data
- **Responsive Design**: Fully functional sidebar with collapsible research findings and demographic context

## 🏛️ Political Context: Understanding Wisconsin's Realignment

### Urban-Rural Polarization: Democrats Confined to Cities

Wisconsin's political transformation over the past 24 years reflects a national pattern: **Democrats increasingly concentrated in urban centers while Republicans dominate rural areas**. This geographic sorting has fundamentally reshaped the state's electoral landscape.

**The Urban Democratic Strongholds:**
- **Milwaukee County** (population ~950,000): The state's largest city has shifted from D+20% (2000) to D+38% (2024). Milwaukee's African American population (40% of the county), Latino communities, and young urban professionals form a deep blue anchor. However, its population has stagnated while Republican rural areas grow in political influence.
- **Dane County** (Madison, population ~550,000): Home to the University of Wisconsin-Madison and state government, Dane has surged from D+18% (2000) to D+51% (2024). This 33-point leftward shift makes it Wisconsin's most Democratic county, driven by college-educated professionals, students, and the tech sector.

**The Suburban Battleground:**
The WOW counties (Waukesha, Ozaukee, Washington) surrounding Milwaukee tell a more complex story. While they remain Republican strongholds, college-educated suburban voters have moderated their conservatism:
- **Waukesha County**: R+35% (2004) → R+20% (2024) - a 15-point Democratic gain
- **Ozaukee County**: R+32% (2004) → R+10% (2024) - a 22-point swing, nearly competitive
- These shifts reflect nationwide trends of college-educated professionals moving left on social issues, even as they remain economically conservative.

**The Rural Republican Surge:**
Wisconsin's rural counties, particularly in the northern and western regions, have experienced dramatic Republican gains:
- **Driftless Area** (southwestern Wisconsin): Counties like **Lafayette** flipped from D+25% (2000) to R+20% (2024) - a stunning 45-point swing. This region, once dominated by family dairy farms and Norwegian/German immigrant communities with strong labor union ties, has been transformed by economic decline, aging populations, and cultural backlash.
- **BOW Counties** (Brown, Outagamie, Winnebago - Fox Valley): Industrial counties anchored by Green Bay and Appleton have shifted sharply rightward, with margins moving 20-30 points Republican since 2000. Manufacturing job losses, declining union membership, and white working-class political realignment drove this change.

The result: **Democrats win big in 2 counties (Milwaukee and Dane) but lose almost everywhere else.** In 2024, Joe Biden won only 10 of Wisconsin's 72 counties while losing the state. This geographic concentration creates a structural disadvantage in statewide races.

### The Scott Walker Era: Catalyst for Polarization

No single figure looms larger in Wisconsin's modern political realignment than **Scott Walker**, whose governorship (2011-2019) accelerated the state's partisan polarization and reshaped its political coalitions.

**2010: The Tea Party Wave**  
Walker's election as governor in November 2010 rode the Tea Party wave that swept Republicans into power nationwide. He defeated Milwaukee Mayor Tom Barrett by 5 points, promising fiscal conservatism and limited government. Republicans also captured both chambers of the state legislature, giving Walker unified control.

**2011: Act 10 and the Capitol Uprising**  
In February 2011, just weeks into his term, Walker introduced **Act 10 (Wisconsin Budget Repair Bill)**, which effectively eliminated collective bargaining rights for most public sector unions. The legislation:
- Prohibited unions from negotiating wages beyond inflation
- Required annual recertification votes
- Ended automatic dues collection
- Exempted police and firefighters (key Walker supporters)

The response was unprecedented: **100,000+ protesters occupied the Wisconsin State Capitol for weeks**, Democratic state senators fled to Illinois to deny quorum, and the nation watched Madison become ground zero for labor battles. The protests failed—Act 10 passed and was upheld by courts.

**2012: The Recall Election**  
Outraged Democrats collected 900,000 signatures to force a gubernatorial recall election, only the third in U.S. history. The June 2012 recall became the most expensive gubernatorial race in American history (over $80 million spent), with Walker defeating Tom Barrett again, this time by 7 points.

**Political Consequences:**  
Walker's victory in the recall had profound effects:
1. **Union Collapse**: Public sector union membership plummeted 50%+ as automatic dues ended. This decimated a key Democratic organizing infrastructure and funding source.
2. **Rural Consolidation**: Walker's aggressive conservatism and "Wisconsin is open for business" messaging solidified Republican gains in rural counties. The Driftless Area's swing from Obama (2008) to Trump (2016) was partially rooted in Walker-era realignment.
3. **FOX Valley Shift**: The BOW counties, with significant public sector employment, swung heavily Republican as Walker's anti-union message resonated with private sector workers who resented public employee benefits.
4. **Permanent Polarization**: The Act 10 fight created bitter partisan divides that persist today. Wisconsin politics became almost tribal, with few crossover voters.

**2016 and Beyond:**  
By the time Walker left office in 2019 (narrowly losing to Democrat Tony Evers), Wisconsin had transformed from a purple swing state into a deeply polarized battleground with razor-thin margins. His legacy includes:
- Republican legislative dominance through aggressive gerrymandering (2011 redistricting)
- Weakened labor unions unable to mobilize for Democrats
- Rural counties shifting 20-40 points Republican
- Urban counties shifting 15-30 points Democratic in backlash
- Suburban WOW counties moderating as college-educated voters rejected Walker's style

**The Trump Connection:**  
Walker's success with white working-class voters, particularly in the Fox Valley and northern Wisconsin, foreshadowed Trump's 2016 coalition. Many Obama-Walker voters became Trump voters, viewing both as anti-establishment figures willing to challenge "elites." Trump's narrow 22,748-vote Wisconsin victory in 2016 was built on the same rural and working-class base Walker cultivated.

Today, Wisconsin remains one of America's most evenly divided states, decided by margins under 1% in four of the last six presidential elections. But the **geographic sorting** is complete: Democrats dominate cities, Republicans dominate everywhere else, and suburbs hold the balance of power.

## 📊 Data Methodology

### Data Sources
- **2000-2022**: [OpenElections Wisconsin](https://github.com/openelections/openelections-data-wi) ward-level CSV files
- **2024**: Wisconsin Elections Commission county-level PDF reports (manually extracted)
- **Geographic Data**: US Census Bureau TIGER/Line shapefiles (2020)

### Calculation Methodology

**Critical**: All margin percentages include third-party votes in the total vote denominator:

```
Margin % = (Rep Votes - Dem Votes) / Total Votes * 100
```

Where `Total Votes = Dem Votes + Rep Votes + Other Votes`

This approach:
- ✅ Matches what voters see on the interactive map
- ✅ Provides more accurate representation of voter behavior
- ✅ Accounts for the impact of third-party candidates (especially significant in 2000, 2016)
- ✅ Consistent with Indiana realignment project methodology

**Example** (Waukesha County 2024):
- Republican: 162,768 votes
- Democrat: 108,478 votes
- Other: 4,541 votes
- Total: 275,787 votes
- Margin: R+19.69% (not R+20.02% if calculated on two-party vote)

### Data Processing Pipeline

1. **Extract** → PDF/CSV files parsed using `tabula-py` and `pandas`
2. **Aggregate** → Ward-level data rolled up to county totals by year
3. **Calculate** → Margins, percentages, and vote shares computed with third-party inclusion
4. **Validate** → Cross-referenced against official state totals
5. **Export** → Single JSON file (`wi_elections_aggregated.json`) consumed by map

## 🗂️ Project Structure

```
WIRealignment/
│
├── index.html                              # Main interactive map page
├── README.md                               # This file
├── RETROFIT_NOTES.md                       # Development history notes
│
├── data/                                   # Election data and geographic files
│   ├── wi_elections_aggregated.json        # Master election data file
│   ├── tl_2020_55_county20.geojson        # Wisconsin county boundaries
│   ├── 20001107__wi__general__ward.csv    # 2000 OpenElections data
│   ├── 20041102__wi__general__ward.csv    # 2004 OpenElections data
│   ├── ... (2002-2022 ward-level CSVs)
│   ├── 20241105__wi_general_county.csv    # 2024 extracted data
│   └── processed/                          # Intermediate processing files
│
├── script/                                 # Data extraction & processing
│   ├── README.md                           # Script-specific documentation
│   ├── requirements.txt                    # Python dependencies
│   ├── extract_election_data.py            # PDF extraction (2024 data)
│   ├── aggregate_elections.py              # Main aggregation script
│   ├── add_2024_data.py                    # Add 2024 to existing JSON
│   ├── convert_shapefile_to_geojson.py    # Geographic data conversion
│   ├── main.js                             # Map initialization logic
│   ├── map.js                              # Core mapping functions
│   └── common.js                           # Shared utilities
│
├── generate_research_findings.py          # Extract margins from JSON for HTML
├── recalculate_margins_with_third_parties.py  # Update JSON margins methodology
│
├── styles/                                 # CSS styling
└── .venv/                                  # Python virtual environment
```

## 🚀 Quick Start

### Prerequisites

- **Python 3.8+** (for data processing)
- **Java Runtime Environment** (for PDF extraction with tabula-py)
- Modern web browser (Chrome, Firefox, Edge)
- Text editor or IDE

### Installation

```powershell
# 1. Clone or download the project
cd WIRealignment

# 2. Create Python virtual environment (optional but recommended)
python -m venv .venv
.venv\Scripts\Activate.ps1

# 3. Install Python dependencies
pip install -r script/requirements.txt

# 4. Install Java (if not already installed)
winget install Oracle.JavaRuntimeEnvironment
```

### Running the Map

**Option 1: Simple Python Server (Recommended)**
```powershell
cd script
python serve.py
```
Then open browser to `http://localhost:8000`

**Option 2: Direct File Open**
- Simply open `index.html` in your web browser
- Note: Some browsers may have CORS restrictions with local files

### Viewing the Visualization

1. **Year Slider**: Use the year slider at the top to select 2000-2024
2. **County Interaction**: Click any county to see detailed vote breakdown
3. **Sidebar Navigation**: Scroll through research findings for curated insights
4. **Color Legend**: Counties colored by margin strength (deep blue = strong D, deep red = strong R)

## 🔧 Data Processing Workflows

### Adding New Election Data

When new Wisconsin election results become available:

```powershell
cd script

# 1. Extract from PDF (if needed)
python extract_election_data.py

# 2. Aggregate into master JSON
python aggregate_elections.py

# 3. Add to existing JSON (preserves previous years)
python add_2024_data.py

# 4. Verify output
python check_senate.py  # Validates data integrity
```

### Updating Margin Calculations

If you need to recalculate margins (e.g., switch between two-party vs total-vote methodology):

```powershell
# Recalculate all margins to include third parties
python recalculate_margins_with_third_parties.py

# Generate updated research findings with new margins
python generate_research_findings.py
```

### Geographic Data Updates

If you need to update county boundaries or add new shapefiles:

```powershell
cd script

# Convert shapefile to GeoJSON
python convert_shapefile_to_geojson.py

# Output: data/tl_2020_55_county20.geojson
```

## 📖 Key Research Findings

### Milwaukee County - Urban Democratic Anchor
**Trend**: D+20.49% (2000) → D+38.41% (2024)  
Wisconsin's largest county has become increasingly Democratic, with margins expanding by 18 points over 24 years. Growth in minority populations and urban-core density drive this trend.

### WOW Counties - Suburban Moderation
**Waukesha, Ozaukee, Washington** - Traditional Republican strongholds showing Democratic gains:
- **Waukesha**: R+35.29% → R+19.69% (16pt D shift)
- **Ozaukee**: R+32.41% → R+10.45% (22pt D shift)
- **Washington**: R+40.58% → R+36.21% (4pt D shift)

College-educated suburban voters shifting left, though all remain Republican.

### Dane County - Progressive Acceleration
**Trend**: D+28.58% (2000) → D+51.53% (2024)  
Madison metro area (UW-Madison, state government, tech sector) showing explosive Democratic growth. Second-largest county by population, rapidly expanding margins offset Republican rural dominance.

### BOW Counties - Fox Valley Realignment
**Brown, Outagamie, Winnebago** - Working-class industrial counties that flipped sharply Republican:
- **Brown**: D+9.15% (2008) → R+10.73% (2016) = 20pt swing
- **Outagamie**: D+11.60% (2008) → R+12.57% (2016) = 24pt swing
- **Winnebago**: D+11.66% (2008) → R+7.34% (2016) = 19pt swing

### Driftless Area - The Obama-Trump Transformation
**Crawford, Grant, Lafayette, Richland, Vernon, Iowa** - Historic Democratic farming region with 30-43pt swings toward Republicans between 2008-2024. Some of America's most dramatic political realignment, driven by working-class white voters in rural areas.

## 📈 Technical Details

### JSON Data Structure

`wi_elections_aggregated.json` format:
```json
{
  "results_by_year": {
    "2024": {
      "presidential": {
        "presidential_2024": {
          "results": {
            "Milwaukee": {
              "dem_votes": 317826,
              "rep_votes": 199329,
              "other_votes": 9713,
              "total_votes": 526868,
              "two_party_total": 517155,
              "margin": 118497,
              "margin_pct": 22.49
            }
          }
        }
      }
    }
  }
}
```

### Color Scale & Margin Ratings

Counties are colored based on margin strength using the following classification system:

| Rating | Margin Range | Color | 2024 County Examples |
|--------|--------------|-------|----------------------|
| **Annihilation Democratic** | D+40.00% or more | 🔵 Deep Blue `#08306b` | Dane (D+51.53%), Menominee (D+49.77%) |
| **Dominant Democratic** | D+30.00% to D+39.99% | 🔵 Blue `#08519c` | Milwaukee (D+38.41%), Douglas (D+30.15%) |
| **Stronghold Democratic** | D+20.00% to D+29.99% | 🔵 Medium Blue `#3182bd` | Bayfield (D+20.34%), Ashland (D+22.89%) |
| **Safe Democratic** | D+10.00% to D+19.99% | 🔵 Light Blue `#6baed6` | La Crosse (D+15.36%), Eau Claire (D+11.94%) |
| **Likely Democratic** | D+5.50% to D+9.99% | 🔵 Lighter Blue `#9ecae1` | Iowa (D+7.63%), Portage (D+6.28%) |
| **Lean Democratic** | D+1.00% to D+5.49% | 🔵 Pale Blue `#c6dbef` | Rock (D+3.92%), Kenosha (D+2.17%) |
| **Tilt Democratic** | D+0.50% to D+0.99% | 🔵 Very Pale Blue `#e1f5fe` | Rare in 2024; most counties polarized |
| **Tossup** | Less than ±0.50% | ⚪ Gray `#f7f7f7` | None in 2024 (closest: Sauk R+0.62%) |
| **Tilt Republican** | R+0.50% to R+0.99% | 🔴 Very Pale Red `#fee8c8` | Sauk (R+0.62%), Door (R+0.97%) |
| **Lean Republican** | R+1.00% to R+5.49% | 🔴 Pale Red `#fcae91` | Pierce (R+2.84%), Trempealeau (R+4.89%) |
| **Likely Republican** | R+5.50% to R+9.99% | 🔴 Light Red `#fb6a4a` | Vernon (R+7.78%), Winnebago (R+7.34%) |
| **Safe Republican** | R+10.00% to R+19.99% | 🔴 Medium Red `#ef3b2c` | Waukesha (R+19.69%), Brown (R+10.73%), Outagamie (R+12.57%) |
| **Stronghold Republican** | R+20.00% to R+29.99% | 🔴 Red `#cb181d` | Lafayette (R+20.23%), Shawano (R+24.15%) |
| **Dominant Republican** | R+30.00% to R+39.99% | 🔴 Dark Red `#a50f15` | Washington (R+36.21%), Calumet (R+31.47%) |
| **Annihilation Republican** | R+40.00% or more | 🔴 Deep Red `#67000d` | Waukesha (2004: R+35.29%), rural counties in past years |

**Note**: These 2024 examples show Wisconsin's political geography - urban/university counties (Dane, Milwaukee) strongly Democratic, suburban counties moderating (Waukesha from R+35% to R+20%), working-class counties (BOW) turned Republican, and rural counties (Driftless Area) showing massive rightward shifts.

### Map Technology Stack

- **Leaflet.js**: Interactive map rendering
- **D3.js**: Color scales and data binding
- **GeoJSON**: County boundary geometries
- **Vanilla JavaScript**: No heavy frameworks for performance
- **CSS Grid/Flexbox**: Responsive layout

## 🤝 Contributing

While this is an academic project, suggestions and improvements are welcome:

1. **Data Quality**: Report any vote count discrepancies
2. **Visualizations**: Suggest additional chart types or views
3. **Research**: Propose new county groupings or analysis themes
4. **Performance**: Optimize loading times or rendering

## 📝 Data Sources & Attribution

- **OpenElections Project**: Ward-level election results (2000-2022)  
  [github.com/openelections](https://github.com/openelections/openelections-data-wi)
  
- **Wisconsin Elections Commission**: Official 2024 results  
  [elections.wi.gov](https://elections.wi.gov/)
  
- **US Census Bureau**: County boundary shapefiles (TIGER/Line 2020)  
  [census.gov/geographies/mapping-files](https://www.census.gov/geographies/mapping-files.html)

## 📄 License

Educational use project for CPT-236 course. Data sources are public domain or used under their respective licenses.

## 👤 Author

**Shamar Davis**  
Course: CPT-236  
Institution: [Your Institution]  
Date: February 2026

## 🔍 Related Projects

- **Indiana Realignment Map**: Similar analysis for Indiana elections
- **North Carolina Map** (`NCMap.html`): NC political trends
- **Florida Map** (`FLMap.html`): FL electoral analysis

## 📞 Support & Questions

For questions about:
- **Data processing**: See `script/README.md`
- **Methodology**: Review this README's "Data Methodology" section
- **Troubleshooting**: Check script README troubleshooting section
- **General questions**: Review research findings in `index.html` sidebar

---

**Last Updated**: February 2026  
**Data Coverage**: 2000-2024 Presidential Elections  
**Counties**: All 72 Wisconsin counties  
**Version**: 1.0
