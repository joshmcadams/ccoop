# Agent Memory & Best Practices

## Start Here

Read [handoff.md](handoff.md) for current progress, [DESIGN.md](DESIGN.md) for design decisions, [BUILD.md](BUILD.md) for the intended construction sequence, and [README.md](README.md) for commands. Check [SUPPLIES.md](SUPPLIES.md) when changing parts or quantities.

This project is a **geometry coordination draft**, not a completed construction release. Geometry checks do not establish structural capacity. Foundations, temporary/permanent bracing, supplier-specific connectors, wall framing, nests, ventilation and enclosure details remain unresolved. Hatches are a documented proposal, not modelled parts. Preserve these distinctions when reporting progress.

## Current User Decisions

- Design for **12 hens**, with room to reassess once the interior is dimensioned.
- Site: **Coatesville, Auckland, New Zealand**. The user reports some wind, usually not severe; the wind zone is unverified. The **10° ground slope** is a reasonable provisional estimate, not a survey.
- Outside flap access is preferred; crouched entry is acceptable. **Standing headroom is not required.**
- The user approved lowering the floor and roof together **450 mm**. Do not revert to the old elevations or raise the roof for standing access.
- Current framing top is **Z=150 mm**, plywood top **Z=167 mm**; roof bearer tops are **Z=1890 mm front / 1570 mm rear**. Z=0 is a modelling datum, not ground.
- The floor is approximately **628 mm front / 906 mm rear** above provisional ground at the pole rows. Pole cuts are approximately **2951 / 2909 mm**, fitting provisional **3.0 m stock** with the current 600 mm embedment assumption.
- Retain the **2400 × 1800 mm main platform**, **3.0 m uncut floor bearers** and rear centre pole. Plan separate rear clean-out openings around that pole.
- No existing material inventory has been specified. Actual site levels, timber grades/sections and foundation design must be resolved before a purchase/cut list is final.

These are the current baseline decisions. When the user changes them, update the inputs and affected documents together; do not let this summary become a competing source of dimensions.

## Source of Truth and Safe Workflow

1. Edit `coop_config.json` for supported inputs and `scripts/build_coop.py` for geometry/animation. Update `scripts/validate_coop.py` and `scripts/check_regressions.py` when the design changes what must be checked. Some footprint/section values are intentionally fixed by the validator; changing them requires revisiting the joints and cutting plan, not bypassing the check.
2. Treat `coop.blend`, `generated/model-report.json` and rendered previews as generated outputs. Do not make an unrecorded fix only in the binary. The Blender file contains an informational README and a configuration snapshot, not the generator.
3. Run the generator in a **separate background Blender process**, initially writing `generated/coop-candidate.blend`. It resets that isolated process to an empty scene and refuses interactive execution. Never transplant its factory reset into the user's open Blender session.
4. Follow the candidate build and regression commands in README.md. Inspect the relevant final and assembly views. Confirm the report's configuration matches `coop_config.json`. Promote the candidate to `coop.blend` only after the required checks pass. Keep previews and test reports current for the promoted model.
5. Preserve `review/original-coop.blend`, `coop.blend1` and the historical review evidence. **Never run `review/embedded-script.txt`**: it is the obsolete destructive generator. `REVIEW.md` describes the original file and its original document line numbers; use handoff.md for correction status.
6. For each major design change, update DESIGN.md and BUILD.md with both the decision and its reason; update SUPPLIES.md for quantities, handoff.md for status/next work, and this file when durable user decisions or workflow rules change. Update README.md when commands or validation coverage change.
7. Report what was changed, what was checked and what remains unresolved. Do not turn illustrative hardware, provisional sizes or a passing collision check into a claim of structural approval. Do not mark an unmodelled phase complete.

The generator checks final timber/post/plywood intersections, notch volumes, rafter seats, stock/embedment arithmetic, kerf allowances, integer-frame plywood and roof-sheet installation paths, roof sheet/support/lap geometry and selected completed holds. It does **not** check structural capacity, all moving assemblies, every subframe, terrain/footings or supplier-specific hardware fit. Read the actual validation code before expanding those claims.


## Working with the User

* **Real-World Buildability:** The user expects the 3D model to accurately reflect real-world construction. Do not use "magic" or clipping. Think about how the builder will actually assemble this.
* **Material Efficiency:** Always default to standard New Zealand lumber/sheet sizes (e.g., 2400x1200mm plywood, 150x50mm timber, 3.0m/3.6m lengths). Design to minimize cuts and waste (like using uncut 3.0m bearers for cantilevers). Include saw kerf, expansion gaps, actual finished timber sizes and usable offcuts; do not promise zero waste without a demonstrated cutting plan.
* **Hardware & Collisions:** Think three steps ahead about hardware. A joist cannot sit where a bolt protrudes. Carriage bolts must face outside-in. This keeps smooth heads outside, but protruding inner thread ends still need clearance and protection wherever accessible.
* **Conversational Pace:** The user often prefers to discuss a structural problem conceptually before committing to a code change (e.g., "Don't make a change yet, just chat with me"). Validate their intuition, lay out the physical realities (like standard spacing math), and align on a plan before touching the files.
* **Documentation is Key:** It is not enough to just update the 3D model. Every major structural decision MUST be documented in `DESIGN.md` and `BUILD.md` so the "why" is preserved for the actual build day.
* **Animation Sequencing:** The user loves logical, sequential construction animations. The sequence must follow actual physical build logic (e.g., Posts -> Floor -> Roof Framing -> Walls -> Nesting Boxes -> Cladding).

## Parts and Cost Tracking

Keep SUPPLIES.md consistent with model quantities and the stock cutting plan. Separate finished parts from purchased stock to avoid charging twice for reused offcuts. Record price source, date, currency, GST basis, stock length, actual section/grade and delivery exclusions. Label unpriced items explicitly; never treat them as zero or call a priced subset the whole-coop estimate. Do not sum alternative products, double-count nuts included with bolts, or substitute different timber sections/treatment to fill a price. Current pricing covers only floor plywood and bolt/nut assemblies; see SUPPLIES.md for the remaining quote requirements.

## Working with Blender via Python

* **Bezier Curve Overshoot:** When animating a "hold" or "wait" period where an object stays still before moving again, Blender's default Bezier interpolation will often cause the object to wildly dip or overshoot. To fix this safely, loop through the hold frames and explicitly `keyframe_insert` the location on every single frame to pin it.
* **Avoid F-Curve API Hacks:** Blender 4.4 introduced Slotted Actions, so do not assume `obj.animation_data.action.fcurves` exists on the installed version. Stick to `keyframe_insert` and simple loop pinning instead of trying to hack interpolation types via the F-Curve API.
* **Clean State:** The background generator starts from an empty scene. For any incremental operation, identify and remove only the procedural objects it owns before regeneration; never globally delete unrelated or user-created geometry. Remove obsolete helper meshes/modifiers as well as visible objects, and verify that reruns do not accumulate duplicates.
* **Keyframe State Hazards:** Never read `obj.location` as a baseline for math if you haven't explicitly set the timeline (`bpy.context.scene.frame_set()`) to the correct frame first, otherwise you might grab an unintended mid-animation coordinate.
* **Targeting Objects:** When targeting objects in loops, be absolutely sure of their internal Blender names (`obj.name`) rather than assuming human names.


## Roof Covering Baseline

The roof covering placement stage now follows purlins. Current scene ends at frame 680; frame 465 shows bare roof framing. Four 2400-long representative corrugated sheets use 845 overall width / 762 cover, candidate factory fleece and five isolation strips. These are provisional product choices, not new user-approved purchasing specifications. Preserve the distinction between sheet placement and a secured, weatherproof roof: actual fixings, edge flashings, ventilation, drainage and structural prerequisites remain open. Update roof quantities, geometry checks and animation when selecting the final product; do not replace fleece-backed sheets with plain sheets without first designing and sequencing condensation control.
