from adafruit_servokit import ServoKit
import time

class PanTilt:

    def __init__(self):
        self.kit = ServoKit(channels=16)
        self.panServo = PTServo(self.kit.servo[0])
        self.tiltServo = PTServo(self.kit.servo[3])

    @property
    def pan(self):
        return self.panServo.angle

    @pan.setter
    def pan(self, angle):
        self.panServo.angle = angle

    @property
    def tilt(self):
        return self.tiltServo.angle

    @tilt.setter
    def tilt(self, angle):
        self.tiltServo.angle = angle

    def center(self):
        self.panServo.center()
        self.tiltServo.center()

class PTServo:
    SPEED = 0.2 / 60.0 # sec/deg

    def __init__(self, servo):
        self.servo = servo
        servo.actuation_range = 180
        servo.set_pulse_width_range(600,2410)

    @property
    def angle(self):
        return self.servo.angle - 90

    @angle.setter
    def angle(self, angle):
        validAngle = min(90,max(-90, angle)) + 90
        currentAngle = self.servo.angle
        change = abs(currentAngle-validAngle)
        t = change * PTServo.SPEED
        self.servo.angle = validAngle
        time.sleep(t)

    def center(self):
        self.angle = 0;
