import cv2
import funcoes_auxiliares.funcs_draw as funcs_draw
import funcoes_auxiliares.funcs_manip_arq as funcs_manip_arq

fatConvPxM = 0.0010612691466083

def get_resolucao(frame):
    return [frame.shape[1], frame.shape[0]]

def calc_velocidades(frame, x,y,w,h, cxant, cyant, tempo0, cont):
    cx, cy = funcs_draw.calc_centro_roi(x,y,w,h)
    largura, altura = get_resolucao(frame)
    print("Largura: "+str(largura)+" Altura: "+str(altura)+"\n")
    tempo1 = cv2.getTickCount()
    deltaT = (tempo1 - tempo0)/cv2.getTickFrequency()
    distancia_percorrida = (cx-cxant)*fatConvPxM
    velocidade = distancia_percorrida/deltaT
    funcs_manip_arq.salva_velocidade(velocidade, cont)
    funcs_manip_arq.salva_dist_percorrida(distancia_percorrida, cont)

