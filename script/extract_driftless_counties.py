"""
Extract Driftless Area county election data for research findings.
Generates HTML snippets for Milwaukee, WOW, Dane, BOW, and Driftless counties.
"""

import json
from typing import Dict, List, Tuple

def load_election_data(json_path: str) -> Dict:
    """Load Wisconsin election data from JSON file."""
    with open(json_path, 'r') as f:
        return json.load(f)

def get_county_margins(data: Dict, counties: List[str], years: List[int]) -> Dict:
    """
    Extract presidential margins for counties across years.
    Returns dict with structure: {county: {year: margin_pct}}
    """
    results = {}
    
    for county in counties:
        results[county] = {}
        for year in years:
            try:
                year_key = str(year)
                pres_key = f"presidential_{year}"
                county_data = data['results_by_year'][year_key]['presidential'][pres_key]['results'][county]
                margin = county_data['margin_pct']
                dem_votes = county_data['dem_votes']
                rep_votes = county_data['rep_votes']
                results[county][year] = {
                    'margin': margin,
                    'dem_votes': dem_votes,
                    'rep_votes': rep_votes,
                    'winner': 'D' if margin > 0 else 'R'
                }
            except KeyError:
                results[county][year] = None
    
    return results

def format_margin_html(margin: float, metric_class: str = "metric") -> str:
    """Format a margin as HTML metric span."""
    if margin is None:
        return "N/A"
    
    sign = "D+" if margin >= 0 else "R+"
    abs_margin = abs(margin)
    
    # Use red class for Republican margins
    css_class = "metric red" if margin < 0 else "metric"
    
    return f'<span class="{css_class}">{sign}{abs_margin:.2f}%</span>'

def generate_county_snippet(county_name: str, margins: Dict[int, Dict], years: List[int]) -> str:
    """Generate HTML snippet for a single county showing margin progression."""
    snippets = []
    
    for i, year in enumerate(years):
        if year in margins:
            data = margins[year]
            if data is None:
                continue
            margin = data['margin']
            html = format_margin_html(margin)
            
            # Format: "2000: D+20.49% → 2024: D+38.41%"
            if i == len(years) - 1:
                snippets.append(f"{year}: {html}")
            else:
                snippets.append(f"{year}: {html} → ")
    
    return "".join(snippets)

def generate_simple_snippet(county_name: str, margins: Dict[int, Dict]) -> str:
    """Generate simple 2000-2024 HTML snippet for a county."""
    if 2000 not in margins or 2024 not in margins:
        return "N/A"
    
    m2000 = margins[2000]
    m2024 = margins[2024]
    
    if m2000 is None or m2024 is None:
        return "N/A"
    
    html_2000 = format_margin_html(m2000['margin'])
    html_2024 = format_margin_html(m2024['margin'])
    
    return f"{html_2000} → {html_2024}"

def main():
    """Main extraction and formatting function."""
    data = load_election_data('data/wi_elections_aggregated.json')
    
    # Define county groups and their years
    all_years = [2000, 2004, 2008, 2012, 2016, 2020, 2024]
    groups = {
        'Milwaukee': {
            'counties': ['Milwaukee'],
            'years': all_years
        },
        'WOW Counties': {
            'counties': ['Waukesha', 'Ozaukee', 'Washington'],
            'years': all_years
        },
        'Dane': {
            'counties': ['Dane'],
            'years': all_years
        },
        'BOW Counties': {
            'counties': ['Brown', 'Outagamie', 'Winnebago'],
            'years': all_years
        },
        'Driftless Area': {
            'counties': ['Lafayette', 'Grant', 'Sauk', 'Crawford', 'Richland', 'Vernon'],
            'years': all_years
        },
        'Additional Surrounding Counties': {
            'counties': ['Rock', 'Racine', 'Kenosha', 'Eau Claire'],
            'years': all_years
        }
    }
    
    # Extract all data
    for group_name, group_info in groups.items():
        print(f"\n{'='*60}")
        print(f"{group_name.upper()}")
        print('='*60)
        
        counties = group_info['counties']
        years = group_info['years']
        
        margins_data = get_county_margins(data, counties, years)
        
        for county in counties:
            if county in margins_data:
                margins = margins_data[county]
                
                # Show raw data
                print(f"\n{county}:")
                for year in years:
                    if year in margins:
                        data_point = margins[year]
                        if data_point:
                            print(f"  {year}: D {data_point['dem_votes']:,} vs R {data_point['rep_votes']:,} = {data_point['margin']:+.2f}%")
                
                # Show full HTML snippet (all years)
                snippet = generate_county_snippet(county, margins, years)
                print(f"  HTML (full): {snippet}")
    
    # Generate side-by-side comparison for specific counties
    print(f"\n{'='*60}")
    print("WAUKESHA: 2000 vs 2024 COMPARISON (to strengthen argument)")
    print('='*60)
    
    waukesha_margins = get_county_margins(data, ['Waukesha'], [2000, 2024])['Waukesha']
    print("\n2000 to 2024 Shift Analysis:")
    margin_2000 = waukesha_margins[2000]['margin']
    margin_2024 = waukesha_margins[2024]['margin']
    shift = margin_2024 - margin_2000
    
    print(f"  2000: R+{abs(margin_2000):.2f}%")
    print(f"  2024: R+{abs(margin_2024):.2f}%")
    print(f"  Shift: {shift:+.2f} percentage points (toward Democrats)")
    print(f"\nHTML for research findings:")
    print(f"  <span class=\"metric red\">2000: R+{abs(margin_2000):.2f}%</span> → <span class=\"metric red\">2024: R+{abs(margin_2024):.2f}%</span>")
    
    # Driftless area dramatic shift
    print(f"\n{'='*60}")
    print("DRIFTLESS AREA: DRAMATIC SWINGS")
    print('='*60)
    
    driftless_counties = ['Lafayette', 'Grant', 'Sauk', 'Crawford', 'Richland', 'Vernon']
    driftless_margins = get_county_margins(data, driftless_counties, [2000, 2024])
    
    for county in driftless_counties:
        margins = driftless_margins[county]
        if 2000 in margins and 2024 in margins:
            m2000 = margins[2000]
            m2024 = margins[2024]
            if m2000 and m2024:
                shift = m2024['margin'] - m2000['margin']
                print(f"\n{county}:")
                print(f"  2000: {'+' if m2000['margin'] > 0 else ''}{m2000['margin']:.2f}%")
                print(f"  2024: {'+' if m2024['margin'] > 0 else ''}{m2024['margin']:.2f}%")
                print(f"  Swing: {shift:+.2f} points")
                print(f"  HTML: <span class=\"{'metric' if m2000['margin'] > 0 else 'metric red'}\">{('D+' if m2000['margin'] > 0 else 'R+')}{abs(m2000['margin']):.2f}%</span> → <span class=\"{'metric' if m2024['margin'] > 0 else 'metric red'}\">{('D+' if m2024['margin'] > 0 else 'R+')}{abs(m2024['margin']):.2f}%</span>")
    
    # La Crosse comparison
    print(f"\n{'='*60}")
    print("LA CROSSE: SWING COUNTY ANALYSIS")
    print('='*60)
    
    lacrosse_margins = get_county_margins(data, ['La Crosse'], [2000, 2008, 2016, 2024])['La Crosse']
    print("\nLa Crosse (Democratic-leaning but trending Republican):")
    for year in [2000, 2008, 2016, 2024]:
        if year in lacrosse_margins and lacrosse_margins[year]:
            m = lacrosse_margins[year]['margin']
            print(f"  {year}: {'+' if m > 0 else ''}{m:.2f}%")

if __name__ == '__main__':
    main()
