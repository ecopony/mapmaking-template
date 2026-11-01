# Elevation Zones (example map)

> Status: in-progress — worked example shipped with the template
> Last updated: 2026-11-01
>
> This is a filled-in example brief so you can see the shape of a real one. Replace it
> with your own map, or delete the project entirely.

## 1. Purpose & audience
- **Core message:** A mountain range isn't one place — it's a stack of worlds. Show the
  foothills → montane → subalpine → alpine bands as distinct zones so the vertical
  structure reads at a glance.
- **Audience:** General/curious readership; no prior ecology needed.
- **Map type:** Thematic — classified (manual-break) polygons over shaded relief.

## 2. Geography & scale
- **Extent / area of interest:** A single mountain range (swap in your own DEM frame).
- **Target scale:** Single sheet, landscape.
- **Projection (EPSG / PROJ):** an equal-area Albers centered on the range.
- **Why this projection:** the map compares the *areas* of the zones, so area must be
  honest — equal-area, not Web Mercator.

## 3. Data
| Layer | Source | Format | CRS | Access / URL | Notes |
|-------|--------|--------|-----|--------------|-------|
| Elevation | Copernicus GLO-90 DEM (or any DEM) | GeoTIFF | 4326 | OpenTopography | Reprojected to the Albers CRS before classifying. |
| Hillshade | derived from the DEM | GeoTIFF | Albers | — | Backdrop for the zone polygons. |
| Basemap | Natural Earth | vector | 4326 | local copy | States, water, cities for context. |

- **Gaps / data still needed:** pick the actual DEM tiles for your frame.
- **Licensing:** Copernicus DEM free w/ attribution; Natural Earth public domain.

## 4. Symbology & visual hierarchy
- **Foreground:** the four zone polygons, filled with a sequential green→tan ramp.
- **Context:** hillshade underneath for terrain; basemap labels on top.
- **Classification:** manual breaks at 1,500 / 2,400 / 3,000 / 3,500 m (edit for your range).
- **Typography:** one label per zone.

## 5. Layout & output
- **Medium:** print-first single sheet; PNG export for sharing/critique.
- **Required elements:** title, legend (the four zones + their elevations), scale bar,
  north arrow, source credit.
- **Output format:** GeoPackage from the pipeline → composed in the GIS tool → PDF/PNG.

## 6. Tools & pipeline
- **Software:** this repo (`main.py`) for processing → QGIS/ArcGIS Pro for cartography.
- **Processing steps (high level):**
  1. Reproject the DEM to the Albers CRS.
  2. Classify into four bands with `mapprep.raster.classify_to_polygons`.
  3. Smooth and sieve out slivers so the zones read cleanly at layout scale.
  4. Build a hillshade from the same DEM.
  5. Write everything to `output/elevation_zones.gpkg` + a hillshade GeoTIFF, and document
     each in `output/LAYERS.md`.

## 7. Open questions / decisions
- [x] **Breaks:** manual at 1,500 / 2,400 / 3,000 / 3,500 m — matches the classic
      montane/subalpine/alpine transitions; revisit per range.
- [x] **Sliver floor:** sieve parts below 1 km² — single-pixel speckle out-shouted the
      zones in the first draft (2026-11-01).
- [ ] **Treeline nuance:** treeline rises with latitude and aspect; a flat elevation break
      is a simplification. Note it in the caption, or derive treeline instead of assuming it.
