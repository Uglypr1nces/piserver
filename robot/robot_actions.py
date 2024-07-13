from time import sleep
import time
from picarx import Picarx

class Robot:
    def __init__(self):
        self.px = Picarx()
        self.servoangle = 3

    def move_forward(self):
        self.px.forward(5)
        time.sleep(1)
        self.px.stop()

    def move_backward(self):
        self.px.backward(5)
        time.sleep(1)
        self.px.stop()

    # Implement other movement methods...

    def set_servo_angle(self, angle):
        self.servoangle = angle
        self.px.set_dir_servo_angle(angle)

    def set_camera_angles(self, pan_angle, tilt_angle):
        self.px.set_cam_pan_angle(pan_angle)
        self.px.set_cam_tilt_angle(tilt_angle)

    def stop():
        self.px.stop()
