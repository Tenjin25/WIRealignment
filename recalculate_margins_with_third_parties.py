import json
from pathlib import Path

# Load the election data
input_file = Path('data/wi_elections_aggregated.json')
with open(input_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Counter for tracking updates
updates = 0
total_contests = 0

# Recalculate all margin_pct values to include third parties
for year in data['results_by_year']:
    for contest_type in data['results_by_year'][year]:
        for contest_name in data['results_by_year'][year][contest_type]:
            contest = data['results_by_year'][year][contest_type][contest_name]
            
            if 'results' in contest:
                for county in contest['results']:
                    county_data = contest['results'][county]
                    total_contests += 1
                    
                    # Recalculate margin_pct using total_votes instead of two_party_total
                    if county_data['total_votes'] > 0:
                        old_margin_pct = county_data['margin_pct']
                        new_margin_pct = (county_data['margin'] / county_data['total_votes']) * 100
                        
                        # Update the value
                        county_data['margin_pct'] = round(new_margin_pct, 2)
                        
                        if abs(old_margin_pct - new_margin_pct) > 0.01:
                            updates += 1

print(f"Processed {total_contests} county results")
print(f"Updated {updates} margin_pct values to include third parties")

# Save the updated data
output_file = Path('data/wi_elections_aggregated.json')
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2)

print(f"\nUpdated file saved to: {output_file}")

# Verify with Waukesha 2024
year = '2024'
if year in data['results_by_year']:
    if 'presidential' in data['results_by_year'][year]:
        pres = data['results_by_year'][year]['presidential']
        contest_key = list(pres.keys())[0]
        
        if 'Waukesha' in pres[contest_key]['results']:
            w = pres[contest_key]['results']['Waukesha']
            print(f"\nVerification - Waukesha 2024:")
            print(f"  New margin_pct: {abs(w['margin_pct']):.2f}% (should be 19.69%)")
