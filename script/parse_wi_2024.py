"""
Extract Wisconsin 2024 election data from PDF reports and create combined CSV.

This parses the specific format of Wisconsin Elections Commission PDF reports.
"""

import fitz
import pandas as pd
import re
from pathlib import Path

# Paths
DATA_DIR = Path(__file__).parent.parent / "data"
OUTPUT_DIR = DATA_DIR / "processed"
OUTPUT_DIR.mkdir(exist_ok=True)

# Input PDF files
POTUS_PDF = DATA_DIR / "County by County Report_POTUS.pdf"
SENATE_PDF = DATA_DIR / "County by County Report_US Senate_1.pdf"

# Wisconsin counties
WI_COUNTIES = [
    'ADAMS', 'ASHLAND', 'BARRON', 'BAYFIELD', 'BROWN', 'BUFFALO', 'BURNETT',
    'CALUMET', 'CHIPPEWA', 'CLARK', 'COLUMBIA', 'CRAWFORD', 'DANE', 'DODGE',
    'DOOR', 'DOUGLAS', 'DUNN', 'EAU CLAIRE', 'FLORENCE', 'FOND DU LAC', 'FOREST',
    'GRANT', 'GREEN', 'GREEN LAKE', 'IOWA', 'IRON', 'JACKSON', 'JEFFERSON',
    'JUNEAU', 'KENOSHA', 'KEWAUNEE', 'LA CROSSE', 'LAFAYETTE', 'LANGLADE',
    'LINCOLN', 'MANITOWOC', 'MARATHON', 'MARINETTE', 'MARQUETTE', 'MENOMINEE',
    'MILWAUKEE', 'MONROE', 'OCONTO', 'ONEIDA', 'OUTAGAMIE', 'OZAUKEE', 'PEPIN',
    'PIERCE', 'POLK', 'PORTAGE', 'PRICE', 'RACINE', 'RICHLAND', 'ROCK', 'RUSK',
    'ST. CROIX', 'SAUK', 'SAWYER', 'SHAWANO', 'SHEBOYGAN', 'TAYLOR', 'TREMPEALEAU',
    'VERNON', 'VILAS', 'WALWORTH', 'WASHBURN', 'WASHINGTON', 'WAUKESHA', 'WAUPACA',
    'WAUSHARA', 'WINNEBAGO', 'WOOD'
]


def parse_presidential_pdf(pdf_path):
    """Parse the presidential election PDF."""
    print(f"\nParsing {pdf_path.name}...")
    
    doc = fitz.open(pdf_path)
    records = []
    
    # Candidate info from the PDF structure
    # Based on the column headers: DEM, REP, CON, LIB, WGR, NP...
    candidates = [
        {'name': 'Kamala D. Harris', 'party': 'DEM'},
        {'name': 'Donald J. Trump', 'party': 'REP'},
        {'name': 'Randall Terry', 'party': 'CON'},
        {'name': 'Chase Russell Oliver', 'party': 'LIB'},
        {'name': 'Jill Stein', 'party': 'WGR'},
        {'name': 'Claudia De la Cruz', 'party': 'NP'},
        {'name': 'Cornel West', 'party': 'NP'},
        {'name': 'Robert F. Kennedy Jr.', 'party': 'NP'},
        {'name': 'Peter Sonski', 'party': 'NP'},
        {'name': 'Cherunda Lynn Fox', 'party': 'NP'},
    ]
    
    for page_num in range(len(doc)):
        page = doc[page_num]
        text = page.get_text()
        lines = text.split('\n')
        
        # Parse line by line, looking for county names followed by numbers
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            
            # Check if this line is a county name
            county_match = None
            for county in WI_COUNTIES:
                if line == county:  # Exact match since county is on its own line
                    county_match = county
                    break
            
            if county_match:
                # Next lines should contain the vote data
                # Collect all numbers from the next few lines
                vote_data = []
                j = i + 1
                while j < len(lines) and j < i + 15:  # Look ahead up to 15 lines
                    next_line = lines[j].strip()
                    # Stop if we hit another county
                    if next_line in WI_COUNTIES:
                        break
                    # Extract numbers
                    numbers = re.findall(r'\d[\d,]*', next_line)
                    for num_str in numbers:
                        try:
                            vote_data.append(int(num_str.replace(',', '')))
                        except ValueError:
                            pass
                    j += 1
                    # Stop after collecting enough data
                    if len(vote_data) >= 11:  # Total + 10 candidates
                        break
                
                # Skip total votes (first number) and match remaining to candidates
                if len(vote_data) > 1:
                    vote_counts = vote_data[1:]
                    for idx, candidate in enumerate(candidates):
                        if idx < len(vote_counts):
                            records.append({
                                'county': county_match.title(),
                                'office': 'President',
                                'district': '',
                                'party': candidate['party'],
                                'candidate': candidate['name'],
                                'votes': vote_counts[idx]
                            })
            
            i += 1
    
    doc.close()
    
    df = pd.DataFrame(records)
    print(f"  Extracted {len(df)} records")
    
    if not df.empty:
        print(f"  Counties: {df['county'].nunique()}")
        print(f"  Candidates: {df['candidate'].nunique()}")
    else:
        print("  Warning: No data extracted - check PDF structure")
    
    return df


def parse_senate_pdf(pdf_path):
    """Parse the U.S. Senate election PDF."""
    print(f"\nParsing {pdf_path.name}...")
    
    doc = fitz.open(pdf_path)
    records = []
    
    # Get candidate names from the PDF
    first_page = doc[0].get_text()
    
    # Look for candidate names in header
    candidates = []
    if 'Baldwin' in first_page and 'Hovde' in first_page:
        candidates = [
            {'name': 'Tammy Baldwin', 'party': 'DEM'},
            {'name': 'Eric Hovde', 'party': 'REP'},
        ]
    
    # Check for third candidate
    if 'Vogel' in first_page:
        candidates.append({'name': 'Phil Anderson', 'party': 'LIB'})
    
    print(f"  Detected candidates: {[c['name'] for c in candidates]}")
    
    for page_num in range(len(doc)):
        page = doc[page_num]
        text = page.get_text()
        lines = text.split('\n')
        
        # Parse line by line, looking for county names followed by numbers
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            
            # Check if this line is exactly a county name
            county_match = None
            for county in WI_COUNTIES:
                if line == county:
                    county_match = county
                    break
            
            if county_match:
                # Next lines should contain the vote data
                vote_data = []
                j = i + 1
                while j < len(lines) and j < i + 10:
                    next_line = lines[j].strip()
                    if next_line in WI_COUNTIES:
                        break
                    numbers = re.findall(r'\d[\d,]*', next_line)
                    for num_str in numbers:
                        try:
                            vote_data.append(int(num_str.replace(',', '')))
                        except ValueError:
                            pass
                    j += 1
                    if len(vote_data) >= len(candidates) + 1:
                        break
                
                # Skip total votes and match to candidates
                if len(vote_data) > 1:
                    vote_counts = vote_data[1:]
                    for idx, candidate in enumerate(candidates):
                        if idx < len(vote_counts):
                            records.append({
                                'county': county_match.title(),
                                'office': 'U.S. Senate',
                                'district': '',
                                'party': candidate['party'],
                                'candidate': candidate['name'],
                                'votes': vote_counts[idx]
                            })
            
            i += 1
    
    doc.close()
    
    df = pd.DataFrame(records)
    print(f"  Extracted {len(df)} records")
    print(f"  Counties: {df['county'].nunique()}")
    print(f"  Candidates: {df['candidate'].nunique()}")
    
    return df


def main():
    """Main execution."""
    print("=" * 70)
    print("Wisconsin 2024 Election Data Extraction")
    print("=" * 70)
    
    all_dfs = []
    
    # Parse Presidential data
    if POTUS_PDF.exists():
        print("\n" + "=" * 70)
        print("PRESIDENTIAL RACE")
        print("=" * 70)
        potus_df = parse_presidential_pdf(POTUS_PDF)
        
        if not potus_df.empty:
            # Save individual file
            output_file = OUTPUT_DIR / "wi_2024_president_general.csv"
            potus_df.to_csv(output_file, index=False)
            print(f"\n✓ Saved to: {output_file}")
            all_dfs.append(potus_df)
    else:
        print(f"\n✗ {POTUS_PDF} not found")
    
    # Parse Senate data
    if SENATE_PDF.exists():
        print("\n" + "=" * 70)
        print("U.S. SENATE RACE")
        print("=" * 70)
        senate_df = parse_senate_pdf(SENATE_PDF)
        
        if not senate_df.empty:
            # Save individual file
            output_file = OUTPUT_DIR / "wi_2024_us_senate_general.csv"
            senate_df.to_csv(output_file, index=False)
            print(f"\n✓ Saved to: {output_file}")
            all_dfs.append(senate_df)
    else:
        print(f"\n✗ {SENATE_PDF} not found")
    
    # Create combined CSV
    if all_dfs:
        print("\n" + "=" * 70)
        print("CREATING COMBINED CSV")
        print("=" * 70)
        
        combined_df = pd.concat(all_dfs, ignore_index=True)
        combined_df = combined_df.sort_values(['office', 'county', 'votes'], 
                                             ascending=[True, True, False])
        
        combined_file = OUTPUT_DIR / "wi_2024_general_combined.csv"
        combined_df.to_csv(combined_file, index=False)
        
        print(f"\n✓ Combined CSV saved to: {combined_file}")
        print(f"\nSummary:")
        print(f"  Total records: {len(combined_df)}")
        print(f"  Offices: {', '.join(combined_df['office'].unique())}")
        print(f"  Counties: {combined_df['county'].nunique()}/72")
        print(f"  Total candidates: {combined_df['candidate'].nunique()}")
        
        # Show breakdown by office
        print(f"\nBreakdown by office:")
        for office in combined_df['office'].unique():
            office_df = combined_df[combined_df['office'] == office]
            print(f"  {office}:")
            print(f"    Records: {len(office_df)}")
            print(f"    Candidates: {office_df['candidate'].nunique()}")
            print(f"    Counties: {office_df['county'].nunique()}")
    
    print("\n" + "=" * 70)
    print("COMPLETE!")
    print("=" * 70)
    print(f"\nOutput directory: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
