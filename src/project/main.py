from pion import Pion
from threading import Thread
from time import sleep
from ultralytics import YOLO
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

drone = Pion(ip,port)
model = YOLO(model_path)

cow_boxes = [(-2.83,1.61), (-2.88,-3.32), (3.55,-2.85)]

frame = None


def detect():
    while True:
        if frame is None:
            continue

        results = model.predict(frame)
        # print('-> ', end='')
        
        for result in results:
            if result.boxes == None:
                continue

            position = list(result.boxes.xywh)
            print(position)
            if position == []:continue
            bot_x,bot_y = get_geobot_coords(position[0][0],position[0][1])
            print('bot x position:', bot_x, '\r\n', 'bot y position:', bot_y)
            quit()
            # frame = cv2.drawMarker(frame, (int(position[0]), int(position[1])), (255,0,0))
            
            names = [result.names[cls.item()] for cls in result.boxes.cls.int()]
            print(names)


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
    global_x = 1.2*height*cam_x
    global_y = 0.9*height*cam_y

    drone_pos_x, drone_pos_y = drone.xyz[0], drone.xyz[1]

    geobot_x = drone_pos_x+global_x
    geobot_y = drone_pos_y+global_y

    return geobot_x, geobot_y


def calculate_trajectory_to():
    pass


def goto(x, y: float):
    drone.goto(x, y, height, 0, wait=True)
    sleep(1)


def fly():
    x = 4
    y = 4
    step = 1
    dist = y * 2

    drone.arm()
    drone.takeoff()
    sleep(10)

    for _ in range(dist//step+1):
        goto(x,y)
        x = -x
        goto(x,y)
        y = y-step
    if y + step > -dist / 2:
        y = -dist / 2
        goto(x,y)
        x = -x
        goto(x,y)

    drone.land()


Thread(target=photo, daemon=True).start()
# fly()
