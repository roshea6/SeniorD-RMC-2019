# Header to keep track of message sequence and timestamp
Header header
  uint32 seq
  time stamp
  string frame_id

# Drivetrain control variables dealing with linear and rotational velocites
geometry_msgs/Vector3 dt_linear # Linear velocities in x, y, and z directions
geometry_msgs/Vector3 dt_angular # Angular velocities around x, y, and z

# End effector control variables
float64 convey_spd # Sotational speed of digging mechanism
float64 lin_act_spd # Speed of linear actuator
float64 rot_spd # Speed of rotation around the pivot

# Dispensing control vriables
float64 scissor_spd # Speed at which the scissor lift lifs
float64 bucket_spd # Speed at which the dump bucket is tilted up