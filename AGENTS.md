# Agent Memory & Best Practices

## Working with the User
* **Real-World Buildability:** The user expects the 3D model to accurately reflect real-world construction. Do not use "magic" or clipping. Think about how the builder will actually assemble this.
* **Material Efficiency:** Always default to standard New Zealand lumber/sheet sizes (e.g., 2400x1200mm plywood, 150x50mm timber, 3.0m/3.6m lengths). Design to minimize cuts and eliminate waste (like using uncut 3.0m bearers for cantilevers).
* **Hardware & Collisions:** Think three steps ahead about hardware. A joist cannot sit where a bolt protrudes. Carriage bolts must face outside-in so sharp threads don't hurt anyone. 
* **Conversational Pace:** The user often prefers to discuss a structural problem conceptually before committing to a code change (e.g., "Don't make a change yet, just chat with me"). Validate their intuition, lay out the physical realities (like standard spacing math), and align on a plan before touching the files.
* **Documentation is Key:** It is not enough to just update the 3D model. Every major structural decision MUST be documented in `DESIGN.md` and `BUILD.md` so the "why" is preserved for the actual build day.
* **Animation Sequencing:** The user loves logical, sequential construction animations. The sequence must follow actual physical build logic (e.g., Posts -> Floor -> Roof Framing -> Walls -> Nesting Boxes -> Cladding).

## Working with Blender via Python
* **Bezier Curve Overshoot:** When animating a "hold" or "wait" period where an object stays still before moving again, Blender's default Bezier interpolation will often cause the object to wildly dip or overshoot. To fix this safely, loop through the hold frames and explicitly `keyframe_insert` the location on every single frame to pin it.
* **Avoid F-Curve API Hacks:** Blender 4.3+ introduced Slotted Actions, which means directly accessing `obj.animation_data.action.fcurves` throws an AttributeError. Stick to `keyframe_insert` and simple loop pinning instead of trying to hack interpolation types via the F-Curve API.
* **Clean State:** Always query and delete old geometry (`obj.select_set(True)`, `bpy.ops.object.delete()`) before regenerating procedural parts of the model to avoid ghost duplicates piling up in the scene.
* **Keyframe State Hazards:** Never read `obj.location` as a baseline for math if you haven't explicitly set the timeline (`bpy.context.scene.frame_set()`) to the correct frame first, otherwise you might grab an unintended mid-animation coordinate.
* **Targeting Objects:** When targeting objects in loops, be absolutely sure of their internal Blender names (`obj.name`) rather than assuming human names.
