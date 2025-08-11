from pion import Pion

height = 2
ip = "127.0.0.1"
port = 8000
drone = Pion(ip,port)

def goto(x, y: float):
    drone.goto(x, y, height, 0, wait=True)


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


fly()