import cv2
import numpy as np
import glob
import redimensiona

def teste_calibracao(pathCoefficients, mtx, dist):
    # Importa as imagens do diretório           Crio um contador 
    imgs = glob.glob("./calibracao/amostras/*.png"); cont = 0;           
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
        cv2.imwrite('./calibracao/res_calibracao/calib'+str(cont)+'.png', calib)
        cont+=1
        
    print("Calibração testada")


        
    