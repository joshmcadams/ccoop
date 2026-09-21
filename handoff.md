# Project Handoff: Chicken Coop 3D Animation

## Current State
We are in the middle of animating a step-by-step 3D construction manual for a pole-barn style chicken coop in Blender. The model strictly adheres to real-world New Zealand building practices and material dimensions (e.g., standard 2400x1200 plywood sheets, 150x50 timber). 

### Completed Phases
1. **Foundation:** 6 round posts set into sloped ground.
2. **Floor Bearers & Joists:** 150x50mm bearers bolted to the *outside* of the posts (carriage bolts inserted outside-in for safety). The bearers cantilever past the side walls by 300mm to act as built-in nesting box supports. The 8 joists are symmetrically spaced (470mm centers) using joist hangers.
3. **Plywood Floor:** The main 2400x1800 floor is floored with 1.5 sheets of 17mm plywood, with boolean-cut notches allowing the tall poles to pass directly through the floor. The side cantilevers are floored using the remaining half-sheet (zero waste!).
4. **Roof Framing:** The roof structure is assembled. A front and rear roof bearer connect the tops of the poles. Five 100x50mm rafters span the bearers, dropping at a 4.9-degree angle towards the rear to shed water downhill.

## Plans Moving Forward
The main structural skeleton is completely locked in. The next phases of construction (and Blender animation) should follow this sequence:

1. **Phase 6: Infill Wall Framing**
   * Lay 90x45mm bottom plates on top of the plywood floor, flush with the outer edge.
   * Frame vertical 90x45 studs up to the slanted roofline.
   * Leave framed openings for the human door, chicken pop-hole, and side nesting box access.
2. **Phase 7: Nesting Boxes**
   * Build the nesting box framing onto the 300mm cantilevered floor on one side.
   * Angle the nesting box roof (-15 degrees) away from the coop.
3. **Phase 8: Cladding & Roofing**
   * Wrap the walls in exterior cladding (dropping it down past the floor frame like a skirt for weatherproofing).
   * Add corrugated iron to the main roof and nesting box roof.
   * Add hardware (hinges, doors, ramp).
4. **Cost & Materials Update:** 
   * As we build the walls and roof, we must continuously tally the lumber, cladding, and hardware in `SUPPLIES.md`.

## Important Notes for Agents
* Read `AGENTS.md` before touching the Blender file.
* Beware of Blender Bezier curve overshoot on "hold" animations.
* Never blindly use `fcurves` API in Blender 4.3+ (Slotted Actions update).
* Always document architectural/structural decisions in `DESIGN.md`.
