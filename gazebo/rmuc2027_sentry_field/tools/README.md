# Geometry regeneration

`build_collision.py` writes `meshes/field_collision.obj` from structural boxes
and cylinders in the legacy RMUC 2027 coordinate frame. It intentionally omits
paint, lane marks, labels, start-zone decals and Blender `NAV_*` overlays.
Run it from the model root or repository root with Python 3.
