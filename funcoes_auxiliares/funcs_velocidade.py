import funcoes_auxiliares.funcs_draw as funcs_draw
import funcoes_auxiliares.funcs_manip_arq as funcs_manip_arq

# Constantes
fatConvPxM = 0.00101750547; altura_mesa = 0.9

def calc_velocidades(x,y,w,h, cxant, cyant,cont, fps):
    
    # Recalculando centro
    cx, cy = funcs_draw.calc_centro_roi(x,w,y,h)

    # Cálculos
    deltaT = 1/fps
    distancia_percorrida_x = (cx-cxant)*fatConvPxM
    distancia_percorrida_y = (cy-cyant)*fatConvPxM + altura_mesa
    velocidade = distancia_percorrida_x/deltaT
    
    # Salvando dados
    funcs_manip_arq.salva_dado(velocidade, cont, "./logs/velocidade_percorrida_em_cada_frame.txt")
    funcs_manip_arq.salva_dado(distancia_percorrida_x, cont, "./logs/distancia_percorrida_x_em_cada_frame.txt")
    funcs_manip_arq.salva_dado(distancia_percorrida_y, cont, "./logs/distancia_percorrida_y_em_cada_frame.txt")
    funcs_manip_arq.salva_dado(deltaT*cont, cont, "./logs/tempo_decorrido.txt")
    funcs_manip_arq.salva_dado(cxant, cont, "./logs/poscoes_x_centro_antigas.txt")
    funcs_manip_arq.salva_dado(cx, cont, "./logs/poscoes_x_centro_atuais.txt")

