import json

# Load the election data
with open('data/wi_elections_aggregated.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

def get_margin(county, year):
    """Get margin_pct and winner for a county in a given year."""
    year_str = str(year)
    if year_str not in data['results_by_year']:
        return None
    if 'presidential' not in data['results_by_year'][year_str]:
        return None
    
    president_contests = data['results_by_year'][year_str]['presidential']
    contest_keys = list(president_contests.keys())
    if not contest_keys:
        return None
    
    contest_key = contest_keys[0]
    contest_data = president_contests[contest_key]
    
    if 'results' not in contest_data:
        return None
    
    if county not in contest_data['results']:
        return None
    
    county_data = contest_data['results'][county]
    return {
        'margin_pct': county_data['margin_pct'],
        'winner': county_data['winner']
    }

def format_margin(margin_data):
    """Format margin as D+X.XX% or R+X.XX%"""
    if not margin_data:
        return "N/A"
    party = 'D' if margin_data['winner'] == 'DEM' else 'R'
    return f"{party}+{margin_data['margin_pct']:.2f}%"

# Print all data we need
print("ALL COUNTIES - EXACT VALUES FROM JSON")
print("="*60)

print("\nMILWAUKEE:")
for year in [2000, 2008, 2016, 2020, 2024]:
    m = get_margin('Milwaukee', year)
    print(f"  {year}: {format_margin(m)}")

print("\nWAUKESHA:")
for year in [2000, 2004, 2008, 2016, 2020, 2024]:
    m = get_margin('Waukesha', year)
    print(f"  {year}: {format_margin(m)}")

print("\nOZAUKEE:")
for year in [2000, 2004, 2008, 2016, 2020, 2024]:
    m = get_margin('Ozaukee', year)
    print(f"  {year}: {format_margin(m)}")

print("\nWASHINGTON:")
for year in [2000, 2004, 2008, 2016, 2020, 2024]:
    m = get_margin('Washington', year)
    print(f"  {year}: {format_margin(m)}")

print("\nDANE:")
for year in [2000, 2008, 2016, 2020, 2024]:
    m = get_margin('Dane', year)
    print(f"  {year}: {format_margin(m)}")

print("\nBOW COUNTIES:")
for county in ['Brown', 'Outagamie', 'Winnebago']:
    print(f"\n{county}:")
    for year in [2008, 2016, 2020, 2024]:
        m = get_margin(county, year)
        print(f"  {year}: {format_margin(m)}")

print("\nDRIFTLESS AREA:")
for county in ['Crawford', 'Grant', 'Lafayette', 'Richland', 'Vernon', 'Iowa']:
    print(f"\n{county}:")
    for year in [2008, 2016, 2024]:
        m = get_margin(county, year)
        print(f"  {year}: {format_margin(m)}")


print("\nWAUKESHA COUNTY")
print("="*60)
for year in [2000, 2004, 2008, 2016, 2020, 2024]:
    m = get_margin('Waukesha', year)
    print(f"{year}: {format_margin(m)}")

print("\nOZAUKEE COUNTY")
print("="*60)
for year in [2000, 2004, 2008, 2016, 2020, 2024]:
    m = get_margin('Ozaukee', year)
    print(f"{year}: {format_margin(m)}")

print("\nWASHINGTON COUNTY")
print("="*60)
for year in [2000, 2004, 2008, 2016, 2020, 2024]:
    m = get_margin('Washington', year)
    print(f"{year}: {format_margin(m)}")

print("\nDANE COUNTY")
print("="*60)
for year in [2000, 2008, 2016, 2020, 2024]:
    m = get_margin('Dane', year)
    print(f"{year}: {format_margin(m)}")

print("\nBOW COUNTIES")
print("="*60)
for county in ['Brown', 'Outagamie', 'Winnebago']:
    print(f"\n{county}:")
    for year in [2008, 2016]:
        m = get_margin(county, year)
        print(f"  {year}: {format_margin(m)}")

print("\nDRIFTLESS AREA")
print("="*60)
for county in ['Crawford', 'Grant', 'Lafayette', 'Richland', 'Vernon', 'Iowa']:
    print(f"\n{county}:")
    for year in [2008, 2016, 2024]:
        m = get_margin(county, year)
        print(f"  {year}: {format_margin(m)}")

