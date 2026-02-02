"""
Aggregate Wisconsin election data from OpenElections CSV files into JSON format.

This script processes ward-level and county-level CSV files to create a comprehensive
JSON file with statewide election results (Presidential, US Senate, Governor, and other
statewide executive offices) aggregated by county.

Output format matches the structure required by the Wisconsin Realignment Map.
"""

import pandas as pd
import json
from pathlib import Path
from collections import defaultdict
import re

# Paths
DATA_DIR = Path(__file__).parent.parent / "data"
OUTPUT_FILE = DATA_DIR / "wi_elections_aggregated.json"

# Wisconsin has 72 counties
WI_COUNTY_COUNT = 72

# Statewide offices to include
STATEWIDE_OFFICES = {
    'President': 'presidential',
    'U.S. Senate': 'us_senate',
    'Senate': 'us_senate',  # OpenElections format
    'Governor': 'governor',
    'Attorney General': 'attorney_general',
    'Secretary of State': 'secretary_of_state',
    'State Treasurer': 'state_treasurer',
    'Lieutenant Governor': 'lieutenant_governor'
}

# Party mapping
PARTY_MAP = {
    'DEM': 'DEM',
    'REP': 'REP',
    'Democratic': 'DEM',
    'Republican': 'REP',
    'D': 'DEM',
    'R': 'REP',
    'DFL': 'DEM',  # Minnesota uses DFL, but Wisconsin might have some
    'GRN': 'GRN',
    'LIB': 'LIB',
    'IND': 'IND',
    'WGR': 'GRN',  # Wisconsin Green
    'CON': 'CON',
    'NP': 'NP'
}

# Competitiveness categories based on margin percentage
def get_competitiveness(margin_pct, winner):
    """Determine competitiveness category based on margin."""
    abs_margin = abs(margin_pct)
    
    if winner == 'DEM':
        if abs_margin >= 40:
            return {'category': 'Annihilation Democratic', 'party': 'Democratic', 'code': 'D_ANNIHILATION', 'color': '#08306b'}
        elif abs_margin >= 30:
            return {'category': 'Dominant Democratic', 'party': 'Democratic', 'code': 'D_DOMINANT', 'color': '#08519c'}
        elif abs_margin >= 20:
            return {'category': 'Stronghold Democratic', 'party': 'Democratic', 'code': 'D_STRONGHOLD', 'color': '#3182bd'}
        elif abs_margin >= 10:
            return {'category': 'Safe Democratic', 'party': 'Democratic', 'code': 'D_SAFE', 'color': '#6baed6'}
        elif abs_margin >= 5.5:
            return {'category': 'Likely Democratic', 'party': 'Democratic', 'code': 'D_LIKELY', 'color': '#9ecae1'}
        elif abs_margin >= 1:
            return {'category': 'Lean Democratic', 'party': 'Democratic', 'code': 'D_LEAN', 'color': '#c6dbef'}
        elif abs_margin >= 0.5:
            return {'category': 'Tilt Democratic', 'party': 'Democratic', 'code': 'D_TILT', 'color': '#e1f5fe'}
        else:
            return {'category': 'Tossup', 'party': 'Tossup', 'code': 'TOSSUP', 'color': '#f7f7f7'}
    elif winner == 'REP':
        if abs_margin >= 40:
            return {'category': 'Annihilation Republican', 'party': 'Republican', 'code': 'R_ANNIHILATION', 'color': '#67000d'}
        elif abs_margin >= 30:
            return {'category': 'Dominant Republican', 'party': 'Republican', 'code': 'R_DOMINANT', 'color': '#a50f15'}
        elif abs_margin >= 20:
            return {'category': 'Stronghold Republican', 'party': 'Republican', 'code': 'R_STRONGHOLD', 'color': '#cb181d'}
        elif abs_margin >= 10:
            return {'category': 'Safe Republican', 'party': 'Republican', 'code': 'R_SAFE', 'color': '#ef3b2c'}
        elif abs_margin >= 5.5:
            return {'category': 'Likely Republican', 'party': 'Republican', 'code': 'R_LIKELY', 'color': '#fb6a4a'}
        elif abs_margin >= 1:
            return {'category': 'Lean Republican', 'party': 'Republican', 'code': 'R_LEAN', 'color': '#fcae91'}
        elif abs_margin >= 0.5:
            return {'category': 'Tilt Republican', 'party': 'Republican', 'code': 'R_TILT', 'color': '#fee8c8'}
        else:
            return {'category': 'Tossup', 'party': 'Tossup', 'code': 'TOSSUP', 'color': '#f7f7f7'}
    else:
        return {'category': 'Tossup', 'party': 'Tossup', 'code': 'TOSSUP', 'color': '#f7f7f7'}


def normalize_party(party):
    """Normalize party codes."""
    if pd.isna(party) or party == '':
        return 'OTH'
    return PARTY_MAP.get(str(party).strip().upper(), 'OTH')


def normalize_county(county_name):
    """Normalize county names."""
    if pd.isna(county_name):
        return None
    county = str(county_name).strip()
    # Remove "County" suffix if present
    county = re.sub(r'\s+County$', '', county, flags=re.IGNORECASE)
    return county.title()


def extract_year_from_filename(filename):
    """Extract year from filename like '20001107__wi__general__ward.csv'."""
    match = re.match(r'^(\d{4})', filename)
    if match:
        return int(match.group(1))
    return None


def process_csv_file(file_path):
    """Process a single CSV file and extract statewide races."""
    print(f"  Processing {file_path.name}...")
    
    try:
        df = pd.read_csv(file_path)
    except Exception as e:
        print(f"    Error reading file: {e}")
        return None
    
    # Determine file format based on columns
    has_ward = 'ward' in df.columns
    
    # Filter for statewide offices only
    if 'office' not in df.columns:
        print(f"    No 'office' column found, skipping")
        return None
    
    # Keep only statewide races
    df = df[df['office'].isin(STATEWIDE_OFFICES.keys())].copy()
    
    if df.empty:
        print(f"    No statewide races found")
        return None
    
    print(f"    Found {len(df)} records for statewide races")
    return df


def aggregate_to_county_level(df, year):
    """Aggregate ward-level data to county level."""
    results = defaultdict(lambda: defaultdict(dict))
    
    # Group by office and county
    for office in df['office'].unique():
        office_df = df[df['office'] == office].copy()
        office_key = STATEWIDE_OFFICES.get(office, office.lower().replace(' ', '_'))
        
        # Get contest name
        contest_name = office
        contest_key = f"{office_key}_{year}"
        
        # Group by county and aggregate
        for county in office_df['county'].unique():
            county_normalized = normalize_county(county)
            if not county_normalized:
                continue
            
            county_df = office_df[office_df['county'] == county].copy()
            
            # Normalize parties
            county_df['party_norm'] = county_df['party'].apply(normalize_party)
            
            # Aggregate votes by party
            party_votes = county_df.groupby('party_norm')['votes'].sum().to_dict()
            
            # Get top candidates by party
            dem_candidates = county_df[county_df['party_norm'] == 'DEM']['candidate'].dropna()
            rep_candidates = county_df[county_df['party_norm'] == 'REP']['candidate'].dropna()
            
            dem_candidate = dem_candidates.iloc[0] if len(dem_candidates) > 0 else ''
            rep_candidate = rep_candidates.iloc[0] if len(rep_candidates) > 0 else ''
            
            # Calculate totals
            dem_votes = party_votes.get('DEM', 0)
            rep_votes = party_votes.get('REP', 0)
            other_votes = sum(v for k, v in party_votes.items() if k not in ['DEM', 'REP'])
            total_votes = sum(party_votes.values())
            two_party_total = dem_votes + rep_votes
            
            # Calculate margin
            if two_party_total > 0:
                margin = dem_votes - rep_votes
                margin_pct = round((margin / two_party_total) * 100, 2)
                
                if margin > 0:
                    winner = 'DEM'
                elif margin < 0:
                    winner = 'REP'
                else:
                    winner = 'TIE'
            else:
                margin = 0
                margin_pct = 0
                winner = 'N/A'
            
            # Get competitiveness
            competitiveness = get_competitiveness(margin_pct, winner)
            
            # Store result
            results[office_key][contest_key] = {
                'contest_name': contest_name,
                'results': results[office_key].get(contest_key, {}).get('results', {})
            }
            
            results[office_key][contest_key]['results'][county_normalized] = {
                'county': county_normalized,
                'contest': contest_name,
                'year': str(year),
                'dem_candidate': dem_candidate,
                'rep_candidate': rep_candidate,
                'dem_votes': int(dem_votes),
                'rep_votes': int(rep_votes),
                'other_votes': int(other_votes),
                'total_votes': int(total_votes),
                'two_party_total': int(two_party_total),
                'margin': int(margin),
                'margin_pct': float(margin_pct),
                'winner': winner,
                'competitiveness': competitiveness,
                'all_parties': {k: int(v) for k, v in party_votes.items()}
            }
    
    return dict(results)


def main():
    """Main aggregation function."""
    print("=" * 70)
    print("Wisconsin Election Data Aggregation")
    print("=" * 70)
    
    # Find all CSV files
    csv_files = sorted(DATA_DIR.glob('*.csv'))
    csv_files = [f for f in csv_files if '__wi__general' in f.name]
    
    print(f"\nFound {len(csv_files)} election CSV files")
    
    # Process each file
    all_results = defaultdict(lambda: defaultdict(dict))
    years_covered = set()
    
    for csv_file in csv_files:
        year = extract_year_from_filename(csv_file.name)
        if not year:
            print(f"\nSkipping {csv_file.name} - couldn't extract year")
            continue
        
        print(f"\n{year}:")
        years_covered.add(year)
        
        df = process_csv_file(csv_file)
        if df is None:
            continue
        
        # Aggregate to county level
        year_results = aggregate_to_county_level(df, year)
        
        # Merge into all_results
        for office_key, contests in year_results.items():
            all_results[year][office_key].update(contests)
    
    # Create final JSON structure
    output_data = {
        'metadata': {
            'state': 'Wisconsin',
            'state_code': 'WI',
            'total_counties': WI_COUNTY_COUNT,
            'years_covered': sorted(list(years_covered)),
            'data_source': 'OpenElections Wisconsin',
            'generated_date': '2026-02-01'
        },
        'results_by_year': dict(all_results)
    }
    
    # Write to file
    print("\n" + "=" * 70)
    print("Writing JSON file...")
    print("=" * 70)
    
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)
    
    print(f"\n✓ Aggregated data saved to: {OUTPUT_FILE}")
    print(f"\nSummary:")
    print(f"  Years covered: {min(years_covered)} - {max(years_covered)}")
    print(f"  Total years: {len(years_covered)}")
    print(f"  Years: {sorted(years_covered)}")
    
    # Count offices
    office_counts = defaultdict(int)
    for year_data in all_results.values():
        for office in year_data.keys():
            office_counts[office] += 1
    
    print(f"\n  Offices included:")
    for office, count in sorted(office_counts.items()):
        print(f"    {office}: {count} years")
    
    print("\n" + "=" * 70)
    print("COMPLETE!")
    print("=" * 70)


if __name__ == "__main__":
    main()
