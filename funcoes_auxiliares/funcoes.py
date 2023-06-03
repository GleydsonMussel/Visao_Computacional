import cv2
import numpy as np
import os

fatConvPxM = 0.0010612691466083

def desenha_roi(frame, x, w, y, h):
    cv2.rectangle(frame,(x, y), (x+w, y+h), (255,0,0),2)

def calc_centro_roi(x, w, y, h):
    cx = int(x+w/2)
    cy = int(y+h/2)
    return [cx, cy]

def desenha_centro(frame, cx, cy):
    cv2.circle(frame, (cx,cy), 5, (0,0,255),-1)

def salvaFrame(frame, caminho):
    cv2.imwrite(caminho , frame)

def desenha_Area(frame, area, cor):
    cv2.polylines(frame,[np.array(area, np.int32)], True, cor, 2)

def escreve_no_video(frame, texto, posicao, cor):
    # Firulas para escrever texto no vídeo
    fonte = cv2.FONT_HERSHEY_SIMPLEX
    # Tamanho da fonte
    tamanho = 1
    # Grossura da letra
    grossura = 2    
    # Efetivamente escreve no vídeo
    cv2.VideoWriter()
    cv2.putText(frame, texto,posicao, fonte, tamanho, cor, grossura)

def entrou_na_area(area, x,w,y,h):
    cx, cy = calc_centro_roi(x,w,y,h)
    # Lista de coordenadas x e lista de coordenadas y
    xs = []
    ys = []
    # Pego as coordenadas xs e ys
    for ponto in area:
        xs.append(ponto[0])
        ys.append(ponto[1])
    # Filtro as maiores de cada uma
    menorX = min(xs); maiorX = max(xs)
    menorY = min(ys); maiorY = max(ys)
    #print(menorX)
    #print(maiorX)
    #print(cx)
    #print("x CSE da bbox: "+str(x)+"Largura da bbox: "+str(w)+"\n")
    # Checo se o centro da roi está na área
    if((cx>=menorX and cx<=maiorX)  and not(cx>=1315 and cx<=1371)):
    #if((cx>=menorX and cx<=maiorX)): 
        return True

    return False
   
def get_resolucao(frame):
    return [frame.shape[0], frame.shape[1]]

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
            
def calc_velocidades(frame, x,y,w,h, cxant, cyant, tempo0, cont):
    cx, cy = calc_centro_roi(x,y,w,h)
    largurara, altura = get_resolucao(frame)
    tempo1 = cv2.getTickCount()
    deltaT = (tempo1 - tempo0)/cv2.getTickFrequency()
    distancia_percorrida = (cx-cxant)*fatConvPxM
    velocidade = distancia_percorrida/deltaT
    salva_velocidade(velocidade, cont)
    salva_dist_percorrida(distancia_percorrida, cont)
    
def limpa_pastas():
    # Limpa pasta de imagens
    dir = './frames/frames_na_area/'
    for arquivo in os.listdir(dir):
        os.remove(os.path.join(dir, arquivo))
    # Limpa pastas de logs
    dir = './log/'
    for arquivo in os.listdir(dir):
        os.remove(os.path.join(dir, arquivo))
