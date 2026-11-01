# Layer Catalog

Index of projects and their layer documentation. Each project keeps an `output/LAYERS.md`
describing every file it produces — cartographic role, source data, processing chain, and
the rationale behind the choices. **Read a project's `LAYERS.md` before using its layers in
a map**; the files alone don't tell you why they exist or how they were made.

Maintained by the `make-layer` skill (`.claude/skills/make-layer/`).

## Documented projects

- [example-elevation-zones](projects/example-elevation-zones/output/LAYERS.md) — worked
  example: a DEM thresholded into four elevation bands (foothills / montane / subalpine /
  alpine) as smoothed polygons over a hillshade, in an equal-area Albers. Demonstrates the
  DEM → classify → polygonize → GeoPackage + `LAYERS.md` shape.
