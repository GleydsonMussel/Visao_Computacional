import cv2
import winsound
from funcoes_auxiliares import funcs_manip_arq 
import funcoes_auxiliares.redimensiona as redimensiona
 
funcs_manip_arq.limpa_calibracao()       

frequency = 2000 ;          duration = 300  

video = cv2.VideoCapture('./videos/Calibracao/Cel_Ronaldo/AAAA.mp4')

cont = 0

while True:

    frame = video.read()[1]
    if frame is None:
        break
    
    k = cv2.waitKey(5)

    if k == ord('s') or cont==0:
        cv2.imwrite('./images/storage/sample'+str(cont)+'.png', frame)
        print("Imagens salvas: "+str(cont))  
        winsound.Beep(frequency, duration)          
        cont+=1
        
    elif k == ord('q'):
        break

    cv2.imshow('Calibrando', frame)
    k = cv2.waitKey(5) 
    
    