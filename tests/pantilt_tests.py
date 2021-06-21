#!/usr/bin/python3
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from skynet.pantilt import PanTilt
from time import sleep

panTilt = PanTilt()
print("center")
panTilt.center()
sleep(1)
print("pan -90")
panTilt.pan = -90
sleep(1)
print("pan 90")
panTilt.pan = 90
sleep(1)
print("tilt -90")
panTilt.tilt = -90
sleep(1)
print("tilt 90")
panTilt.tilt = 90
sleep(1)
print("center")
panTilt.center()
sleep(1)
print("done")
