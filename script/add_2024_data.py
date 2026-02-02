"""
Add 2024 election data to the aggregated JSON file.

This reads the 2024 county-level CSV we created from the PDFs and adds it to the
main wi_elections_aggregated.json file.
"""

import json
import pandas as pd
from pathlib import Path
from collections import defaultdict

# Paths
DATA_DIR = Path(__file__).parent.parent / "data"
AGGREGATED_JSON = DATA_DIR / "wi_elections_aggregated.json"
CSV_2024 = DATA_DIR / "processed" / "wi_2024_general_combined.csv"

# Party mapping
PARTY_MAP = {
    'DEM': 'DEM',
    'REP': 'REP',
    'GRN': 'GRN',
    'LIB': 'LIB',
    'IND': 'IND',
    'WGR': 'GRN',
    'CON': 'CON',
    'NP': 'OTH'
}

# Office mapping
OFFICE_MAP = {
    'President': 'presidential',
    'U.S. Senate': 'us_senate'
}


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


def process_2024_data():
    """Process 2024 CSV data."""
    print("Loading 2024 data...")
    df = pd.read_csv(CSV_2024)
    
    results = defaultdict(lambda: defaultdict(dict))
    
    # Process each office
    for office in df['office'].unique():
        office_df = df[df['office'] == office].copy()
        office_key = OFFICE_MAP.get(office, office.lower().replace(' ', '_'))
        contest_key = f"{office_key}_2024"
        
        print(f"  Processing {office}...")
        
        # Process each county
        for county in office_df['county'].unique():
            county_df = office_df[office_df['county'] == county].copy()
            
            # Normalize parties and aggregate
            county_df['party_norm'] = county_df['party'].map(lambda x: PARTY_MAP.get(x, 'OTH'))
            
            # Aggregate by normalized party
            party_votes = county_df.groupby('party_norm')['votes'].sum().to_dict()
            
            # Get candidates
            dem_candidates = county_df[county_df['party_norm'] == 'DEM']['candidate']
            rep_candidates = county_df[county_df['party_norm'] == 'REP']['candidate']
            
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
                winner = 'DEM' if margin > 0 else ('REP' if margin < 0 else 'TIE')
            else:
                margin = 0
                margin_pct = 0
                winner = 'N/A'
            
            # Get competitiveness
            competitiveness = get_competitiveness(margin_pct, winner)
            
            # Store result
            if office_key not in results:
                results[office_key] = {}
            
            if contest_key not in results[office_key]:
                results[office_key][contest_key] = {
                    'contest_name': office,
                    'results': {}
                }
            
            results[office_key][contest_key]['results'][county] = {
                'county': county,
                'contest': office,
                'year': '2024',
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
    """Main function."""
    print("=" * 70)
    print("Adding 2024 Data to Aggregated JSON")
    print("=" * 70)
    
    # Load existing JSON
    print("\nLoading existing aggregated data...")
    with open(AGGREGATED_JSON, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Process 2024 data
    print("\nProcessing 2024 CSV data...")
    results_2024 = process_2024_data()
    
    # Add to JSON
    print("\nAdding 2024 to aggregated data...")
    data['results_by_year']['2024'] = results_2024
    
    # Update metadata
    years = sorted([int(y) for y in data['results_by_year'].keys()])
    data['metadata']['years_covered'] = years
    
    # Save updated JSON
    print("\nSaving updated JSON...")
    with open(AGGREGATED_JSON, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"\n✓ Updated file saved: {AGGREGATED_JSON}")
    print(f"\nSummary:")
    print(f"  Years covered: {min(years)} - {max(years)}")
    print(f"  Total years: {len(years)}")
    print(f"  2024 offices: {list(results_2024.keys())}")
    
    print("\n" + "=" * 70)
    print("COMPLETE!")
    print("=" * 70)


if __name__ == "__main__":
    main()
