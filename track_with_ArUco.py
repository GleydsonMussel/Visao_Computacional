import cv2
import sys
sys.path.append('./Methods')
from Classes.CameraData import CameraData
import Methods.Drawer as Drawer
import Methods.Manipulate_Files as Manip
import Methods.Calculator as Calculator
import Methods.Graphics as Plot
import Methods.Calibration as Calibration
import Methods.ArUco_Things as ArUco_Things
import Methods.Data_Cleaner as Data_Cleaner

# Garante que as pastas necessárias existem
Manip.create_folders()
# Limpa tudo que for necessário para realizar o processamento
Manip.clean_tracker_processing()

#-----------------------------PREENCHER-----------------------------------

# SETAR NOME VÍDEO
nome_video = 'Teste_Arthur_2x'; extencao = '.mp4'

# Setar o aruko utilizado
marker_used = "./ArUco/ArUco_Markers/marker_DICT_7X7_50_id_12.png"

# Dicionário ArUco utilizado
arucoDict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_7X7_50)

# Fator de COnversão de pixel para m
fatConvPxToM = 0.06

# Tamanho do marcador em metros 
#marker_size = 0.105 # (Id 12 impresso)
#marker_size = 0.08

tempos = {
    49:[],
    0:[],
    24:[],
}
marker_z_positions={
    49:[],
    0:[],
    24:[],
}
marker_x_positions={
    49:[],
    0:[],
    24:[],
}
marker_y_positions={
    49:[],
    0:[],
    24:[],
}
posicoes_referencia={
    49:9.47,
    24:3.47
}

# Caminho para importar os dados da câmera utilizada
dados_camera = CameraData('./Cameras_Data/celular_Gleydson2/coeficientes_Zoom_2x.npz')

# Se desejar aplicar a calibração de câmera, True, se não, False
aplicaCalib = True

#--------------------------------------------------------------------------

# Cria pasta para exportar os dados necessários para a realização dessa análise
caminho_pasta_output = "./dados_extraidos/"+nome_video
caminho_pasta_output = Manip.create_folder(caminho_pasta_output)

# Cria os parâmetros para o ArUco
arucoParams = ArUco_Things.generate_detector_params(caminho_pasta_output)

video = cv2.VideoCapture('./videos/Testes_ArUco/'+nome_video+extencao)
alturaVideo = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT)); 
larguraVideo = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
fps = video.get(cv2.CAP_PROP_FPS)
videoSaida = cv2.VideoWriter(caminho_pasta_output+nome_video+'_Output'+extencao, cv2.VideoWriter_fourcc('m', 'p', '4', 'v'), fps, (larguraVideo, alturaVideo))
 
contFrame = 0                          

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
        
        for corner, id in zip(corners, ids):    
            if id[0] == 24:
                marker_size = 0.105/2
            else:
                 marker_size = 0.105
            # Obtem os vetores de rotação e translação da câmera
            rvecs, tvecs = Calculator.calc_marker_position(corner, marker_size, dados_camera)
            # Calcula a posição do centro do marcador ArUco
            cx, cy = Calculator.calc_marker_positions_x_y(corner)
            marker_x_positions[id[0]].append(cx)
            marker_y_positions[id[0]].append(cy)
            #rvecs, tvecs = [None, None]
            
            if rvecs is not None:
                for rvec, tvec in zip(rvecs, tvecs):
                    cv2.drawFrameAxes(frame, dados_camera.mtx, dados_camera.distortion, rvec, tvec, 0.1)
                    print(f"ID: {id[0]}")
                    print(f"Translation Vector (tvec): {tvec.flatten()}")
                    print(f"Position in Z: {tvec[0][2]} meters")
                    tempos[id[0]].append(1/round(video.get(cv2.CAP_PROP_FPS)) * contFrame)
                    marker_z_positions[id[0]].append(tvec[0][2])

            print((marker_x_positions[id[0]][-1], marker_y_positions[id[0]][-1]))
    
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
    # Habilita função de fechar o vídeo quando desejar      
    elif k == ord('q'):
        break
    
    videoSaida.write(frame)
    
    contFrame+=1
    
    print("Li o frame: "+str(contFrame))

#-----------------Fim do Processamento do Vídeo------------------
video.release(); cv2.destroyAllWindows()
duracao_video = contFrame/fps

# Calculando o deslocamento já convertendo de px para m
marker_x_positions = Calculator.calc_deslocamento_converted(marker_x_positions, fatConvPxToM)
marker_y_positions = Calculator.calc_deslocamento_converted(marker_y_positions, fatConvPxToM)

# Cálculo das Velocidades
Calculator.calc_speed_in_any_axis(caminho_pasta_output, "speed_markers_z.pkl", marker_z_positions, tempos, [49, 0, 24])
Calculator.calc_speed_in_any_axis(caminho_pasta_output, "speed_markers_x.pkl", marker_x_positions, tempos, [49, 0, 24])
Calculator.calc_speed_in_any_axis(caminho_pasta_output, "speed_markers_y.pkl", marker_y_positions, tempos, [49, 0, 24])

# Salvando dados extraídos
Manip.save_as_pickle_data(tempos, caminho_pasta_output, "times_to_each_marker.pkl")
Manip.save_as_pickle_data(marker_z_positions, caminho_pasta_output, "markers_z_positions.pkl")
Manip.save_as_pickle_data(posicoes_referencia, caminho_pasta_output, "reference_positions.pkl")
Manip.save_as_pickle_data(marker_x_positions, caminho_pasta_output, "marker_x_positions.pkl")
Manip.save_as_pickle_data(marker_y_positions, caminho_pasta_output, "marker_y_positions.pkl")
 
# Primeira higiennização dos dados de Deslocamento e Velocidade
Data_Cleaner.clean_data(caminho_pasta_output, "cleaned_markers_z_positions", caminho_pasta_output+"markers_z_positions.pkl", [49, 0, 24])
Data_Cleaner.clean_data(caminho_pasta_output, "cleaned_speed_markers_z", caminho_pasta_output+"speed_markers_z.pkl", [49, 0, 24])
Data_Cleaner.clean_data(caminho_pasta_output, "cleaned_marker_x_positions", caminho_pasta_output+"marker_x_positions.pkl", [49, 0, 24])
Data_Cleaner.clean_data(caminho_pasta_output, "cleaned_speed_markers_x", caminho_pasta_output+"speed_markers_x.pkl", [49, 0, 24])
Data_Cleaner.clean_data(caminho_pasta_output, "cleaned_marker_y_positions", caminho_pasta_output+"marker_y_positions.pkl", [49, 0, 24])
Data_Cleaner.clean_data(caminho_pasta_output, "cleaned_speed_markers_y", caminho_pasta_output+"speed_markers_y.pkl", [49, 0, 24])

# Segunda higiennização dos dados de Deslocamento e Velocidade
marker_z_positions_cleaned = Manip.load_pickle_data(caminho_pasta_output+"cleaned_markers_z_positions.pkl")
Calculator.calc_speed_in_any_axis(caminho_pasta_output, "speed_markers_with_clean_z_positions.pkl", marker_z_positions_cleaned, tempos, [49, 0, 24])
Data_Cleaner.clean_data(caminho_pasta_output, "cleaned_speed_markers_with_clean_z_positions", caminho_pasta_output+"speed_markers_with_clean_z_positions.pkl", [49, 0, 24])

marker_x_positions_cleaned = Manip.load_pickle_data(caminho_pasta_output+"cleaned_marker_x_positions.pkl")
Calculator.calc_speed_in_any_axis(caminho_pasta_output, "speed_markers_with_clean_x_positions.pkl", marker_x_positions_cleaned, tempos, [49, 0, 24])
Data_Cleaner.clean_data(caminho_pasta_output, "cleaned_speed_markers_with_clean_x_positions", caminho_pasta_output+"speed_markers_with_clean_x_positions.pkl", [49, 0, 24])

marker_y_positions_cleaned = Manip.load_pickle_data(caminho_pasta_output+"cleaned_marker_y_positions.pkl")
Calculator.calc_speed_in_any_axis(caminho_pasta_output, "speed_markers_with_clean_y_positions.pkl", marker_y_positions_cleaned, tempos, [49, 0, 24])
Data_Cleaner.clean_data(caminho_pasta_output, "cleaned_speed_markers_with_clean_y_positions", caminho_pasta_output+"speed_markers_with_clean_y_positions.pkl", [49, 0, 24])

# Plotando gráficos
Plot.plot_graphic_from_pickles_dicts(caminho_pasta_output+"Posicao_Z_x_Tempo", caminho_pasta_output+"times_to_each_marker.pkl", caminho_pasta_output+"markers_z_positions.pkl", "Posicao em Z do Marcador x Tempo", "Tempo (s)", "Posicao (m)", video_duration=duracao_video, ids_wanted_markers=[49,0,24])
Plot.plot_graphic_from_pickles_dicts(caminho_pasta_output+"Velocidade_em_Z_x_Tempo", caminho_pasta_output+"times_to_each_marker.pkl", caminho_pasta_output+"speed_markers_z.pkl", "Velocidade em Z do Marcador x Tempo", "Tempo (s)", "Velocidade (m/s)", video_duration=duracao_video, ids_wanted_markers=[0])
Plot.plot_graphic_from_pickles_dicts(caminho_pasta_output+"Velocidade_em_Z_Tratatatatatada_x_Tempo", caminho_pasta_output+"times_to_each_marker.pkl", caminho_pasta_output+"cleaned_speed_markers_with_clean_z_positions.pkl", "Velocidade em Z Tratatatatatada x Tempo", "Tempo (s)", "Velocidade (m/s)", video_duration=duracao_video, ids_wanted_markers=[0])

Plot.plot_graphic_from_pickles_dicts(caminho_pasta_output+"Posicao_Z_Tratada_x_Tempo", caminho_pasta_output+"times_to_each_marker.pkl", caminho_pasta_output+"cleaned_markers_z_positions.pkl", "Posicao em Z do Marcador x Tempo", "Tempo (s)", "Posicao (m)", video_duration=duracao_video, ids_wanted_markers=[49,0,24])
Plot.plot_graphic_from_pickles_dicts(caminho_pasta_output+"Velocidade_em_Z_Tratada_x_Tempo", caminho_pasta_output+"times_to_each_marker.pkl", caminho_pasta_output+"cleaned_speed_markers_z.pkl", "Velocidade em Z do Marcador x Tempo", "Tempo (s)", "Velocidade (m/s)", video_duration=duracao_video, ids_wanted_markers=[0])

Plot.plot_graphic_from_pickles_dicts(caminho_pasta_output+"Deslocamento_em_X_x_Tempo", caminho_pasta_output+"times_to_each_marker.pkl", caminho_pasta_output+"marker_x_positions.pkl", "Deslocamento em X x Tempo", "Tempo (s)", "Posicao (m)", video_duration=duracao_video, ids_wanted_markers=[49,0,24])
Plot.plot_graphic_from_pickles_dicts(caminho_pasta_output+"Deslocamento_em_Y_x_Tempo", caminho_pasta_output+"times_to_each_marker.pkl", caminho_pasta_output+"marker_y_positions.pkl", "Deslocamento em Y x Tempo", "Tempo (s)", "Posicao (m)", video_duration=duracao_video, ids_wanted_markers=[49,0,24])

Plot.plot_graphic_from_pickles_dicts(caminho_pasta_output+"Deslocamento_em_X_Tratado_x_Tempo", caminho_pasta_output+"times_to_each_marker.pkl", caminho_pasta_output+"cleaned_marker_x_positions.pkl", "Deslocamento em X x Tempo", "Tempo (s)", "Posicao (m)", video_duration=duracao_video, ids_wanted_markers=[49,0,24])
Plot.plot_graphic_from_pickles_dicts(caminho_pasta_output+"Deslocamento_em_Y_x_Tempo", caminho_pasta_output+"times_to_each_marker.pkl", caminho_pasta_output+"cleaned_marker_y_positions.pkl", "Deslocamento em Y x Tempo", "Tempo (s)", "Posicao (m)", video_duration=duracao_video, ids_wanted_markers=[49,0,24])

Plot.plot_graphic_from_pickles_dicts(caminho_pasta_output+"Velocidade_em_X_x_Tempo", caminho_pasta_output+"times_to_each_marker.pkl", caminho_pasta_output+"speed_markers_x.pkl", "Velocidade em X x Tempo", "Tempo (s)", "Velocidade (m/s)", video_duration=duracao_video, ids_wanted_markers=[49,0,24])
Plot.plot_graphic_from_pickles_dicts(caminho_pasta_output+"Velocidade_em_X_Tratada_x_Tempo", caminho_pasta_output+"times_to_each_marker.pkl", caminho_pasta_output+"cleaned_speed_markers_x.pkl", "Velocidade em X Tratada x Tempo", "Tempo (s)", "Velocidade (m/s)", video_duration=duracao_video, ids_wanted_markers=[49,0,24])
Plot.plot_graphic_from_pickles_dicts(caminho_pasta_output+"Velocidade_em_X_Tratatatatatada_x_Tempo", caminho_pasta_output+"times_to_each_marker.pkl", caminho_pasta_output+"cleaned_speed_markers_with_clean_x_positions.pkl", "Velocidade em X Tratatatatatada x Tempo", "Tempo (s)", "Velocidade (m/s)", video_duration=duracao_video, ids_wanted_markers=[49,0,24])

