from pion import Pion
from threading import Thread
from time import sleep
from ultralytics import YOLO
import cv2


drone = Pion('127.0.0.1', '8000')

height = 0.4


def goto(x, y: float):
    drone.goto(x, y, height, 0, wait=True)
    sleep(1)

