import numpy as np

class CameraData:
    def __init__(self, path_to_data) -> None:
        dadosCalib = np.load(path_to_data)
        self.distortion = dadosCalib['distortion']
        self.mtx = dadosCalib['camera']; 
        self.newCameraMtx = dadosCalib['new_camera']