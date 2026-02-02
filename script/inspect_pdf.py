"""
Inspect PDF structure to understand how to parse it.
"""

import fitz
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data"
POTUS_PDF = DATA_DIR / "County by County Report_POTUS.pdf"

doc = fitz.open(POTUS_PDF)
page = doc[0]  # First page

print("=" * 70)
print("FIRST PAGE TEXT:")
print("=" * 70)
text = page.get_text()
print(text)

print("\n" + "=" * 70)
print("LINES:")
print("=" * 70)
lines = text.split('\n')
for i, line in enumerate(lines[:30], 1):
    print(f"{i:3d}: {repr(line)}")

doc.close()
