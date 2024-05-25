import cv2
import numpy as np
import glob
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import Methods.Manipulate_Files as Manip
import Methods.Calibration as Calib

#-----------------------------PREENCHER-----------------------------------
pathCoefficients = './Cameras_Data/celular_Gleydson2/coeficientes_Zoom_1x.npz'
# Tamanho dos quadrados na vida real em m
tamQuad = 0.025
#--------------------------------------------------------------------------

# Dimensões do tabuleiro
CHECKERBOARD = (7, 11)

# Critério de parada
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# Creating vector to store vectors of 3D points for each checkerboard image
objpoints = []
# Creating vector to store vectors of 2D points for each checkerboard image
imgpoints = [] 
 
# Defining the world coordinates for 3D points
objp = np.zeros((1, CHECKERBOARD[0] * CHECKERBOARD[1], 3), np.float32)
objp[0,:,:2] = np.mgrid[0:CHECKERBOARD[0], 0:CHECKERBOARD[1]].T.reshape(-1, 2)

lins, cols, prof = objp.shape

# Preencho considerando a largura real dos quadrados em m
for i in range(0, lins):
    for j in range(0, cols): 
            objp[i][j] = [objp[i][j][0]*tamQuad, objp[i][j][1]*tamQuad, 0]

# Pegas as imagens na pasta

imgs = glob.glob("./Calibration/Samples/*.png"); cont = 0

for file in imgs:

    frame = cv2.imread(file)
    
    if frame is None:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cv2.waitKey(30)
    
    # corners: coordenada de cada um dos pontos encontrados referente a imagem
    achouNumeroDePontosDeReferenciaCerto, corners = cv2.findChessboardCorners(gray, CHECKERBOARD, cv2.CALIB_CB_ADAPTIVE_THRESH + cv2.CALIB_CB_FAST_CHECK + cv2.CALIB_CB_NORMALIZE_IMAGE)
    
    if achouNumeroDePontosDeReferenciaCerto == True:
        # Dá um append nas coordenadas do objeto localizado na imagem
        objpoints.append(objp)
        # refining pixel coordinates for given 2d points.
        corners2 = cv2.cornerSubPix(gray, corners, (11,11),(-1,-1), criteria)
        # Vai salvando os corners baseado agora nos subpixcels
        imgpoints.append(corners2)
        # Draw and display the corners
        img = cv2.drawChessboardCorners(frame, CHECKERBOARD, corners2, achouNumeroDePontosDeReferenciaCerto)

        cv2.imwrite('./Calibration/Res_Calib/original'+str(cont)+'.png', img)
        
        cv2.imshow('Calibrando', img)
        
        k = cv2.waitKey(1) 

        if k == ord('q'):
            break
        
        print("ACHOU "+str(cont))
    
    else:
        print("Procurando pontos... "+str(cont))
        cv2.destroyAllWindows()
    
    cv2.imshow('Calibrando', frame)
    
    cont+=1
    
# Parte para a calibração
ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

# Pega as dimensões do gray usado
h,  w = gray.shape[:2]

# Refina a matrix dos coeficientes de distorção
newcameramtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (w,h), 0, (w,h))

np.savez(pathCoefficients, distortion=dist, camera=mtx, new_camera = newcameramtx)

incerteza = 0

for i in range(len(objpoints)):
 imgpoints2, _ = cv2.projectPoints(objpoints[i], rvecs[i], tvecs[i], mtx, dist)
 error = cv2.norm(imgpoints[i], imgpoints2, cv2.NORM_L2)/len(imgpoints2)
 incerteza += error
 
print("Incerteza total: {}".format(incerteza/len(objpoints)))

Calib.test_calibration(pathCoefficients, mtx, dist)



