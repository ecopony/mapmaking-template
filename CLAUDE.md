# CLAUDE.md

A combined planning + map-prep workspace. Each map lives in `projects/<slug>/` and holds
**both** its plan (`brief.md`) and its pipeline (`main.py`, `output/`). Planning and
processing are one repo here for simplicity.

## Where things live

- `ideas.md` — raw backlog. New idea → add a line here. Don't start a brief until the user
  says they want to build the map.
- `templates/project-brief.md` — copy to `projects/<slug>/brief.md` to start a map.
- `projects/<slug>/` — one map: `brief.md` (the plan), `main.py` (the pipeline), `output/`
  (generated files + `LAYERS.md`), `pyproject.toml` (its deps).
- `packages/mapprep/` — shared Python; import as `from mapprep import raster`. Never use
  `sys.path` hacks.
- `shared/styles/` — ArcGIS Pro symbology recipes in words (Pro styling is invisible to
  the repo, so it's recorded here).
- `CATALOG.md` — index of every project's `LAYERS.md`.

## Before building a map

**Read the project's `brief.md` first.** It carries the purpose, extent, projection, data
sources, and every decision made so far. If the project already has `output/LAYERS.md`,
read that too — it says how the existing layers were made and why.

## When building or changing a layer

Use the **`make-layer`** skill. It covers the processing *and* the documentation: every
file written to a project's `output/` gets an entry in that project's `output/LAYERS.md`,
mixing extracted facts (CRS, extent, counts) with rationale written from the conversation
(why this dataset, why these parameters, what was rejected). A layer isn't done until its
entry exists. Regenerating a layer appends to its rationale rather than overwriting it.

## Running pipelines (uv workspace)

- Python 3.12, single root `.venv` and `uv.lock`.
- Run a project from its directory with `uv run main.py`, or from the root with
  `uv run --package <slug> main.py`.
- A new project is a workspace member: add `projects/<slug>` to the `members` list in the
  root `pyproject.toml`, and give it a `pyproject.toml` with `mapprep = { workspace = true }`.
- Bulk source data lives outside the repo; locate it via a `.env` at the repo root
  (copy `.env.example`). Load with `dotenv.load_dotenv(dotenv.find_dotenv())`.

## The division of labor

Data prep is code and belongs to Claude. Composing the map (QGIS / ArcGIS Pro) is the
craft and stays with the user. Prefer fixing display problems in the **pipeline** over
one-off GIS definition queries, so the fix is recorded and reproducible — but symbology
decisions live in `shared/styles/` via the `style` skill, since the GIS tool doesn't
expose them to the repo.
