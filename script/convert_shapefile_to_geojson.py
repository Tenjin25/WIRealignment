"""
Convert Wisconsin county shapefile to GeoJSON format.

This reads the TIGER/Line shapefile and converts it to GeoJSON for use
in the web map application.
"""

import geopandas as gpd
from pathlib import Path
import json

# Paths
DATA_DIR = Path(__file__).parent.parent / "data"
SHAPEFILE = DATA_DIR / "tl_2020_55_county20" / "tl_2020_55_county20.shp"
OUTPUT_GEOJSON = DATA_DIR / "tl_2020_55_county20.geojson"

def main():
    """Convert shapefile to GeoJSON."""
    print("=" * 70)
    print("Converting Wisconsin County Shapefile to GeoJSON")
    print("=" * 70)
    
    # Check if shapefile exists
    if not SHAPEFILE.exists():
        print(f"\n✗ Error: Shapefile not found at {SHAPEFILE}")
        print("\nPlease ensure the shapefile exists in the data directory.")
        return
    
    print(f"\nReading shapefile: {SHAPEFILE.name}")
    
    # Read shapefile
    gdf = gpd.read_file(SHAPEFILE)
    
    print(f"  Found {len(gdf)} counties")
    print(f"  CRS: {gdf.crs}")
    print(f"  Columns: {list(gdf.columns)}")
    
    # Display sample data
    print("\nSample counties:")
    for idx, row in gdf.head(5).iterrows():
        print(f"  - {row.get('NAME', row.get('NAMELSAD', 'Unknown'))}")
    
    # Convert to WGS84 (standard for web mapping)
    if gdf.crs.to_string() != 'EPSG:4326':
        print("\nConverting to WGS84 (EPSG:4326)...")
        gdf = gdf.to_crs('EPSG:4326')
    
    # Simplify column names if needed
    print("\nPreparing GeoJSON...")
    
    # Write to GeoJSON
    print(f"\nWriting to: {OUTPUT_GEOJSON}")
    gdf.to_file(OUTPUT_GEOJSON, driver='GeoJSON')
    
    # Verify output
    file_size = OUTPUT_GEOJSON.stat().st_size / 1024  # KB
    
    print(f"\n✓ GeoJSON created successfully!")
    print(f"  File size: {file_size:.1f} KB")
    print(f"  Location: {OUTPUT_GEOJSON}")
    
    # Display structure
    with open(OUTPUT_GEOJSON, 'r') as f:
        geojson_data = json.load(f)
    
    print(f"\nGeoJSON structure:")
    print(f"  Type: {geojson_data['type']}")
    print(f"  Features: {len(geojson_data['features'])}")
    
    if geojson_data['features']:
        sample_feature = geojson_data['features'][0]
        print(f"  Sample feature properties: {list(sample_feature['properties'].keys())}")
    
    print("\n" + "=" * 70)
    print("COMPLETE!")
    print("=" * 70)


if __name__ == "__main__":
    main()
