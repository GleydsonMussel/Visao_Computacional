import cv2
import os

def salvaFrame(frame, caminho):
    cv2.imwrite(caminho , frame)
    
def salva_dado(dado, cont, caminho):
    if cont==0:
        with open(caminho, 'w') as arquivo:
                arquivo.write(str(dado))
                arquivo.write('\n')
    else:
        with open(caminho, 'a') as arquivo:
            arquivo.write(str(dado))
            arquivo.write('\n')
    
def limpa_pastas():
    # Limpa pasta de imagens
    dir = './frames'
    for arquivo in os.listdir(dir):
        os.remove(os.path.join(dir, arquivo))
    # Limpa pastas de logs
    dir = './logs/'
    for arquivo in os.listdir(dir):
        os.remove(os.path.join(dir, arquivo))

def limpa_calibracao():
    # Limpa diretório de imagens da calibração
    dir = './images/res_calibracao/'
    for arquivo in os.listdir(dir):
        os.remove(os.path.join(dir, arquivo))