"""Elevation Zones — worked example pipeline.

Classifies a DEM into four elevation bands, dissolves each into smoothed polygons, and
writes them to a GeoPackage alongside a hillshade. See brief.md for the plan and
output/LAYERS.md for what each output file is.

Run from this directory:

    uv run main.py

It expects a DEM. Point DEM_DIR in the repo-root .env at a folder of DEM tiles, or set
DEM_PATH to a single GeoTIFF. With no DEM present it prints what it would do and exits —
so the template runs out of the box without shipping a large raster.
"""
from __future__ import annotations

import os
from pathlib import Path

import dotenv

from mapprep import raster

HERE = Path(__file__).parent
OUTPUT = HERE / "output"

# Four bands: foothills / montane / subalpine / alpine. Edit for your range (brief §4).
BREAKS = [1500, 2400, 3000, 3500]
LABELS = ["foothills", "montane", "subalpine", "alpine", "icecap"]


def find_dem() -> Path | None:
    dotenv.load_dotenv(dotenv.find_dotenv())
    explicit = os.environ.get("DEM_PATH")
    if explicit and Path(explicit).exists():
        return Path(explicit)
    dem_dir = os.environ.get("DEM_DIR")
    if dem_dir and Path(dem_dir).exists():
        tifs = sorted(Path(dem_dir).glob("*.tif"))
        if tifs:
            return tifs[0]
    return None


def main() -> None:
    OUTPUT.mkdir(exist_ok=True)
    dem = find_dem()
    if dem is None:
        print(
            "No DEM found. Set DEM_PATH to a GeoTIFF, or DEM_DIR to a folder of tiles, "
            "in the repo-root .env (copy .env.example). Would then:\n"
            f"  1. reproject {dem} to the project's equal-area Albers CRS\n"
            f"  2. classify at breaks {BREAKS} m into {len(LABELS)} zones\n"
            "  3. smooth + sieve slivers below 1 km^2\n"
            "  4. write output/elevation_zones.gpkg (layer 'zones') and a hillshade\n"
            "  5. run the make-layer skill to document both in output/LAYERS.md"
        )
        return

    # Real runs would reproject first; here we classify the DEM as-is for brevity.
    polys = raster.classify_to_polygons(
        str(dem),
        BREAKS,
        labels=LABELS,
        simplify_m=90.0,
        min_area_m2=1_000_000,  # 1 km^2
    )

    import geopandas as gpd
    import pyogrio

    gdf = gpd.GeoDataFrame(
        {"zone": [label for label, _ in polys]},
        geometry=[geom for _, geom in polys],
        crs="EPSG:4326",
    )
    out = OUTPUT / "elevation_zones.gpkg"
    pyogrio.write_dataframe(gdf, out, layer="zones")
    print(f"Wrote {out} with {len(gdf)} zones: {list(gdf['zone'])}")
    print("Next: run the make-layer skill to document this in output/LAYERS.md.")


if __name__ == "__main__":
    main()
