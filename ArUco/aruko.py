import cv2
import numpy as np

# Exibe o marcador Gerado
def display_aruco_marker(marker_image):    
    if marker_image is not None:
        cv2.imshow('ArUco Marker', marker_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    else:
        print("Nenhuma imagem de marcador para exibir.")

# Gera uma imagem de um marcador ArUco.    
def generate_aruco_marker(id, dictionary, marker_size):
    """
    Args:
        id (int): ID do marcador a ser gerado.
        dictionary (int): Tipo de dicionário ArUco a ser usado.
        marker_size (int): Tamanho do marcador em pixels.
    """
    # Seleciona o dicionário ArUco
    aruco_dict = cv2.aruco.getPredefinedDictionary(dictionary)
    
    # Gera o marcador ArUco
    return cv2.aruco.generateImageMarker(aruco_dict, id, marker_size)

# Dicionário de dicionários ArUco
ARUCO_DICT = {
    "DICT_4X4_50": cv2.aruco.DICT_4X4_50,
    "DICT_4X4_100": cv2.aruco.DICT_4X4_100,
    "DICT_4X4_250": cv2.aruco.DICT_4X4_250,
    "DICT_4X4_1000": cv2.aruco.DICT_4X4_1000,
    "DICT_5X5_50": cv2.aruco.DICT_5X5_50,
    "DICT_5X5_100": cv2.aruco.DICT_5X5_100,
    "DICT_5X5_250": cv2.aruco.DICT_5X5_250,
    "DICT_5X5_1000": cv2.aruco.DICT_5X5_1000,
    "DICT_6X6_50": cv2.aruco.DICT_6X6_50,
    "DICT_6X6_100": cv2.aruco.DICT_6X6_100,
    "DICT_6X6_250": cv2.aruco.DICT_6X6_250,
    "DICT_6X6_1000": cv2.aruco.DICT_6X6_1000,
    "DICT_7X7_50": cv2.aruco.DICT_7X7_50,
    "DICT_7X7_100": cv2.aruco.DICT_7X7_100,
    "DICT_7X7_250": cv2.aruco.DICT_7X7_250,
    "DICT_7X7_1000": cv2.aruco.DICT_7X7_1000,
}

# ID do marcador a ser gerado
marker_id = 24
# Tamanho do marcador em pixel
marker_size = 200
# Dicionário a ser utilizado
dict_to_use = "DICT_7X7_50"

# Gera o marcador ArUco
marker = generate_aruco_marker(marker_id, ARUCO_DICT[dict_to_use], marker_size)

# Salva o marcador como uma imagem
if marker is not None:
    cv2.imwrite(f'./ArUco/ArUco_Markers/marker_{dict_to_use}_id_{marker_id}.png', marker)

# Exibe o marcador ArUco
display_aruco_marker(marker)

print("Ginga Eyuu Densetsu")

"""
Dicionários Aruko seguem o padrão: cv2.aruco.DICT_NxN_M,

The NxN value is the 2D bit size of the ArUco marker. For example, for a 6×6 marker we have a total of 36 bits.

The integer M following the grid size specifies the total number of unique ArUco IDs that can be generated with that dictionary.

"""
