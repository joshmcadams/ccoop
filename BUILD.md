# Build sequence and animation

This is the sequence for developing and reviewing the model, followed by the intended erection order. **It is not yet a construction release.** Read DESIGN.md for dimensions and decisions; site foundations, bracing and connection schedules remain unresolved. The Blender animation demonstrates assembly geometry and omits those unresolved components. [AUDIT.md](AUDIT.md) explains the 25 September 2026 changes: dressed timber, the pole tolerance rule, walls to the roof with eave vents, and nests on the shelves.

All dimensions below are millimetres unless stated otherwise. Front is negative Y, rear is positive Y; Z=0 is a modelling datum, not ground level.

## Before purchasing or excavating

1. Confirm site ground levels and floor height. The 10° slope and 600 pole embedment remain provisional. The front poles have only about 53 spare on 3.0 m stock; deeper footings mean 3.6 m poles.
2. Resolve structural pole grade/diameter, footing dimensions, wind/soil assumptions, gravity/lateral/uplift load paths and temporary erection bracing. Allow concrete curing before loading.
3. Buy **dressed** 140 × 45 (structural) and 90 × 45 (walls, purlins). Select compatible hangers or an alternative joist-end detail, fasteners, roofing profile and plywood grade. Check the roof seats and remaining rafter section against the selected structural design.
4. **Measure the delivered poles** at floor and roof levels. The model accepts up to 140 there (120 nominal + 20 allowance) and 10 set-out error. If the poles are fatter, update `coop_config.json` and regenerate before cutting.
5. Complete the 12-hen interior and weatherproof enclosure layout. The user accepts crouched entry and prefers outside flap access; standing headroom is not required.

## Phase 1: Posts and temporary stability

1. Mark three holes in each of two rows: X=-1075, 0, 1075; Y=-810, 810. All coordinates are from the platform centre. Each coordinate is the pole centre with the 15 nominal flat; allow 10 set-out tolerance.
2. Excavate and set the poles to the resolved foundation design. Keep temporary braces in place until the permanent system can take the loads. The animation does not demonstrate a footing or brace design.
3. Use the ground-to-top schedule in DESIGN.md to establish cuts. The present geometry needs approximately 2947 front poles and 2913 rear poles, all within 3000 stock. Remeasure on site before cutting.
4. From a level line, mark on every pole the floor bearer (Z=10 to 150) and roof bearer (Z=1750 to 1890 front, 1430 to 1570 rear) positions. Cut a flat with a bearing shoulder at each bearer position, so every bearer face on a row lies in one plane. The flat is about 15 deep on a nominal pole and 5–35 on real poles.

## Phase 2: Floor bearers and bolts

1. Establish a level framing top at the agreed datum; in the model it is Z=150, with framing bottom Z=10.
2. Bring two uncut 3000 × 140 × 45 bearers in horizontally from outside and seat them on the pole shoulders, against the flats, centred left-to-right. They cannot be slid down the poles: above and below each flat, the full round stands 15 proud of the bearer face. Their 300 extensions are measured beyond the main 2400 platform, not from the outside pole centres.
3. Fit the selected connection hardware. The drawing illustrates two M12 × 200 bolts per pole, outside-in, 60 apart and centred in the bearer depth. Joint capacities, edge distances and drilling/washer details remain pending. Provide clearance and protection for exposed thread ends.

## Phase 3: Joists, shelf support and seam blocking

1. Cut eight 1710 × 140 × 45 joists. Centres are X=-1477.5, -1177.5, -706.5, -235.5, 235.5, 706.5, 1177.5, 1477.5. The edge joists at ±1177.5 must keep 20 clear of the corner poles.
2. Install the chosen joist-end supports before placing the joists. Standard face-fixed hangers do not fit at the edge joists, sisters or shelf-edge joists; resolve that detail first (DESIGN.md, Hardware).
3. Add two 1710 × 140 × 45 sister members outside the main-floor edge joists. Their centre lines are X=±1222.5. Fit their designed end supports and member-to-member fasteners.
4. Install five 426 × 140 × 45 seam blocks between the main joists, centred at Y=-301.5.
5. Install four 210 × 140 × 45 cross blocks: two on each shelf, at Y=±285. Select the blocking connections with the rest of the floor fixings.
6. Check that all sheet edges have bearing and room for the specified fasteners. Verify bolt/hanger/joist clearances using the actual chosen products before decking hides them.

## Phase 4: Plywood

Use the two-sheet cutting sequence in DESIGN.md, including kerf. Finished panels are 2400 × 1200, 2400 × 597, and two 1800 × 297. These are actual panel sizes, not gap-inclusive layout dimensions.

1. Cut three 160 × 170 open edge notches in each main panel, centred at X=-1075, 0, 1075. They keep the 20 pole clearance. Adjust them to the measured poles.
2. Lower the rear panel between the pole rows, centred at Y=0, then slide it rearward 300 into its final position. The open rear notches receive the rear poles. Lowering the panel directly over its final position would pass it through the poles.
3. Lower the front panel near Y=-300, keeping it at least one panel thickness plus handling clearance above the installed rear sheet. Slide it forward into its final position, then lower it onto the joists. The animation uses 6 extra clearance beyond the panel thickness.
4. Place the shelf strips with 3 gaps to the main floor. Their inner edges bear on the sister members; the cross blocks support the strips across their grain direction.
5. Fasten and protect the plywood using the selected product's schedule. Close every pole notch with a collar scribed to the pole. The rough notch gaps are large enough for rats, and the notches alone do not seal the enclosure.

## Phase 5: Infill wall framing and access openings

1. Keep the designed temporary bracing in place. Set out the four nest entrances, separate front service/pop-hole openings and two rear cleaning openings from DESIGN.md before cutting.
2. Fix the six sole plates on the completed floor, 20 clear of every pole. Check their bearing and selected floor fixings. These are 90 × 45 infill frames, not an independently verified structural wall system.
3. Fit the full-height studs and opening jambs. Front/rear studs stop at the roof-bearer marks less a 45 top plate. Side-wall stud tops are bevelled to the roof pitch. Fit headers through the open wall faces, then the two short rear infill studs above their headers. The nest entrances need no separate sills: the side sole plate is the sill.
4. Fit top plates: front/rear plates at the roof-bearer marks, side plates on the edge-rafter line, parallel to the roof. Check the side plates with a string line between the bearer marks.
5. Complete the designed pole junctions, anchors and permanent bracing. The model shows the frame members but not those unresolved fittings. Do not treat the frame rectangles or future flaps as bracing.
6. Verify rough openings: front service 825 × 1493, chicken 400 × 450, two rear cleaning openings 825 × 800, and four nest entrances 350 × 400. Leaves, lip boards, seals and linings reduce these sizes. The fixed 45-high sole plate remains a cleaning threshold.

## Phase 6: Roof framing

1. Maintain the resolved temporary bracing. Seat the front/rear roof bearers on their pole shoulders and on the wall top plates, with tops at Z=1890/1570.
2. Install the selected pole-to-bearer connections. Roof bolts in the model are illustrative envelopes only.
3. Cut the two bearing seats in each of six 2400 × 140 × 45 rafters. Their centre-line X positions match the six main floor joists. Check the approved seat detail and remaining section before cutting.
4. Place the rafters falling to the rear at 10.334°, bearing on the bearers and the side top plates, then fit the designed restraints.
5. Add seven 3000 × 90 × 45 purlins at the positions in DESIGN.md, subject to the roof product's load/span/fixing checks. The two eave purlins sit over the bearers with their outer faces on the wall line. Leave the rafter bays below them open: those are the eave vents.
6. Install and verify permanent bracing before relying on the roof skeleton for stability. The roof is not deemed rigid merely because the members touch.

## Phase 7: Roof covering placement

1. Complete and check the specified foundations, bracing and roof connections before loading or covering the frame. These remain unresolved in the current model. Do not rely on future movable wall flaps for bracing.
2. Confirm the profile, coating, fasteners, lap direction and condensation-control option. The animation assumes four 2400-long corrugated sheets with factory-bonded fleece. Prepare drip edges and stop-ends to the selected supplier's instructions before installation where required.
3. Fit compatible isolation strips along all seven purlins. The animation shows these at frames 640–655.
4. Place and progressively secure each sheet, working across the roof. The representative layout advances each 845-wide sheet by 762, providing an 83 side lap. Keep corrugations parallel to the fall and edges aligned. Fleece is bonded at the factory and arrives with the sheet. Actual roof fixing geometry/pattern is still pending and is not demonstrated by the animation.
5. Complete the selected high-edge/verge/eaves flashings, profiled closures over the eave purlins and drainage with the enclosure junctions. These are not yet modelled; do not leave loose sheets on the structure or treat the placement animation as a completed weatherproofing sequence.

## Subsequent phases — not yet modelled

1. Build the four nest shells on the side shelves (two each side). Fit liner battens so the liner floor is level with the sole plate top, and fit removable 100-high lip boards. Provide exterior lid access and weathering. Cap or enclose the shelf lengths beyond the shells. The current wire guides represent clear interior space only.
2. Fit enclosure cladding, corner studs outside the corner poles and pole collars. Fix mesh over the ten eave vents and close the gaps above the edge rafters. Complete roof/nest flashings and drainage. Reserve access for those junctions; coordinate any concealed flashing before closing the relevant cladding.
3. Fit front doors, rear cleaning flaps and nest-access lids, with positive latches, mechanically secured stays and removable bedding boards.
4. Install removable roosts and nest liners, the ramp, and final protective finishes. Check ventilation, predator protection, fasteners, cleaning and all access routes before housing hens.

## Animation markers

| Frame | Phase |
| --- | --- |
| 20–55 | Posts; foundations and temporary bracing still pending |
| 80–105 | Floor bearers, brought in horizontally onto the pole shoulders |
| 120–145 | Illustrative floor bolt assemblies |
| 160–190 | Joists and blocking; connection detail pending |
| 215–250 | Rear plywood lowers between rows, then slides rearward |
| 260–300 | Front plywood clears installed sheet, slides, then lowers |
| 307–320 | Shelf panels |
| 335–350 | Wall sole plates |
| 365–390 | Full-height studs and jambs |
| 405–425 | Opening headers |
| 430–435 | Rear upper infill studs, after their headers |
| 440–460 | Wall top plates |
| 480 | Prerequisite checkpoint: designed bracing, pole junctions and connections |
| 510–535 | Roof bearers and illustrative bolts |
| 555–580 | Seated rafters |
| 600–620 | Purlins, including the two eave purlins |
| 640–655 | Purlin isolation strips |
| 675–700 | Roof sheet 1 with factory fleece |
| 720–745 | Roof sheet 2 |
| 765–790 | Roof sheet 3 |
| 810–835 | Roof sheet 4 |
| 860–900 | Review; nest shells and enclosure next |

The quick animation has a fixed camera; camera pans and tutorial call-outs are deliberately deferred. Frame 465 shows completed wall framing before the roof. Frame 780 shows roof sheet 3 arriving. The sequence includes prerequisite markers for unresolved work, so it is not yet a complete safe-building tutorial. Viewport nest/roost guides are not installed components and do not appear in renders.
