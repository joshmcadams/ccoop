"""Rebuild an isolated coordination model. Never runs in an interactive Blender session.
Run: blender --background --factory-startup --python scripts/build_coop.py -- --output coop.blend
Dimensions in metres. This does not size structural members or connections.
"""
import argparse
import json
import math
import sys
from pathlib import Path

import bpy
from mathutils import Vector

ROOT = Path(__file__).resolve().parents[1]
PARTS = []
COLLECTIONS = {}


def collection(name):
    if name not in COLLECTIONS:
        c = bpy.data.collections.new(name)
        bpy.context.scene.collection.children.link(c)
        COLLECTIONS[name] = c
    return COLLECTIONS[name]


def finish(obj, name, phase, material, kind, stock=None):
    obj.name = name
    for c in list(obj.users_collection):
        c.objects.unlink(obj)
    collection(phase).objects.link(obj)
    obj.data.materials.append(material)
    obj['kind'] = kind
    obj['phase'] = phase
    if stock:
        obj['stock_section'] = stock
    PARTS.append(obj)
    return obj


def material(name, color, metallic=0):
    m = bpy.data.materials.new(name)
    m.diffuse_color = (*color, 1)
    m.use_nodes = True
    bsdf = m.node_tree.nodes.get('Principled BSDF')
    bsdf.inputs['Base Color'].default_value = (*color, 1)
    bsdf.inputs['Metallic'].default_value = metallic
    bsdf.inputs['Roughness'].default_value = .6
    return m


def box(name, center, size, phase, mat, kind='timber', rotation=0):
    bpy.ops.mesh.primitive_cube_add(size=1, location=center)
    obj = bpy.context.object
    obj.dimensions = size
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    obj.rotation_euler.x = rotation
    return finish(obj, name, phase, mat, kind)


def cylinder(name, center, radius, depth, phase, mat, kind='hardware', axis_y=False, vertices=32):
    bpy.ops.mesh.primitive_cylinder_add(vertices=vertices, radius=radius, depth=depth, location=center)
    obj = bpy.context.object
    if axis_y:
        obj.rotation_euler.x = math.pi / 2
    return finish(obj, name, phase, mat, kind)


def subtract_box(obj, center, size):
    bpy.ops.mesh.primitive_cube_add(size=1, location=center)
    cutter = bpy.context.object
    cutter.dimensions = size
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    mod = obj.modifiers.new('Machined cut', 'BOOLEAN')
    mod.operation = 'DIFFERENCE'
    mod.solver = 'EXACT'
    mod.object = cutter
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.modifier_apply(modifier=mod.name)
    mesh = cutter.data
    bpy.data.objects.remove(cutter, do_unlink=True)
    bpy.data.meshes.remove(mesh)


def bounds(obj):
    pts = [obj.matrix_world @ Vector(p) for p in obj.bound_box]
    return [[min(p[i] for p in pts) for i in range(3)], [max(p[i] for p in pts) for i in range(3)]]


def animate(obj, start, end, offset=(0, 0, 1.2), waypoints=None):
    # Final transforms are captured before any animation is evaluated.
    final = obj.location.copy()
    obj['final_location'] = list(final)
    obj['assembly_start'] = start
    obj['assembly_end'] = end
    points = waypoints or [(start, final + Vector(offset)), (end, final)]
    first = Vector(points[0][1])
    axes = [i for i in range(3) if any(abs(Vector(point)[i]-final[i])>1e-8 for _,point in points)]
    def key_location(frame):
        for axis in axes:
            obj.keyframe_insert(data_path='location', index=axis, frame=frame)
    # Pin holds with ordinary key insertion, including every intermediate frame.
    for frame in range(1, start + 1):
        obj.location = first
        key_location(frame)
    for (a, p), (b, q) in zip(points, points[1:]):
        p, q = Vector(p), Vector(q)
        for frame in range(a, b + 1):
            t = (frame - a) / (b - a)
            t = t*t*(3 - 2*t)
            obj.location = p.lerp(q, t)
            key_location(frame)
    for frame in range(end, bpy.context.scene.frame_end + 1):
        obj.location = final
        key_location(frame)
    obj.location = final
    # Parts do not sit floating above the build before their phase.
    for path in ('hide_render', 'hide_viewport'):
        setattr(obj, path, True)
        obj.keyframe_insert(data_path=path, frame=1)
        obj.keyframe_insert(data_path=path, frame=start-1)
        setattr(obj, path, False)
        obj.keyframe_insert(data_path=path, frame=start)


def bolt_set(prefix, x, side, z, y_outer, through, length, diameter, mat, phase):
    # Smooth head outside, shaft travels inward through the bearer and the
    # flatted pole (`through`). Washer/nut remain beyond the pole face.
    direction = -side
    shaft = cylinder(prefix+'_Shaft', (x, y_outer+direction*length/2, z), diameter/2, length, phase, mat, axis_y=True)
    bpy.ops.mesh.primitive_uv_sphere_add(segments=16, ring_count=8, radius=1, location=(x, y_outer+side*.004, z))
    head = bpy.context.object
    head.scale = (.014, .004, .014)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    finish(head, prefix+'_DomedHead', phase, mat, 'hardware')
    inner = y_outer+direction*through
    washer = cylinder(prefix+'_Washer', (x, inner+direction*.002, z), .015, .004, phase, mat, axis_y=True)
    nut = cylinder(prefix+'_Nut', (x, inner+direction*.009, z), .0105, .01, phase, mat, axis_y=True, vertices=6)
    # Hardware is diagrammatic. Rings/threads/drilled holes are not represented.
    for obj in (shaft, head, washer, nut):
        obj['connection_status'] = 'illustrative envelope; supplier selection and load check pending'
    return (shaft, head, washer, nut)


def roof_strip(name, x0, x1, length, thickness, height_fn, origin, pitch, mat, kind):
    # Shared global sampling keeps adjacent lap profiles coincident in X, without
    # polygonal approximation producing interpenetration between thin sheets.
    step = .0762 / 24
    xs = [x0] + [i*step for i in range(math.floor(x0/step)+1, math.ceil(x1/step))] + [x1]
    verts = []
    for x in xs:
        h = height_fn(x)
        verts.extend([(x,-length/2,h),(x,length/2,h),
                      (x,-length/2,h+thickness),(x,length/2,h+thickness)])
    faces = [(0,2,3,1)]
    for i in range(len(xs)-1):
        a,b = 4*i,4*(i+1)
        faces.extend([(a,b,b+1,a+1),(a+2,a+3,b+3,b+2),
                      (a,a+2,b+2,b),(a+1,b+1,b+3,a+3)])
    a = 4*(len(xs)-1)
    faces.append((a,a+1,a+3,a+2))
    mesh=bpy.data.meshes.new(name)
    mesh.from_pydata(verts,[],faces); mesh.update()
    obj=bpy.data.objects.new(name,mesh)
    bpy.context.scene.collection.objects.link(obj)
    obj.location=origin; obj.rotation_euler.x=-pitch
    return finish(obj,name,'13 Roof sheets',mat,kind)


def add_roof_covering(r, pitch, top_plane, purlin_ys, derived):
    steel=material('Roof — provisional grey coated steel',(.24,.30,.32),.65)
    fleece=material('Factory bonded condensation fleece — candidate',(.62,.65,.63))
    separator=material('Compatible purlin isolation strip — provisional',(.07,.07,.07))
    normal=Vector((0,math.sin(pitch),math.cos(pitch)))
    base=Vector((0,0,top_plane+r['purlin_depth_m']/math.cos(pitch)))
    width=r['sheet_width_m']+(r['sheet_count']-1)*r['sheet_cover_m']
    for i,y in enumerate(purlin_ys):
        center=Vector((0,y,base.z-math.tan(pitch)*y))+normal*r['separator_thickness_m']/2
        box(f'Roof_Separator_{i}',center,(3,r['purlin_width_m'],r['separator_thickness_m']),
            '12 Roof isolation',separator,'roof_separator',-pitch)
    origin=base+Vector((-width/2,0,0))
    lap=r['sheet_width_m']-r['sheet_cover_m']
    for i in range(r['sheet_count']):
        left=i*r['sheet_cover_m']; right=left+r['sheet_width_m']
        def profile(x):
            return r['corrugation_height_m']*(1-math.cos(2*math.pi*x/r['corrugation_pitch_m']))/2
        def bottom(x):
            # A small local formed lift represents the nesting side lap, not a
            # whole-sheet vertical offset. Exact edge tooling remains supplier-specific.
            lift=(r['sheet_bmt_m']+.00015)*max(0,min(1,(left+lap+.0381-x)/.0381)) if i else 0
            return r['separator_thickness_m']+r['fleece_thickness_m']+profile(x)+lift
        sheet=roof_strip(f'Roof_Sheet_{i+1}',left,right,r['sheet_length_m'],r['sheet_bmt_m'],bottom,origin,pitch,steel,'roof_sheet')
        sheet['sheet_index']=i
        sheet['cut_length_m']=r['sheet_length_m']
        sheet['lap_m']=lap
        sheet['design_status']='Representative corrugate; fixing/edge/weatherproof details pending'
        # Bonded underside travels with the sheet; leave the upper lap fleece-free.
        lining=roof_strip(f'Roof_Fleece_{i+1}',left+(lap+.0381 if i else 0),right,r['sheet_length_m'],r['fleece_thickness_m'],
            lambda x: r['separator_thickness_m']+profile(x),origin,pitch,fleece,'roof_fleece')
        lining['sheet_index']=i
        lining['design_status']='Factory bonded fleece candidate; end treatment and ventilation required; no separate underlay'
    derived['roof_covering']={'sheet_count':r['sheet_count'],'overall_width_m':width,
        'length_on_slope_m':r['sheet_length_m'],'side_lap_m':lap,
        'gross_sheet_area_m2':r['sheet_count']*r['sheet_width_m']*r['sheet_length_m'],
        'covered_slope_area_m2':width*r['sheet_length_m'],
        'status':'coordination only; supplier profile, fleece suitability, fixings and flashings pending'}


def main():
    if not bpy.app.background:
        raise RuntimeError('Run this generator in a separate background process; it does not modify an open session.')
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, default=ROOT/'coop.blend')
    parser.add_argument('--config', type=Path, default=ROOT/'coop_config.json')
    parser.add_argument('--render', action='store_true')
    args = parser.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
    cfg = json.loads(args.config.read_text())
    f, p, r, site = (cfg[k] for k in ('floor','posts','roof','site'))
    from validate_coop import validate_config
    validate_config(cfg)
    # Fresh isolated process: no legacy geometry, orphan cutters or accumulated duplicates.
    bpy.ops.wm.read_factory_settings(use_empty=True)
    PARTS.clear()
    COLLECTIONS.clear()
    s = bpy.context.scene
    s.name = 'Coop — geometry coordination'
    s.unit_settings.system = 'METRIC'
    s.unit_settings.length_unit = 'MILLIMETERS'
    s.frame_start, s.frame_end = 1, 900
    s.render.fps = 24
    s['design_status'] = cfg['status']
    wood = material('H3.2 timber', (.55,.31,.12))
    polemat = material('H5 pole intent', (.28,.36,.17))
    plymat = material('17 mm plywood', (.76,.61,.35))
    metal = material('Galvanised hardware — indicative', (.43,.49,.53), .6)
    groundmat = material('Provisional terrain', (.13,.20,.12))
    w, d, bw, bh, z = f['width_m'],f['depth_m'],f['timber_width_m'],f['timber_depth_m'],f['framing_top_m']
    t, gap, kerf = f['ply_thickness_m'], f['sheet_gap_m'], f['saw_kerf_m']
    rad = p['diameter_m']/2
    # Pole tolerance rule (AUDIT.md finding 1). Nothing is tangent to a round pole:
    # bearers bear on a flat with a shoulder cut into the pole; every other member
    # keeps `clear` from the nominal pole surface (taper/size allowance + set-out).
    clear = p['diameter_allowance_m']/2+p['setout_tolerance_m']
    flat = p['bearer_flat_depth_m']
    post_x = w/2-bw-rad-clear
    post_y = d/2-bw-(rad-flat)
    by = d/2-bw/2
    pitch = math.atan2(r['front_bearer_top_m']-r['rear_bearer_top_m'],2*by)
    slope = math.tan(pitch)
    mean_top = (r['front_bearer_top_m']+r['rear_bearer_top_m'])/2
    joists = [-f['bearer_length_m']/2+bw/2] + [-w/2+bw/2+i*(w-bw)/5 for i in range(6)] + [f['bearer_length_m']/2-bw/2]
    derived = {'roof_pitch_degrees':math.degrees(pitch), 'joist_centres_m':joists, 'post_grid_m':[2*post_x,2*post_y], 'posts':[]}
    # Worst-case bolt path: fattest accepted pole, set out away from the bearer.
    rad_max = rad+p['diameter_allowance_m']/2
    bolt_len = cfg['hardware']['bolt_length_m']
    through_nominal = bw+rad+(rad-flat)
    through_max = bw+rad_max+(rad-flat)+p['setout_tolerance_m']
    derived['pole_rule'] = {'nominal_diameter_m':p['diameter_m'],'max_accepted_diameter_m':2*rad_max,
        'clearance_to_non_bearing_timber_m':clear,'nominal_flat_depth_m':flat,
        'flat_depth_range_m':[max(0,flat-p['setout_tolerance_m']),rad_max-(rad-flat)+p['setout_tolerance_m']],
        'bolt_thread_past_nut_m':{'nominal':bolt_len-through_nominal-.014,'worst_case':bolt_len-through_max-.014},
        'status':'coordination rule; measure delivered poles at floor and roof levels and re-run'}
    ground = box('Ground', (0,0,site['ground_at_origin_m']-.02/math.cos(math.radians(site['slope_degrees']))), (8,8,.04), '00 Site', groundmat, 'terrain', -math.radians(site['slope_degrees']))
    for side, row in [(-1,'Front'),(1,'Back')]:
        top = r['front_bearer_top_m'] if side < 0 else r['rear_bearer_top_m']
        for i,x in enumerate([-post_x,0,post_x]):
            y = side*post_y
            g = site['ground_at_origin_m']-math.tan(math.radians(site['slope_degrees']))*y
            bottom = g-site['embedment_m']
            length = top-bottom
            if length > p['stock_length_m']:
                raise ValueError(f'{row} post needs {length:.3f} m; exceeds stock')
            obj = cylinder(f'Post_{row}_{i}', (x,y,(top+bottom)/2),rad,length,'01 Posts',polemat,'post')
            # Flat with a bearing shoulder at each bearer: the bearer face stays in one
            # plane and sits on the shoulder, instead of touching a curve along a line.
            inner_face = side*(d/2-bw)
            subtract_box(obj,(x,inner_face+side*.05,z-bh/2),(.2,.1,bh))
            subtract_box(obj,(x,inner_face+side*.05,top-bh/2+.025),(.2,.1,bh+.05))
            obj['cut_length_m'] = length
            obj['bearer_flat_depth_m'] = flat
            obj['clearance_m'] = clear
            obj['ground_elevation_m'] = g
            obj['embedment_m'] = site['embedment_m']
            obj['design_status'] = 'diameter, embedment and footing design provisional'
            derived['posts'].append({'name':obj.name,'length_m':length,'ground_m':g,'bottom_m':bottom,'top_m':top})
        box('Bearer_'+row,(0,side*by,z-bh/2),(f['bearer_length_m'],bw,bh),'02 Floor bearers',wood)
        box('Roof_Bearer_'+row,(0,side*by,top-bh/2),(w,bw,bh),'09 Roof bearers',wood)
        for i,x in enumerate([-post_x,0,post_x]):
            # Two bolts 60 apart, centred on the bearer depth.
            for j,dz in enumerate([bh/2-.03,bh/2+.03]):
                bolt_set(f'FloorBolt_{row}_{i}_{j}',x,side,z-dz,side*d/2,through_nominal,bolt_len,cfg['hardware']['bolt_diameter_m'],metal,'03 Floor bolts')
                bolt_set(f'RoofBolt_{row}_{i}_{j}',x,side,top-dz,side*d/2,through_nominal,bolt_len,cfg['hardware']['bolt_diameter_m'],metal,'09 Roof bearers')
    for i,x in enumerate(joists):
        box(f'Joist_{i}',(x,0,z-bh/2),(bw,d-2*bw,bh),'04 Floor joists and blocking',wood)
    # Sister the two main floor edge joists to give the shelf its own 50 mm bearing.
    for side in (-1,1):
        box(f'Shelf_Sister_{side}',(side*(w/2+bw/2),0,z-bh/2),(bw,d-2*bw,bh),'04 Floor joists and blocking',wood)
    seam_y = d/2-1.2-gap/2
    for i,(a,b) in enumerate(zip(joists[1:6],joists[2:7])):
        box(f'Floor_Seam_Block_{i}',((a+b)/2,seam_y,z-bh/2),(b-a-bw,bw,bh),'04 Floor joists and blocking',wood)
    # Grain on the reused shelf strips runs front-to-back. Cross supports make three spans.
    for side in (-1,1):
        inner, outer = w/2+bw, f['bearer_length_m']/2-bw
        for i,y in enumerate([-(d-2*bw)/6,(d-2*bw)/6]):
            box(f'Shelf_Cross_Block_{side}_{i}',(side*(inner+outer)/2,y,z-bh/2),(outer-inner,bw,bh),'04 Floor joists and blocking',wood)
    back = box('Ply_Back',(0,d/2-.6,z+t/2),(w,1.2,t),'05 Plywood',plymat,'plywood')
    front_depth = d-1.2-gap
    front = box('Ply_Front',(0,-d/2+front_depth/2,z+t/2),(w,front_depth,t),'05 Plywood',plymat,'plywood')
    # Rough notches keep the pole clearance; seal to the actual pole on site.
    notch_depth = d/2-post_y+rad+clear
    notch_width = 2*(rad+clear)
    for obj,side in [(back,1),(front,-1)]:
        for x in [-post_x,0,post_x]:
            subtract_box(obj,(x,side*(d/2-notch_depth/2+.001),z+t/2),(notch_width,notch_depth+.002,t+.04))
        obj['notch_width_m'] = notch_width
        obj['notch_depth_m'] = notch_depth
    shelf_width = (f['bearer_length_m']-w)/2-gap
    for side in (-1,1):
        box('Ply_Cantilever_'+('L' if side<0 else 'R'),(side*(w/2+gap+shelf_width/2),0,z+t/2),(shelf_width,d,t),'05 Plywood',plymat,'plywood')
    # Six rafters align with the main joists, clearing every pole and fully bearing on beam ends.
    bottom_plane = mean_top-r['seat_depth_at_centre_m']
    center_height = bottom_plane+r['rafter_depth_m']/(2*math.cos(pitch))
    for i,x in enumerate(joists[1:7]):
        obj = box(f'Roof_Rafter_{i}',(x,0,center_height),(r['rafter_width_m'],r['rafter_length_m'],r['rafter_depth_m']),'10 Rafters',wood,rotation=-pitch)
        for side in [-1,1]:
            top = mean_top-slope*side*by
            subtract_box(obj,(x,side*by,top-.15),(r['rafter_width_m']+.02,bw,.3))
        obj['cut_length_m'] = r['rafter_length_m']
        obj['seat_depth_max_m'] = r['seat_depth_at_centre_m']+slope*bw/2
    top_plane = bottom_plane+r['rafter_depth_m']/math.cos(pitch)
    # Eave purlins sit over each bearer, outer face on the wall line, closing the roof
    # edge above the rafter bays so those bays can become mesh-covered vents.
    eave_y = d/2-r['purlin_width_m']/2
    purlin_ys = sorted(r['field_purlin_centres_y']+[-eave_y,eave_y])
    for i,y in enumerate(purlin_ys):
        obj = box(f'Purlin_{i}',(0,y,top_plane-slope*y+r['purlin_depth_m']/(2*math.cos(pitch))),(3.0,r['purlin_width_m'],r['purlin_depth_m']),'11 Purlins',wood,rotation=-pitch)
        obj['purlin_role'] = 'eave closure and sheet fixing line' if abs(abs(y)-eave_y)<1e-9 else 'field purlin'
    derived['purlin_centres_y_m'] = purlin_ys
    geo = {'post_x':post_x,'post_y':post_y,'pole_radius':rad,'clearance':clear,
           'front_wall_top':r['front_bearer_top_m']-bh,'rear_wall_top':r['rear_bearer_top_m']-bh,
           'rafter_underside_at_origin':bottom_plane,'roof_slope':slope}
    from wall_layout import add_wall_layout
    add_wall_layout(cfg,box,finish,collection,wood,derived,geo)
    add_roof_covering(r, pitch, top_plane, purlin_ys, derived)
    # No fictional hangers/bracing: unresolved connections are explicit scene metadata and docs.
    s['pending_connections'] = 'Joist and doubled-edge hangers; blocking fixings; roof restraints; temporary/permanent bracing; footing design'
    bpy.context.view_layer.update()
    # Validate the static final state before animation can conceal an error.
    from validate_coop import validate_geometry
    validation = validate_geometry(s, cfg, derived)
    schedule = {'01 Posts':(20,55),'02 Floor bearers':(80,105),'03 Floor bolts':(120,145),'04 Floor joists and blocking':(160,190),'05b Wall sole plates':(335,350),'06 Wall studs':(365,390),'07 Opening rails':(405,425),'07b Upper infill studs':(430,435),'08 Wall top plates':(440,460),'09 Roof bearers':(510,535),'10 Rafters':(555,580),'11 Purlins':(600,620),'12 Roof isolation':(640,655)}
    for obj in PARTS:
        phase = obj['phase']
        if phase in schedule:
            start,end = schedule[phase]
            offset = (0,0,1.2)
            if phase=='07 Opening rails':
                if obj.name.startswith(('Wall_Left','Wall_Right')):
                    offset=(-.5 if obj.name.startswith('Wall_Left') else .5,0,0)
                else:
                    offset=(0,-.5 if 'Front' in obj.name else .5,0)
            if obj['kind']=='hardware':
                side = -1 if 'Front' in obj.name else 1
                offset = (0,side*.35,0)
            if obj.name.startswith('Bearer_'):
                # The pole is only flatted over the bearer depth; above it the full
                # round stands proud of the bearer face. Bring the bearer in from
                # outside onto its shoulders instead of sliding it down the poles.
                offset = (0,(-1 if 'Front' in obj.name else 1)*.5,0)
            animate(obj,start,end,offset)
    for obj in PARTS:
        if obj.get('kind') in ('roof_sheet','roof_fleece'):
            start=675+obj['sheet_index']*45
            animate(obj,start,start+25,offset=(0,0,.85))
    # Lower panels between rows first, then move the open notches onto the poles.
    final = back.location.copy()
    animate(back,215,250,waypoints=[(215,Vector((0,0,z+t/2+.6))),(235,Vector((0,0,z+t/2))),(250,final)])
    final = front.location.copy()
    lifted = z+t/2+t+.006
    animate(front,260,300,waypoints=[(260,Vector((0,-.30,z+t/2+.6))),(278,Vector((0,-.30,lifted))),(290,Vector((0,final.y,lifted))),(300,final)])
    for obj in PARTS:
        if obj.name.startswith('Ply_Cantilever'):
            animate(obj,307,320,offset=(0,0,.7))
    for name,frame in [('01 Posts — footings and temporary bracing prerequisite',20),('02 Bearers',80),('03 Bolts — illustrative',120),('04 Joists and blocking — connectors pending',160),('05 Notched plywood',215),('06 Wall sole plates',335),('07 Wall studs and opening jambs',365),('08 Opening headers',405),('08b Upper infill studs',430),('09 Wall top plates',440),('HOLD: permanent bracing and connections must be resolved',480),('10 Roof bearers',510),('11 Seated rafters',555),('12 Purlins, including eave purlins',600),('13 Purlin isolation',640),('14 Roof sheet 1',675),('14 Roof sheet 2',720),('14 Roof sheet 3',765),('14 Roof sheet 4',810),('15 Review — nest shells and enclosure next',860)]:
        s.timeline_markers.new(name,frame=frame)
    from validate_coop import validate_animation
    validation.update(validate_animation())
    s.frame_set(s.frame_end)
    bpy.context.view_layer.update()
    camdata = bpy.data.cameras.new('Assembly camera')
    camera = bpy.data.objects.new('Assembly camera',camdata)
    collection('14 Presentation').objects.link(camera)
    camera.location = (5,-7,z+3.4)
    camera.rotation_euler = (Vector((0,0,z+.7))-camera.location).to_track_quat('-Z','Y').to_euler()
    camdata.type='ORTHO'; camdata.ortho_scale=6.2
    s.camera = camera
    s.render.engine = 'BLENDER_WORKBENCH'
    s.display.shading.light = 'STUDIO'
    s.display.shading.color_type = 'MATERIAL'
    s.display.shading.show_shadows = True
    s.display.shading.show_cavity = True
    s.world = bpy.data.worlds.new('Studio background')
    s.world.color = (.12,.12,.12)
    s.display.shading.background_type = 'WORLD'
    s.render.resolution_x=1200; s.render.resolution_y=1100; s.render.resolution_percentage=100
    s.render.image_settings.file_format='PNG'
    s.render.filepath=str(ROOT/'renders'/'assembly_')
    for screen in bpy.data.screens:
        for area in screen.areas:
            if area.type=='VIEW_3D':
                area.spaces.active.region_3d.view_distance=6
                area.spaces.active.region_3d.view_location=(0,0,z+.35)
                area.spaces.active.shading.color_type='MATERIAL'
    text = bpy.data.texts.new('README — regenerate from external source')
    text.write('Geometry coordination draft. See DESIGN.md and BUILD.md.\nSource: scripts/build_coop.py and coop_config.json\nRun in a separate background Blender process. This text is deliberately not executable.\nConnections, footings, bracing and occupied-coop layout remain pending.\n')
    configtext = bpy.data.texts.new('CONFIG.json')
    configtext.write(json.dumps(cfg,indent=2))
    report = {'config':cfg,'derived':derived,'validation':validation,'parts':[{'name':o.name,'kind':o['kind'],'phase':o['phase'],'bounds_m':bounds(o),'cut_length_m':o.get('cut_length_m')} for o in PARTS]}
    (ROOT/'generated').mkdir(exist_ok=True)
    from wall_cut_schedule import write_schedule
    report['derived']['wall_stock_allowance']=write_schedule(report)
    (ROOT/'generated'/'model-report.json').write_text(json.dumps(report,indent=2)+'\n')
    args.output.parent.mkdir(parents=True,exist_ok=True)
    bpy.context.preferences.filepaths.save_version=0
    bpy.ops.wm.save_as_mainfile(filepath=str(args.output.resolve()))
    if args.render:
        s.render.filepath=str(ROOT/'generated'/'assembly-preview.png')
        bpy.ops.render.render(write_still=True)
        s.frame_set(780)
        s.render.filepath=str(ROOT/'generated'/'roof-installation.png')
        bpy.ops.render.render(write_still=True)
        for frame,name in [(465,'wall-framing.png'),(200,'floor-framing.png'),(240,'floor-installation.png')]:
            s.frame_set(frame)
            s.render.filepath=str(ROOT/'generated'/name)
            bpy.ops.render.render(write_still=True)
        s.frame_set(s.frame_end)
    print('COOP_BUILD_OK', json.dumps(validation))


if __name__=='__main__':
    sys.path.insert(0,str(Path(__file__).resolve().parent))
    main()
