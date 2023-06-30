import cv2
import winsound
from funcoes_auxiliares import funcs_manip_arq 
import funcoes_auxiliares.redimensiona as redimensiona
 
# Limpo a pasta de imagens da calibração
funcs_manip_arq.limpa_calibracao()       
# Frequencia de 2500 Hz     Duração de 0.3 s 
frequency = 2000 ;          duration = 300  
# Pego o video                                          Crio um contador
video = cv2.VideoCapture('./videos/f10.mp4');    cont = 0

while True:
    # Extraio um frame
    frame = video.read()[1]
    if frame is None:
        break
   # frame = redimensiona.redimensiona(50, frame)
    k = cv2.waitKey(5)
    k = 's'
    if k == ord('s') or k=='s':
        cv2.imwrite('./images/storage/sample'+str(cont)+'.png', frame)
        print("Imagens salvas: "+str(cont))  
        winsound.Beep(frequency, duration)           
        # Atualiza o contador
        cont+=1
    # Aborta o programa
    elif k == ord('q'):
        break
    # Mostra na tela as imagens sendo pegas
    cv2.imshow('Calibrando', frame)
    k = cv2.waitKey(5) 
    
    