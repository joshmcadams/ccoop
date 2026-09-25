# Design audit — 25 September 2026

The user asked for a check that the documentation is sound and that the Blender model is appropriately sized, physically buildable and pleasant to look at. This file records what was checked, what was found and why, and how each finding was dispositioned. **Measurements quoted in the findings describe the model as audited, before the 25 September revision.** Current dimensions live in `coop_config.json`, DESIGN.md and `generated/model-report.json`; do not copy numbers from this record into new work.

## How the audit was done

- Read every Markdown file, the configuration, the generator, the wall layout and cut-schedule scripts, the validator and the regression script.
- Confirmed `coop.blend` was byte-identical to the validated candidate, that the report's recorded configuration matched `coop_config.json`, and re-ran the regression suite from a scratch copy (results identical to the committed `regression-results.json`).
- Ran an independent read-only inspection of `coop.blend` in background Blender: dimension inventory, clearances at every pole interface, wall-top gaps, overhangs, heights above provisional ground, bolt thread, notch gaps, material slots and terrain intersections.
- Rendered close-ups (corner junction from above, floor framing from below, side and front elevations, roof/pole corner from inside, nest side) and a contact sheet of the construction video.
- Searched for a better wall-framing cut plan than the generated first-fit schedule.

## What checked out

- **Documents agree with the model.** Post lengths, joist centres, notch sizes, opening sizes, animation markers, stock totals and price arithmetic in DESIGN, BUILD, SUPPLIES, AGENTS and README all matched the generator and report.
- **Build sequence is physically sensible.** The rear plywood sheet lowers between the pole rows and slides onto its notches; the front sheet clears it; wall rails slide in through the open wall faces; walls precede the roof.
- **Heights relative to the provisional ground are practical:** pop-hole sill about 650 above ground on the uphill (short-ramp) side; rear clean-out sill about 970, near wheelbarrow height, on the downhill side; roosts well above the nests so hens are not encouraged to sleep in them.
- **Waste control is good for the modelled parts:** a two-sheet plywood plan with named offcuts; uncut 3.0 m bearers and purlins; uncut 2.4 m rafters; 32.4 m of floor/roof-bearer stock for 30.7 m of parts. For wall framing, the 24 long studs/jambs fit only two per 3.0 m stick, so the 16-stick schedule was effectively minimal; only the last stick (1.18 m used) could have been a 2.4 m length.
- **The look is clean and legible.** The 10.4° roof almost parallels the 10° ground, so both eaves sit about 2.5 m above ground and the building sits naturally on the slope.

## Findings

### 1. Zero clearance around the round poles — highest priority

The corner poles were positioned exactly tangent to the bearers, the main-floor edge joists and the edge rafters (0 mm). Beside each corner pole the edge rafter's underside ran 25–37 mm below the pole top with no side clearance. Three different tolerance rules applied to the same poles: 0 mm at the framing, 5 mm per side at the plywood notches, 25 mm at the walls. M12×200 bolts left only 16 mm of thread past the nut, and only for a perfect 120 mm pole.

**Why it matters:** H5 round poles are sold by small-end diameter and taper toward the butt. The floor connection is about 1.8 m below the pole top, so the pole is fatter there than its nominal size, and poles set in concrete are not placed to the millimetre. The model would have produced clashes at the edge joists and rafters, notches too tight to fit and bolts too short. The bearers also touched a curved surface along a single line, so gravity load relied entirely on bolt shear.

**Why the validator missed it:** it only rejects overlapping volume. A tangent contact has zero overlap, so it passes; a pole 1 mm fatter would have failed.

### 2. Standard joist hangers could not fit at 12 of the 20 joist ends

Each main edge joist had a pole on one side (3–15 mm off the bearer face) and its sister member hard against the other; the sister shared that constraint; each shelf-edge joist finished at the bearer end, so a face-fixed hanger's outer flange would hang off the end. The docs framed this as product selection, but it probably needs a geometry change: ledgers, bolting the edge joist to the pole, or joists sitting on the bearers.

### 3. Wall frames were only fixed at their sole plates

Top plates stopped 90 mm (front) and 70 mm (rear) below the roof bearers and 198–242 mm below the edge rafters; jambs stopped 25–33 mm from the poles. Each frame was a free-standing rectangle. Front/rear cladding could have bridged to the bearers, but the wedge-shaped strip above each side wall had nothing to fix to, and the side top plates sloped at 12.1° against the roof's 10.4°, adding bevel angles. Recommendation: take the walls up to the roof members, side plates parallel to the roof, and use the rafter bays above the bearers as mesh-covered high vents, which need closing anyway.

### 4. Pole junctions are a predator item, not only a weather item

A rectangular notch around a round pole left corner gaps that pass a 26 mm probe straight up through the floor into the coop — rat-sized. There were also L-shaped openings around each corner pole and 170 mm gaps either side of the centre poles. Because each pole sits inside the outer wall faces, exterior cladding can run continuously past the poles; it needs a small corner stud outside each corner pole and a sealed collar at floor level.

### 5. Exposed shelves and raised nests

The 300 mm shelves are horizontal plywood outside the walls, and the roof extends only 65–70 mm beyond them from about 2 m up, so they will get wet. The nest floors sat 300 mm above the shelves, leaving an open void, so the shelves had no clear function.

### 6. Timber sections and pole stock

The model used actual 150 × 50 and 100 × 50: rough-sawn sizes that vary by a few millimetres. The most common NZ retail framing is dressed (gauged) 140 × 45 and 90 × 45. Combined with finding 1, the purchased section had to be chosen before any quote. Separately, 600 mm embedment left only 49 mm spare on the 3.0 m front poles; any deeper footing means 3.6 m poles.

### 7. Minor model realism

- All six posts passed through the ground mesh (about 456 cm³ each, no holes) while dropping in and in the final state, contrary to the no-clipping rule; the validator deliberately skips terrain.
- Eight Boolean-cut parts carried an empty second material slot. Harmless: every face uses slot 0.

### 8. Found while implementing the pole rule — floor bearers clipped through the poles

The flats with bearing shoulders cover only the bearer depth, so above each flat the full round pole stands 15 mm proud of the bearer face. The animation still dropped the floor bearers vertically from 1.2 m, passing them through each pole. No installation-path check covered the floor or roof framing phases, so nothing caught it. This came out of the independent review after the first implementation pass. **Fixed:** floor bearers now come in horizontally from outside onto their shoulders, which is also how they would be fitted on site. New integer-frame path checks cover floor framing (frames 80–190) and roof framing (510–620). A scratch rebuild with the old vertical drop is rejected at frame 80.

### Against the project goals

- **Video instructions:** the 37.5 s fixed-camera preview (720 × 660, 8 fps) followed the build order correctly, but it is a sequence check, not yet instructions — no call-outs, dimensions or fixings. For the tutorial, 1280 × 720 at 24 fps would be smoother and more shareable.
- **Cost:** only the floor plywood and bolts were priced ($295.16 or $361.36 depending on the plywood alternative). Poles, framing timber, roofing, hangers and concrete were unpriced, so no whole-coop figure exists. Unpriced does not mean zero.
- **Look:** the coop sat low in the frame with about a third of the image empty; the hard edges of the 8 m ground tile showed in every frame; there were no fascia or barge boards, so raw rafter and purlin ends showed; all timber was one colour. Once cladding and nests are modelled it will read as a coop rather than a cage.

### Documentation housekeeping

- handoff.md carried older sections with superseded frame numbers and check counts.
- `floor-framing.png` and `floor-installation.png` predated the camera change and were not refreshed by `--render`.
- SUPPLIES.md had the roof and wall additions appended as separate sections rather than one purchasing table.
- The entire wall-framing revision (22 files) was uncommitted since `725f491`.

## User decisions — 25 September 2026

| Question | Decision | Reasoning |
| --- | --- | --- |
| Rough-sawn 150 × 50 or dressed 140 × 45? | **Dressed** (user's instinct, recommended) | Consistent to about 1 mm, which matters once pole clearances are 15–20 mm; stocked everywhere in standard lengths with the grade stamped; one structural section plus 90 × 45. About 25% less stiff than a true 150 × 50, still ample for a 1.7 m coop floor span. |
| Rafter section (follows from dressed: 100 × 50 has no dressed equivalent) | **140 × 45** (Claude's choice, flagged to the user) | Rafters have never been span-checked, so the extra margin helps; one structural section throughout; eave vents about 130 mm tall instead of about 80. Costs roughly $40–60 more than 90 × 45; a single config value if the user prefers to save it. |
| Add a pole tolerance rule? | **Yes** | Findings 1 and 6. |
| Walls up to the roof with eave vents? | **Yes, eave vents** | Finding 3. |
| Nests on the shelves or 300 mm up? | **On the shelves** | Finding 5. |

## Disposition

| Finding | Disposition |
| --- | --- |
| 1. Pole clearance | Addressed in the 25 September revision — see DESIGN.md "Pole tolerance rule". |
| 2. Hanger room | **Open.** Clearance helps the edge joists but does not by itself make room for a standard hanger flange beside the pole or at the bearer ends. Needs a chosen detail. |
| 3. Wall top restraint | Addressed — walls now reach the roof members; eave vents dimensioned. |
| 4. Pole junction gaps | **Open.** The larger clearance notches make sealed collars more important. Corner studs and collars belong to the enclosure stage. |
| 5. Shelves/nests | Partly addressed — nests now sit on the shelves. **Open:** shelf lengths beyond the nest shells remain exposed, and the roof still extends only about 70 mm past the nest shells. |
| 6. Sections and pole stock | Sections addressed (dressed). **Open:** embedment/footing design and 3.0 vs 3.6 m poles. |
| 7. Ground clipping | **Open**, low priority. |
| 8. Bearer path through poles | Fixed in this revision; floor and roof framing paths are now validated. |
| Goals: video, cost, look | **Open** — tutorial pass, quotations and presentation polish follow the construction design. |
| Documentation housekeeping | Addressed in this revision: handoff.md pruned to current state plus a short history; floor previews added to `--render`; SUPPLIES.md reorganised around one stock-to-buy table. Committing is the user's call. |
