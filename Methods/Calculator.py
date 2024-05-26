import cv2
import math
import copy as cp
import sys
sys.path.append('./Methods/Manipulate_Files.py')
from Manipulate_Files import save_data, save_as_pickle_data

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
    
    [save_data(dado, caminho) for dado, caminho in zip(dados, caminhos)]
    
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
    
    [save_data(dado, caminho) for dado, caminho in zip(dados, caminhos)]
    
    # Retorno
    return [distancia_acumulada_X, altura_acumulada]

# Calcula a posição do centro do marcador ArUco
def calc_marker_positions_x_y(corners):
    """
    Calcula as posições centrais dos marcadores ArUco detectados.

    Args:
        corners (list): Lista de esquinas dos marcadores detectados.

    Returns:
        list: Lista de tuplas com as posições centrais (x, y) dos marcadores.
    """
    positions = []
    for corner in corners:
        corner = corner.reshape((4, 2))
        top_left, top_right, bottom_right, bottom_left = corner
        center_x = (top_left[0] + top_right[0] + bottom_right[0] + bottom_left[0]) / 4.0
        center_y = (top_left[1] + top_right[1] + bottom_right[1] + bottom_left[1]) / 4.0
        positions.append((center_x, center_y))
    return positions

# Calcula os vetores de rotação e translação relacionados ao ArUco com relação a câmera
def calc_marker_position(corners, marker_length, camera_data):
    """
    Estima a pose dos marcadores ArUco.

    Args:
        corners (list): Lista de esquinas dos marcadores detectados.
        marker_length (float): Tamanho do lado do marcador (em metros).
        camera_matrix (numpy.ndarray): Matriz de calibração da câmera.
        dist_coeffs (numpy.ndarray): Coeficientes de distorção da câmera.

    Returns:
        tuple: Vetores de rotação e translação dos marcadores detectados.
    """
    rvecs, tvecs, _ = cv2.aruco.estimatePoseSingleMarkers(corners, marker_length, camera_data.mtx, camera_data.distortion)
    return rvecs, tvecs

def calc_speed_in_Z_axis(destiny_folder, file_name, marker_z_positions, times_to_each_marker, ids_wanted_markers):
    
    speeds = {}
    ids_markers = list(marker_z_positions.keys())
    
    for id_marker in ids_markers:
        speed = []
        is_wanted = False
        for desired_marker in ids_wanted_markers:
            if id_marker == desired_marker:
                is_wanted = True
                break
        if is_wanted:        
            for i in range(1, len(marker_z_positions[id_marker])):
                speed.append(abs( (marker_z_positions[id_marker][i] - marker_z_positions[id_marker][i-1])/(times_to_each_marker[id_marker][i] - times_to_each_marker[id_marker][i-1])))
            speeds[id_marker] = cp.deepcopy(speed)
        
    save_as_pickle_data(speeds, destiny_folder, file_name)
     


