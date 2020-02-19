#!/usr/bin/env python

import odrive

print "Connecting to Odrive..."

# Find an available odrive device. This function will hold until a device is found
odrv0 = odrive.find_any()

# Print the voltage to make sure we're actually connected
print(str(odrv0.vbus_voltage))