"""
Extract election data from Wisconsin PDF reports and convert to OpenElections CSV format.

This script uses tabula-py to extract tables from PDF files and formats them
according to OpenElections standards for Wisconsin election data.

Requirements:
    pip install tabula-py pandas openpyxl

Usage:
    python extract_election_data.py
"""

import tabula
import pandas as pd
import os
from pathlib import Path

# Paths
DATA_DIR = Path(__file__).parent.parent / "data"
OUTPUT_DIR = DATA_DIR / "processed"
OUTPUT_DIR.mkdir(exist_ok=True)

# Input PDF files
POTUS_PDF = DATA_DIR / "County by County Report_POTUS.pdf"
SENATE_PDF = DATA_DIR / "County by County Report_US Senate_1.pdf"


def extract_pdf_tables(pdf_path, pages='all'):
    """
    Extract tables from PDF using tabula.
    
    Args:
        pdf_path: Path to PDF file
        pages: Pages to extract (default 'all')
    
    Returns:
        List of DataFrames
    """
    print(f"Extracting tables from {pdf_path.name}...")
    
    try:
        # Extract all tables from PDF
        tables = tabula.read_pdf(
            str(pdf_path),
            pages=pages,
            multiple_tables=True,
            pandas_options={'header': None}
        )
        
        print(f"  Found {len(tables)} tables")
        return tables
    
    except Exception as e:
        print(f"  Error extracting from {pdf_path.name}: {e}")
        return []


def clean_county_name(county_str):
    """Clean and standardize county names."""
    if pd.isna(county_str):
        return None
    
    county = str(county_str).strip()
    
    # Remove "County" suffix if present
    county = county.replace(" County", "").replace(" COUNTY", "")
    
    # Handle common formatting issues
    county = county.strip()
    
    return county if county else None


def convert_to_openelections_format(tables, office, year, election_type='general'):
    """
    Convert extracted tables to OpenElections CSV format.
    
    OpenElections Wisconsin format:
    - county: County name
    - office: Office being contested (e.g., 'President', 'U.S. Senate')
    - district: District number (blank for statewide)
    - party: Party affiliation (DEM, REP, LIB, GRN, etc.)
    - candidate: Candidate name
    - votes: Vote count
    
    Args:
        tables: List of DataFrames from tabula
        office: Office name (e.g., 'President', 'U.S. Senate')
        year: Election year
        election_type: 'general' or 'primary'
    
    Returns:
        DataFrame in OpenElections format
    """
    records = []
    
    for table_idx, df in enumerate(tables):
        print(f"\nProcessing table {table_idx + 1}/{len(tables)}")
        print(f"  Shape: {df.shape}")
        print(f"  Columns: {list(df.columns)}")
        
        # Display first few rows for inspection
        print("\nFirst few rows:")
        print(df.head(10))
        
        # Try to identify structure
        # Common patterns:
        # - First column: County name
        # - Subsequent columns: Candidate names with vote counts
        
        if df.shape[1] < 2:
            print("  Skipping table - not enough columns")
            continue
        
        # Attempt to detect header row
        # Look for rows with candidate names (usually contain recognizable patterns)
        header_row = None
        for idx, row in df.iterrows():
            # Check if row contains potential candidate names
            if any(pd.notna(val) and isinstance(val, str) and 
                   any(keyword in str(val).upper() for keyword in 
                       ['TRUMP', 'BIDEN', 'HARRIS', 'CLINTON', 'OBAMA', 'MCCAIN', 
                        'ROMNEY', 'BUSH', 'KERRY', 'GORE', 'JOHNSON', 'STEIN',
                        'BALDWIN', 'VUKMIR', 'FEINGOLD', 'JOHNSON', 'MANDELA']
                   ) for val in row
            ):
                header_row = idx
                print(f"  Detected header row at index {idx}")
                break
        
        if header_row is not None:
            # Use detected header
            candidate_names = df.iloc[header_row].tolist()
            data_df = df.iloc[header_row + 1:].reset_index(drop=True)
            data_df.columns = range(len(data_df.columns))
        else:
            # Assume first row is header
            print("  No clear header detected, using first row")
            candidate_names = df.iloc[0].tolist()
            data_df = df.iloc[1:].reset_index(drop=True)
        
        print(f"  Candidate names: {candidate_names}")
        
        # Process each row (each row is a county)
        for _, row in data_df.iterrows():
            county = clean_county_name(row[0])
            
            if not county:
                continue
            
            # Skip total rows
            if any(word in county.upper() for word in ['TOTAL', 'STATEWIDE', 'SUMMARY']):
                continue
            
            # Process each candidate column
            for col_idx in range(1, len(row)):
                if col_idx >= len(candidate_names):
                    break
                
                candidate = candidate_names[col_idx]
                votes = row[col_idx]
                
                # Skip if no candidate name or votes
                if pd.isna(candidate) or pd.isna(votes):
                    continue
                
                candidate = str(candidate).strip()
                if not candidate:
                    continue
                
                # Try to convert votes to integer
                try:
                    if isinstance(votes, str):
                        votes = votes.replace(',', '').replace(' ', '')
                    votes = int(float(votes))
                except (ValueError, TypeError):
                    print(f"    Warning: Could not convert votes for {candidate} in {county}: {votes}")
                    continue
                
                # Detect party from candidate name or known candidates
                party = detect_party(candidate, office, year)
                
                records.append({
                    'county': county,
                    'office': office,
                    'district': '',
                    'party': party,
                    'candidate': candidate,
                    'votes': votes
                })
    
    # Create DataFrame
    result_df = pd.DataFrame(records)
    
    if not result_df.empty:
        # Sort by county, then by votes descending
        result_df = result_df.sort_values(['county', 'votes'], ascending=[True, False])
    
    return result_df


def detect_party(candidate_name, office, year):
    """
    Attempt to detect party affiliation from candidate name.
    
    Args:
        candidate_name: Candidate name string
        office: Office being contested
        year: Election year
    
    Returns:
        Party code (DEM, REP, LIB, GRN, IND, etc.) or empty string
    """
    candidate_upper = candidate_name.upper()
    
    # Known Republican presidential candidates
    rep_presidential = ['TRUMP', 'ROMNEY', 'MCCAIN', 'BUSH', 'DOLE', 'REAGAN', 'NIXON']
    # Known Democratic presidential candidates
    dem_presidential = ['BIDEN', 'HARRIS', 'CLINTON', 'OBAMA', 'KERRY', 'GORE', 'CARTER', 'MONDALE', 'DUKAKIS']
    # Known Libertarian candidates
    lib_candidates = ['JOHNSON', 'JORGENSEN', 'BADNARIK']
    # Known Green candidates
    grn_candidates = ['STEIN', 'NADER', 'HAWKINS']
    
    # Known Wisconsin Senate candidates
    dem_senate = ['BALDWIN', 'FEINGOLD', 'KOHL']
    rep_senate = ['VUKMIR', 'HOVDE', 'FITZGERALD', 'NEUMANN']
    
    # Check for known candidates
    for rep_name in rep_presidential + rep_senate:
        if rep_name in candidate_upper:
            return 'REP'
    
    for dem_name in dem_presidential + dem_senate:
        if dem_name in candidate_upper:
            return 'DEM'
    
    for lib_name in lib_candidates:
        if lib_name in candidate_upper:
            return 'LIB'
    
    for grn_name in grn_candidates:
        if grn_name in candidate_upper:
            return 'GRN'
    
    # Check if party is in the name (sometimes formatted as "Name (Party)")
    if '(DEM)' in candidate_upper or 'DEMOCRATIC' in candidate_upper:
        return 'DEM'
    if '(REP)' in candidate_upper or 'REPUBLICAN' in candidate_upper:
        return 'REP'
    if '(LIB)' in candidate_upper or 'LIBERTARIAN' in candidate_upper:
        return 'LIB'
    if '(GRN)' in candidate_upper or 'GREEN' in candidate_upper:
        return 'GRN'
    if '(IND)' in candidate_upper or 'INDEPENDENT' in candidate_upper:
        return 'IND'
    
    # If unable to detect, return empty string
    return ''


def main():
    """Main execution function."""
    print("=" * 70)
    print("Wisconsin Election Data Extraction - OpenElections Format")
    print("=" * 70)
    
    # Check if PDFs exist
    if not POTUS_PDF.exists():
        print(f"\nError: {POTUS_PDF} not found")
        return
    
    if not SENATE_PDF.exists():
        print(f"\nError: {SENATE_PDF} not found")
        return
    
    # Extract and process Presidential data
    print("\n" + "=" * 70)
    print("PROCESSING PRESIDENTIAL DATA")
    print("=" * 70)
    
    potus_tables = extract_pdf_tables(POTUS_PDF)
    
    if potus_tables:
        # You may need to adjust the year based on the PDF content
        # Check the PDF to determine the election year
        year = 2024  # Adjust this based on your PDF
        
        potus_df = convert_to_openelections_format(
            potus_tables,
            office='President',
            year=year
        )
        
        if not potus_df.empty:
            output_file = OUTPUT_DIR / f"wi_{year}_president_general.csv"
            potus_df.to_csv(output_file, index=False)
            print(f"\n✓ Presidential data saved to: {output_file}")
            print(f"  Total records: {len(potus_df)}")
            print(f"  Counties: {potus_df['county'].nunique()}")
            print(f"  Candidates: {potus_df['candidate'].nunique()}")
        else:
            print("\n✗ No presidential data extracted")
    
    # Extract and process Senate data
    print("\n" + "=" * 70)
    print("PROCESSING U.S. SENATE DATA")
    print("=" * 70)
    
    senate_tables = extract_pdf_tables(SENATE_PDF)
    
    if senate_tables:
        year = 2024  # Adjust this based on your PDF
        
        senate_df = convert_to_openelections_format(
            senate_tables,
            office='U.S. Senate',
            year=year
        )
        
        if not senate_df.empty:
            output_file = OUTPUT_DIR / f"wi_{year}_us_senate_general.csv"
            senate_df.to_csv(output_file, index=False)
            print(f"\n✓ Senate data saved to: {output_file}")
            print(f"  Total records: {len(senate_df)}")
            print(f"  Counties: {senate_df['county'].nunique()}")
            print(f"  Candidates: {senate_df['candidate'].nunique()}")
        else:
            print("\n✗ No senate data extracted")
    
    print("\n" + "=" * 70)
    print("EXTRACTION COMPLETE")
    print("=" * 70)
    print(f"\nOutput directory: {OUTPUT_DIR}")
    print("\nNext steps:")
    print("1. Review the generated CSV files")
    print("2. Manually verify candidate names and party affiliations")
    print("3. Check for any missing or incorrect county names")
    print("4. Add any additional metadata (e.g., precinct-level data if available)")


if __name__ == "__main__":
    main()
