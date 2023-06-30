import math
import funcoes_auxiliares.funcs_draw as funcs_draw
import funcoes_auxiliares.funcs_manip_arq as funcs_manip_arq
import funcoes_auxiliares.plot_graficos as plot_graficos

# Constantes
fatConvPxM = 0.0017241379310345; altura_mesa = 0.9

def calc_velocidades(x,y,w,h, cxant, cyant,cont, fps, distanciaPercorridaPassada):
    # Recalculando centro
    cx, cy = funcs_draw.calc_centro_roi(x,w,y,h)

    # Cálculos
    deltaT = 1/fps; distancia_percorrida_x = (cx-cxant)*fatConvPxM; distancia_percorrida_y = (cy-cyant)*fatConvPxM + altura_mesa
    distanciaPercorridaPassada +=distancia_percorrida_x
    velocidade = distancia_percorrida_x/deltaT
    dados = [velocidade, distancia_percorrida_x, distancia_percorrida_y, deltaT*cont, cxant, cx, distanciaPercorridaPassada]
    caminhos = ["./logs/velocidade_percorrida_em_cada_frame.txt", "./logs/distancia_percorrida_x_em_cada_frame.txt", "./logs/distancia_percorrida_y_em_cada_frame.txt", "./logs/tempo_decorrido.txt", "./logs/poscoes_x_centro_antigas.txt", "./logs/poscoes_x_centro_atuais.txt", "./logs/distancias_cumulativas.txt"]
    # Salvando Gráficos
    for i in range(len(dados)):
        funcs_manip_arq.salva_dado(dados[i], cont, caminhos[i])
        
    return distanciaPercorridaPassada

def calc_velocidades_saida_chao(x,y,w,h, cxant, cyant,cont, fps, distanciaPercorridaPassada):
    # Recalculando centro
    cx, cy = funcs_draw.calc_centro_roi(x,w,y,h)

    # Cálculos
    deltaT = 1/fps
    distancia_percorrida_x = (cx-cxant)*fatConvPxM; distancia_percorrida_y = (cy-cyant)*fatConvPxM
    distancia_percorrida = math.sqrt(((distancia_percorrida_x*distancia_percorrida_x) + (distancia_percorrida_y*distancia_percorrida_y)))
    velocidade = distancia_percorrida/deltaT
    distanciaPercorridaPassada +=distancia_percorrida
    dados = [velocidade, distancia_percorrida_x, distancia_percorrida_y, distancia_percorrida, deltaT*cont, cxant, cx, distanciaPercorridaPassada]
    caminhos = ["./logs/velocidade_percorrida_em_cada_frame.txt", "./logs/distancia_percorrida_x_em_cada_frame.txt", "./logs/distancia_percorrida_y_em_cada_frame.txt", "./logs/distancia_percorrida_em_cada_frame.txt","./logs/tempo_decorrido.txt", "./logs/poscoes_x_centro_antigas.txt", "./logs/poscoes_x_centro_atuais.txt", "./logs/distancias_cumulativas.txt"]
    # Salvando Gráficos
    for i in range(len(dados)):
        funcs_manip_arq.salva_dado(dados[i], cont, caminhos[i])
        
    return distanciaPercorridaPassada

def salvaGraficosVelocidade(sourceDados1, sourceDados2, titulos, labelsX, labelsY):
    for i in range(len(sourceDados1)):
        plot_graficos.plot_grafico( sourceDados1[i], sourceDados2[i], titulos[i], labelsX[i], labelsY[i])        
        
     
