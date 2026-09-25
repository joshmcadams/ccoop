"""Geometric regression checks; these do not calculate structural capacity."""
import math
import bpy
import bmesh
from mathutils import Vector


def bounds(o):
    pts=[o.matrix_world @ Vector(p) for p in o.bound_box]
    return [[min(p[i] for p in pts) for i in range(3)],[max(p[i] for p in pts) for i in range(3)]]


def volume(mesh):
    bm=bmesh.new()
    try:
        bm.from_mesh(mesh)
        return abs(bm.calc_volume(signed=True))
    finally:
        bm.free()


def intersection_volume(a,b):
    ba,bb=bounds(a),bounds(b)
    if any(min(ba[1][i],bb[1][i])-max(ba[0][i],bb[0][i])<1e-6 for i in range(3)):
        return 0.0
    obj=bpy.data.objects.new('Audit intersection',a.data.copy())
    bpy.context.scene.collection.objects.link(obj)
    obj.matrix_world=a.matrix_world.copy()
    mod=obj.modifiers.new('Intersection','BOOLEAN')
    mod.operation='INTERSECT';mod.solver='EXACT';mod.object=b
    bpy.context.view_layer.update()
    evaluated=obj.evaluated_get(bpy.context.evaluated_depsgraph_get())
    mesh=evaluated.to_mesh()
    try:
        result=volume(mesh)
    finally:
        evaluated.to_mesh_clear()
        data=obj.data
        bpy.data.objects.remove(obj,do_unlink=True)
        bpy.data.meshes.remove(data)
    return result


def validate_geometry(scene,cfg,derived):
    timber=[o for o in scene.objects if o.get('kind') in ('timber','post','plywood')]
    collisions=[]
    checked=0
    for i,a in enumerate(timber):
        for b in timber[i+1:]:
            v=intersection_volume(a,b)
            checked+=1
            if v>1e-8:
                collisions.append({'a':a.name,'b':b.name,'volume_m3':v})
    assert not collisions, f'Solid geometry intersections: {collisions}'
    f,r=cfg['floor'],cfg['roof']
    assert len([o for o in timber if o.name.startswith('Post_')])==6
    assert len([o for o in timber if o.name.startswith('Joist_')])==8
    assert len([o for o in timber if o.name.startswith('Roof_Rafter_')])==6
    for row in derived['posts']:
        assert math.isclose(row['ground_m']-row['bottom_m'],cfg['site']['embedment_m'],abs_tol=1e-8)
        assert row['length_m']<=cfg['posts']['stock_length_m']
    # Verify real material was removed, not merely that modifiers exist.
    for name,depth in [('Ply_Back',1.2),('Ply_Front',f['depth_m']-1.2-f['sheet_gap_m'])]:
        o=bpy.data.objects[name]
        assert not o.modifiers
        expected=(f['width_m']*depth-3*o['notch_width_m']*o['notch_depth_m'])*f['ply_thickness_m']
        assert math.isclose(volume(o.data),expected,abs_tol=1e-7),(name,volume(o.data),expected)
    # Each rafter must have actual coplanar, full-width seat faces on both beams.
    for o in [o for o in timber if o.name.startswith('Roof_Rafter_')]:
        by=(f['depth_m']-f['timber_width_m'])/2
        for y,top in [(-by,r['front_bearer_top_m']),(by,r['rear_bearer_top_m'])]:
            area=0.0
            for poly in o.data.polygons:
                vs=[o.matrix_world @ o.data.vertices[i].co for i in poly.vertices]
                if all(abs(v.z-top)<1e-5 and abs(v.y-y)<=f['timber_width_m']/2+1e-5 for v in vs):
                    area+=poly.area
            assert area>=r['rafter_width_m']*f['timber_width_m']*.99,(o.name,y,area)
    # Kerf-aware two-sheet feasibility at the retained platform dimensions.
    front=f['depth_m']-1.2-f['sheet_gap_m']
    remaining=1.2-front-f['saw_kerf_m']
    shelf=(f['bearer_length_m']-f['width_m'])/2-f['sheet_gap_m']
    assert front>0 and shelf>0
    assert 2*shelf+2*f['saw_kerf_m']<=remaining+1e-8
    wall_results=validate_walls(scene,cfg)
    roof_results={**wall_results,**validate_roof(scene,cfg),**validate_pole_clearance(scene,cfg),
                  **validate_wall_tops(scene,cfg),**validate_eave_vents(scene,cfg)}
    return {**roof_results,'solid_pairs_checked':checked,'solid_intersections':0,'notched_panels_checked':2,'rafter_bearing_seats_checked':12,'post_stock_and_embedment_checked':6,'two_sheet_kerf_check':'passed','structural_capacity':'not evaluated'}


def validate_animation():
    s=bpy.context.scene
    issues=[]
    checked=0
    # Check installation paths against all poles and already installed plywood.
    for frame in range(215,321):
        s.frame_set(frame);bpy.context.view_layer.update()
        panels=[o for o in s.objects if o.get('kind')=='plywood' and not o.hide_viewport]
        poles=[o for o in s.objects if o.get('kind')=='post']
        for panel in panels:
            for other in poles+[p for p in panels if p.name<panel.name]:
                checked+=1
                v=intersection_volume(panel,other)
                if v>1e-8:issues.append([frame,panel.name,other.name,v])
    assert not issues,f'Plywood installation collisions: {issues[:10]}'
    roof_pairs=0
    for frame in range(640,s.frame_end+1):
        s.frame_set(frame);bpy.context.view_layer.update()
        moving=[o for o in s.objects if o.get('kind')=='roof_sheet' and o.get('assembly_start',0)<=frame<=o.get('assembly_end',0)]
        installed=[o for o in s.objects if o.get('kind') in ('roof_sheet','timber') and o.get('assembly_end',9999)<frame]
        for o in moving:
            for other in installed:
                roof_pairs+=1
                assert intersection_volume(o,other)<1e-9,('roof path',frame,o.name,other.name)
    for frame in (1,465,674,700,719,745,764,790,809,835,900):
        s.frame_set(frame);bpy.context.view_layer.update()
        for obj in s.objects:
            if obj.get('kind') in ('roof_sheet','roof_fleece','roof_separator'):
                expected=frame<obj['assembly_start']
                assert obj.hide_render==expected and obj.hide_viewport==expected,(frame,obj.name,'visibility')
    # Timber installation paths: floor framing, walls and roof framing must not pass
    # through anything already installed (plywood and roof sheets are checked above).
    wall_pairs=0;framing_pairs=0
    for first,last,label in [(80,190,'floor framing'),(335,460,'wall'),(510,620,'roof framing')]:
        for frame in range(first,last+1):
            s.frame_set(frame);bpy.context.view_layer.update()
            moving=[o for o in s.objects if o.get('kind')=='timber' and 'assembly_start' in o and o['assembly_start']<=frame<=o['assembly_end']]
            installed=[o for o in s.objects if o.get('kind') in ('post','timber','plywood') and o.get('assembly_end',9999)<frame]
            for o in moving:
                for other in installed:
                    if label=='wall': wall_pairs+=1
                    else: framing_pairs+=1
                    assert intersection_volume(o,other)<1e-8,(label+' installation collision',frame,o.name,other.name)
    ends={phase:max(o['assembly_end'] for o in s.objects if o.get('phase')==phase) for phase in ('08 Wall top plates','11 Purlins')}
    assert ends['08 Wall top plates']<min(o['assembly_start'] for o in s.objects if o.get('phase')=='09 Roof bearers')
    assert ends['11 Purlins']<min(o['assembly_start'] for o in s.objects if o.get('kind')=='roof_sheet')
    # Assembled parts must stay fixed until the end of the scene.
    for frame in [55,105,145,190,250,300,320,350,390,425,460,535,580,620,655,700,745,790,835,900]:
        s.frame_set(frame);bpy.context.view_layer.update()
        for obj in s.objects:
            if obj.get('assembly_end',s.frame_end+1)<=frame:
                assert (obj.location-Vector(obj['final_location'])).length<1e-6,(frame,obj.name)
    s.frame_set(s.frame_end);bpy.context.view_layer.update()
    return {'wall_path_pairs_checked':wall_pairs,'wall_path_intersections':0,'framing_path_pairs_checked':framing_pairs,'framing_path_intersections':0,'construction_phase_order':'passed','roof_path_pairs_checked':roof_pairs,'roof_path_intersections':0,'plywood_path_pairs_checked':checked,'plywood_path_intersections':0,'assembled_holds':'passed'}


def validate_config(cfg):
    assert cfg['schema_version']==1, 'Unsupported configuration version'
    f=cfg['floor']
    # The reviewed platform/stock layout is retained. The section changed deliberately
    # to dressed 140 x 45 on 25 Sep 2026 (AUDIT.md); joints and cut plan were revisited.
    fixed={'width_m':2.4,'depth_m':1.8,'bearer_length_m':3.0,'timber_width_m':.045,'timber_depth_m':.14}
    for key,value in fixed.items():
        assert math.isclose(f[key],value,abs_tol=1e-9), f'{key}: revise the joint/cutting layout and checks before changing this baseline'
    for group in ('floor','posts','roof','hardware'):
        for key,value in cfg[group].items():
            if key.endswith('_m'):
                assert isinstance(value,(int,float)) and math.isfinite(value) and value>0,(group,key)
    assert math.isfinite(cfg['site']['ground_at_origin_m'])
    assert 0<=cfg['site']['slope_degrees']<30
    assert 0<cfg['site']['embedment_m']<cfg['posts']['stock_length_m']
    assert cfg['roof']['front_bearer_top_m']>cfg['roof']['rear_bearer_top_m']
    pitch=math.atan2(cfg['roof']['front_bearer_top_m']-cfg['roof']['rear_bearer_top_m'],f['depth_m']-f['timber_width_m'])
    assert math.degrees(pitch)>=8, 'Corrugate design intent needs at least 8 degrees; product/load checks still required'
    assert cfg['roof']['seat_depth_at_centre_m']>math.tan(pitch)*f['timber_width_m']/2
    # Pole tolerance rule: the flat must leave most of the pole, and the bolt must
    # still engage its nut on the fattest accepted pole set out away from the bearer.
    p=cfg['posts']; rad=p['diameter_m']/2
    assert p['bearer_flat_depth_m']<=rad/3,'bearer flat removes too much pole'
    assert p['bearer_flat_depth_m']>p['setout_tolerance_m'],'flat must absorb set-out towards the bearer'
    through=f['timber_width_m']+rad+p['diameter_allowance_m']/2+(rad-p['bearer_flat_depth_m'])+p['setout_tolerance_m']
    washer_nut,min_thread=.004+.010,.005
    assert through+washer_nut+min_thread<=cfg['hardware']['bolt_length_m'],('bolt too short for worst-case pole',through)


def validate_roof(scene,cfg):
    r=cfg['roof']; sheets=sorted([o for o in scene.objects if o.get('kind')=='roof_sheet'],key=lambda o:o.name)
    assert len(sheets)==r['sheet_count']==4
    pitch=math.atan2(r['front_bearer_top_m']-r['rear_bearer_top_m'],cfg['floor']['depth_m']-cfg['floor']['timber_width_m'])
    width=r['sheet_width_m']+3*r['sheet_cover_m']
    assert width>=3 and math.isclose(r['sheet_cover_m']/r['corrugation_pitch_m'],10)
    pairs=0
    top=(r['front_bearer_top_m']+r['rear_bearer_top_m'])/2-r['seat_depth_at_centre_m']+(r['rafter_depth_m']+r['purlin_depth_m'])/math.cos(pitch)
    origin=Vector((-width/2,0,top))
    obstacles=[o for o in scene.objects if o.get('kind') in ('timber','post','plywood','roof_separator')]
    for i,o in enumerate(sheets):
        assert (o.location-origin).length<1e-6,('roof sheet moved off support plane',o.name)
        xs=[v.co.x for v in o.data.vertices]; ys=[v.co.y for v in o.data.vertices]
        assert math.isclose(min(xs),i*r['sheet_cover_m'],abs_tol=1e-6)
        assert math.isclose(max(xs),i*r['sheet_cover_m']+r['sheet_width_m'],abs_tol=1e-6)
        assert math.isclose(max(ys)-min(ys),r['sheet_length_m'],abs_tol=1e-6)
        lining=bpy.data.objects[f'Roof_Fleece_{i+1}']
        assert (lining.location-o.location).length<1e-6
        assert math.isclose(o.rotation_euler.x,-pitch,abs_tol=1e-6)
        assert math.isclose(o.dimensions.x,r['sheet_width_m'],abs_tol=1e-5)
        assert math.isclose(o['cut_length_m'],r['sheet_length_m'])
        for other in obstacles+sheets[:i]:
            assert intersection_volume(o,other)<1e-9,('roof collision',o.name,other.name)
            pairs+=1
    # Corrugations run down the fall, with each purlin inside the sheet run.
    outer=max(abs(y) for y in r['field_purlin_centres_y'])
    assert r['sheet_length_m']/2>outer/math.cos(pitch)+r['purlin_width_m']/2
    return {'roof_sheets_checked':4,'roof_static_pairs_checked':pairs,'roof_intersections':0}


def validate_walls(scene,cfg):
    walls=[o for o in scene.objects if o.get('wall_member')]
    assert len(walls)>=40, 'Wall framing missing'
    # Every sole plate bears directly on floor ply; all frame pieces are solid meshes.
    floor=cfg['floor']['framing_top_m']+cfg['floor']['ply_thickness_m']
    for o in walls:
        assert volume(o.data)>1e-7,(o.name,'degenerate member')
        if o.name.endswith('_Sole'):
            assert math.isclose(bounds(o)[0][2],floor,abs_tol=1e-6),(o.name,'floating sole plate')
    assert len([o for o in scene.objects if o.name.startswith('Future_Nest_')])==4
    import json
    openings=json.loads(scene['layout_openings_json'])
    assert len(openings)==8
    for opening in openings:
        x,y=opening['center_xy_m']; width=opening['clear_width_m']; height=opening['clear_height_m']
        side=opening['kind']=='nest entrance'
        bpy.ops.mesh.primitive_cube_add(size=1,location=(x,y,opening['sill_z_m']+height/2))
        probe=bpy.context.object
        probe.dimensions=(.088,width-.00002,height-.00002) if side else (width-.00002,.088,height-.00002)
        bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
        bpy.context.view_layer.update()
        try:
            for wall in walls:
                assert intersection_volume(probe,wall)<1e-8,('blocked opening',opening['name'],wall.name)
        finally:
            mesh=probe.data;bpy.data.objects.remove(probe,do_unlink=True);bpy.data.meshes.remove(mesh)

    return {'wall_members_checked':len(walls),'nest_clearance_guides':4,'clear_openings_checked':8}


def _probe_box(center,size):
    bpy.ops.mesh.primitive_cube_add(size=1,location=center)
    probe=bpy.context.object
    probe.dimensions=size
    bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
    bpy.context.view_layer.update()
    return probe


def _remove(obj):
    mesh=obj.data;bpy.data.objects.remove(obj,do_unlink=True);bpy.data.meshes.remove(mesh)


def validate_pole_clearance(scene,cfg):
    """Pole tolerance rule: only the bearers may touch a pole (on its cut flat)."""
    p=cfg['posts']
    envelope=p['diameter_m']/2+p['diameter_allowance_m']/2+p['setout_tolerance_m']
    others=[o for o in scene.objects if o.get('kind') in ('timber','plywood')]
    checked=0
    for post in [o for o in scene.objects if o.get('kind')=='post']:
        row='Front' if 'Front' in post.name else 'Back'
        bearing={'Bearer_'+row,'Roof_Bearer_'+row}
        lo,hi=bounds(post)
        bpy.ops.mesh.primitive_cylinder_add(vertices=64,radius=envelope-.0005,depth=hi[2]-lo[2],
            location=(post.location.x,post.location.y,(lo[2]+hi[2])/2))
        probe=bpy.context.object
        bpy.context.view_layer.update()
        try:
            for o in others:
                if o.name in bearing:
                    continue
                checked+=1
                assert intersection_volume(probe,o)<1e-9,('pole clearance',post.name,o.name)
        finally:
            _remove(probe)
    return {'pole_clearance_pairs_checked':checked,'pole_clearance_m':envelope-p['diameter_m']/2}


def _roof_planes(cfg):
    f,r=cfg['floor'],cfg['roof']
    by=(f['depth_m']-f['timber_width_m'])/2
    pitch=math.atan2(r['front_bearer_top_m']-r['rear_bearer_top_m'],2*by)
    under0=(r['front_bearer_top_m']+r['rear_bearer_top_m'])/2-r['seat_depth_at_centre_m']
    return by,math.tan(pitch),under0,under0+r['rafter_depth_m']/math.cos(pitch)


def validate_wall_tops(scene,cfg):
    """Top plates must meet the roof members rather than stop short of them."""
    f,r=cfg['floor'],cfg['roof']
    _,slope,under0,_=_roof_planes(cfg)
    checked=0
    for row,top in [('Front',r['front_bearer_top_m']),('Rear',r['rear_bearer_top_m'])]:
        for bay in ('Left','Right'):
            o=bpy.data.objects[f'Wall_{row}_{bay}_Top']
            assert math.isclose(bounds(o)[1][2],top-f['timber_depth_m'],abs_tol=1e-6),(o.name,'gap under roof bearer')
            checked+=1
    for label in ('Left','Right'):
        o=bpy.data.objects[f'Wall_{label}_Top']
        tops=[o.matrix_world@v.co for v in o.data.vertices]
        tops=[v for v in tops if v.z>=max(t.z for t in tops if abs(t.y-v.y)<1e-6)-1e-9]
        for v in tops:
            assert math.isclose(v.z,under0-slope*v.y,abs_tol=1e-6),(o.name,'gap under edge rafter')
        checked+=1
    return {'wall_top_plates_meeting_roof':checked}


def validate_eave_vents(scene,cfg):
    """Rafter bays above both roof bearers stay clear for mesh-covered vents."""
    f,r=cfg['floor'],cfg['roof']
    by,slope,_,top0=_roof_planes(cfg)
    bw=f['timber_width_m']
    rafters=sorted([o for o in scene.objects if o.name.startswith('Roof_Rafter_')],key=lambda o:o.location.x)
    solids=[o for o in scene.objects if o.get('kind') in ('timber','post','plywood')]
    area=0.0;count=0
    for side,top in [(-1,r['front_bearer_top_m']),(1,r['rear_bearer_top_m'])]:
        # Lowest point of the rafter top plane across the bearer width.
        y_low=side*(by+bw/2) if side>0 else side*(by-bw/2)
        height=top0-slope*y_low-top
        for a,b in zip(rafters,rafters[1:]):
            x0=bounds(a)[1][0];x1=bounds(b)[0][0]
            probe=_probe_box(((x0+x1)/2,side*by,top+height/2),(x1-x0-.0002,bw-.0002,height-.0002))
            try:
                for o in solids:
                    assert intersection_volume(probe,o)<1e-9,('eave vent blocked',side,o.name)
            finally:
                _remove(probe)
            area+=(x1-x0)*height;count+=1
    return {'eave_vent_openings_checked':count,'eave_vent_clear_height_m':height,'eave_vent_gross_area_m2':area}
