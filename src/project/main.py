from pion import Pion
from threading import Thread
from time import sleep
from ultralytics import YOLO
import numpy as np
import cv2

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
            bot_x, bot_y = get_geobot_coords(position[0][0], position[0][1])
            print('bot position:', bot_x, bot_y)
            print('drone position:', *drone.xyz[0:2])
            print('going from:', *calculate_trajectory((bot_x, bot_y), (-2.83, 1.61)))

            names = [result.names[cls.item()] for cls in result.boxes.cls.int()]
            print(names)
            if ('cow1' in names) or ('cow2' in names):
                cow_go((bot_x, bot_y), cow_boxes[0])
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


def get_geobot_coords(cam_x, cam_y):
    frame_width_global = height * 1.2
    frame_height_global = height * 0.9

    bot_x = (cam_x * frame_width_global) / 640
    bot_y = (cam_y * frame_height_global) / 480

    return drone.xyz[0] + bot_x, drone.xyz[1] + bot_y


def calculate_trajectory(bot_pos: tuple, base_pos: tuple):
    bot = np.array(bot_pos)
    base = np.array(base_pos)
    dist = base - bot
    dist = dist / np.linalg.norm(dist)
    dist = -dist * 0.5
    dist += bot_pos

    return dist[0], dist[1]


def goto(x, y: float, force=False):
    
    while stop_fly and not force:
        sleep(1)
    drone.goto(x, y, height, 0, wait=True)
    sleep(1)



def cow_go(bot: tuple, base: tuple):
    global stop_fly
    global height
    stop_fly = True
    drone.stop_moving()
    sleep(2)

    drone_goto_x, drone_goto_y = calculate_trajectory(bot, base)

    height = 0.35
    goto(drone_goto_x, drone_goto_y, True)
    goto(-2.83, 1.61, True)

    goto(1.2, -3.8, True)
    drone.stop_moving()
    drone.land()


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
