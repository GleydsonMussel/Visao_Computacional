import cv2
import winsound
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import Methods.Manipulate_Files as Manip

# Limpa os diretórios necessários para realizar a calibração
Manip.clean_calibrations_processing()

# Parâmetros para fazer o barulho de quando um frame é salvo
frequency = 2000 ; duration = 300; cont = 0  

video = cv2.VideoCapture('./videos/Calibracao/Google_Pixel_7/video.mp4')

while True:

    frame = video.read()[1]
    
    if frame is None:
        break
    
    k = cv2.waitKey(1)

    if k == ord('s') or cont==0:
        cv2.imwrite('./Calibration/Samples/sample'+str(cont)+'.png', frame)
        print("Imagens salvas: "+str(cont))  
        winsound.Beep(frequency, duration)          
        cont+=1
        
    elif k == ord('q'):
        break

    cv2.imshow('Reproduzindo Video', frame)
    
    