import cv2
import numpy as np
import glob
import funcoes_auxiliares.redimensiona as redimensiona

def teste_calibracao(pathCoefficients, ret, mtx, dist, rvecs, tvecs, objpoints, imgpoints):
    # Importa as imagens do diretório           Crio um contador    # Pego o erro
    imgs = glob.glob("./images/samples/*.png"); cont = 0;           meanError = 0
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
        cv2.imwrite('./images/res_calibracao/calib'+str(cont)+'.png', calib)
        cont+=1
        #meanError+=get_incerteza(mtx, dist, rvecs, tvecs, objpoints, imgpoints, cont, meanError)
        
    print("Calibração testada")

def get_incerteza(mtx, dist, rvecs, tvecs, objpoints, imgpoints, i, meanError):
    imgpoints2, _ = cv2.projectPoints(objpoints[i], rvecs[i], tvecs[i], mtx, dist)
    error = cv2.norm(imgpoints[i], imgpoints2, cv2.NORM_L2)/len(imgpoints2)
    meanError += error
    print( "total error: {}".format(meanError/len(objpoints)) )
    return meanError

        
    