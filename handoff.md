# Project handoff

## Current state — 22 September 2026

The user asked to work through the review and fix the system. They confirmed **12 hens, with room to reassess**, and said **10° is a fair provisional estimate of the slope**. Site/material inputs remain provisional. The user located the site in Coatesville, reports wind that is usually not too severe, and accepts crouched entry with outside flap access. Do not infer a verified wind zone from that description.

The working model is now generated from `coop_config.json` and `scripts/build_coop.py`. It contains four sequentially animated corrugated roof sheets, candidate bonded fleece, purlin isolation strips and the coordinated post/floor/roof skeleton, with real plywood notches and rafter seats, phase collections, visibility animation, markers and a Workbench camera. The generator validates geometry before saving. External source replaces the obsolete embedded Python; the file's embedded README is deliberately non-executable.

The old model is preserved as `review/original-coop.blend`; `coop.blend1` remains the older pre-roof backup. `REVIEW.md` and the other review evidence describe the original state. Do not regenerate from `review/embedded-script.txt`.

## Findings and disposition

| Review item | Current disposition |
| --- | --- |
| 1. Roof misses bearers | Geometry corrected: rearward 10.362° slope; six pole-clear rafters with twelve real seats. Connections and member capacity pending. |
| 2. Plywood notches fail | Corrected: baked notch geometry, no orphan cutters; installation paths checked against posts and panels. |
| 3. Post lengths/embedment conflict | Corrected geometrically: approximately 2951 front / 2909 rear, all from 3000 stock, 600 provisional embedment. Foundation design pending. |
| 4. Sheet support missing | Added five seam blocks, two shelf sisters and four shelf cross blocks. Fastening/end-support design pending. |
| 5. Bracing/load path absent | Open. Removed claims that the skeleton is rigid or structurally verified. |
| 6. Source cannot rebuild model | Corrected: external configuration, isolated generator, validation and regression checks. |
| 7. Hardware mismatch | M12 envelopes, outside-in heads, nuts/washers and consistent counts added. False solid-block hangers removed. Supplier-specific joints remain open. |
| 8. Joist spacing description | Corrected: six main joists at 470 plus two shelf-edge joists; all positions documented. |
| 9. Kerf/zero-waste claims | Corrected: two-sheet plan with 3 kerf, 3 gaps and explicit offcuts. |
| 10. Layout/capacity claims | Target is 12; usable-area description corrected. Roost/nest/ventilation/door layout still open; rear centre pole retained. |
| 11. Animation/deliverable | Phase collections, visibility, markers, camera and render settings added. Unbuilt enclosure phases remain explicit. |
| 12. API version claim | AGENTS.md now identifies Blender 4.4 as the Slotted Actions introduction. |

## Next design work

1. Resolve foundations, temporary/permanent bracing and structural connections using actual site/loading information. Pick compatible single/doubled-member and beam-end supports, then add their real geometry and fixing quantities. Do not treat illustrative bolt envelopes as approved connections.
2. Resolve the 12-hen interior: roost length/spacing, nest interiors and support, ventilation, human access/headroom, pop-hole/ramp and cleaning. The low roof is acceptable. Use outside flaps as the main service method and allow crouched entry. The user chose to lower the floor and roof together 450. The new floor clearances are approximately 628/906 at the post rows, with provisional 3000 pole stock. Internal headroom and roof pitch are unchanged.
3. Detail wall plate support and pole junctions, two rear clean-out openings, exposed shelf drainage and roof/wall flashings.
4. Extend the model and animation in build order, and update DESIGN.md, BUILD.md and SUPPLIES.md together. Quantify and price only after the materials are selected.

## Parts and costing status

SUPPLIES.md contains the component schedule, stock-length quotation list and dated advertised price references checked on 22 September 2026. Only floor plywood and bolt/nut assemblies are currently priced: $295.16 or $361.36 depending on the plywood alternative. Those figures are not a framing or whole-coop total. Poles, exact-section framing, foundations, remaining hardware and enclosure still require selection/quotations. No supplier messages or orders have been sent.

## Working instructions

Read AGENTS.md and README.md. Regenerate in a separate background Blender process; the generator refuses an interactive session. Use a candidate output path for development and validate it before replacing `coop.blend`. The saved scene ends at frame 680. Read `generated/model-report.json` and `generated/regression-results.json` for the latest checks.

Model units are metres internally and millimetres in the UI/docs. Keep actual timber dimensions distinct from nominal stock names. Never infer final transforms from an arbitrary animation frame. The generator captures them before animation and pins holds with ordinary key insertion. Geometric tests do not establish structural capacity or prove every construction step is safe.


## Latest addition: roof covering placement

User asked to add the actual next construction stage. Roof covering was added after purlins, conditional on resolving and installing the existing foundation/bracing/connection prerequisites. Frames 485–500 show isolation strips; 515–645 place four sheets individually; 660–680 hold. See DESIGN.md for the provisional profile/fleece choice and BUILD.md for erection conditions. Roof screws, edge flashings, drainage and wall junctions remain unmodelled. This is not a completed weathertight roof. SUPPLIES.md contains the four-sheet quotation quantities and NZ product links; no roof price has been verified.

Validation for this addition passed: 202 final roof-sheet collision pairs, 3692 integer-frame roof placement pairs, existing 946 framing pairs and 1301 floor placement pairs. Roof visibility and completed holds passed. Regression checks rejected a floating roof sheet, floating rafter, uncut plywood and insufficient pole stock. Candidate/report inputs match; final and roof-installation previews were inspected before promotion to `coop.blend`. These checks do not establish structural capacity, fixing adequacy or weathertightness.
