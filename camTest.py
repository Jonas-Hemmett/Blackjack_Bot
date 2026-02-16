# Tests computer vision

from picamera2 import Picamera2
from DisplayBase import *
import openAIFunctions as f1
import time

cam = Picamera2()
f1.client = f1.keyRead() 

config = cam.create_still_configuration()
cam.configure(config)
cam.start()

camRatio = 4 / 3

frame = cam.capture_array()
camIn = Image.fromarray(frame).resize((int(width * (1 if camRatio > 1 else camRatio)), int(height * (1 if camRatio < 1 else 1 / camRatio))), Image.NEAREST)
print(f1.analyzeImagePIL(camIn))
# print(f1.analyzeImage("../hand.png"))

cam.stop()

image