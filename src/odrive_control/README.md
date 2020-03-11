Package for controlling the motors of various subsystems using the ODrive motor controller. 

Launch using roslaunch controller_teleop rmc_teleop.launch js:=jsx (where x is the joystick index matched with your connected controller)physical:=true (and physical is whether you're using on a physical setup or not)

ODrive parameters for NEO motor:
	odrv0.axis0.controller.config.vel_limit = 2000
	odrv0.axis0.controller.config.vel_limit_tolerance = 0
	odrv0.axis0.controller.config.vel_gain = .5
	odrv0.axis0.controller.config.vel_integrator_gain = .001
	odrv0.axis0.encoder.config.cpr = 28
	odrv0.axis0.encoder.config.bandwidth = 1000
	odrv0.axis0.motor.config.current_lim = 30
	odrv0.axis0.motor.config.current_lim_tolerance = 30
	odrv0.axis0.motor.config.requested_current_range = 100
	odrv0.axis0.motor.config.motor_type = 0


	or

	odrv0.axis1.controller.config.vel_limit = 2000
	odrv0.axis1.controller.config.vel_limit_tolerance = 0
	odrv0.axis1.controller.config.vel_gain = .5
	odrv0.axis1.controller.config.vel_integrator_gain = .001
	odrv0.axis1.encoder.config.cpr = 28
	odrv0.axis1.encoder.config.bandwidth = 1000
	odrv0.axis1.motor.config.current_lim = 30
	odrv0.axis1.motor.config.current_lim_tolerance = 30
	odrv0.axis1.motor.config.requested_current_range = 100
	odrv0.axis1.motor.config.motor_type = 0
	