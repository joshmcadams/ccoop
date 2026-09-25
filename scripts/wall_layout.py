"""Infill framing and explicit future nest/roost clearance guides.

Walls reach the roof members (AUDIT.md finding 3): front/rear top plates sit under
the roof bearers and side top plates under the edge rafters, parallel to the roof.
Every bay end keeps the pole clearance rule. Nests sit on the side shelves.
"""
import json
import math
import bpy


def add_wall_layout(cfg, box, finish, collection, wood, derived, geo):
    f=cfg['floor']; a=cfg['layout']; floor=f['framing_top_m']+f['ply_thickness_m']
    w,d=f['width_m'],f['depth_m']
    thin=.045; deep=.09
    px,py,rc=geo['post_x'],geo['post_y'],geo['pole_radius']+geo['clearance']
    under0,slope=geo['rafter_underside_at_origin'],geo['roof_slope']
    openings=[]
    def member(name,center,size,stage):
        o=box(name,center,size,stage,wood)
        o['wall_member']=True
        o['cut_length_m']=max(size)
        o['stock_section']='90 x 45 dressed; structural suitability pending'
        return o
    def vertical(name,x,y,z0,z1,sidewall=False,stage="06 Wall studs"):
        return member(name,(x,y,(z0+z1)/2),(deep if sidewall else thin,thin if sidewall else deep,z1-z0),stage)
    # Each long-wall bay spans between pole clearance envelopes.
    bay_half=(px-2*rc)/2
    for row,side,top in [('Front',-1,geo['front_wall_top']),('Rear',1,geo['rear_wall_top'])]:
        y=side*(d/2-deep/2)
        for bay,x in [('Left',-px/2),('Right',px/2)]:
            lo,hi=x-bay_half,x+bay_half
            width=2*bay_half-2*thin
            prefix=f'Wall_{row}_{bay}'
            member(prefix+'_Sole',(x,y,floor+thin/2),(2*bay_half,deep,thin),'05b Wall sole plates')
            member(prefix+'_Top',(x,y,top-thin/2),(2*bay_half,deep,thin),'08 Wall top plates')
            for edge,xx in [('L',lo+thin/2),('R',hi-thin/2)]:
                vertical(prefix+'_Jamb_'+edge,xx,y,floor+thin,top-thin)
            if row=='Rear':
                sill=floor+thin; height=a['cleanout_height_m']
                header=sill+height
                member(prefix+'_Header',(x,y,header+thin/2),(width,deep,thin),'07 Opening rails')
                vertical(prefix+'_UpperStud',x,y,header+thin,top-thin,stage='07b Upper infill studs')
                kind='rear clean-out'
            elif bay=='Left':
                sill=floor+thin; height=top-thin-sill; kind='front service'
            else:
                sill=floor+thin; height=a['pophole_height_m']; width=a['pophole_width_m']; kind='chicken pop-hole'
                for sign in (-1,1):
                    vertical(prefix+'_PopJamb_'+str(sign),x+sign*(width+thin)/2,y,sill,top-thin)
                member(prefix+'_PopHeader',(x,y,sill+height+thin/2),(width,deep,thin),'07 Opening rails')
            openings.append(dict(name=prefix,kind=kind,clear_width_m=width,clear_height_m=height,sill_z_m=sill,center_xy_m=[x,y]))
    # Narrow walls stop short of the corner-pole envelopes; pole seals remain a separate detail.
    half=.7
    wall_inner=w/2-deep
    limit=py-math.sqrt(rc**2-(wall_inner-px)**2) if wall_inner-px<rc else py
    assert half<=limit,('side wall reaches pole clearance envelope',half,limit)
    under=lambda y: under0-slope*y
    plate_vertical=thin*math.sqrt(1+slope*slope)
    def shaped(name,x,y,length,zbottom_fn,ztop_fn,stage):
        verts=[]
        for xx,yy in [(x-deep/2,y-length/2),(x+deep/2,y-length/2),(x+deep/2,y+length/2),(x-deep/2,y+length/2)]:
            verts.append((xx,yy,zbottom_fn(yy)))
        for xx,yy in [(x-deep/2,y-length/2),(x+deep/2,y-length/2),(x+deep/2,y+length/2),(x-deep/2,y+length/2)]:
            verts.append((xx,yy,ztop_fn(yy)))
        mesh=bpy.data.meshes.new(name);mesh.from_pydata(verts,[],[(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)]);mesh.update()
        obj=bpy.data.objects.new(name,mesh);bpy.context.scene.collection.objects.link(obj)
        finish(obj,name,stage,wood,'timber');obj['wall_member']=True
        obj['stock_section']='90 x 45 dressed; bevel cuts'
        obj['cut_length_m']=max(v[2] for v in verts)-min(v[2] for v in verts) if length==thin else math.hypot(length,length*slope)+thin*slope
        return obj
    nest_w=a['nest_clear_width_m']
    nest_ys=[-(thin/2+nest_w/2),thin/2+nest_w/2]
    stud_ys=[-(half-thin/2),-(thin+nest_w+thin/2),0,thin+nest_w+thin/2,half-thin/2]
    nest_sill=floor+thin
    for sign,label in [(-1,'Left'),(1,'Right')]:
        x=sign*(w/2-deep/2); prefix='Wall_'+label
        member(prefix+'_Sole',(x,0,floor+thin/2),(deep,2*half,thin),'05b Wall sole plates')
        shaped(prefix+'_Top',x,0,2*half,lambda y:under(y)-plate_vertical,under,'08 Wall top plates')
        for i,y in enumerate(stud_ys):
            shaped(prefix+'_Stud_'+str(i),x,y,thin,lambda y:floor+thin,lambda y:under(y)-plate_vertical,'06 Wall studs')
        # Nests sit on the shelf, so the sole plate is the framed entrance sill; a
        # removable lip board (not modelled) retains bedding.
        for i,y in enumerate(nest_ys):
            height=a['nest_clear_height_m']
            member(f'{prefix}_NestHeader_{i}',(x,y,nest_sill+height+thin/2),(deep,nest_w,thin),'07 Opening rails')
            openings.append(dict(name=f'{prefix}_Nest_{i+1}',kind='nest entrance',clear_width_m=nest_w,clear_height_m=height,sill_z_m=nest_sill,center_xy_m=[x,y]))
    guides=collection('Layout guides — future parts, not installed')
    def guide(name,center,size):
        o=bpy.data.objects.new(name,None);guides.objects.link(o)
        o.empty_display_type='CUBE';o.empty_display_size=1;o.location=center;o.scale=tuple(v/2 for v in size)
        o.hide_render=True;o['kind']='layout_guide';o['status']='clear-space reservation, not constructed geometry'
        return o
    # Clear depth starts behind a lip board at the wall's inner face and runs out
    # over the shelf. The nest liner floor is level with the sole plate top.
    nest_in=wall_inner+a['nest_lip_board_thickness_m']
    nest_out=nest_in+a['nest_clear_depth_m']
    shell_out=nest_out+a['nest_shell_thickness_m']
    shelf_edge=f['bearer_length_m']/2
    assert shell_out<=shelf_edge,('nest shell overhangs shelf',shell_out)
    for sign,label in [(-1,'Left'),(1,'Right')]:
        for i,y in enumerate(nest_ys):
            guide(f'Future_Nest_{label}_{i+1}_clear',(sign*(nest_in+nest_out)/2,y,nest_sill+a['nest_clear_height_m']/2),
                  (a['nest_clear_depth_m'],nest_w,a['nest_clear_height_m']))
    roost_z=floor+.75
    assert roost_z>nest_sill+a['nest_clear_height_m'],'roosts must stay above the nests'
    for i,y in enumerate([-.23,.23]):
        guide(f'Future_Removable_Roost_{i+1}',(0,y,roost_z),(1.8,.05,.05))
    bpy.context.scene['layout_openings_json']=json.dumps(openings)
    derived['layout']={'openings':openings,'nest_count':4,
        'nest_clear_size_m':[a['nest_clear_depth_m'],nest_w,a['nest_clear_height_m']],
        'nest_clear_x_m':[nest_in,nest_out],'nest_liner_floor_z_m':nest_sill,
        'nest_shell_outer_x_m':shell_out,'nest_shell_to_shelf_edge_m':shelf_edge-shell_out,
        'roost_reserved_total_length_m':3.6,'roost_z_m':roost_z,
        'wall_tops_m':{'front':geo['front_wall_top'],'rear':geo['rear_wall_top'],
                       'side_at_ends':[under(-half),under(half)]},
        'side_wall_end_to_pole_envelope_m':limit-half,
        'status':'framed openings and clearance guides only; boxes, leaves, roosts, supports, pole closures and bracing pending'}
