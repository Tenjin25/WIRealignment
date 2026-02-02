"""Debug - check county matching."""

import fitz
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data"
POTUS_PDF = DATA_DIR / "County by County Report_POTUS.pdf"

WI_COUNTIES = ['ADAMS', 'ASHLAND', 'BARRON', 'BAYFIELD', 'BROWN']

doc = fitz.open(POTUS_PDF)
page = doc[0]
text = page.get_text()
lines = text.split('\n')

print("Checking first 30 lines for county matches:\n")
for i, line in enumerate(lines[:30], 1):
    line_stripped = line.strip()
    
    matched = False
    for county in WI_COUNTIES:
        if line_stripped.startswith(county):
            print(f"{i:3d}: MATCH '{county}' -> {repr(line_stripped[:80])}")
            matched = True
            break
    
    if not matched and len(line_stripped) > 3:
        print(f"{i:3d}: {repr(line_stripped[:80])}")

doc.close()
