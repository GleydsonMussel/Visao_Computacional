import cv2
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import Methods.Manipulate_Files as Manip
import Methods.Calibration as Calib
import Classes.CameraData as CameraData

# Limpando as pastas para
Manip.clean_calibrations_processing()

#-----------------------------PREENCHER-----------------------------------

video = cv2.VideoCapture("./videos/Voos/Voo6Editado.mp4")

dadosCalib = CameraData('./Cameras_Data/celular_Ronaldo/coeficientes2.npz')

#--------------------------------------------------------------------------

contFrame = 0

while True:
    
    frame = video.read()[1]
    
    if frame is None:
        break
    
    Manip.save_data(frame, './Calibration/Res_Calib_Video_Processed/frameCRU_'+str(contFrame)+'.png')
    
    frame = Calib.aply_calib(frame, dadosCalib)

    Manip.save_data(frame, './Calibration/Res_Calib_Video_Processed/frameCALIB_'+str(contFrame)+'.png')
    
    cv2.imshow('Calibrando', frame)
    
    k = cv2.waitKey(100)
    
    print("Li o frame: "+str(contFrame))
    contFrame+=1
    
    if k == ord('q'):
        break


