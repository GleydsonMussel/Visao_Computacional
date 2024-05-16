
import math
import Methods.Drawer as Drawer
import Methods.Manipulate_Files as Manip
import Methods.Graphics as Plot

# Calcula o ponto do centro da região de interesse
def get_center_roi(x, w, y, h):
    return [int(x+w/2), int(y+h/2)]

def calc_speed(x, y, w, h, cxant, cyant, iteracao, fps, distancia_acumulada_X, altura_acumulada, fatConvPxM):
    # Pega o centro atualizado da região de interesse
    cx, cy = get_center_roi(x,w,y,h)

    # Cálculos
    deltaT = 1/fps 
    deltaX = (cx-cxant)*fatConvPxM 
    deltaY = (cy-cyant)*fatConvPxM
    distancia_acumulada_X +=deltaX 
    altura_acumulada+=deltaY 
    velocidade = deltaX/deltaT
    # Armazenamento
    dados = [velocidade, 
             deltaX, 
             deltaY, 
             deltaX, 
             deltaT*iteracao, 
             cxant, 
             cx, 
             cyant,
             cy,
             distancia_acumulada_X, 
             altura_acumulada, 
             ]
    with open("./Methods/Textual_Inputs/paths_to_tracker_processing.txt", 'r') as arquivo:
        caminhos = arquivo.readlines()
        caminhos = [caminho.split(" ")[0].replace("\n", "") for caminho in caminhos]
        arquivo.close()
    
    [Manip.save_data(dado, caminho) for dado, caminho in zip(dados, caminhos)]
    
    # Retorno
    return [distancia_acumulada_X, altura_acumulada]

def calc_speed_diagonal(x, y, w, h, cxant, cyant, iteracao, fps, distancia_acumulada_X, altura_acumulada, fatConvPxM):
    # Pega o centro atualizado da região de interesse
    cx, cy = get_center_roi(x,w,y,h)

    # Cálculos
    deltaT = 1/fps 
    deltaX = (cx-cxant)*fatConvPxM 
    deltaY = (cy-cyant)*fatConvPxM
    distancia_acumulada_X +=deltaX 
    altura_acumulada+=deltaY 
    distancia_percorrida = math.sqrt(((deltaX*deltaX) + (deltaY*deltaY)))
    velocidade = deltaX/deltaT
    # Armazenamento
    dados = [velocidade, 
             deltaX, 
             deltaY, 
             distancia_percorrida, 
             deltaT*iteracao, 
             cxant, 
             cx, 
             cyant,
             cy,
             distancia_acumulada_X, 
             altura_acumulada, 
             ]
    with open("./Methods/Textual_Inputs/paths_to_tracker_processing.txt", 'r') as arquivo:
        caminhos = arquivo.readlines()
        caminhos = [caminho.split(" ")[0].replace("\n", "") for caminho in caminhos]
        arquivo.close()
    
    [Manip.save_data(dado, caminho) for dado, caminho in zip(dados, caminhos)]
    
    # Retorno
    return [distancia_acumulada_X, altura_acumulada]
     
        
     


