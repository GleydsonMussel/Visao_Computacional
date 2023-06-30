import cv2
import numpy as np
import glob
from funcoes_auxiliares import funcs_manip_arq
from funcoes_auxiliares.teste_calibrador import teste_calibracao
from funcoes_auxiliares.redimensiona import redimensiona
    
# Dimensões do tabuleiro, ou seja, o número de quadrados a serem analisados na horizontal e na vertical
CHECKERBOARD = (7, 11)
# Define o critério de parada
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
# Limpo a pasta de imagens da calibração
funcs_manip_arq.limpa_calibracao()

# Creating vector to store vectors of 3D points for each checkerboard image
objpoints = []
# Creating vector to store vectors of 2D points for each checkerboard image
imgpoints = [] 
 
# Defining the world coordinates for 3D points
objp = np.zeros((1, CHECKERBOARD[0] * CHECKERBOARD[1], 3), np.float32)
objp[0,:,:2] = np.mgrid[0:CHECKERBOARD[0], 0:CHECKERBOARD[1]].T.reshape(-1, 2)

# Pego as dimensões da matrix
lins, cols, prof = objp.shape
# Tamanho dos quadrados na vida real em m
tamQuad = 0.02
# Preencho considerando a largura real dos quadrados em m
for i in range(0, lins):
    for j in range(0, cols): 
            objp[i][j] = [objp[i][j][0]*tamQuad, objp[i][j][1]*tamQuad, 0]

# Importa as imagens do diretório           Crio um contador
imgs = glob.glob("./images/samples/*.png"); cont = 0
# Porcentagem para o resize
scale_percent = 50
# Começa a percorrer
for file in imgs:
    frame = cv2.imread(file)
    if frame is None:
        break
    # Redimensionamento para caber na tela, se necessario
    width = int(frame.shape[1] * scale_percent / 100)
    height = int(frame.shape[0] * scale_percent / 100)
    dim = (width, height)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cv2.waitKey(30)
    # ret: retorna se o número desejado de pontos foi encontrado, corners: coordenada de cada um dos pontos encontrados referente a imagem
    ret, corners = cv2.findChessboardCorners(gray, CHECKERBOARD, cv2.CALIB_CB_ADAPTIVE_THRESH + cv2.CALIB_CB_FAST_CHECK + cv2.CALIB_CB_NORMALIZE_IMAGE)
    # Se achou o número de pontos de referencia desejados
    if ret == True:
        # Dá um append nas coordenadas do objeto localizado na imagem
        objpoints.append(objp)
        # refining pixel coordinates for given 2d points.
        corners2 = cv2.cornerSubPix(gray, corners, (11,11),(-1,-1), criteria)
        # Vai salvando os corners baseado agora nos subpixcels
        imgpoints.append(corners2)
        # Draw and display the corners
        img = cv2.drawChessboardCorners(frame, CHECKERBOARD, corners2, ret)
        cv2.imwrite('./images/res_calibracao/original'+str(cont)+'.png', img)
        # Mostra na tela as imagens sendo pegas
        redimensionada = redimensiona(50, img)
        cv2.imshow('Calibrando', redimensionada)
        k = cv2.waitKey(30) 
        # Se digitar q, aborta o programa
        if k == ord('q'):
            break
        print("ACHOU "+str(cont))
    # Caso não ache os pontos logo de cara, printa no terminal que ainda está procurando
    else:
        print("Procurando pontos... "+str(cont))
    # Atualiza o contador 
    cont+=1
    
# Parte para a calibração
ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)
# Pega as dimensões do gray usado
h,  w = gray.shape[:2]
# Refina a matrix dos coeficientes de distorção
newcameramtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (w,h), 1, (w,h))
# Caminho para os coeficientes
pathCoefficients = './coeficientes/celular_Gleydson/coeficientes.npz'
# Salva os coeficientes
np.savez(pathCoefficients, distortion=dist, camera=mtx, new_camera = newcameramtx)
# Testa a calibração
teste_calibracao(pathCoefficients, ret, mtx, dist, rvecs, tvecs, objpoints, imgpoints)



