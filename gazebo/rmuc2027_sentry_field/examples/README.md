# Sentry radar / 2-D lidar example

`sentry_lidar_demo.sdf` includes the static field and a small mobile-style base
with a 720-sample horizontal `ray` sensor. It is a Gazebo Classic world file,
so no ROS package is required to check geometry or Gazebo transport output.

Run with the model directory on the model path:

```bash
export GAZEBO_MODEL_PATH="$PWD:$GAZEBO_MODEL_PATH"
gazebo sentry_lidar_demo.sdf
```

The ray sensor is 2-D (horizontal plane), 15 Hz, 0.12–30 m, 1 cm resolution.
For ROS 2, insert this plugin inside the sensor (package name depends on your
Gazebo/ROS distribution):

```xml
<plugin name="gazebo_ros_ray_sensor" filename="libgazebo_ros_ray_sensor.so">
  <ros><remapping>~/out:=scan</remapping></ros>
  <output_type>sensor_msgs/LaserScan</output_type>
  <frame_name>sentry_lidar_link</frame_name>
</plugin>
```

For ROS 1 / Gazebo Classic, use `libgazebo_ros_laser.so` with
`<topicName>scan</topicName><frameName>sentry_lidar_link</frameName>` instead.
