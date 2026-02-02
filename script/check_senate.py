import json

data = json.load(open(r'C:\Users\Shama\OneDrive\Documents\Course_Materials\CPT-236\Side_Projects\WIRealignment\data\wi_elections_aggregated.json'))

print('Years with US Senate data:')
for year in sorted(data['results_by_year'].keys()):
    senate_contests = data['results_by_year'][year].get('us_senate', {})
    if senate_contests:
        print(f'  {year}: {list(senate_contests.keys())}')
    else:
        print(f'  {year}: (none)')
