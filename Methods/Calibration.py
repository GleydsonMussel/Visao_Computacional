import cv2
import numpy as np
import glob
import Cameras_Data

def aply_calib(frame, camera_data, charuco = False):
    if charuco:
        clean_frame = cv2.undistort(frame, camera_data.mtx, camera_data.distortion, camera_data.roi, camera_data.newCameraMtx)
        x, y, w, h = camera_data.roi
        return clean_frame[y:y+h, x:x+w]
    else:
        clean_frame = cv2.undistort(frame, camera_data.mtx, camera_data.distortion, None, camera_data.newCameraMtx)
    return clean_frame

def test_calibration(pathCoefficients, mtx, dist):
    # Importa as imagens do diretório           Crio um contador 
    imgs = glob.glob("./Calibration/Samples/*.png"); cont = 0;           
    # Carregar os coeficientes do arquivo
    data = np.load(pathCoefficients)
    if data is None:
        return
    # Acessar os coeficientes salvos
    dist = data['distortion']
    mtx = data['camera']
    newcameramtx = data['new_camera']
    for img in imgs:
        frame = cv2.imread(img)
        calib = cv2.undistort(frame, mtx, dist, None, newcameramtx)
        cv2.imwrite('./Calibration/Res_Calib/calib'+str(cont)+'.png', calib)
        cont+=1
        
    print("Cagayake! Girls")


        
    