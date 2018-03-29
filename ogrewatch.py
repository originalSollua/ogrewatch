# Ogrewatch - the door watching ogre
# use the camera to detect things at your door.

import io
import signal
import random
import numpy as np
from time import sleep
from picamera import PiCamera
import picamera.array
import time
import threading
import datetime

still_interval = 5
motion_detected = False
prev_cap_time = datetime.datetime.now()

class DetectMotion(picamera.array.PiMotionAnalysis):
    def analyse(self, a):
        global still_interval, motion_detected, prev_cap_time
        b = 0
        c = 0
        i = 0
        if datetime.datetime.now() > prev_cap_time + datetime.timedelta(seconds=still_interval):
            while i < 10:
                b = np.sqrt(np.square(a[0]['x'].astype(np.float)) + np.square(a[0]['y'].astype(np.float))).clip(0, 255).astype(np.uint8)
                for j in b:
                    if j > 60:
                        c = c+1
                i = i+1
        
        if(c > 10 ):
            print("we saw a thing!")
            motion_detected = True


camera = picamera.PiCamera()
with DetectMotion(camera) as output:
    try:
        camera.resolution = (720, 640)
        camera.framerate = 30
        camera.start_recording('/dev/null', format='h264',motion_output=output)
        while True:
            while not motion_detected:
                print("saw noting")
                camera.wait_recording(0.5)
            print("stop recording and grab a still")
            camera.stop_recording()
            motion_detected = False
            filename = '/home/pi/ogrewatch/'+datetime.datetime.now().strftime('%Y-%m-%dT%H.%M.%S.%f')+'.jpg'
            camera.capture(filename, format='jpeg', use_video_port=True)
            print('captured!')
            camera.start_recording('/dev/null', format='h264',motion_output=output)
    except KeyboardInterrupt as e:
        print('keyboad happened')
        pass
    finally:
        camera.close()
        print("ending")


