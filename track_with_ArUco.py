import cv2
import numpy as np
from Classes.CameraData import CameraData
import Methods.Drawer as Drawer
import Methods.Manipulate_Files as Manip
import Methods.Calculator as Calculator
import Methods.Graphics as Plot
import Methods.Calibration as Calibration

# Garante que as pastas necessárias existem
Manip.create_folders()
# Limpa tudo que for necessário para realizar o processamento
Manip.clean_tracker_processing()

#-----------------------------PREENCHER-----------------------------------

# SETAR NOME VÍDEO
nome_video = 'Teste_ArUco_Casa_1m_55cm'; extencao = '.mp4'

# Setar o aruko utilizado
marker_used = "./ArUco/ArUco_Markers/marker_DICT_7X7_50_id_12.png"

# Dicionário ArUco utilizado
arucoDict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_7X7_50)

# Tamanho do marcador em metros 
marker_size = 0.105 # (Id 12 impresso)
#marker_size = 0.08

# Caminho para importar os dados da câmera utilizada
dados_camera = CameraData('./Cameras_Data/celular_Gleydson2/coeficientes_2.npz')

# Se desejar aplicar a calibração de câmera, True, se não, False
aplicaCalib = True

#--------------------------------------------------------------------------

# Cria os parâmetros para o ArUco
arucoParams = cv2.aruco.DetectorParameters()

video = cv2.VideoCapture('./videos/Testes_ArUco/'+nome_video+extencao)
alturaVideo = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT)); 
larguraVideo = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
videoSaida = cv2.VideoWriter('./videos/Outputs/'+nome_video+'_output'+extencao, cv2.VideoWriter_fourcc('m', 'p', '4', 'v'), video.get(cv2.CAP_PROP_FPS), (larguraVideo, alturaVideo))
 
contFrame = 0    
tempos = []   
marker_z_positions = []                       

#-----------------Começo Processamento------------------
while True:
    # Tenta coletar o frame a ser processado
    frame = video.read()[1]
    
    if frame is None:
        break
    
    Manip.save_data(frame, './frames/frameCRU_'+str(contFrame)+'.png')
    
    # Caso se deseje aplicar a calibração
    if aplicaCalib:
        frame = Calibration.aply_calib(frame, dados_camera)
        Manip.save_data(frame, './frames/frameCALIB_'+str(contFrame)+'.png')
    
    # Converte para cinza para melhor detecção
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # corners: A list containing the (x, y)-coordinates of our detected ArUco markers
    # ids: The ArUco IDs of the detected markers
    # rejected: A list of potential markers that were found but ultimately rejected due to the inner code of the marker being unable to be parsed
    (corners, ids, rejected) = cv2.aruco.detectMarkers(frame, arucoDict, parameters=arucoParams)
    
    # Converte para as cores originais para exibição
    frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2RGB)
    
    # Se há uma região de interesse para o rastreador rastrear
    if corners is not None:
        
        cv2.aruco.drawDetectedMarkers(frame, corners, ids)
        
        # Obtem os vetores de rotação e translação da câmera
        rvecs, tvecs = Calculator.calc_marker_position(corners, marker_size, dados_camera)
        
        if rvecs is not None:
            for rvec, tvec, id in zip(rvecs, tvecs, ids):
                cv2.drawFrameAxes(frame, dados_camera.mtx, dados_camera.distortion, rvec, tvec, 0.1)
                print(f"ID: {id[0]}")
                print(f"Translation Vector (tvec): {tvec.flatten()}")
                print(f"Position in Z: {tvec[0][2]} meters")
                tempos.append(1/round(video.get(cv2.CAP_PROP_FPS)) * contFrame)
                marker_z_positions.append(tvec[0][2])
        
        # Calcula a posição do centro do marcador ArUco
        posicao = Calculator.calc_marker_positions(corners)
        
        print(posicao)
    
    Drawer.write_on_video(frame, "Fps: "+str(round(video.get(cv2.CAP_PROP_FPS))),(0,25), (255,0,0))
    Drawer.write_on_video(frame, "Frame: "+str(contFrame),(0,60), (0,255,0))
     
    cv2.imshow('Rastreando',frame)   
    
    k = cv2.waitKey(30)
    
    # Habilita dar pause no vídeo
    if k == ord('p'):
        while True:
            j = cv2.waitKey(30)
            if j == ord('v'):
                break
            
    elif k == ord('q'):
        break
    
    videoSaida.write(frame)
    
    contFrame+=1
    
    print("Li o frame: "+str(contFrame))

#-----------------Fim do processamento------------------
video.release(); cv2.destroyAllWindows() 

marker_z_positions_np_array = np.array(marker_z_positions)

np.save("./logs/Marker_z_Positions"+nome_video+".np", marker_z_positions_np_array)
Plot.plot_graphic_with_direct_values(tempos, marker_z_positions, "Posicao em Z do Marcador x Tempo", "Tempo (s)", "Posicao (m)")


   


