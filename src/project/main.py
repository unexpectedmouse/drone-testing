from threading import Thread
from time import sleep

import cv2
import numpy as np
from pion import Pion
from ultralytics import YOLO

from camera import Camera

# config
height = 2
ip = '10.1.100.160'
port = 5656

# ip = '127.0.0.1'
# port = 8000
camera_ip = 'rtsp://10.1.100.160:8554/pioneer_stream'
model_path = 'best.pt'

drone = Pion(ip, port)

cow_boxes = [(-2.83, 1.61), (-2.88, -3.32), (3.55, -2.85)]

frame = None

stop_fly = False


# noinspection PyUnreachableCode
def detect():
    model = YOLO(model_path)
    while True:
        if frame is None:
            continue

        results = model.predict(frame, conf=0.6)
        for result in results:
            if result.boxes is None:
                continue

            position = list(result.boxes.xywh)
            if not position: continue
            print(position or '')

            names = [result.names[cls.item()] for cls in result.boxes.cls.int()]
            print(names)
            if ('cow1' in names) or ('cow2' in names):
                cow_go()
                return


def photo():
    global frame
    camera = Camera(camera_ip)
    Thread(target=detect, daemon=True).start()
    while True:
        frame = camera.get()
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        cv2.imshow('frame', frame)




def goto(x, y: float, force=False):
    while stop_fly and not force:
        sleep(1)
    drone.goto(x, y, height, 0, wait=True)
    sleep(1)


def cow_go():
    global height
    global stop_fly
    height = 0.5
    flip_x = 1
    flip_y = 1

    if drone.xyz[1] < 0:
        flip_y = -1
    if drone.xyz[0] < 0:
        flip_x = -1
    drone.stop_moving()
    sleep(2)
    stop_fly = True
    goto(0,0, True)

    
    x, y = 0, 0.5
    for i in range(6):
        goto(x * flip_x, ';', y * flip_y, True)
        x = y
        y = 0
        goto(x * flip_x, ';', y * flip_y, True)
        y = x + 0.5
        x = 0


    
    


def fly():
    x = 3
    y = 3
    step = 1
    dist = y * 2

    drone.arm()
    drone.takeoff()
    sleep(10)
    drone.goto_yaw(0)

    for _ in range(dist // step + 1):
        if stop_fly: return
        goto(x, y)
        if stop_fly: return
        x = -x
        goto(x, y)
        if stop_fly: return
        y = y - step
    if y + step > -dist / 2:
        y = -dist / 2
        goto(x, y)
        x = -x
        goto(x, y)
    drone.stop_moving()
    drone.land()


Thread(target=photo, daemon=True).start()
fly()
