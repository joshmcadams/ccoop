"""Run in background Blender against a generated model; never saves mutations."""
import copy
import json
import sys
from pathlib import Path
import bpy

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(Path(__file__).resolve().parent))
from validate_coop import validate_geometry, validate_animation, validate_config

if not bpy.app.background:
    raise RuntimeError('Use a separate background Blender process for destructive regression cases')

s=bpy.context.scene
s.frame_set(s.frame_end)
bpy.context.view_layer.update()
cfg=json.loads(bpy.data.texts['CONFIG.json'].as_string())
f=cfg['floor']
posts=[]
for o in s.objects:
    if o.get('kind')=='post':
        posts.append({'name':o.name,'ground_m':o['ground_elevation_m'],'bottom_m':o['ground_elevation_m']-o['embedment_m'],'length_m':o['cut_length_m']})
derived={'posts':posts}
validate_config(cfg)
results={'baseline':validate_geometry(s,cfg,derived),'animation':validate_animation()}

def must_reject(label,config=cfg):
    try:
        validate_geometry(s,config,derived)
    except AssertionError:
        results[label]='correctly rejected'
    else:
        raise AssertionError(f'Regression was not detected: {label}')

obj=bpy.data.objects['Roof_Rafter_2']
original=obj.location.copy()
obj.location.z+=.03
bpy.context.view_layer.update()
must_reject('floating rafter')
obj.location=original
bpy.context.view_layer.update()

obj=bpy.data.objects['Ply_Back']
original=obj.data
verts=list(obj.bound_box)
mesh=bpy.data.meshes.new('Intentionally uncut panel')
mesh.from_pydata(verts,[],[(0,1,2,3),(4,7,6,5),(0,4,5,1),(1,5,6,2),(2,6,7,3),(3,7,4,0)])
mesh.update()
obj.data=mesh
bpy.context.view_layer.update()
must_reject('uncut plywood')
obj.data=original
bpy.data.meshes.remove(mesh)
bpy.context.view_layer.update()

bad=copy.deepcopy(cfg)
bad['posts']['stock_length_m']=min(p['length_m'] for p in posts)-.1
must_reject('insufficient post stock',bad)

obj=bpy.data.objects['Roof_Sheet_2']
original=obj.location.copy()
obj.location.z+=.03
bpy.context.view_layer.update()
must_reject('floating roof sheet')
obj.location=original
bpy.context.view_layer.update()

obj=bpy.data.objects['Wall_Front_Left_Sole']
original=obj.location.copy()
obj.location.z+=.03
bpy.context.view_layer.update()
must_reject('floating wall sole plate')
obj.location=original
bpy.context.view_layer.update()

# Pole tolerance rule: a pole set 5 mm towards the edge joist breaks the clearance
# without any solid overlap, which the intersection check alone would miss.
obj=bpy.data.objects['Post_Front_2']
original=obj.location.copy()
obj.location.x+=.005
bpy.context.view_layer.update()
must_reject('pole inside clearance envelope')
obj.location=original
bpy.context.view_layer.update()

# A floating block in a rafter bay blocks an eave vent without touching anything.
bpy.ops.mesh.primitive_cube_add(size=1,location=(0,-(f['depth_m']-f['timber_width_m'])/2,cfg['roof']['front_bearer_top_m']+.04))
block=bpy.context.object
block.dimensions=(.1,.03,.05)
block['kind']='timber'
bpy.context.view_layer.update()
must_reject('blocked eave vent')
mesh=block.data;bpy.data.objects.remove(block,do_unlink=True);bpy.data.meshes.remove(mesh)
bpy.context.view_layer.update()

bad=copy.deepcopy(cfg)
bad['hardware']['bolt_length_m']=.17
try:
    validate_config(bad)
except AssertionError:
    results['bolt too short for worst-case pole']='correctly rejected'
else:
    raise AssertionError('Regression was not detected: short bolt')

results['restored_baseline']=validate_geometry(s,cfg,derived)
(ROOT/'generated'/'regression-results.json').write_text(json.dumps(results,indent=2)+'\n')
print('COOP_REGRESSIONS_OK',json.dumps(results))
