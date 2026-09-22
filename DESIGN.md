# Coop design decisions

## Status and source of truth

This is a **geometry coordination draft for 12 hens**, with room to reassess capacity after the interior layout is drawn. It is not a completed structural design or a construction release. The user confirmed that the 10° ground slope is a fair estimate; site levels and material sizes remain provisional. No existing stock constrains the design at present. The site is Coatesville, north of Auckland. The user reports some wind, typically not severe; this is not a verified wind-zone classification. Standing headroom is not required: outside flap access is preferred, with occasional crouched entry acceptable.

`coop_config.json` holds the model inputs. `scripts/build_coop.py` regenerates `coop.blend` in an isolated background Blender process. `generated/model-report.json` records derived dimensions and geometric checks. See `README.md` for commands. The generator deliberately retains the reviewed platform dimensions; changing the footprint requires revisiting the cutting layout and joint details, not just changing a number.

`REVIEW.md` describes the original model. The correction status is tracked in `handoff.md`; the original Blender files and review evidence remain available.

## Dimensions and floor arrangement

All dimensions below are millimetres. Front is negative Y, rear/downhill is positive Y. Z=0 is a modelling datum, not ground level.

| Item | Coordination value |
| --- | --- |
| Main platform outside dimensions | 2400 × 1800 |
| Platform including both side shelves | 3000 × 1800 |
| Floor framing top / plywood top | Z=150 / Z=167 |
| Floor bearers | Two uncut 3000 × 150 × 50 |
| Post grid, centre to centre | 2180 × 1580; three posts per row |
| Round post diameter | 120, pending structural pole selection |
| Main joist centres X | -1175, -705, -235, 235, 705, 1175 |
| Additional shelf-edge joist centres X | -1475, 1475 |
| Joist length / section | 1700 / actual 150 × 50 |
| Consecutive joist spacings | 300, 470, 470, 470, 470, 470, 300 |

The floor's outside dimensions are not its usable interior dimensions. With future 90-thick walls flush to the main platform edges, the nominal internal rectangle is 2220 × 1620, or 3.5964 m², before post projections and fittings. Capacity remains a layout decision; no claim of suitability for 20 hens is retained.

The 470 spacing keeps the main joists clear of the central post bolts. It is a layout choice, not a structural span verification. Timber dimensions in the current model are **actual**, not nominal; a change to dressed sections changes the fit of the framing and connectors.

## Ground, posts and foundations

Ground elevation at a post is `-600 - tan(10°) × Y`. The current 600 embedment is a coordination assumption, not a sized footing. It is measured from ground at each pole centre. All pole lengths are derived from the ground, embedment and roof-bearer elevations independently.

| Row | Ground Z | Post bottom Z | Post top Z | Cut length | Stock allowance |
| --- | --- | --- | --- | --- | --- |
| Front | -460.7 | -1060.7 | 1890 | 2950.7 | 3000 |
| Rear | -739.3 | -1339.3 | 1570 | 2909.3 | 3000 |

The design intent is **H5 structural poles**, replacing the earlier H4 fence-post assumption. [Goldpine's treatment guidance](https://goldpine.co.nz/products/piling-systems/h5-building-poles-and-piles/treatment) distinguishes structural ground-contact uses. Grade, diameter, footing depth/diameter, soil suitability and anchorage still need resolution against the actual site loads. There is no six-bag concrete estimate: quantity depends on the selected footing dimensions and bag yield.

Temporary bracing, concrete curing and a permanent lateral/uplift load path are required design tasks. Roof framing alone is not treated as sufficient bracing. These unresolved assemblies are explicitly listed in the Blender scene and build sequence, rather than represented by invented connections.

## Floor bearing, seams and plywood

The two main floor edge joists receive an additional 1700 × 150 × 50 sister member on their shelf sides. The main sheet bears on the original joist; each shelf panel bears on its added sister with 47 bearing width after the 3 sheet gap. This changes the old unsupported shelf seam into a real timber bearing arrangement. **The doubled-member connections and end support remain to be selected.**

Five 420 × 150 × 50 blocks support the main sheet seam at Y=-301.5 between the six main joists. Two additional 200 × 150 × 50 cross blocks per shelf support the reused strips at Y=±283.3. Their face grain runs front-to-back, so those cross blocks provide support across the grain direction. Sister members, blocking and their fastening requirements must all be included in the material and connection schedule.

The adopted cutting layout assumes two 2400 × 1200 × 17 sheets, a **3 mm saw kerf** and **3 mm inter-panel gaps**:

1. Sheet A stays 2400 × 1200, except for its post notches, and covers the rear portion from Y=-300 to Y=900.
2. Rip Sheet B to a 2400 × 597 front panel. The 3 kerf leaves a 2400 × 600 strip.
3. Rip a 2400 × 297 strip from the remainder. The kerf leaves 2400 × 300. Trim that strip to 297; the final 3 is the saw kerf.
4. Crosscut both strips to 1800 × 297. Each leaves a 597 × 297 offcut after its crosscut kerf. Retain those offcuts for later uses; do not count them as nest-box components until a cut plan exists.

The front panel ends at Y=-303, leaving the 3 gap to the rear panel. Each shelf begins 3 outside the main platform edge and ends at X=±1500. This is an efficient two-sheet plan, **not zero waste**. Confirm actual sheet sizes, kerf and the selected plywood manufacturer's installation details before cutting.

Both main panels have three open **130-wide × 175-deep** notches. Each notch gives a nominal 5 clearance to a 120 pole. These are now machined mesh geometry, with no live Boolean cutters or parenting dependency. They are not weather seals; close the eventual wall/pole junctions as part of the enclosure detail.

[CHH's Ecoply guide](https://chhply.co.nz/assets/Uploads/EcoplySpecificationInstallationGuideCurrent.pdf) distinguishes square-edge support from tongue-and-groove joints, describes grain orientation and requires expansion allowances. The final panel grade, span/load suitability, fasteners and perimeter detail remain to be selected. Future wall plates need a complete load-transfer and pole-junction detail; the earlier unsupported plywood overhang justification is withdrawn.

## Roof geometry

The roof falls towards the rear, using the updated bearer elevations after the 450 mm lowering:

- Front and rear roof bearers: 2400 × 150 × 50, with tops at Z=1890 and Z=1570.
- Roof bearer centre separation: 1750; fall: 320; pitch: **10.362°**.
- Six 2400 × 100 × 50 rafters align with the six main floor joists. This replaces five rafters: the new positions clear all pole bodies and provide full-width bearing at the beam ends.
- Each rafter has two horizontal 50-long bearing seats, cut 10 deep at the seat centre and approximately 14.57 at the deepest edge. The remaining section, spans, overhangs and uplift connections need structural verification.
- Five uncut 3000 × 90 × 45 purlins run across the rafters at Y=-1100, -550, 0, 550, 1100, flat to the roof slope. Their underside meets the rafter top plane. Section, spacing and fasteners remain subject to the selected roofing/load tables.

The current covering intent is corrugated metal. [Metalcraft Corrugate specifies an 8° minimum after deflection](https://www.metalcraftgroup.co.nz/products/roofing-and-cladding/products/corrugate/). The model's nominal 10.362° is geometrically consistent with that intent; this does not establish deflection, wind resistance or waterproofing performance. Four roof sheets and their candidate bonded condensation fleece are now modelled. Flashings, guttering, edge support and uplift restraint remain unresolved.

### Roof covering — added coordination stage

Roof covering follows the purlins in the animation, before the future enclosure. The pole-supported roof can be covered before infill walls **only after its foundations, bracing and connections are resolved and installed**. This stage shows sheet placement, not a demonstration of an adequately secured roof. Roof screws and flashings are not yet modelled; sheets must be secured progressively on the actual build.

The provisional geometry uses four full-length **2400 × 845 sheets**, advanced **762** across the roof: **83 side laps**, **3131 overall width**, and no end laps. Corrugations run down the 10.362° fall. Reference dimensions (76.2 pitch, 18 height, 845 width and 762 cover) come from [Roofing Industries Corrugate](https://www.roof.co.nz/product/corrugate) and its [profile data sheet](https://assets-global.website-files.com/64a4bd09f03a4c32ba27a747/65398c2f4099f7a17112292c_Corrugate_APRIL_16_8_2018.pdf). The model uses provisional 0.55 BMT steel. The profile is a sampled sinusoid with a locally lifted upper lap; it is not the supplier's exact roll-form tooling or a verified lap detail.

The sheets extend 65.5 beyond each purlin end and approximately 37 beyond each outer purlin edge along the fall. They cover 7.5144 m² of slope; four full sheets represent 8.112 m² of nominal rectangular material including side laps. Confirm actual edge cover, end overhang and flashing support before ordering. Lay direction is illustrative; orient laps to the actual exposure and supplier instructions. No roof colour has been selected by the user.

A **factory-bonded 1.2 mm condensation fleece** is a candidate, based on [COLORSTEEL DRIDEX design guidance](https://www.colorsteel.co.nz/assets/default-site/Dridex-Design-Guide_A4_AW-July-2024-FA.pdf). It moves with each sheet; it is not separately installed underlay. The upper lap is fleece-free in the representative mesh. Confirm poultry-environment suitability, cleaning, product availability and coating with the supplier. The [installation guide](https://www.colorsteel.co.nz/assets/Brochures/COLORSTEEL_Installers_Guide_.pdf) requires drip-edge treatment to prevent wicking; this treatment is a build operation, not separate geometry. Ventilation remains necessary. Do not substitute conventional sheets without designing and sequencing condensation control first.

Five provisional **3000 × 90 × 1 compatible isolation strips** sit on the purlins below the fleece. Their thickness is a coordination allowance; select an approved separator for the roofing and timber treatment. Fleece thickness is represented along the roof normal, without compression. Sheet thickness is likewise a roof-normal approximation. Fastener penetrations, exact edge tooling, stop-ends, high-edge cap, verge flashings, gutter/eaves and protected ventilation remain to be detailed with the wall junctions. Do not call this a finished weathertight roof.

## Hardware and unresolved connections

The model shows twelve floor and twelve roof **M12 × 200 outside-in bolt envelopes**, with rounded heads outside and washers/nuts inside. Bolts are now 12 diameter. Threads extend beyond the nuts into the underfloor/interior space; they are not hidden inside the pole. Select appropriate protection for accessible ends. The illustrations omit drilled holes, threads, square necks and detailed washer/nut bores.

Bolt quantity, grade, corrosion protection, washer sizes, pole bearing and edge distances are **not a verified connection specification**. Galvanised is only a display material name; the appropriate finish depends on exposure and product requirements.

The former solid blocks labelled as joist hangers have been removed. No replacement product is implied. Select compatible hangers for actual 50-wide members, doubled edges and beam-end positions, then model the manufacturer's geometry and fastening schedule. [MiTek's connector guide](https://miteknz.co.nz/wp-content/uploads/2021/06/LUMBERLOK-Timber-Connectors-Characteristic-Loadings-Data.pdf) identifies different hanger widths, fastening requirements and exposure limitations. Do not buy 47-wide hangers on the assumption that they fit actual 50 timber.

## Interior and enclosure decisions still to make

Design around 12 hens and check the finished layout before revising capacity. Draw roost length and spacing, nest interiors, ventilation, human access, chicken door/ramp, cleaning access and predator protection. The 300-deep shelf allowance does not establish useful nest depth; nesting boxes may need a different support arrangement.

Retain the rear centre pole. The clean-out concept is now **two openings around that pole**, with sizes and hinges pending, rather than a continuous full-width opening through it. Coordinate wall plates with round poles and detail the transition between walls and exposed shelves, including drainage and flashing. Wall frames, nests, cladding, doors and ramps remain unbuilt in this model.

## Access layout — next coordination pass

The agreed operating preference is outside servicing, with crouched entry possible. Keep the existing internal roof heights; increasing the roof for standing access is unnecessary.

Proposed opening layout (not yet added to the model or released for cutting):

| Position | Function and detail to develop |
| --- | --- |
| Rear, either side of centre pole | Two independently top-hinged clean-out flaps; removable bedding-retaining boards to permit sweeping at floor level |
| Front, one pole bay | A larger service/entry opening for crouched access and removal of roost components |
| Front, other pole bay | Separate chicken pop-hole and ramp, clear of the human access route |
| Nest side | Outside egg collection and removable nest liners; nest depth must be resolved against the 300 shelf |
| High wall zones | Permanent protected ventilation, independent of whether service panels are open |

The clear distance between the round poles at the middle of a bay is approximately 970. Allowing 45-wide jambs on both sides gives an initial **880-wide opening allowance**. Actual jamb-to-round-pole joints, flashings and clear opening dimensions still need detailing. A rear opening approximately 750 high is an initial layout allowance, not a finished panel size.

Large removable or hinged wall sections cannot be counted as fixed wall bracing. Reserve a separate permanent bracing system around the selected openings. Flaps need positive latches when closed, mechanically secured stays when open, hinge-head flashing, overlapping weather edges and predator-resistant closures. Do not rely on the weight of a flap or a loose prop to hold it open in wind.

Roosts should be removable through the service openings so that routine cleaning does not require crawling around fixed internal obstructions. The 12-hen nest/roost layout remains a separate dimensioning task; the flap preference does not establish its capacity.

### Floor height — confirmed revision

The user chose to lower the floor and roof together by **450**, keeping all internal headroom and the roof pitch unchanged. Framing top is now Z=150 and plywood top Z=167. Above the provisional ground at the pole rows, the floor is approximately **628 front / 906 rear**. At the outer front/rear floor edges those heights are approximately 608 / 926 because the ground continues to slope.

The post bottoms and provisional 600 embedment are unchanged. Pole cuts become approximately **2951 front / 2909 rear**, fitting **3000 stock** with approximately 49 / 91 remaining before allowances for trimming. Increased embedment, different actual ground levels or defective stock ends may require longer stock; confirm on site before purchasing or cutting.

The former Z=600 floor framing and Z=2340/2020 roof elevations are superseded. All subsequent wall, nest and opening elevations must be derived from the new floor datum, not copied from the historical review.
