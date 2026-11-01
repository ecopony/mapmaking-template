# Elevation zones ramp

**Layer kind**: classified elevation-band polygons (the `zones` layer)
**First used**: example-elevation-zones (2026-11-01)

## Recipe
1. Unique-values symbology on the `zone` field.
2. Sequential ramp, low→high: foothills warm tan → montane olive → subalpine green →
   alpine pale grey-green.
3. Polygon fill ~50% opacity, no outline (the hillshade underneath does the edges).

## Draw order
Above the hillshade raster, below basemap labels.

## Notes
Example recipe shipped with the template — replace with your own.

## History
- 2026-11-01: created (example-elevation-zones)
