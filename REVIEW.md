# Coop design, Blender and code review

Historical review of the pre-repair file. See [handoff.md](handoff.md) for correction status and [DESIGN.md](DESIGN.md) for the current coordination design.

Reviewed 22 September 2026. **The project is a useful concept model, but it is not ready to serve as a construction manual.** At the time of this review, the original geometry contained disconnected roof members and uncut plywood penetrations, and the original documents overstated how resolved the structure was.

The initial review left the original `.blend`, backup and Markdown files unchanged. Subsequent repair work is recorded in handoff.md. Findings and line references below describe that original snapshot, not the current files; this report is retained as historical evidence.

Evidence: [frame 285 preview](review/frame-285.png), [scene measurements](review/scene-audit.json), and [embedded Text script](review/embedded-script.txt). The preview uses a temporary review camera; the supplied file has no camera. Distances below are millimetres unless noted. Front is negative Y, rear is positive Y.

## High-priority findings

### 1. Roof rafters do not bear on either roof bearer — P1

**Location:** `coop.blend`: `Roof_Rafter_0`–`4`, `Roof_Bearer_Front`, `Roof_Bearer_Back`; `handoff.md:10`.

The front bearer top is Z=2340 and the rear bearer top is Z=2020. They require a roof falling towards positive Y. All five rafters instead rotate **+10.36° about X**, so their height increases towards positive Y. At the bearer centre lines:

| Position | Bearer vertical extent | Rafter vertical extent | Result |
| --- | --- | --- | --- |
| Front, Y=-875 | 2190–2340 | 2019–2121 | Rafter is below the bearer, separated by about 69 |
| Rear, Y=875 | 1870–2020 | 2339–2441 | Rafter floats about 319 above the bearer |

These are evaluated final placements, not transient assembly positions. The handoff's 4.9° claim also disagrees with the saved 10.36° geometry. Rear posts extend to Z=2195, about 175 above their bearer top; simply reversing the rafter rotation does not resolve all post/roof intersections or bearing details.

**Fix:** Derive the roof plane, pole tops, bearer heights and rafter bearing seats from one shared set of elevations. Model the selected connections and uplift restraints. Do not continue wall framing from the present roof. Select the roof covering before fixing pitch: for example, [Metalcraft Corrugate specifies an 8° minimum after deflection](https://www.metalcraftgroup.co.nz/products/roofing-and-cladding/products/corrugate/), so the documented 4.9° is not suitable for that product.

### 2. The plywood notches are nonfunctional — P1

**Location:** `coop.blend`: `Ply_Back`, `Ply_Front`, their `Cut_0`–`Cut_2` modifiers and cutter children; `BUILD.md:18`; `handoff.md:9`.

After modifier evaluation, each main panel still has eight vertices and six faces: both remain solid rectangular boxes. All six posts intersect the floor. At the completed state, the cutters occupy Z=-100…100, while the plywood occupies Z=600…617. The cutters' parent-inverse transforms cancel the intended panel offset; their Y positions are also wrong in world space. Each panel additionally has a `Cutters` Boolean modifier with no operand object.

**Fix:** Establish cutter coordinates consistently in panel-local space, with a deliberate parent inverse. Confirm each cutter overlaps its panel at the intended post location. Verify evaluated geometry and the whole insertion path, then remove empty modifiers. Animate the installation method specified in BUILD.md: sheets currently descend vertically while the instructions describe sliding them around the posts.

### 3. Post lengths and embedment contradict the build instructions — P1

**Location:** `coop.blend`: `Post_0`–`5`, `Ground`; `DESIGN.md:15–16`; `BUILD.md:7–8`; `SUPPLIES.md:6–7`.

Ground elevation at a post centre is `-0.6 - tan(10°) * Y` metres. Measured from that plane:

| Row | Model post length | Model embedment | Documented stock / embedment |
| --- | --- | --- | --- |
| Front | 3451 | 645 | 3600 / 600 |
| Rear | 3149 | 215 | 3000 / 600 |

The rear members cannot be cut from the purchased stock and do not reach the documented depth. Holding their present top elevation while restoring 600 embedment would require approximately 3534-long rear posts. That is diagnostic arithmetic, not a final post specification: roof heights must be resolved first.

**Fix:** Set ground elevations, footing bottoms and roof elevations independently, then derive each post length. Record actual site slope and select stock after those values are reconciled. Also review the specified H4 fence posts for this structural use: [Goldpine's treatment guidance identifies H5 for structural ground-contact applications](https://goldpine.co.nz/products/piling-systems/h5-building-poles-and-piles/treatment). Treatment is not a substitute for confirming pole grade, diameter and load capacity.

### 4. Floor seams and shelf edges lack a complete support detail — P1

**Location:** `DESIGN.md:21,23`; `BUILD.md:18–19`; `coop.blend`: `Ply_Front`, `Ply_Back`, `Ply_Cantilever_L/R`, `Joist_1/6`.

There is a 2400-long sheet joint at Y=-300, contrary to the claim that there are no sheet seams to match. No blocking is modelled beneath this joint between joists, and neither the purchasing list nor instructions specify a retained tongue-and-groove joint.

The shelf panels begin at X=±1200. The adjacent main-floor edge joists terminate at that same line, so the shelves have no bearing width on those joists along their inner edges. A shared sheet seam needs actual support width and fastening edge distances. The shelf strips also have a different grain orientation from the main floor when cut as described.

**Fix:** Detail support under the main square-edge joint and both shelf junctions, or specify a suitable proprietary flooring joint where applicable. Show panel orientation, bearing, fixing positions and expansion gaps. [CHH's Ecoply guide](https://chhply.co.nz/assets/Uploads/EcoplySpecificationInstallationGuideCurrent.pdf) distinguishes supported square edges from tongue-and-groove joints, requires face grain across supports, and specifies movement allowances. Verify the selected panel grade/thickness against the actual span and loading; spacing symmetry alone is not a strength check.

### 5. The build sequence asserts rigidity without defining bracing or connections — P1

**Location:** `BUILD.md:5–9,21–25`; `handoff.md:13`; `DESIGN.md:20,23–25`.

The files specify neither temporary bracing during erection nor a permanent lateral bracing system. The model has no roof-bearer bolts, rafter restraints or purlins. Placing roof members across posts does not, by itself, establish the rigidity asserted in BUILD.md. No site wind/soil assumptions, member strength grades, footing diameter, anchorage design or connection capacities establish the load path. The six-bag concrete allowance cannot be checked without footing dimensions and bag yield.

**Fix:** Resolve foundation, bracing and connections before presenting the skeleton as complete. Include temporary bracing and concrete curing in the sequence. Show how gravity, lateral and uplift loads reach the foundations, including the cantilevered nest loads. Document the basis for sizes and fasteners; remove unconditional claims such as “structurally perfect” until substantiated.

### 6. The only source script cannot reproduce the current project — P1

**Location:** `coop.blend` text block `Text`, especially lines 4–6 and 30–64; [extracted source](review/embedded-script.txt).

The script begins with global selection/deletion and regenerates an older concept: posts on the original 2400×1800 grid, different bearer sections, a single thick floor, primitive walls and doors, and no current construction animation. Running it is a destructive regression, not a rebuild of the saved scene. There is no external generator or change history for the later model operations among the supplied files.

**Fix:** Preserve this script as a clearly labelled legacy reference. Create a current generator with a single dimension specification, explicit build phases and cleanup scoped to its own collections. Separate geometry creation from animation. Store final transforms independently of the current timeline, and validate the regenerated result before replacing the working file.

## Other corrections needed

### 7. Hardware is inconsistent across the model, design and shopping list — P2

**Location:** `SUPPLIES.md:13–14`; `BUILD.md:14`; `coop.blend`: `Bolt_*`, `Hanger_*`.

- BUILD calls for twelve M12×200 carriage bolts; SUPPLIES instead lists twelve lag/coach screws. Nuts, washers and hanger fasteners are not itemised.
- Model bolt shafts are **16 diameter**, not M12. Heads are hexagonal prisms rather than carriage-bolt domes, and washers are absent. Outside-in direction is correct, but the threads protrude beyond the inner post face; they are not “inside the post” as the prose says.
- Each hanger is a solid 54×50×100 cuboid overlapping the joist, not a steel U-shaped support. Its flanges, seat, fastener positions and end-of-bearer clearances cannot be assessed from this placeholder.
- The model uses actual 50-wide joists, while the list specifies 47-wide hangers. “Nominal 50” and actual 50 are not interchangeable. [MiTek distinguishes hanger sizes and their fastening schedules](https://miteknz.co.nz/wp-content/uploads/2024/02/MiTek-NZ-On-site-Guide-2024-Edition.pdf); confirm the actual timber finish and compatible connector.

**Fix:** Select real hardware first, then use its dimensions in the model and quantities in the list. Model enough of each connector to check clearances, bearing, installation access and fastening into timber. Check bolt spacing/edge distances and bearing on round posts.

### 8. Eight joists are not all at 470 centres — P2

**Location:** `DESIGN.md:23`; `BUILD.md:15`; `handoff.md:8`.

The model has eight joists, correctly including two shelf-edge joists, with centre positions:

`-1475, -1175, -705, -235, 235, 705, 1175, 1475`.

The consecutive spacings are `300, 470, 470, 470, 470, 470, 300`. Six joists form the main floor; the additional two close the shelves. The outermost two form a 3000-wide platform, not a 2400-wide box. The main 2350 measurement is between edge-joist centres, not an internal clear dimension. The chosen arrangement does avoid the central bolt shafts in final position, but that does not resolve the missing panel supports.

**Fix:** Publish the positions or a dimensioned framing plan and distinguish main-floor joists from shelf joists. Retain the useful symmetry if the final floor-support and hardware checks permit it.

### 9. The two-sheet cutting plan ignores kerf and overclaims zero waste — P2

**Location:** `DESIGN.md:5,21`; `BUILD.md:17–19`; `handoff.md:9`.

Two exact 600 strips cannot be cut from a 1200 sheet once saw kerf is included; two exact 300 strips cannot then be cut from the remaining 600 strip. The proposed crosscuts also leave two nominal 600×300 offcuts, totalling 0.36 m², before notches and kerf. This can still be an efficient two-sheet scheme, but the exact dimensions and “zero waste” claims are false as written.

**Fix:** Produce a kerf-aware nesting diagram with actual finished widths and manufacturer-required gaps. Identify a use for the remaining offcuts rather than pretending they do not exist. The existing cost arithmetic does sum correctly to $633; it is an incomplete, unverified estimate, not a current project budget.

### 10. The proposed wall and flock layout remains unresolved — P2

**Location:** `DESIGN.md:4,8–11,25,30`; `BUILD.md:28–34`.

2400×1800 describes the main platform's outside dimensions, not clear internal space. With 90-thick walls flush to those edges, the nominal inside rectangle is 2220×1620 = **3.5964 m²**, before post projections and fittings. Calling 4.32 m² “extremely generous” for 20 birds is unsupported by a completed layout.

There are no current roosts, nest compartments, ventilation openings, doors, wall frames, cladding, roof sheets or ramp in the saved scene. The 300-deep shelf is a support allowance, not proof of usable nest-box depth. A continuous full-width rear clean-out opening is interrupted by the rear centre post. Wall plates meeting the round posts also need actual junction details. A cladding skirt alone does not detail the waterproof transition to a level exposed shelf.

**Fix:** Dimension usable nest interiors, roost length/spacing, ventilation, door access, cleaning access and weatherproof junctions. Resolve the rear hatch as multiple openings or a deliberately redesigned structure. Confirm flock capacity from the finished usable layout and management assumptions. [MPI's layer-hen code](https://www.mpi.govt.nz/animals/animal-welfare/codes/all-animal-welfare-codes/code-of-welfare-layer-hens) addresses access to perches, nests and suitable housing; gross platform area alone is not enough evidence.

### 11. The animation is lightweight but not a finished deliverable — P2

**Location:** `coop.blend`: Scene and collection organisation; `handoff.md:6–13`.

The file contains 94 mesh objects, 1804 source vertices, 79 actions and 12,762 scalar keyframe points, all in one collection. There are no cameras, lights or timeline markers. A normal scene render has no assigned camera. Dense hold keys are not a meaningful performance problem at this size, and there is no reason to sacrifice individual construction parts by merging them.

The general order is sensible: posts settle, bearers and bolts assemble, hangers precede joists, plywood follows, and roof members arrive last. Rafters finish arriving by frame 283. Some final hold keys extend to 333 beyond the scene end of 300; this does **not** truncate their actual assembly. Sampling integer frames 1–333 found no more than 1 mm of drift between equal-value hold keys. This does not test every subframe or prove that moving parts avoid collisions.

**Fix:** After correcting geometry, organise components into phase collections, add phase markers and useful pause durations, and provide an intentional camera/render setup. Keep the simple geometry; spend effort on accurate joints and explanatory views. Purlins and the other unbuilt phases must be labelled as pending in the handoff.

### 12. Agent documentation misdates the animation API change — P3

**Location:** `AGENTS.md:13`; `handoff.md:32`.

Slotted Actions were introduced in **Blender 4.4**, not 4.3. Avoiding assumptions about `action.fcurves` is sensible, but the version claim should follow [Blender's official migration guide](https://developer.blender.org/docs/release_notes/4.4/upgrading/slotted_actions/). Keeping simple `keyframe_insert` calls is appropriate. The existing per-frame hold policy was respected during this read-only review.

## Recommended order of repair

1. Establish one dimensional specification: site ground levels, finished floor level, actual timber sizes/grades, usable interior dimensions, roof covering and roof elevations.
2. Resolve footing/post specification, permanent and temporary bracing, bearer connections and uplift restraint. Derive post lengths and purchase stock from those decisions.
3. Correct the floor's seam supports, shelf bearing and hardware geometry. Produce the final joist coordinates and kerf-aware plywood cutting plan.
4. Correct the roof plane, bearing seats, pole clearances, connections and purlins. Check construction access before enclosing anything.
5. Complete the wall, nest, roost, ventilation, hatch and flashing layout, including usable flock space.
6. Record these decisions together in DESIGN.md and BUILD.md, replace provisional quantities in SUPPLIES.md, and make handoff.md describe only verified completed work.
7. Implement a reproducible generator and staged animation. Check final contact/clearance geometry, then scrub assembly paths. Add phase labels, camera views and render settings last.

## Review coverage and limits

All five Markdown files and the embedded Python were read. The main file was opened in background Blender 5.2.1 LTS with automatic script execution disabled. Object transforms, dimensions, modifiers, parenting, keyframe data and scene settings were inspected; the plywood was checked after dependency-graph evaluation, roof contact was calculated, and a temporary-camera preview was rendered and visually inspected. Neither source Blender file was saved or modified. The backup was inventoried separately: 87 objects, no roof objects, frame range 1–240; it predates the current roof work and is not an alternate completed design.

This review verifies the stated geometric/documentary discrepancies. It does not establish structural capacities, certify footing sizes, verify current retail prices or exhaustively test all mesh-pair collisions. Those questions need the missing product and site specifications; they should remain explicit design tasks rather than be treated as resolved by the animation.
