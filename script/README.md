# Election Data Extraction Scripts

## Overview
Scripts to extract election data from Wisconsin PDF reports and convert to OpenElections CSV format.

## Setup

### 1. Install Dependencies
```powershell
pip install -r requirements.txt
```

**Note**: `tabula-py` requires Java to be installed on your system. 
- Download Java from: https://www.java.com/download/
- Or install via: `winget install Oracle.JavaRuntimeEnvironment`

### 2. Verify PDF Files
Ensure these files exist in the `data/` directory:
- `County by County Report_POTUS.pdf`
- `County by County Report_US Senate_1.pdf`

## Usage

### Extract Election Data
```powershell
python extract_election_data.py
```

This will:
1. Extract tables from both PDF files
2. Parse county-level vote counts
3. Detect candidate party affiliations
4. Generate OpenElections-formatted CSVs in `data/processed/`

### Output Format
Generated CSV files follow OpenElections Wisconsin format:
```csv
county,office,district,party,candidate,votes
Adams,President,,REP,Donald J. Trump,5234
Adams,President,,DEM,Kamala Harris,3456
...
```

## OpenElections Format Specification

| Column | Description | Example |
|--------|-------------|---------|
| `county` | County name (without "County" suffix) | `Milwaukee` |
| `office` | Office being contested | `President`, `U.S. Senate` |
| `district` | District number (blank for statewide) | `` |
| `party` | Party code | `DEM`, `REP`, `LIB`, `GRN`, `IND` |
| `candidate` | Candidate full name | `Kamala Harris` |
| `votes` | Vote count (integer) | `5234` |

## Manual Review Steps

After extraction, review the CSV files for:

1. **Party Affiliations**: The script attempts auto-detection but may miss minor party candidates
   - Check candidates without party codes
   - Verify party assignments for lesser-known candidates

2. **County Names**: Verify all 72 Wisconsin counties are present
   - Check for formatting issues (extra spaces, special characters)
   - Ensure consistency across files

3. **Vote Counts**: Spot-check totals against PDF
   - Look for obvious errors (missing commas, decimal points)
   - Verify totals add up correctly

4. **Candidate Names**: Check for formatting consistency
   - Middle initials, suffixes (Jr., Sr.)
   - Nickname handling (e.g., "Bill" vs "William")

## Wisconsin Counties Reference

Wisconsin has **72 counties**:
Adams, Ashland, Barron, Bayfield, Brown, Buffalo, Burnett, Calumet, Chippewa, Clark, Columbia, Crawford, Dane, Dodge, Door, Douglas, Dunn, Eau Claire, Florence, Fond du Lac, Forest, Grant, Green, Green Lake, Iowa, Iron, Jackson, Jefferson, Juneau, Kenosha, Kewaunee, La Crosse, Lafayette, Langlade, Lincoln, Manitowoc, Marathon, Marinette, Marquette, Menominee, Milwaukee, Monroe, Oconto, Oneida, Outagamie, Ozaukee, Pepin, Pierce, Polk, Portage, Price, Racine, Richland, Rock, Rusk, St. Croix, Sauk, Sawyer, Shawano, Sheboygan, Taylor, Trempealeau, Vernon, Vilas, Walworth, Washburn, Washington, Waukesha, Waupaca, Waushara, Winnebago, Wood

## Troubleshooting

### Java Not Found Error
```
tabula.errors.JavaNotFoundError
```
**Solution**: Install Java Runtime Environment
```powershell
winget install Oracle.JavaRuntimeEnvironment
```

### Extraction Issues
If tables aren't extracting correctly:
1. Open the PDF and check structure
2. Try specifying specific pages: `extract_pdf_tables(pdf_path, pages='1-5')`
3. Adjust `pandas_options` in the script
4. Consider using `lattice=True` for PDFs with clear grid lines

### Party Detection Failures
If many candidates show blank party:
1. Update the `detect_party()` function with more candidate names
2. Check PDF for party abbreviations in candidate names
3. Manually add party codes after extraction

## Additional Resources

- [OpenElections Documentation](https://github.com/openelections/openelections-data-wi)
- [Tabula-py Documentation](https://tabula-py.readthedocs.io/)
- [Wisconsin Elections Commission](https://elections.wi.gov/)
