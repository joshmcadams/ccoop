# Coop design decisions

## Status and source of truth

This is a **geometry coordination draft for 12 hens**, with room to reassess capacity after the interior layout is drawn. It is not a completed structural design or a construction release. The user confirmed that the 10° ground slope is a fair estimate; site levels and material sizes remain provisional. No existing stock constrains the design at present. The site is Coatesville, north of Auckland. The user reports some wind, typically not severe; this is not a verified wind-zone classification. Standing headroom is not required: outside flap access is preferred, with occasional crouched entry acceptable.

`coop_config.json` holds the model inputs. `scripts/build_coop.py` regenerates `coop.blend` in an isolated background Blender process. `generated/model-report.json` records derived dimensions and geometric checks. See `README.md` for commands. The generator deliberately retains the reviewed platform dimensions; changing the footprint requires revisiting the cutting layout and joint details, not just changing a number.

`REVIEW.md` describes the original model. [AUDIT.md](AUDIT.md) records the 25 September 2026 audit: its findings, the reasoning, and the user's decisions that produced this revision. The correction status is tracked in `handoff.md`; the original Blender files and review evidence remain available.

## Timber sections — dressed, 25 September 2026

The user chose **dressed (gauged) timber** over rough-sawn. All structural framing — floor bearers, joists, sisters, blocking, roof bearers and rafters — is actual **140 × 45**. Wall framing and purlins are actual **90 × 45**. H3.2 SG8 is the intent; grade and treatment still need confirmation on the quote.

Why dressed:

- Dressed timber is consistent to about 1 mm. Rough-sawn varies by a few millimetres, which matters once members keep 15–20 mm clearances to round poles.
- 140 × 45 and 90 × 45 are stocked everywhere in the standard lengths the cut plan uses, with the grade stamped.
- The project now uses only two sections.
- 140 × 45 is about 25% less stiff than a true 150 × 50. That remains ample for a 1.7 m coop floor span, but it is not a structural verification.

The rafters were 100 × 50, which has no dressed equivalent. **140 × 45 was Claude's recommendation**: the rafters have never been span-checked, so the extra margin helps; it keeps one structural section; and it makes the eave vents about 128 mm tall rather than about 80. It costs roughly $40–60 more than 90 × 45. Switching to 90 × 45 is a single configuration value, but needs a span check first.

## Pole tolerance rule — 25 September 2026

The audit found the corner poles exactly tangent to the bearers, edge joists and edge rafters. Real H5 poles are sold by small-end diameter and taper toward the butt; the floor connection is about 1.8 m below the pole top; and poles set in concrete are not placed to the millimetre. A tangent fit would clash on site. The user approved a tolerance rule:

| Input | Value | Meaning |
| --- | --- | --- |
| Nominal diameter | 120 | Design size, pending pole selection |
| Diameter allowance | 20 | Extra diameter accepted at the floor/roof connections: taper and size-class variation |
| Set-out tolerance | 10 | Pole position error when setting in concrete |
| Clearance to non-bearing timber | **20** | Half the allowance plus set-out tolerance, from the nominal surface |
| Bearer flat depth | 15 nominal | A flat with a bearing shoulder cut where each bearer bolts on |

- **Bearers bear on a flat, not a curve.** Each pole has a flat cut over the bearer depth, ending in a shoulder under the bearer. The bearer face then sits in one straight plane, and the shoulder gives gravity bearing instead of relying only on bolt shear. On site the flat is cut to suit each pole so all bearer faces line up: about 5–35 mm deep across the accepted diameter and set-out range.
- **Bearers go on from outside.** The flat covers only the bearer depth, and the full round stands 15 proud of the bearer face elsewhere. So a floor bearer cannot slide down the pole; it is brought in horizontally onto its shoulders. The animation does this, and a path check covers it. The roof bearers can still be lowered: their flats run out through the pole tops.
- **Everything else keeps 20 mm clearance** from the nominal pole surface: edge joists, edge rafters, wall members and plywood notches. The validator probes every pole with a 20 mm-inflated cylinder and rejects anything other than the bearers inside it.
- **Bolts are checked against the worst case.** That means a 140 pole set 10 mm away from the bearer; the M12 × 200 bolt must still pass through the bearer and pole and leave at least 5 mm of thread past the nut. Result: 36 mm of spare thread nominally, 16 mm in the worst case.
- **Measure the delivered poles** at floor and roof levels before cutting anything. If they exceed the allowance, update the configuration and regenerate; the validator will then reject any clash.

The rule does not make standard joist hangers fit beside the poles (see Hardware below), and the larger notches make pole-junction sealing more important.

## Dimensions and floor arrangement

All dimensions below are millimetres. Front is negative Y, rear/downhill is positive Y. Z=0 is a modelling datum, not ground level.

| Item | Coordination value |
| --- | --- |
| Main platform outside dimensions | 2400 × 1800 |
| Platform including both side shelves | 3000 × 1800 |
| Floor framing top / plywood top | Z=150 / Z=167 |
| Floor bearers | Two uncut 3000 × 140 × 45 |
| Post grid, centre to centre | 2150 × 1620; three posts per row |
| Round post diameter | 120 nominal, with the tolerance rule above |
| Main joist centres X | -1177.5, -706.5, -235.5, 235.5, 706.5, 1177.5 |
| Additional shelf-edge joist centres X | -1477.5, 1477.5 |
| Joist length / section | 1710 / actual 140 × 45 |
| Consecutive joist spacings | 300, 471, 471, 471, 471, 471, 300 |

The floor's outside dimensions are not its usable interior dimensions. With 90-thick walls flush to the main platform edges, the nominal internal rectangle is 2220 × 1620, or 3.5964 m², before post projections and fittings. Each pole projects 60 past the inner wall face. At about 0.3 m² per hen this is at the tight end of common backyard guidance, so the birds need a run with good daytime access. Capacity remains a layout decision; no claim of suitability for 20 hens is retained.

The 471 spacing keeps the main joists clear of the central post bolts. It is a layout choice, not a structural span verification. Timber dimensions in the model are **actual**, not nominal.

## Ground, posts and foundations

Ground elevation at a post is `-600 - tan(10°) × Y`. The current 600 embedment is a coordination assumption, not a sized footing. It is measured from ground at each pole centre. All pole lengths are derived from the ground, embedment and roof-bearer elevations independently.

| Row | Ground Z | Post bottom Z | Post top Z | Cut length | Stock allowance |
| --- | --- | --- | --- | --- | --- |
| Front | -457.2 | -1057.2 | 1890 | 2947.2 | 3000 |
| Rear | -742.8 | -1342.8 | 1570 | 2912.8 | 3000 |

The design intent is **H5 structural poles**, replacing the earlier H4 fence-post assumption. [Goldpine's treatment guidance](https://goldpine.co.nz/products/piling-systems/h5-building-poles-and-piles/treatment) distinguishes structural ground-contact uses. Grade, diameter, footing depth/diameter, soil suitability and anchorage still need resolution against the actual site loads. There is no six-bag concrete estimate: quantity depends on the selected footing dimensions and bag yield.

The front poles have only about 53 spare on 3000 stock. 600 embedment is shallow for poles standing 2.3–2.6 m out of the ground under a clad box in wind. If the footing design asks for more depth, the poles become 3.6 m stock; price both.

Temporary bracing, concrete curing and a permanent lateral/uplift load path are required design tasks. Roof framing alone is not treated as sufficient bracing. These unresolved assemblies are explicitly listed in the Blender scene and build sequence, rather than represented by invented connections.

## Floor bearing, seams and plywood

The two main floor edge joists receive an additional 1710 × 140 × 45 sister member on their shelf sides, centred at X=±1222.5. The main sheet bears on the original joist; each shelf panel bears on its added sister with 42 bearing width after the 3 sheet gap. **The doubled-member connections and end support remain to be selected.**

Five 426 × 140 × 45 blocks support the main sheet seam at Y=-301.5 between the six main joists, giving each sheet edge about 21 bearing after the 3 gap. Two additional 210 × 140 × 45 cross blocks per shelf support the reused strips at Y=±285. The strips' face grain runs front-to-back, so those cross blocks provide support across the grain direction. Sister members, blocking and their fastening requirements must all be included in the material and connection schedule.

The adopted cutting layout assumes two 2400 × 1200 × 17 sheets, a **3 mm saw kerf** and **3 mm inter-panel gaps**:

1. Sheet A stays 2400 × 1200, except for its post notches, and covers the rear portion from Y=-300 to Y=900.
2. Rip Sheet B to a 2400 × 597 front panel. The 3 kerf leaves a 2400 × 600 strip.
3. Rip a 2400 × 297 strip from the remainder. The kerf leaves 2400 × 300. Trim that strip to 297; the final 3 is the saw kerf.
4. Crosscut both strips to 1800 × 297. Each leaves a 597 × 297 offcut after its crosscut kerf. Retain those offcuts for later uses; do not count them as nest-box components until a cut plan exists.

The front panel ends at Y=-303, leaving the 3 gap to the rear panel. Each shelf begins 3 outside the main platform edge and ends at X=±1500. This is an efficient two-sheet plan, **not zero waste**. Confirm actual sheet sizes, kerf and the selected plywood manufacturer's installation details before cutting.

Both main panels have three open **160-wide × 170-deep** rough notches, which keep the 20 pole clearance. They are machined mesh geometry, with no live Boolean cutters or parenting dependency. **They are not weather or predator seals.** A rectangular notch around a round pole leaves gaps straight through the floor into the coop, larger than a rat needs. Close each junction with a collar scribed to the actual pole as part of the enclosure detail.

[CHH's Ecoply guide](https://chhply.co.nz/assets/Uploads/EcoplySpecificationInstallationGuideCurrent.pdf) distinguishes square-edge support from tongue-and-groove joints, describes grain orientation and requires expansion allowances. The final panel grade, span/load suitability, fasteners and perimeter detail remain to be selected. Consider a washable floor covering over the plywood.

## Roof geometry

The roof falls towards the rear:

- Front and rear roof bearers: 2400 × 140 × 45, with tops at Z=1890 and Z=1570, each bearing on pole flats.
- Roof bearer centre separation: 1755; fall: 320; pitch: **10.334°**.
- Six 2400 × 140 × 45 rafters align with the six main floor joists, clear of every pole by at least 20 and with full-width bearing at the beam ends.
- Each rafter has two horizontal 45-long bearing seats, cut 10 deep at the seat centre and approximately 14.1 at the deepest edge. The remaining section, spans, overhangs and uplift connections need structural verification.
- **Seven** uncut 3000 × 90 × 45 purlins run across the rafters, flat to the roof slope, at Y=-1100, -855, -550, 0, 550, 855, 1100. The two at Y=±855 are **eave purlins**: their outer faces sit on the wall line over each bearer. They close the roof edge above the rafters, so the rafter bays below them can become vents, and they add a sheet-fixing line at each eave. Section, spacing and fasteners remain subject to the selected roofing/load tables. Once the product's span tables are known, the field purlins may be reducible.

The current covering intent is corrugated metal. [Metalcraft Corrugate specifies an 8° minimum after deflection](https://www.metalcraftgroup.co.nz/products/roofing-and-cladding/products/corrugate/). The model's nominal 10.334° is geometrically consistent with that intent; this does not establish deflection, wind resistance or waterproofing performance. The roof almost parallels the 10° ground, so both eaves sit about 2.5 m above the provisional ground. Flashings, guttering, edge support and uplift restraint remain unresolved.

### Roof covering

Roof covering follows wall framing, roof bearers, rafters and purlins in the animation, before nest shells and enclosure finishes. The pole-supported roof can be covered before infill cladding **only after its foundations, bracing and connections are resolved and installed**. This stage shows sheet placement, not a demonstration of an adequately secured roof. Roof screws and flashings are not yet modelled; sheets must be secured progressively on the actual build.

The provisional geometry uses four full-length **2400 × 845 sheets**, advanced **762** across the roof: **83 side laps**, **3131 overall width**, and no end laps. Corrugations run down the fall. Reference dimensions (76.2 pitch, 18 height, 845 width and 762 cover) come from [Roofing Industries Corrugate](https://www.roof.co.nz/product/corrugate) and its [profile data sheet](https://assets-global.website-files.com/64a4bd09f03a4c32ba27a747/65398c2f4099f7a17112292c_Corrugate_APRIL_16_8_2018.pdf). The model uses provisional 0.55 BMT steel. The profile is a sampled sinusoid with a locally lifted upper lap; it is not the supplier's exact roll-form tooling or a verified lap detail.

The sheets extend 65.5 beyond each purlin end and approximately 37 beyond each outer purlin edge along the fall. They cover 7.5144 m² of slope; four full sheets represent 8.112 m² of nominal rectangular material including side laps. The roof reaches only about 70 past the nest shells at the sides, so nest lids need their own weathering. Confirm actual edge cover, end overhang and flashing support before ordering. Lay direction is illustrative; orient laps to the actual exposure and supplier instructions. No roof colour has been selected by the user.

A **factory-bonded 1.2 mm condensation fleece** is a candidate, based on [COLORSTEEL DRIDEX design guidance](https://www.colorsteel.co.nz/assets/default-site/Dridex-Design-Guide_A4_AW-July-2024-FA.pdf). It moves with each sheet; it is not separately installed underlay. The upper lap is fleece-free in the representative mesh. Confirm poultry-environment suitability, cleaning, product availability and coating with the supplier. The [installation guide](https://www.colorsteel.co.nz/assets/Brochures/COLORSTEEL_Installers_Guide_.pdf) requires drip-edge treatment to prevent wicking; this treatment is a build operation, not separate geometry. Do not substitute conventional sheets without designing and sequencing condensation control first.

Seven provisional **3000 × 90 × 1 compatible isolation strips** sit on the purlins below the fleece. Their thickness is a coordination allowance; select an approved separator for the roofing and timber treatment. Fleece and sheet thicknesses are roof-normal approximations. Fastener penetrations, exact edge tooling, profiled closures over the eave purlins, stop-ends, high-edge cap, verge flashings, gutter/eaves and vent mesh remain to be detailed. Do not call this a finished weathertight roof.

## Ventilation — eave vents, 25 September 2026

The user chose eave vents. The walls now reach the roof members, so the only designed openings under the roof are the **rafter bays above both bearers**. Each vent is bounded by the bearer top, two rafters and the eave purlin above.

| Item | Value |
| --- | --- |
| Openings | 10: five bays at each eave |
| Clear size, each | 426 wide × 128 high |
| Gross free area | 0.546 m², before mesh |

- **Air path.** The front vents are high and the rear vents low. Warm, moist air can leave at the front while fresh air enters at the rear, all above roost height, so birds are not in a draught.
- **Rain protection.** The roof sheets oversail both eaves by about 280.
- **Validation.** The validator checks that all ten bays stay clear of timber.
- **Still to select.** Mesh (predator- and rodent-proof, fixed to the bearer and eave purlin) and profiled closures over the eave purlins. Mesh reduces the free area; check the net area against the flock once the product is chosen. Vents must stay effective with every access panel closed.
- **Side edges.** Above each edge rafter, between purlins, there are 45-high gaps under the sheets. These need solid blocking or mesh as part of the enclosure stage.

## Hardware and unresolved connections

The model shows twelve floor and twelve roof **M12 × 200 outside-in bolt envelopes**, with rounded heads outside and washers/nuts inside. Each bolt passes through the 45 bearer and the flatted pole: 105 of pole for a nominal pole. Bolts are 60 apart, centred in the 140 bearer depth, leaving 40 to each edge. Threads extend beyond the nuts into the underfloor/interior space; select appropriate protection for accessible ends. The illustrations omit drilled holes, threads, square necks and detailed washer/nut bores.

Bolt quantity, grade, corrosion protection, washer sizes, pole bearing, edge distances and the flat/shoulder detail are **not a verified connection specification**. Galvanised is only a display material name; the appropriate finish depends on exposure and the timber treatment.

The former solid blocks labelled as joist hangers have been removed. No replacement product is implied. Dressed 45-wide framing matches standard 45-wide hangers, **but standard face-fixed hangers still do not fit at 12 of the 20 joist ends**:

- Each main edge joist has a pole on one side, with only a narrow strip of bearer face beside the flat, and its sister hard against the other side. The sister shares that constraint.
- Each shelf-edge joist finishes at the bearer end, so a hanger's outer flange would hang off the end.

This needs a chosen detail — ledgers, bolting the edge joist to the pole, concealed-flange hangers, or joists sitting on the bearers — not just a product. [MiTek's connector guide](https://miteknz.co.nz/wp-content/uploads/2021/06/LUMBERLOK-Timber-Connectors-Characteristic-Loadings-Data.pdf) identifies hanger widths, fastening requirements and exposure limitations.

## Interior and enclosure decisions still to make

Design around 12 hens and check the finished layout before revising capacity. Roost length and spacing, nest interiors and openings are now dimensioned (below). Still to draw: human access details, chicken door/ramp, cleaning access and predator protection.

Retain the rear centre pole. The clean-out concept is **two openings around that pole**, with sizes and hinges pending, rather than a continuous full-width opening through it. The poles sit 30 inside the front/rear outer wall faces, and the corner poles 65 inside the side wall faces, so exterior cladding can run continuously past every pole. Each corner then needs a small corner stud outside the pole for the cladding, plus a sealed collar at floor level; both belong to the enclosure stage. Detail the transition between walls and exposed shelves, including drainage and flashing.

## Wall framing and dimensioned layout

The user chose nests on **both narrow sides**, two on each side. [SPCA NZ guidance](https://www.spca.nz/advice-and-welfare/article/providing-a-good-environment-for-backyard-chickens?cat=pets&subcat=lifestyle-block-animals) recommends at least one nest for every 3–4 hens.

The model has **41 actual 90 × 45 infill framing members**. Front and rear each have two 915-wide frames at X=±537.5, Y=±855. Each frame ends 80 from the pole centres: 20 clear of the nominal pole surface, under the pole tolerance rule. Narrow-side frames are 1400 long, centred X=±1155, ending at Y=±700, 38 clear of the corner-pole envelopes. These gaps are deliberate allowances for fitted pole junctions and seals, not finished openings to leave exposed.

**Walls reach the roof members (25 September 2026).** The audit found the old frames stopped 70–242 below the roof, fixed only at their sole plates, with nothing to fix cladding or mesh to above the side walls. Now:

- Front top plates sit directly under the front roof bearer (top Z=1750) and rear plates under the rear bearer (Z=1430). Half of each plate's width bears under the bearer.
- Side top plates run **parallel to the roof** directly under the edge rafters, from Z=1847.6 at the front end to Z=1592.4 at the rear, with matching bevels on the stud tops. This removes the old second slope angle.
- Front/rear cladding can run floor-to-bearer continuously, and side cladding floor-to-rafter.
- **Consequence:** the frames are now fixed between the floor and the roof members, so in practice they carry some load and will contribute to bracing once sheathed. The structural design must account for the sole-plate bearing, wall fixings and floor. **No wall member capacity or bracing rating is claimed.**

| Opening | Count | Clear framing opening | Location / use |
| --- | --- | --- | --- |
| Front service | 1 | 825 wide × 1493 high | Left front bay viewed from outside; crouched access |
| Chicken pop-hole | 1 | 400 wide × 450 high | Other front bay, uphill side for the shortest ramp; door mechanism pending |
| Rear clean-out | 2 | 825 wide × 800 high | One each side of rear centre pole, downhill; proposed top-hinged flaps |
| Nest entrances | 4 | 350 wide × 400 high | Two on each narrow side; sill is the sole plate top, Z=212 |

These are **rough clear framing sizes**, before linings, door stops, lip boards, seals or bedding boards. Service, pop-hole and clean-out openings have a fixed 45-high sole-plate threshold; removable bedding boards would sit above it. Cleaning involves sweeping over that small threshold, not a promised flush-floor exit. Do not cut away the sole plate without revisiting support and framing continuity.

The sole plates overlap continuous framing below: 45 of the 90 front/rear plate width is over the bearer, and 45 of the side plate width is over its edge joist. Plywood carries the remaining strip. Confirm bearing, plate fixings and floor loading before treating this as a construction detail.

Large hinged openings cannot be counted as permanent bracing. Retain separate bracing and connection design as a prerequisite. Cleaning flaps need positive latches, secured stays, protected hinge lines and predator-resistant weather seals.

### Nests on the shelves — 25 September 2026

The audit found the raised nests left a 300 void above an exposed shelf, so the shelf had no clear job. The user chose to **sit the nests on the shelves**:

| Item | Value |
| --- | --- |
| Nest boxes | Four; the shells sit on the side shelves |
| Liner floor | Level with the side-wall sole plate top, Z=212, on 45 battens on the shelf |
| Clear interior, each | 350 deep (X=1130–1480) × 350 wide × 400 high |
| Lip board | Removable, 100 high × 20 thick, at the wall's inner face (not modelled) |
| Clear entrance above the lip | 300 |
| Shell | 15 allowance, reaching X=1495, 5 inside the shelf edge |
| Egg-collection lid | About 1.23 m above provisional ground at mid-length |
| Roosts | 305 above the nest tops, so hens are not encouraged to sleep in the nests |

- **Nest floor.** Level with the sole plate, so the sole plate is the framed entrance sill. The four separate nest sill members are gone.
- **Size.** The extra height over the old 350 cube leaves a practical entrance above the lip. This is a medium-hen starting layout, subject to the actual birds.
- **Shelf protection.** The shelf under each nest is protected inside the shell.
- **Still open:**
  - The shelf lengths beyond the nest shells stay exposed; either extend the nest enclosure the full side length or cap and flash those ends.
  - The roof reaches only about 70 past the shells, so lids need their own weathering.
  - The 5 edge margin is small; check it after panel thicknesses are chosen.
  - Shells, supports, lids, liners, flashing and egg-access clearances remain to be modelled. Nest shell sizes are not final stock sizes.

Viewport-only wire guides reserve the four nest interiors and two **1800-long removable roosts** at Y=±230, Z=917 (750 above floor). The roost allowance totals 3.6 m, or 300 per hen; their height, section, supports, landing space and removal route need checking with the actual flock. These guides are not installed parts, do not render, and are excluded from purchasing quantities.

## Construction animation intent

The user requires the quick animation to follow hand construction order. The current sequence is:

1. posts, with the unresolved footing/temporary-bracing prerequisites;
2. floor frame and decking;
3. wall sole plates, then studs and jambs;
4. opening rails, then upper infill studs;
5. wall top plates;
6. a permanent-bracing/connection checkpoint;
7. roof framing, including the eave purlins;
8. roof covering.

The wall members arrive before any roof can obstruct installation. Opening rails enter horizontally through the open wall faces, and upper infill studs follow their supporting headers.

Because the top plates now meet the roof members, mark the roof-bearer heights on the poles from level before building the walls. The wall tops then support the roof bearers while they are bolted.

This quick pass ends at frame 900. Next come nest supports/shells, then enclosure/cladding/flashings/vent mesh, doors and lids, removable roosts/liners, ramp and final checks. The future tutorial pass will add camera movement, detailed connections and call-outs **after** the build sequence and unresolved prerequisites are resolved. Timeline markers are not evidence that foundations or bracing have been designed or installed in the model.

### Floor height — confirmed revision

The user chose to lower the floor and roof together by **450**, keeping all internal headroom and the roof pitch unchanged. Framing top is Z=150 and plywood top Z=167. Above the provisional ground at the pole rows, the floor is approximately **624 front / 910 rear**; at the outer front/rear floor edges approximately 608 / 926.

The post bottoms follow the provisional 600 embedment. Pole cuts are approximately **2947 front / 2913 rear**, fitting **3000 stock** with approximately 53 / 87 remaining before allowances for trimming. Increased embedment, different actual ground levels or defective stock ends may require longer stock; confirm on site before purchasing or cutting.

The former Z=600 floor framing and Z=2340/2020 roof elevations are superseded. All subsequent wall, nest and opening elevations must be derived from the current floor datum, not copied from the historical review.
