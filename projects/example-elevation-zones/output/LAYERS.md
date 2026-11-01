# example-elevation-zones — layer documentation

**Map**: Elevation Zones (example)
**Script**: `main.py` (template, 2026-11-01)
**Overview**: One classified-polygon layer over a hillshade. The DEM is binned into four
elevation bands and dissolved into smooth polygons (`zones`); the hillshade is the terrain
backdrop they're drawn over. Draw order in the GIS tool: hillshade at the bottom, `zones`
filled above it with ~50% opacity so the relief shows through, basemap labels on top.

> This is an example entry showing the format. Facts below are illustrative placeholders —
> a real entry pastes the exact output of `make-layer`'s `extract_facts.py` after the
> pipeline runs.

## elevation_zones.gpkg
### zones
- **Role**: the subject of the map — four elevation bands (foothills, montane, subalpine,
  alpine) as filled polygons.
- **Source**: derived from the project DEM (Copernicus GLO-90 or any DEM pointed at by
  `DEM_DIR` / `DEM_PATH`).
- **Processing**: reproject DEM → equal-area Albers; `mapprep.raster.classify_to_polygons`
  with breaks `[1500, 2400, 3000, 3500]` m, `simplify_m=90`, `min_area_m2=1e6`.
- **Rationale**: manual breaks at the classic montane/subalpine/alpine transitions rather
  than quantiles — the thresholds are the point, so they should be nameable, not
  data-driven. 1 km² sieve added 2026-11-01 because single-pixel speckle from the raw
  classification out-shouted the zones at layout scale (fixed in the pipeline, not with a
  GIS definition query, so the fix is reproducible).
- **Facts** *(extracted YYYY-MM-DD)*: _(paste `extract_facts.py` output here after a run —
  CRS, geometry type, feature count, fields)_

## hillshade.tif
- **Role**: terrain backdrop under the zone polygons.
- **Source**: same DEM.
- **Processing**: standard hillshade (az 315°, alt 45°) from the reprojected DEM.
- **Rationale**: gives the flat-colored zones three-dimensional structure without
  competing for attention.
- **Facts** *(extracted YYYY-MM-DD)*: _(paste `extract_facts.py` output here after a run)_
