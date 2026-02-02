"""
Extract election data from Wisconsin PDF reports using PyMuPDF (no Java required).

This script uses PyMuPDF (fitz) to extract text from PDF files and parses it
to create OpenElections-formatted CSV files.

Requirements:
    pip install pymupdf pandas

Usage:
    python extract_election_data_pymupdf.py
"""

import fitz  # PyMuPDF
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

# Wisconsin counties for validation
WI_COUNTIES = [
    'Adams', 'Ashland', 'Barron', 'Bayfield', 'Brown', 'Buffalo', 'Burnett',
    'Calumet', 'Chippewa', 'Clark', 'Columbia', 'Crawford', 'Dane', 'Dodge',
    'Door', 'Douglas', 'Dunn', 'Eau Claire', 'Florence', 'Fond du Lac', 'Forest',
    'Grant', 'Green', 'Green Lake', 'Iowa', 'Iron', 'Jackson', 'Jefferson',
    'Juneau', 'Kenosha', 'Kewaunee', 'La Crosse', 'Lafayette', 'Langlade',
    'Lincoln', 'Manitowoc', 'Marathon', 'Marinette', 'Marquette', 'Menominee',
    'Milwaukee', 'Monroe', 'Oconto', 'Oneida', 'Outagamie', 'Ozaukee', 'Pepin',
    'Pierce', 'Polk', 'Portage', 'Price', 'Racine', 'Richland', 'Rock', 'Rusk',
    'St. Croix', 'Sauk', 'Sawyer', 'Shawano', 'Sheboygan', 'Taylor', 'Trempealeau',
    'Vernon', 'Vilas', 'Walworth', 'Washburn', 'Washington', 'Waukesha', 'Waupaca',
    'Waushara', 'Winnebago', 'Wood'
]


def extract_text_from_pdf(pdf_path):
    """Extract text from all pages of PDF."""
    print(f"Extracting text from {pdf_path.name}...")
    
    try:
        doc = fitz.open(pdf_path)
        text_by_page = []
        
        for page_num in range(len(doc)):
            page = doc[page_num]
            text = page.get_text()
            text_by_page.append(text)
            print(f"  Page {page_num + 1}: {len(text)} characters")
        
        doc.close()
        return text_by_page
    
    except Exception as e:
        print(f"  Error extracting from {pdf_path.name}: {e}")
        return []


def parse_election_table(text_pages, office, year):
    """
    Parse election data from extracted text.
    
    This function looks for county names followed by vote counts.
    """
    records = []
    
    # Combine all pages
    full_text = "\n".join(text_pages)
    lines = full_text.split('\n')
    
    # Try to find candidate names in header
    candidates = find_candidates(lines, office)
    print(f"\nDetected candidates: {candidates}")
    
    if not candidates:
        print("Warning: Could not detect candidates automatically")
        return pd.DataFrame()
    
    # Process each line looking for county data
    for i, line in enumerate(lines):
        line = line.strip()
        
        # Check if line starts with a county name
        county = None
        for wi_county in WI_COUNTIES:
            if line.startswith(wi_county):
                county = wi_county
                break
        
        if not county:
            continue
        
        # Extract numbers from the line
        # Look for patterns like: "County Name 12,345 23,456 1,234"
        numbers = re.findall(r'[\d,]+', line)
        vote_counts = []
        
        for num_str in numbers:
            try:
                votes = int(num_str.replace(',', ''))
                vote_counts.append(votes)
            except ValueError:
                continue
        
        # Match vote counts to candidates
        if len(vote_counts) >= len(candidates):
            for idx, candidate_info in enumerate(candidates):
                if idx < len(vote_counts):
                    records.append({
                        'county': county,
                        'office': office,
                        'district': '',
                        'party': candidate_info['party'],
                        'candidate': candidate_info['name'],
                        'votes': vote_counts[idx]
                    })
        else:
            print(f"Warning: {county} - Found {len(vote_counts)} votes but expected {len(candidates)}")
    
    df = pd.DataFrame(records)
    
    if not df.empty:
        df = df.sort_values(['county', 'votes'], ascending=[True, False])
    
    return df


def find_candidates(lines, office):
    """
    Attempt to find candidate names in the text.
    """
    candidates = []
    
    # Known 2024 candidates
    if office == 'President':
        # Common presidential candidates in 2024
        candidate_patterns = [
            ('Trump', 'REP'),
            ('Harris', 'DEM'),
            ('Biden', 'DEM'),
            ('Kennedy', 'IND'),
            ('Stein', 'GRN'),
            ('Oliver', 'LIB'),
            ('West', 'IND'),
        ]
    elif office == 'U.S. Senate':
        # Wisconsin Senate candidates
        candidate_patterns = [
            ('Baldwin', 'DEM'),
            ('Hovde', 'REP'),
            ('Vogel', 'IND'),
        ]
    else:
        return []
    
    # Search for these candidates in the text
    for pattern, party in candidate_patterns:
        for line in lines[:50]:  # Check first 50 lines for header
            if pattern.upper() in line.upper():
                # Try to extract full name
                # Look for pattern like "Lastname, Firstname" or "Firstname Lastname"
                name_match = re.search(rf'(\w+,?\s+\w+(?:\s+\w+)?)', line, re.IGNORECASE)
                if name_match and pattern.upper() in name_match.group(1).upper():
                    full_name = name_match.group(1).strip()
                    candidates.append({'name': full_name, 'party': party})
                    break
                else:
                    # Use the pattern as the name
                    candidates.append({'name': pattern, 'party': party})
                    break
    
    return candidates


def main():
    """Main execution function."""
    print("=" * 70)
    print("Wisconsin Election Data Extraction - PyMuPDF Method")
    print("=" * 70)
    
    # Check if PDFs exist
    if not POTUS_PDF.exists():
        print(f"\nError: {POTUS_PDF} not found")
        return
    
    if not SENATE_PDF.exists():
        print(f"\nError: {SENATE_PDF} not found")
        return
    
    all_records = []
    
    # Extract Presidential data
    print("\n" + "=" * 70)
    print("PROCESSING PRESIDENTIAL DATA")
    print("=" * 70)
    
    potus_pages = extract_text_from_pdf(POTUS_PDF)
    
    if potus_pages:
        year = 2024
        potus_df = parse_election_table(potus_pages, 'President', year)
        
        if not potus_df.empty:
            output_file = OUTPUT_DIR / f"wi_{year}_president_general.csv"
            potus_df.to_csv(output_file, index=False)
            print(f"\n✓ Presidential data saved to: {output_file}")
            print(f"  Total records: {len(potus_df)}")
            print(f"  Counties: {potus_df['county'].nunique()}")
            print(f"  Candidates: {potus_df['candidate'].nunique()}")
            
            all_records.append(potus_df)
        else:
            print("\n✗ No presidential data extracted")
    
    # Extract Senate data
    print("\n" + "=" * 70)
    print("PROCESSING U.S. SENATE DATA")
    print("=" * 70)
    
    senate_pages = extract_text_from_pdf(SENATE_PDF)
    
    if senate_pages:
        year = 2024
        senate_df = parse_election_table(senate_pages, 'U.S. Senate', year)
        
        if not senate_df.empty:
            output_file = OUTPUT_DIR / f"wi_{year}_us_senate_general.csv"
            senate_df.to_csv(output_file, index=False)
            print(f"\n✓ Senate data saved to: {output_file}")
            print(f"  Total records: {len(senate_df)}")
            print(f"  Counties: {senate_df['county'].nunique()}")
            print(f"  Candidates: {senate_df['candidate'].nunique()}")
            
            all_records.append(senate_df)
        else:
            print("\n✗ No senate data extracted")
    
    # Combine all records into one CSV
    if all_records:
        print("\n" + "=" * 70)
        print("CREATING COMBINED CSV")
        print("=" * 70)
        
        combined_df = pd.concat(all_records, ignore_index=True)
        combined_file = OUTPUT_DIR / f"wi_2024_general_combined.csv"
        combined_df.to_csv(combined_file, index=False)
        
        print(f"\n✓ Combined data saved to: {combined_file}")
        print(f"  Total records: {len(combined_df)}")
        print(f"  Offices: {combined_df['office'].unique().tolist()}")
        print(f"  Counties: {combined_df['county'].nunique()}")
        print(f"  Total candidates: {combined_df['candidate'].nunique()}")
    
    print("\n" + "=" * 70)
    print("EXTRACTION COMPLETE")
    print("=" * 70)
    print(f"\nOutput directory: {OUTPUT_DIR}")
    print("\nIMPORTANT: This is a basic text extraction. Please:")
    print("1. Open the generated CSV and verify all data")
    print("2. Check candidate names and party affiliations")
    print("3. Verify vote counts against the original PDFs")
    print("4. The PDFs may require manual data entry if structure is complex")


if __name__ == "__main__":
    main()
