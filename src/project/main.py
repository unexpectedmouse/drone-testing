from pion import Pion

height = 2
ip = "127.0.0.1"
drone = Pion()

def goto(x, y: float):
    drone.goto(x, y, height, 0, wait=True)


def fly():
    drone.arm()
    drone.takeoff()

    goto(1, 1)

    drone.land()
    drone.disarm()

fly()