# RMUC 2027 sentry field for Gazebo

This package separates rendering from navigation collision:

- `meshes/field_visual.obj` + `.mtl`: visual field mesh.
- `meshes/field_collision.obj`: lightweight collision proxy, metres, Z-up, no materials.
- `model.sdf`: static Gazebo model with visual, collision and a 2D GPU lidar example.
- `tools/build_collision.py`: regenerates the collision proxy.

The collision proxy is intentionally simplified for sentry radar navigation. Do not use the beauty Blender scene or `NAV_AUX_ON_OFF` guides as collision geometry. Install by copying this directory into a Gazebo model path, then set:

```bash
export GZ_SIM_RESOURCE_PATH=$PWD/gazebo:$GZ_SIM_RESOURCE_PATH
# Gazebo Classic:
export GAZEBO_MODEL_PATH=$PWD/gazebo:$GAZEBO_MODEL_PATH
```

The model uses a 28 x 15 m field footprint and Z-up metre coordinates. Check lidar range and obstacle heights against the official field before benchmarking.


Visual source note: the pushed `field_visual.obj` is a compact 439 KB visual LOD generated in the same RMUC/MuJoCo coordinate frame, so this navigation package stays portable through the GitHub API. The full `RMUC2027_MuJoCo_Blender_beauty.blend` is retained in the supplied Library archive; replace the visual OBJ with a full export when high-detail rendering is needed. The SDF visual URI and collision coordinates remain unchanged.
