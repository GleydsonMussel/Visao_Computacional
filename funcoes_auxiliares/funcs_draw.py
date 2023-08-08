import cv2
import numpy as np

def desenha_roi(frame, x, w, y, h):
    cv2.rectangle(frame,(x, y), (x+w, y+h), (255,0,0),2)

def calc_centro_roi(x, w, y, h):
    cx = int(x+w/2); cy = int(y+h/2)
    return [cx, cy]

def desenha_centro(frame, cx, cy):
    cv2.circle(frame, (cx,cy), 5, (0,0,255),-1)
    
def desenha_Area(frame, area, cor):
    cv2.polylines(frame,[np.array(area, np.int32)], True, cor, 2)
    
def escreve_no_video(frame, texto, posicao, cor):
    fonte = cv2.FONT_HERSHEY_SIMPLEX
    tamanho = 1; grossura = 2    
    cv2.VideoWriter()
    cv2.putText(frame, texto,posicao, fonte, tamanho, cor, grossura)