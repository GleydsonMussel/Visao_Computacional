import cv2

id_tabuleiro = 6
dicionario_desejado = "DICT_6X6_1000"

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

# Parâmetros do tabuleiro de Charuco
squares_x = 12  # Número de quadrados na direção x
squares_y = 9  # Número de quadrados na direção y
square_length = 0.04  # Comprimento dos quadrados em metros
marker_length = 0.02  # Comprimento das marcas Aruco em metros
MARGIN_PX = 20    # Tamanho da Margem do Marcador em pixel

# Carregar o dicionário Aruco
aruco_dict = cv2.aruco.getPredefinedDictionary(ARUCO_DICT[dicionario_desejado])

# Criar o tabuleiro de Charuco usando a classe CharucoBoard diretamente
charuco_board = cv2.aruco.CharucoBoard((squares_x, squares_y), square_length, marker_length, aruco_dict)

# Tamanho da imagem do tabuleiro em pixels (Tamanho padrão para uma folha A4)
img_width = 3508; img_height = 2480

# Gerando de fato a imagem do tabuleiro para a calibração
img = cv2.aruco.CharucoBoard.generateImage(charuco_board, (img_width, img_height), marginSize=MARGIN_PX)

# Salvar a imagem do tabuleiro
cv2.imwrite('./ArUco/ChArUcos/Tabuleiro_id_'+str(id_tabuleiro)+"_"+dicionario_desejado+'_sqx_'+str(squares_x)+'_sqy_'+str(squares_y)+'_sqrl_'+str(square_length).replace(".","")+'_mkrl_'+str(marker_length).replace(".","")+'.png', img)

# Mostrar a imagem do tabuleiro
cv2.imshow('Tabuleiro', img)
cv2.destroyAllWindows()

print("Boogie Wonderland !")
