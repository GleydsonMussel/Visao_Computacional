from asyncio import sleep
import cv2
import numpy as np

def desenha_roi(frame, x, w, y, h):
    cv2.rectangle(frame,(x, y), (x+w, y+h), (255,0,0),2)

def calc_centro_roi(x, w, y, h):
    cx = int(x+w/2)
    cy = int(y+h/2)
    return [cx, cy]

def desenha_centro(frame, x, w, y, h):
    cx, cy = calc_centro_roi(x,w,y,h)
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
    print(menorX)
    print(maiorX)
    print(cx)
    sleep(100)
    # Checo se o centro da roi está na área
    if((cx>=menorX and cx<=maiorX) and (cy>=menorY and cy<=maiorY)):
        return True

    return False    
