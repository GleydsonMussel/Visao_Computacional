import cv2
import numpy as np
import funcoes_auxiliares.funcs_manip_arq as funcs_manip_arq
import funcoes_auxiliares.redimensiona as redimensiona

funcs_manip_arq.limpa_res_teste_calibracao()

video = cv2.VideoCapture("./videos/Voos/Voo1.mp4")
dadosCalib = np.load('./coeficientes/celular_Vitor/coeficientes.npz')

dist = dadosCalib['distortion']; mtx = dadosCalib['camera']; newcameramtx = dadosCalib['new_camera']; distpercorridaPassada = 0; alturapercorrisaPassada = 0

redimensionaJanela = True
contFrame = 0

while True:
    
    frame = video.read()[1]
    if frame is None:
        break
    funcs_manip_arq.salvaFrame('./images/res_calib_video_teste/frameCRU'+str(contFrame)+'.png', frame)
    frame = cv2.undistort(frame, mtx, dist, None, newcameramtx)
    funcs_manip_arq.salvaFrame('./images/res_calib_video_teste/frameCALIB'+str(contFrame)+'.png', frame)
    
    print("Li o frame: "+str(contFrame))
    contFrame+=1
    
    if redimensionaJanela:
        cv2.imshow('Calibrando', redimensiona.redimensiona(50, frame))
    else:
        cv2.imshow('Calibrando', frame)
        
    k = cv2.waitKey(100)
    
    if k == ord('q'):
        break


