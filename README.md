# Chicken coop model

A reproducible Blender coordination model for a proposed 12-hen coop. Future agents should first read [AGENTS.md](AGENTS.md). Start with [DESIGN.md](DESIGN.md), [BUILD.md](BUILD.md) and [handoff.md](handoff.md); [AUDIT.md](AUDIT.md) records the 25 September 2026 audit and the decisions it produced. The project is still resolving structural connections, foundations and the enclosure; geometric checks are not structural design calculations.

## Regenerate

On this Mac:

```sh
/Applications/Blender.app/Contents/MacOS/Blender --background --factory-startup --python-exit-code 1 --python scripts/build_coop.py -- --output generated/coop-candidate.blend --render
```

On another system, replace the executable path with `blender`. Run from the repository root. The generator requires Blender's Python (`bpy`), not ordinary system Python. Development and checks currently use Blender 5.2.1 LTS; other versions have not been validated.

The command reads `coop_config.json`, creates a clean scene in a **separate background process**, runs the geometry/installation checks, and saves only after those pass. It refuses to run in an interactive Blender session. The command above writes a candidate so the working model remains available during review. `--render` additionally creates `generated/assembly-preview.png`, `roof-installation.png`, `wall-framing.png`, `floor-framing.png` and `floor-installation.png`.

Outputs include the requested Blender file and `generated/model-report.json`. The latter records inputs, derived post lengths, component bounds and validation results. Treat generated files as outputs; edit the external source/configuration. The embedded text block is instructions, not an obsolete executable generator.

## Checks

The generator checks:

- all pairwise final-state post/timber/plywood volumes for unintended solid intersections;
- actual notch volumes in both main panels;
- all twelve horizontal rafter bearing seats;
- post embedment and stock-length fit;
- the two-sheet kerf allowance;
- plywood/post and plywood/plywood intersections on every integer frame during floor installation;
- roof sheet counts, profile alignment, end-support coverage and final sheet/timber/lap intersections;
- integer-frame sheet placement against installed timber and earlier sheets;
- eight rough opening clearances, wall sole-plate elevations, and integer-frame installation paths for floor framing, walls and roof framing;
- the pole tolerance rule: a clearance-inflated probe around every pole may touch only the bearers on their cut flats;
- worst-case bolt length (fattest accepted pole, set out away from the bearer) and flat depth limits;
- wall top plates meeting the roof bearers and edge rafters;
- the ten eave vent openings staying clear, with their gross free area;
- wall-before-roof phase ordering;
- selected completed-phase holds through frame 900.

Hardware envelopes, terrain/footing intersections, structural capacity, subframe motion, every moving timber assembly, real pole taper beyond the configured allowance, joist-hanger fit and supplier-specific connector clearance are outside this validation. See the pending design tasks in DESIGN.md.

Run the deliberate-regression checks against a generated file:

```sh
/Applications/Blender.app/Contents/MacOS/Blender --background --disable-autoexec generated/coop-candidate.blend --python-exit-code 1 --python scripts/check_regressions.py
```

These run in memory and do not save the altered test scene. A successful run prints `COOP_REGRESSIONS_OK` and refreshes `generated/regression-results.json`. The build prints `COOP_BUILD_OK`; the `--python-exit-code 1` option makes an uncaught script error fail the command.

After the checks pass, inspect the candidate and `generated/assembly-preview.png`, confirm the configuration recorded in `generated/model-report.json` matches `coop_config.json`, then promote it:

```sh
cp generated/coop-candidate.blend coop.blend
```

This replaces the working generated model; retain any manual work separately before promotion. The original pre-repair model remains archived in `review/original-coop.blend`.

For an assembly-stage preview, open the candidate, select the required frame from BUILD.md and render with its supplied camera. Restore frame 900 for the current roof-sheet view. `--render` refreshes all five previews, including the floor-framing (frame 200) and floor-installation (frame 240) images. Reports and previews describe the most recent run, so do not present old results as evidence for a new candidate.

## Files

- `coop.blend`: regenerated working model; frame 900 shows the skeleton and roof covering placement.
- `coop_config.json`: retained dimensions and explicit provisional choices.
- `scripts/build_coop.py`: geometry and animation generator.
- `scripts/validate_coop.py`: geometric regression checks.
- `scripts/wall_layout.py`: infill framing, openings and non-rendering nest/roost guides.
- `scripts/wall_cut_schedule.py`: kerf-aware wall stock allocation, written to `generated/wall-cut-list.md`.
- `AUDIT.md`: dated audit findings, reasoning and dispositions.
- `review/original-coop.blend`: original pre-repair model.
- `coop.blend1`: untouched older backup from before the original roof work.
- `REVIEW.md` and `review/`: historical review evidence, not the current design specification.

The camera uses Blender Workbench studio lighting, so separate light objects are unnecessary. Use the timeline markers to inspect assembly phases. Wall framing reaches the roof members; eave vent openings are framed. Nest shells, cladding, vent mesh and door leaves are pending.

Roof sheets are representative corrugated meshes with candidate bonded fleece. Roof screws, flashings and final condensation/ventilation details remain pending. Frame 465 shows wall framing before the roof; frame 620 shows bare roof framing; frame 780 shows sheet 3 arriving. The roof checks do not validate supplier tooling, fleece compression, fixing capacity or weathertightness.


For the small fixed-camera video preview (requires `ffmpeg` on PATH):

```sh
/Applications/Blender.app/Contents/MacOS/Blender --background --disable-autoexec generated/coop-candidate.blend --python-exit-code 1 --python scripts/render_quick_preview.py
```

This writes `generated/construction-preview.mp4`, sampling every third master frame at 8 fps to preserve the 24 fps timeline duration. It uses temporary PNGs, cleans them afterwards and never saves changes to the Blender file. The quick preview is a sequence review, not the later narrated/camera-pan tutorial. `scripts/wall_layout.py` defines infill framing and non-rendering future nest/roost guides.
