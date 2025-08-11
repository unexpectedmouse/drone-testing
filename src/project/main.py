from pion import Pion
import cv2
from camera import Camera
from threading import Thread

height = 2
ip = "127.0.0.1"
camera_ip = '127.0.0.1'
port = 8000
drone = Pion(ip,port)


def goto(x, y: float):
    drone.goto(x, y, height, 0, wait=True)


def photo():
    camera = Camera(camera_ip)

    while True:
        frame = camera.get()
        cv2.imshow('frame', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


def fly():
    x = 4
    y = 4
    step = 1
    dist = y * 2

    drone.arm()
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
    drone.disarm()

Thread(target=photo, daemon=True).start()
fly()