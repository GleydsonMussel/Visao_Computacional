import cv2
import os

def salvaFrame(caminho, frame):
    cv2.imwrite(caminho, frame)
    
def salva_dado(dado, cont, caminho):
    if cont==0:
        with open(caminho, 'w') as arquivo:
                arquivo.write(str(dado))
                arquivo.write('\n')
    else:
        with open(caminho, 'a') as arquivo:
            arquivo.write(str(dado))
            arquivo.write('\n')
    
def limpa_frames_logs():

    dir = './frames'
    for arquivo in os.listdir(dir):
        os.remove(os.path.join(dir, arquivo))

    dir = './logs/'
    for arquivo in os.listdir(dir):
        os.remove(os.path.join(dir, arquivo))

def limpa_calibracao():

    dir = './calibracao/res_calibracao/'
    for arquivo in os.listdir(dir):
        os.remove(os.path.join(dir, arquivo))
    dir = './calibracao/amostras/'
    for arquivo in os.listdir(dir):
        os.remove(os.path.join(dir, arquivo))
        
def limpa_res_teste_calibracao():
    dir = "./calibracao/res_calib_teste_video/"
    for arquivo in os.listdir(dir):
        os.remove(os.path.join(dir, arquivo))