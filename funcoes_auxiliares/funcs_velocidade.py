import math
import funcoes_auxiliares.funcs_draw as funcs_draw
import funcoes_auxiliares.funcs_manip_arq as funcs_manip_arq
import funcoes_auxiliares.plot_graficos as plot_graficos

# Voo 6
#fatConvPxM = 0.0050

# Atrito 1
fatConvPxM = 0.0065

def calc_velocidades(x,y,w,h, cxant, cyant,cont, fps, distanciaPercorridaPassada, alturaPercorridaPassada, h0):
    
    cx, cy = funcs_draw.calc_centro_roi(x,w,y,h)

    if h0==-999999999999:
        h0 = cy

    # Cálculos
    deltaT = 1/fps; distancia_percorrida_x = (cx-cxant)*fatConvPxM; distancia_percorrida_y = (cy-cyant)*fatConvPxM
    distanciaPercorridaPassada +=distancia_percorrida_x; alturaPercorridaPassada+=distancia_percorrida_y
    alturaPercorridaRefh0 = (cy - h0)*fatConvPxM 
    velocidade = distancia_percorrida_x/deltaT
    dados = [velocidade, distancia_percorrida_x, distancia_percorrida_y, distancia_percorrida_x, deltaT*cont, cxant, cx, distanciaPercorridaPassada, alturaPercorridaPassada, alturaPercorridaRefh0]
    caminhos = ["./logs/velocidade_percorrida_em_cada_frame.txt", 
                "./logs/distancia_percorrida_x_em_cada_frame.txt", 
                "./logs/distancia_percorrida_y_em_cada_frame.txt",
                "./logs/distancia_percorrida_em_cada_frame.txt", 
                "./logs/tempo_decorrido.txt", 
                "./logs/poscoes_x_centro_antigas.txt", 
                "./logs/poscoes_x_centro_atuais.txt", 
                "./logs/distancias_cumulativas.txt", 
                "./logs/alturasCumulativas.txt",
                "./logs/alturaPercorrida_Ref_h0.txt"
                ]
    
    for i in range(len(dados)):
        funcs_manip_arq.salva_dado(dados[i], cont, caminhos[i])
        
    return [distanciaPercorridaPassada, alturaPercorridaPassada, h0]

def calc_velocidades_diagonalmente(x,y,w,h, cxant, cyant,cont, fps, distanciaPercorridaPassada, alturaPercorridaPassada, h0):
    
    cx, cy = funcs_draw.calc_centro_roi(x,w,y,h)

    if h0==-999999999999:
        h0 = cy
        
    # Cálculos
    deltaT = 1/fps
    distancia_percorrida_x = (cx-cxant)*fatConvPxM; distancia_percorrida_y = (cy-cyant)*fatConvPxM
    distancia_percorrida = math.sqrt(((distancia_percorrida_x*distancia_percorrida_x) + (distancia_percorrida_y*distancia_percorrida_y)))
    alturaPercorridaRefh0 = (cy - h0)*fatConvPxM 
    velocidade = distancia_percorrida/deltaT
    distanciaPercorridaPassada +=distancia_percorrida; alturaPercorridaPassada+=distancia_percorrida_y
    dados = [velocidade, distancia_percorrida_x, distancia_percorrida_y, distancia_percorrida, deltaT*cont, cxant, cx, distanciaPercorridaPassada, alturaPercorridaPassada, alturaPercorridaRefh0]
    caminhos = ["./logs/velocidade_percorrida_em_cada_frame.txt", 
                "./logs/distancia_percorrida_x_em_cada_frame.txt", 
                "./logs/distancia_percorrida_y_em_cada_frame.txt", 
                "./logs/distancia_percorrida_em_cada_frame.txt",
                "./logs/tempo_decorrido.txt", 
                "./logs/poscoes_x_centro_antigas.txt", 
                "./logs/poscoes_x_centro_atuais.txt", 
                "./logs/distancias_cumulativas.txt", 
                "./logs/alturasCumulativas.txt",
                "./logs/alturaPercorrida_Ref_h0.txt"
                ]
    
    for i in range(len(dados)):
        funcs_manip_arq.salva_dado(dados[i], cont, caminhos[i])
        
    return [distanciaPercorridaPassada, alturaPercorridaPassada, h0]

def salvaGraficosVelocidade(sourceDados1, sourceDados2, titulos, labelsX, labelsY):
    for i in range(len(sourceDados1)):
        plot_graficos.plot_grafico( sourceDados1[i], sourceDados2[i], titulos[i], labelsX[i], labelsY[i])        
        
     
