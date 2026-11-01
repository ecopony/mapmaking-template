"""Raster → vector helpers.

`classify_to_polygons` is the workhorse behind several map styles: bin a continuous
raster (elevation, precipitation, an aridity index…) into classes, then dissolve each
class into smooth polygons suitable for filling in a GIS. Smoothing and a minimum-area
sieve keep the output from being a mess of single-pixel slivers at layout scale.
"""
from __future__ import annotations

import numpy as np
import rasterio
from rasterio.features import shapes
from shapely.geometry import shape
from shapely.ops import unary_union


def classify_to_polygons(
    dem_path: str,
    breaks: list[float],
    *,
    labels: list[str] | None = None,
    simplify_m: float = 0.0,
    min_area_m2: float = 0.0,
):
    """Bin a single-band raster by `breaks` and return dissolved polygons per class.

    Args:
        dem_path: path to a single-band raster (e.g. a DEM).
        breaks: ascending break values. ``[1000, 2000, 3000]`` makes classes
            ``(-inf,1000], (1000,2000], (2000,3000], (3000,inf)``.
        labels: optional name per class; defaults to ``class_0``, ``class_1``, …
        simplify_m: Douglas-Peucker tolerance in CRS units (0 = no simplification).
        min_area_m2: drop polygon parts smaller than this (0 = keep all).

    Returns:
        list of ``(label, shapely geometry)`` tuples, one per non-empty class.

    This is a compact reference implementation — real pipelines often reproject first,
    fill nodata, or run a morphological smooth before polygonizing. Extend as needed and
    record what you changed in the project's ``LAYERS.md``.
    """
    with rasterio.open(dem_path) as src:
        band = src.read(1, masked=True)
        transform = src.transform

    classed = np.digitize(band.filled(np.nan), breaks).astype("int32")
    classed = np.ma.array(classed, mask=band.mask)

    if labels is None:
        labels = [f"class_{i}" for i in range(len(breaks) + 1)]

    results = []
    for value, label in enumerate(labels):
        mask = (classed == value) & ~np.ma.getmaskarray(classed)
        if not mask.any():
            continue
        geoms = [
            shape(geom)
            for geom, v in shapes(classed.filled(-1).astype("int32"), mask=mask, transform=transform)
            if v == value
        ]
        if not geoms:
            continue
        merged = unary_union(geoms)
        if min_area_m2:
            merged = _drop_small_parts(merged, min_area_m2)
        if simplify_m:
            merged = merged.simplify(simplify_m, preserve_topology=True)
        if not merged.is_empty:
            results.append((label, merged))
    return results


def _drop_small_parts(geom, min_area_m2: float):
    """Remove polygon parts below a minimum area, keeping the multipolygon otherwise."""
    polys = getattr(geom, "geoms", [geom])
    kept = [p for p in polys if p.area >= min_area_m2]
    if not kept:
        return geom.__class__()
    return unary_union(kept)
