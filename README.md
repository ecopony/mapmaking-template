# Mapmaking (template)

A starter for planning **and** building maps in one place, driven from Claude Code
sessions. It's the public shape of a private workflow: one folder per map, each holding
both the *plan* (a structured brief) and the *pipeline* (Python that prepares the data),
with the cartography itself done in a GIS tool (QGIS, ArcGIS Pro, …).

> This is a template. It ships the **structure** and one generic worked example —
> not anyone's real map ideas. Clone it, delete the example, and start talking to Claude
> about a map of your own.

## The idea

Data preparation is code, so hand it to Claude Code. Composing the map is the craft, so
keep it yourself. What makes that split work over months is not the scripts — it's the
written context around them: a **brief** that records what the map is for and every
decision made, and a **`LAYERS.md`** in each project that records how every output file
was made and why. A session three weeks from now reads those and picks up where you left
off, instead of asking you to re-explain.

## Layout

```
mapmaking-template/
├── README.md                  ← you are here
├── CLAUDE.md                  ← how Claude should work in this repo
├── ideas.md                   ← running backlog of map ideas
├── CATALOG.md                 ← index of every project's LAYERS.md
├── templates/
│   └── project-brief.md       ← copy this to start a new map
├── projects/
│   └── example-elevation-zones/   ← one folder per map: PLAN + PIPELINE together
│       ├── brief.md               ← the plan (from the template)
│       ├── main.py                ← the pipeline (`uv run main.py`)
│       ├── pyproject.toml         ← its dependencies (uv workspace member)
│       └── output/
│           └── LAYERS.md          ← what each output file is, how, and why
├── packages/
│   └── mapprep/               ← shared Python imported by projects
├── shared/
│   └── styles/                ← ArcGIS Pro symbology recipes, in words
└── .claude/
    └── skills/
        ├── make-layer/        ← process a layer AND document it in LAYERS.md
        └── style/             ← save/retrieve a styling recipe
```

The real workflow this template is modeled on keeps planning and processing in two
separate repos (privacy, and leaner sessions). This template **combines them** so there's
one thing to clone and read.

## Workflow

1. **Capture** — drop a one-line idea into [`ideas.md`](ideas.md).
2. **Plan** — when an idea firms up, copy [`templates/project-brief.md`](templates/project-brief.md)
   to `projects/<slug>/brief.md` and fill it in over a conversation.
3. **Build** — tell Claude to build it. It reads the brief, writes `projects/<slug>/main.py`,
   and runs it with `uv run main.py`. Every output file gets an entry in that project's
   `output/LAYERS.md` (the `make-layer` skill does both halves).
4. **Compose** — point your GIS tool at the project's `output/` directory and make the map.
   Export a PNG, paste it back into a session for critique, and iterate. Decisions go back
   into the brief; styling recipes go into `shared/styles/` (the `style` skill).

## Conventions

- Slugs are lowercase-kebab (`front-range-snowpack`).
- Record the **projection (EPSG or PROJ string)** explicitly in every brief — it's the
  decision most often regretted.
- Keep bulk source data *out* of git; point at it with paths in a local `.env`
  (see [`.env.example`](.env.example)) and note the source in the brief.
- A layer isn't done until its `LAYERS.md` entry exists.

## Getting set up

This repo is a [uv](https://docs.astral.sh/uv/) workspace (Python 3.12). To run the example
pipeline:

```bash
cp .env.example .env     # then edit paths for your machine
uv run --package example-elevation-zones main.py
```
