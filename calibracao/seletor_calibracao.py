import cv2
import sys
import winsound
import os
# Obtenha o caminho absoluto para a pasta 'funcoes_auxiliares'
caminho_funcoes_auxiliares = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'funcoes_auxiliares'))
# Adicione o caminho ao diretório de busca do Python
sys.path.append(caminho_funcoes_auxiliares)
import funcs_manip_arq
import redimensiona
 
funcs_manip_arq.limpa_calibracao()      

frequency = 2000 ;          duration = 300  

video = cv2.VideoCapture('./videos/Calibracao/Cel_Ronaldo/calibRonaldo.mp4')

cont = 0

while True:

    frame = video.read()[1]
    
    if frame is None:
        break
    
    k = cv2.waitKey(1)

    if k == ord('s') or cont==0:
        cv2.imwrite('./calibracao/amostras/sample'+str(cont)+'.png', frame)
        print("Imagens salvas: "+str(cont))  
        winsound.Beep(frequency, duration)          
        cont+=1
        
    elif k == ord('q'):
        break

    cv2.imshow('Reproduzindo Video', frame)
    
    