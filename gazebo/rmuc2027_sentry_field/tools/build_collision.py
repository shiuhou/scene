#!/usr/bin/env python3
"""Generate the lightweight, material-free collision mesh for the RMUC 2027 field.

This deliberately contains only structural blockers (floor, fences, platforms and
obstacles). Painted markings, labels, lane marks and other navigation aids remain
visual-only. Coordinates are metres, Z-up, with the field origin at its centre.
"""
from math import cos, sin, radians
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "meshes" / "field_collision.obj"
verts = []
faces = []
objects = []

def transform(p, center, rot=(0.0, 0.0, 0.0)):
    x,y,z = p
    rx,ry,rz = [radians(v) for v in rot]
    # X then Y then Z (sufficient for the small floor tilt used here)
    cy, sy = cos(ry), sin(ry)
    x,z = cy*x + sy*z, -sy*x + cy*z
    cx, sx = cos(rx), sin(rx)
    y,z = cx*y - sx*z, sx*y + cx*z
    cz, sz = cos(rz), sin(rz)
    x,y = cz*x - sz*y, sz*x + cz*y
    return (x+center[0], y+center[1], z+center[2])

def add_box(name, center, size, rot=(0.0,0.0,0.0)):
    sx,sy,sz = [v/2 for v in size]
    local = [(-sx,-sy,-sz),(sx,-sy,-sz),(sx,sy,-sz),(-sx,sy,-sz),
             (-sx,-sy,sz),(sx,-sy,sz),(sx,sy,sz),(-sx,sy,sz)]
    start = len(verts)+1
    verts.extend(transform(p, center, rot) for p in local)
    # Closed, outward-facing quad shell. Gazebo accepts quads and triangulates.
    for f in ((0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)):
        faces.append(tuple(start+i for i in f))
    objects.append(name)

def add_cylinder(name, center, radius, depth, segments=24, rot=(0.0,0.0,0.0)):
    start = len(verts)+1
    # Bottom and top rings, local z axis.
    for z in (-depth/2, depth/2):
        for i in range(segments):
            a = 2*3.141592653589793*i/segments
            verts.append(transform((radius*cos(a), radius*sin(a), z), center, rot))
    faces.append(tuple(start+i for i in range(segments-1,-1,-1)))
    faces.append(tuple(start+segments+i for i in range(segments)))
    for i in range(segments):
        j = (i+1) % segments
        faces.append((start+i, start+j, start+segments+j, start+segments+i))
    objects.append(name)

# Base and perimeter.
add_box("field_floor", (0,0,-0.08), (28.0,15.0,0.16), rot=(1.5,0,0))
add_box("fence_w", (-14.05,0,1.20), (0.10,15.2,2.40))
add_box("fence_e", (14.05,0,1.20), (0.10,15.2,2.40))
add_box("fence_s", (0,-7.55,1.20), (28.1,0.10,2.40))
add_box("fence_n", (0,7.55,1.20), (28.1,0.10,2.40))

# Central obstacle stack.
add_box("central_highland", (0,0,0.25), (6.8,5.2,0.50))
add_box("central_platform", (0,0,0.58), (4.4,3.0,0.18))
add_cylinder("energy_mechanism", (0,0,1.05), 1.15, 0.70)

# Red and blue base structures. Flat coloured zones are intentionally omitted.
for side, y in (("red",-5.35),("blue",5.35)):
    add_box(f"{side}_base_platform", (0,y,0.30), (3.2,2.1,0.60))
    add_box(f"{side}_base_tower", (0,y,1.15), (1.4,1.1,1.1))

# Tunnel shells are structural obstacles in the beauty scene approximation.
add_box("north_tunnel", (0,5.3,0.8), (4.5,1.2,1.5))
add_box("south_tunnel", (0,-5.3,0.8), (4.5,1.2,1.5))

# Side highlands, steps and launch/radar stations.
for side,x in (("west",-10.7),("east",10.7)):
    add_box(f"{side}_highland", (x,0,0.30), (3.4,4.5,0.60))
    for i in range(3):
        direction = 1 if x < 0 else -1
        add_box(f"{side}_step_{i}", (x + direction*(i*0.35+0.2),0,0.15+i*0.12), (0.55,4.0,0.25+i*0.06))
    add_box(f"{side}_launch_station", (x,(-4.5 if x>0 else 4.5),0.65), (2.4,1.2,1.3))
    add_box(f"{side}_radar_base", (x,(4.5 if x>0 else -4.5),1.0), (2.2,1.2,2.0))

# Work/resource stations.
for side,y in (("red",-3.9),("blue",3.9)):
    add_box(f"{side}_worktable", (-4.0,y,0.45), (1.8,0.8,0.8))
    add_box(f"{side}_resource_station", (4.0,y,0.40), (1.6,1.0,0.7))

with OUT.open("w", encoding="utf-8") as f:
    f.write("# RMUC 2027 lightweight collision proxy; metres, Z-up; no materials by design.\n")
    f.write("o field_collision\n")
    for x,y,z in verts:
        f.write(f"v {x:.6f} {y:.6f} {z:.6f}\n")
    for face in faces:
        f.write("f " + " ".join(str(i) for i in face) + "\n")
print(f"wrote {OUT} ({len(verts)} vertices, {len(faces)} faces, {len(objects)} objects)")
