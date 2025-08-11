import cv2


class CameraError(IOError):
    def __init__(self, message: str = 'CameraError'):
        self.message = message

    def __str__(self):
        return self.message


class Camera:
    def __init__(self, address: str | int) -> None:
        self.c = cv2.VideoCapture(address)
    
    def get(self):
        res, frame = self.c.read()
        if res:
            return frame
        else:
            raise CameraError('no frame')
