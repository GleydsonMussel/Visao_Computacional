import cv2
import numpy as np
import os
import sys

sys.path.append('./Methods')
import ArUco_Things

# -------------------AJUSTAR----------------------------------

squares_x = 11  # Número de quadrados na direção x
squares_y = 9  # Número de quadrados na direção y
square_length = 0.022  # Comprimento dos quadrados em metros
marker_length = 0.011  # Comprimento das marcas Aruco em metros
MARGIN_PX = 20    # Tamanho da Margem do Marcador em pixel

dicionario_desejado = "DICT_6X6_1000"
pathCoeficients = "./Cameras_Data/celular_Gleydson2/testeCharuco.npz"

# -----------------------------------------------------------

PATH_TO_SAMPLES = './Calibration/Samples/'
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

# Define the aruco dictionary and charuco board
dictionary = cv2.aruco.getPredefinedDictionary(ARUCO_DICT[dicionario_desejado])
board = cv2.aruco.CharucoBoard((squares_x, squares_y), square_length, marker_length, dictionary)
params = ArUco_Things.generate_detector_params()

# Load PNG images from folder
image_files = [os.path.join(PATH_TO_SAMPLES, f) for f in os.listdir(PATH_TO_SAMPLES) if f.endswith(".png")]
image_files.sort()  # Ensure files are in order

all_charuco_corners = []
all_charuco_ids = []
all_images = []

for image_file in image_files:
    image = cv2.imread(image_file)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    image_copy = image.copy()
    marker_corners, marker_ids, _ = cv2.aruco.detectMarkers(gray, dictionary, parameters=params)
    
    if marker_ids is not None and len(marker_ids) > 0:
        nome_arquivo = image_file.split("/")[-1]
        print(f"Número de IDs detectados em {nome_arquivo}: {len(marker_ids)}")
        # If at least one marker is detected
        imagem = cv2.aruco.drawDetectedMarkers(image_copy, marker_corners, marker_ids)
        cv2.imshow("Calibrando", imagem)
        k = cv2.waitKey(1) 
        if k == ord('q'):
            break
        
        charuco_retval, charuco_corners, charuco_ids = cv2.aruco.interpolateCornersCharuco(marker_corners, marker_ids, gray, board)
        
        if charuco_retval and charuco_corners is not None and charuco_ids is not None and len(charuco_corners) >= 4 and len(charuco_ids) >= 4:
            all_charuco_corners.append(charuco_corners)
            all_charuco_ids.append(charuco_ids)
            all_images.append(gray) 
        else:
            nome_arquivo = image_file.split("/")[-1]
            print(f"Falha ao interpolar cantos suficientes em {nome_arquivo}")
    else:
        nome_arquivo = image_file.split("/")[-1]
        print(f"Nenhum Aruco detectado em: {nome_arquivo}")

cv2.destroyAllWindows()

# Verifique se há dados suficientes para calibração
if len(all_charuco_corners) > 0 and len(all_charuco_ids) > 0:
    # Calibrate camera
    image_size = gray.shape[::-1]  # (width, height)
    retval, camera_matrix, dist_coeffs, rvecs, tvecs = cv2.aruco.calibrateCameraCharuco(
        all_charuco_corners, all_charuco_ids, board, image_size, None, None
    )

    if retval:
        # Pega as dimensões da imagem utilizada
        h, w = gray.shape[:2]

        # Refina a matrix dos coeficientes de distorção
        newcameramtx, roi = cv2.getOptimalNewCameraMatrix(camera_matrix, dist_coeffs, (w, h), 1, (w, h))

        # Save calibration data
        np.savez(pathCoeficients, distortion=dist_coeffs, camera=camera_matrix, new_camera=newcameramtx)

        # Estimativa do erro de reprojeção
        total_error = 0
        total_points = 0
        
        print("\nQuantidade de Imagens Utilizadas na Calibração: "+str(len(all_images))+"\n")
                
        # Iterate through displaying all the images
        for image_file in image_files:
            print(f'Processando Imagem {image_file.split("/")[-1]}')
            image = cv2.imread(image_file)
            undistorted_image = cv2.undistort(image, camera_matrix, dist_coeffs, None, newcameramtx)
            cv2.imshow('Imagem sem Distorcao', undistorted_image)
            
            k = cv2.waitKey(0)
            

        cv2.destroyAllWindows()
    else:
        print("Calibração falhou.")
else:
    print("Dados insuficientes para calibração.")
