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
camera_ip = 'rtsp://10.1.100.160:8554/pioneer_stream'
model_path = 'best.pt'

drone = Pion(ip,port)
model = YOLO(model_path)


def photo():
    camera = Camera(camera_ip)

    while True:
        frame = camera.get()

        results = model.predict(frame)
        print('-> ', end='')
        for result in results:
            if result.boxes == None:
                continue

            position = result.boxes.xywh
            # frame = cv2.drawMarker(frame, (int(position[0]), int(position[1])), (255,0,0))
            names = [result.names[cls.item()] for cls in result.boxes.cls.int()]
            print(names)

        cv2.imshow('frame', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


def goto(x, y: float):
    drone.goto(x, y, height, 0)
    sleep(5)


def fly():
    x = 4
    y = 4
    step = 1
    dist = y * 2

    drone.arm()
    sleep(5)
    drone.takeoff()

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
#fly()
