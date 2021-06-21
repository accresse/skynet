#!/usr/bin/python3

import time
import board
from wiichuck.nunchuk import Nunchuk
from pantilt import PanTilt

class SentryGun:

    def __init__(self):
        self.pantilt = PanTilt()
        self.nunchuck = Nunchuk(board.I2C())
        self.manual = True

    def run(self):
        while True:
            if self.manual:
                self.runManual()
            else:
                self.runAuto()

    def runManual(self):
        x, y = self.nunchuck.joystick
        if(x<100):
            delta = (100-x)/(100-17)*10
            self.pantilt.pan+=delta
            print("LEFT "+str(delta))
        elif(x>132):
            delta = (x-132)/(216-132)*10
            self.pantilt.pan-=delta
            print("RIGHT "+str(delta))
        
        if(y<118):
            delta = (118-y)/(118-33)*10
            self.pantilt.tilt-=delta
            print("DOWN "+str(delta))
        elif(y>150):
            delta = (y-150)/(231-150)*10
            self.pantilt.tilt+=delta
            print("UP "+str(delta))

        if self.nunchuck.buttons.C:
            print("button C")
            self.pantilt.center()
        if self.nunchuck.buttons.Z:
            print("button Z")
        time.sleep(0.1)

    def runAuto(self):
        pass

gun = SentryGun()
gun.run()
