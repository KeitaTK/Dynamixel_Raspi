from dynamixel_sdk import *  # Uses Dynamixel SDK library

dxl = Dynamixel("/dev/ttyUSB0", 57600)
dxl.enable_torque(1)
dxl.set_mode_position(1)
dxl.set_min_max_position(1, 0, 4095)
dxl.set_max_velocity(1, 200)
# 以降、目的に応じて制御
