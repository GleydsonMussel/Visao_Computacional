import cv2
import winsound
from funcoes_auxiliares import funcs_manip_arq 
 
# Limpo a pasta de imagens da calibração
funcs_manip_arq.limpa_calibracao()       
# Frequencia de 2500 Hz     Duração de 0.3 s 
frequency = 2000 ;          duration = 300  
# Pego o video                                          Crio um contador
video = cv2.VideoCapture('./videos/calibracao.mp4');    cont = 0

while True:
    # Extraio um frame
    frame = video.read()[1]
    
    if frame is None:
        break
    k = cv2.waitKey(5)
    if k == ord('s'):
        cv2.imwrite('./images/storage/sample'+str(cont)+'.png', frame)
        print("Imagens salvas: "+str(cont))  
        winsound.Beep(frequency, duration)           
        # Atualiza o contador
        cont+=1
    elif k == ord('q'):
        break
    # Mostra na tela as imagens sendo pegas
    cv2.imshow('Calibrando', frame)
    k = cv2.waitKey(5) 
    # Se digitar q, aborta o programa
    if k == ord('q'):
        break
    
    