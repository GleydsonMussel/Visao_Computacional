import cv2

def redimensiona(porcentagem, frame):
    width = int(frame.shape[1] * porcentagem / 100)
    height = int(frame.shape[0] * porcentagem / 100)
    dim = (width, height)
    frame = cv2.resize(frame, dim, interpolation = cv2.INTER_AREA)
    return frame