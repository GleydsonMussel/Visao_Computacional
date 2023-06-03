import cv2
import os

def salva_velocidade(velocidade, cont):
    if cont==0:
        with open('./log/velocidade_percorrida_em_cada_frame.txt', 'w') as arquivo:
                arquivo.write(str(velocidade))
                arquivo.write('\n')
    else:
        with open('./log/velocidade_percorrida_em_cada_frame.txt', 'a') as arquivo:
            arquivo.write(str(velocidade))
            arquivo.write('\n')

def salva_dist_percorrida(dist, cont):
    if cont==0:
        with open('./log/distancia_percorrida_em_cada_frame.txt', 'w') as arquivo:
                arquivo.write(str(dist))
                arquivo.write('\n')
    else:
        with open('./log/distancia_percorrida_em_cada_frame.txt', 'a') as arquivo:
            arquivo.write(str(dist))
            arquivo.write('\n')

def salvaFrame(frame, caminho):
    cv2.imwrite(caminho , frame)
    
def limpa_pastas():
    # Limpa pasta de imagens
    dir = './frames/frames_na_area/'
    for arquivo in os.listdir(dir):
        os.remove(os.path.join(dir, arquivo))
    # Limpa pastas de logs
    dir = './log/'
    for arquivo in os.listdir(dir):
        os.remove(os.path.join(dir, arquivo))