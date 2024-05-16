import cv2
import numpy as np
import sys
import os

from funcoes_auxiliares import funcs_manip_arq
from funcoes_auxiliares import redimensiona

# Obtenha o caminho absoluto para a pasta 'funcoes_auxiliares'
caminho_funcoes_auxiliares = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'funcoes_auxiliares'))
# Adicione o caminho ao diretório de busca do Python
sys.path.append(caminho_funcoes_auxiliares)

funcs_manip_arq.limpa_res_teste_calibracao()

video = cv2.VideoCapture("./videos/Voos/Voo6Editado.mp4")
dadosCalib = np.load('./coeficientes/celular_Ronaldo/coeficientes2.npz')

dist = dadosCalib['distortion']; mtx = dadosCalib['camera']; newcameramtx = dadosCalib['new_camera']; distpercorridaPassada = 0; alturapercorrisaPassada = 0

redimensionaJanela = True
contFrame = 0

while True:
    
    frame = video.read()[1]
    if frame is None:
        break
    funcs_manip_arq.salvaFrame('./calibracao/res_calib_teste_video/frameCRU_'+str(contFrame)+'.png', frame)
    frame = cv2.undistort(frame, mtx, dist, None, newcameramtx)
    funcs_manip_arq.salvaFrame('./calibracao/res_calib_teste_video/frameCALIB_'+str(contFrame)+'.png', frame)
    
    print("Li o frame: "+str(contFrame))
    contFrame+=1
    
    if redimensionaJanela:
        cv2.imshow('Calibrando', redimensiona.redimensiona(50, frame))
    else:
        cv2.imshow('Calibrando', frame)
        
    k = cv2.waitKey(100)
    
    if k == ord('q'):
        break


