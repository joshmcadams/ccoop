# Project handoff

## Current state — 25 September 2026

The user asked for an audit of the documents and model for real-world buildability, sizing and appearance, and for every finding and its reasoning to be recorded in the Markdown files. [AUDIT.md](AUDIT.md) holds the dated findings, the reasoning and the disposition of each item. The user then made four decisions, now implemented and recorded in AGENTS.md, DESIGN.md, BUILD.md and SUPPLIES.md:

1. **Dressed timber:** 140 × 45 for all structural framing, 90 × 45 for walls and purlins. The user asked which was better and guessed dressed; Claude recommended dressed. **Rafters at 140 × 45 was Claude's choice**: it adds margin, keeps one structural section and gives taller eave vents. It costs roughly $40–60 more than 90 × 45, which remains an option after a span check.
2. **Pole tolerance rule:**
   - 120 nominal pole, 20 diameter allowance and 10 set-out tolerance, giving 20 clearance to all non-bearing timber.
   - Bearers bear on a 15-deep nominal flat with a bearing shoulder.
   - The validator enforces the clearance and a worst-case bolt length.
3. **Walls up to the roof, with eave vents:** front/rear top plates sit under the roof bearers and side plates under the edge rafters, parallel to the roof. Two eave purlins close the roof edge above ten rafter-bay vents (426 × 128 each, 0.546 m² gross).
4. **Nests on the shelves:** four 350 × 350 × 400 clear interiors, with the liner floor level with the side sole plate (Z=212) and a removable 100 lip board. The nest sill members were removed.

The model is generated from `coop_config.json` and `scripts/build_coop.py`, with `wall_layout.py`, `wall_cut_schedule.py` and `validate_coop.py`. The generator validates geometry before saving. `review/original-coop.blend`, `coop.blend1` and the review evidence are preserved; never regenerate from `review/embedded-script.txt`.

### Checks for this revision

**The generator passes all its checks:**
- 3741 final solid pairs with no intersections;
- 474 pole-clearance pairs;
- 6 wall top plates meeting the roof members;
- 10 clear eave vents;
- 8 clear openings;
- 12 rafter seats and 2 notched panels;
- 39679 wall and 32072 floor/roof-framing installation-path pairs, 8164 roof-sheet path pairs and 1301 plywood path pairs;
- phase ordering and completed holds.

**Installation-path checks** now also cover floor framing and roof framing. The floor bearers come in horizontally onto the pole shoulders; a vertical drop would pass through the poles (AUDIT finding 8).

**The regression suite rejects all eight deliberate faults:** floating rafter, uncut plywood, insufficient post stock, floating roof sheet, floating sole plate, a pole moved 5 mm inside its clearance envelope, a block left in an eave vent, and a bolt too short for the worst-case pole. The pole and vent cases were confirmed to fail for the intended reason.

**Visual inspection:** the final, wall, roof and floor previews, close-ups of the pole flats, notches, eave vents, side elevation and nest wall, and a contact sheet of the 37.5 s quick preview were inspected before promotion. These checks do not establish structural capacity, fixing adequacy or weathertightness.

## Open items, in rough priority

1. **Foundations, bracing and connections.** Resolve footings from actual site and loading information; the 600 embedment is shallow for this pole height. Front poles have about 53 spare on 3.0 m stock, so deeper footings mean 3.6 m poles. Walls now touch the roof members and so share load in practice; include them in the bracing and load-path design without claiming a rating.
2. **Joist-end supports (AUDIT finding 2).** Standard face-fixed hangers do not fit at 12 of 20 joist ends: edge joists, sisters and shelf-edge joists. Choose a detail — ledgers, bolting to the pole, concealed flanges or joists on bearers — then model it.
3. **Pole junctions (finding 4).** Scribed collars at the floor notches, which are larger now and rat-sized, and corner studs outside the corner poles so cladding can run past them.
4. **Enclosure.** Cladding, vent mesh, profiled closures over the eave purlins, blocking or mesh in the 45 gaps above the edge rafters, and flashings. Check net vent area once the mesh is chosen.
5. **Nests (finding 5, partly resolved).** Model the shells, liners and battens, lip boards and lids. The shelf lengths beyond the shells remain exposed: extend the enclosure or cap and flash them. The roof reaches only about 70 past the shells, so lids need weathering.
6. **Measured poles.** Once poles are delivered, measure their diameters at floor and roof levels and update the configuration if they exceed 140.
7. **Model polish (finding 7).** Posts pass through the ground mesh without holes. Camera framing is loose, the ground tile edges show, there are no fascia or barge boards, and all timber is one colour. The tutorial pass needs 24 fps output, call-outs and camera movement.
8. **Costing.** Only plywood and bolts are priced; the 140 × 45 framing has an indicative per-metre reference. Poles, 90 × 45, roofing and hardware need quotations. A consolidated purchasing table now heads SUPPLIES.md.
9. **Version control.** The 22 September wall revision and this revision are both uncommitted since `725f491`. Committing is the user's call.

## Working instructions

Read AGENTS.md and README.md. Regenerate in a separate background Blender process; the generator refuses an interactive session. Use a candidate output path for development and validate it before replacing `coop.blend`. The saved scene ends at frame 900. Read `generated/model-report.json` and `generated/regression-results.json` for the latest checks.

Model units are metres internally and millimetres in the UI/docs. Keep actual timber dimensions distinct from nominal stock names. Never infer final transforms from an arbitrary animation frame. The generator captures them before animation and pins holds with ordinary key insertion. Geometric tests do not establish structural capacity or prove every construction step is safe.

## History

- **Original review** (`REVIEW.md`, `review/`): twelve findings on the first model, all dispositioned in the 22 September rebuild. Roof seats, plywood notches, pole lengths, sheet support, reproducible source, hardware counts, joist spacing and kerf claims were corrected. Bracing, footings and connections remained open, and still are.
- **22 September 2026:** floor and roof lowered 450 together. Roof covering added: four fleece-backed corrugated sheets and isolation strips. Wall framing, eight rough openings and nest/roost guides added, with walls before roof in the animation.
- **25 September 2026:** audit and the four decisions above.
