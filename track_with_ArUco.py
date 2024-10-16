import cv2
import sys
sys.path.append('./Classes')
from CameraData import CameraData
from Drawer import Drawer
from Manipulate_Files import Manipulate_Files as Manip
from Calculator import Calculator
from Graphics import Graphics as Plot
from Calibration import Calibration
from ArUco_Things import ArUco_Things
from Data_Cleaner import Data_Cleaner

# Garante que as pastas necessárias existem
Manip.create_folders()
# Limpa tudo que for necessário para realizar o processamento
Manip.clean_tracker_processing()

#-----------------------------PREENCHER-----------------------------------

# SETAR NOME VÍDEO
nome_video = 'Voo10Editado'; extencao = '.mp4'

# Dicionário ArUco utilizado (apenas para referencia do dicionário utilizado)
arucoDict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_7X7_50)

# Fator de COnversão de pixel para m
fatConvPxToM = 3/660 # Xadrez voo 9
fatConvPxToM = 3/596 # ChArUco voo 9
fatConvPxToM = 4.2/826 # ChArUco voo 10
#fatConvPxToM = 4.2/873 # ChArUco Decolagem_FInal_Countdown

# Tamanho do marcador em metros 
marker_size = 0.119 # (Id 37 impresso)

# Lista que armazena os ids dos marcadores dos quais se deseja extrair informações
ids_desejados = [37]

posicoes_referencia={}

# Caminho para importar os dados da câmera utilizada
dados_camera = CameraData('./Cameras_Data/celular_Gleydson2/testeCharuco.npz')

# Se desejar aplicar a calibração de câmera, True, se não, False
aplicaCalib = True

# Define se os coeficientes foram obtidos pela calibração usando tabuleiro de xadrez ou ChArUco 
ChArUco = True

# Determina se o processamento será feito considerando o deslocamento do objeto na diagonal ou na horizontal
NORMAL = True

#--------------------------------------------------------------------------

# Cria dicionários
tempos = {}
marker_x_positions={}
marker_y_positions={}
marker_z_positions={}

# Cria pasta para exportar os dados necessários para a realização dessa análise
caminho_pasta_output = "./dados_extraidos/"+nome_video+"_ArUco"
caminho_pasta_output = Manip.create_folder(caminho_pasta_output)

# Cria os parâmetros para o ArUco
arucoParams = ArUco_Things.generate_detector_params(caminho_pasta_output)

# Coletando altura e largura do vídeo para garantir que o vídeo de saída tenha a resolução certa
ok, frame = cv2.VideoCapture('./videos/Voos/'+nome_video+extencao).read()
if aplicaCalib:
    frame = Calibration.aply_calib(frame, dados_camera, ChArUco)
cv2.VideoCapture('./videos/Voos/'+nome_video+extencao).release()
alturaVideo, larguraVideo = frame.shape[:2]
cv2.imwrite("./frames/Frame_Ref.png", frame)

video = cv2.VideoCapture('./videos/Voos/'+nome_video+extencao)

fps = video.get(cv2.CAP_PROP_FPS)
videoSaida = cv2.VideoWriter(
    caminho_pasta_output+nome_video+'_Output'+extencao, 
    cv2.VideoWriter_fourcc('m', 'p', '4', 'v'), 
    fps, 
    (larguraVideo, alturaVideo)
)
 
contFrame = 0    
inicializei_dicionarios = False                      

#-----------------Começo Processamento------------------
while True:
    # Tenta coletar o frame a ser processado
    frame = video.read()[1]
    
    if frame is None:
        break
    
    Manip.save_data(frame, './frames/frameCRU_'+str(contFrame)+'.png')
    
    # Caso se deseje aplicar a calibração
    if aplicaCalib:
        frame = Calibration.aply_calib(frame, dados_camera, ChArUco)
        cv2.imwrite('./frames/frameCALIB_'+str(contFrame)+'.png', frame)
    
    # Converte para cinza para melhor detecção
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # corners: A list containing the (x, y)-coordinates of our detected ArUco markers
    # ids: The ArUco IDs of the detected markers
    # rejected: A list of potential markers that were found but ultimately rejected due to the inner code of the marker being unable to be parsed
    (corners, ids, rejected) = cv2.aruco.detectMarkers(frame, arucoDict, parameters=arucoParams)
    
    # Converte para as cores originais para exibição
    frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2RGB)
    
    # Se há uma região de interesse para o rastreador rastrear
    if len(corners) != 0:
        
        cv2.aruco.drawDetectedMarkers(frame, corners, ids)
        
        # Inicializa os índices para cada marcador nos dicionários
        if not inicializei_dicionarios:
            for id in ids:
                marker_x_positions[id[0]] = []
                marker_y_positions[id[0]] = []   
                marker_z_positions[id[0]] = [] 
                tempos[id[0]] = []
            inicializei_dicionarios = True
            
        for corner, id in zip(corners, ids):    
        
            # Obtem os vetores de rotação e translação da câmera
            rvecs, tvecs = Calculator.calc_marker_position(corner, marker_size, dados_camera)
            # Calcula a posição do centro do marcador ArUco
            cx, cy = Calculator.calc_marker_positions_x_y(corner)
            marker_x_positions[id[0]].append(cx)
            marker_y_positions[id[0]].append(cy)
            
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
    Drawer.write_on_video(frame, "Tempo: "+str(round(contFrame/round(video.get(cv2.CAP_PROP_FPS)), 2)),(0,95), (0,0,255))
     
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
Calculator.calc_speed_ArUco(caminho_pasta_output, "speed_markers_z.pkl", marker_z_positions, tempos, ids_desejados)

if NORMAL:
    Calculator.calc_speed_ArUco(caminho_pasta_output, "speed_markers_x.pkl", marker_x_positions, tempos, ids_desejados)
    Calculator.calc_speed_ArUco(caminho_pasta_output, "speed_markers_y.pkl", marker_y_positions, tempos, ids_desejados)
else:
    Calculator.calc_speed_ArUco_Diagonal(caminho_pasta_output, "speed_markers_x.pkl", marker_x_positions, marker_y_positions, tempos, ids_desejados)

# Salvando dados extraídos
dados_salvar = [tempos, marker_x_positions, marker_y_positions, marker_z_positions, posicoes_referencia]
nomes_arquivos = ["times_to_each_marker.pkl", "marker_x_positions.pkl", "marker_y_positions.pkl", "markers_z_positions.pkl", "reference_positions.pkl"]
[Manip.save_as_pickle_data(dado, caminho_pasta_output,caminho) for dado, caminho in zip(dados_salvar, nomes_arquivos)]

# PRIMEIRA HIGIENIZAÇÃO dos dados de Deslocamento e Velocidade
nomes_arquivos_base = ["cleaned_marker_x_positions", "cleaned_speed_markers_x", "cleaned_marker_y_positions", "cleaned_markers_z_positions", "cleaned_speed_markers_z"]
nomes_arquivos = ["marker_x_positions.pkl", "speed_markers_x.pkl", "marker_y_positions.pkl", "markers_z_positions.pkl", "speed_markers_z.pkl"]
if NORMAL: nomes_arquivos_base.append("cleaned_speed_markers_y"); nomes_arquivos.append("speed_markers_y.pkl")
for nome_arquivo_base, nome_arquivo in zip(nomes_arquivos_base, nomes_arquivos):
    Data_Cleaner.clean_data(caminho_pasta_output, nome_arquivo_base, caminho_pasta_output+nome_arquivo, ids_desejados)

# SEGUNDA HIGIENIZAÇÃO dos dados de Deslocamento e Velocidade
marker_x_positions_cleaned = Manip.load_pickle_data(caminho_pasta_output+"cleaned_marker_x_positions.pkl")
marker_y_positions_cleaned = Manip.load_pickle_data(caminho_pasta_output+"cleaned_marker_y_positions.pkl")
marker_z_positions_cleaned = Manip.load_pickle_data(caminho_pasta_output+"cleaned_markers_z_positions.pkl")

Calculator.calc_speed_ArUco(caminho_pasta_output, "speed_markers_with_clean_z_positions.pkl", marker_z_positions_cleaned, tempos, ids_desejados)
Data_Cleaner.clean_data(caminho_pasta_output, "cleaned_speed_markers_with_clean_z_positions", caminho_pasta_output+"speed_markers_with_clean_z_positions.pkl", ids_desejados)

if NORMAL:
    Calculator.calc_speed_ArUco(caminho_pasta_output, "speed_markers_with_clean_x_positions.pkl", marker_x_positions_cleaned, tempos, ids_desejados)
    Data_Cleaner.clean_data(caminho_pasta_output, "cleaned_speed_markers_with_clean_x_positions", caminho_pasta_output+"speed_markers_with_clean_x_positions.pkl", ids_desejados)
    Calculator.calc_speed_ArUco(caminho_pasta_output, "speed_markers_with_clean_y_positions.pkl", marker_y_positions_cleaned, tempos, ids_desejados)
    Data_Cleaner.clean_data(caminho_pasta_output, "cleaned_speed_markers_with_clean_y_positions", caminho_pasta_output+"speed_markers_with_clean_y_positions.pkl", ids_desejados)
else:
    Calculator.calc_speed_ArUco_Diagonal(caminho_pasta_output, "speed_markers_with_clean_x_positions.pkl", marker_x_positions_cleaned, marker_y_positions_cleaned, tempos, ids_desejados)
    Data_Cleaner.clean_data(caminho_pasta_output, "cleaned_speed_markers_with_clean_x_positions", caminho_pasta_output+"speed_markers_with_clean_x_positions.pkl", ids_desejados)

# PLOTAGEM DOS GRÁFICOS

# X
Plot.plot_graphic_from_pickles_dicts(caminho_pasta_output+"Deslocamento_em_X_x_Tempo", caminho_pasta_output+"times_to_each_marker.pkl", caminho_pasta_output+"marker_x_positions.pkl", "Deslocamento em X x Tempo", "Tempo (s)", "Posicao (m)", video_duration=duracao_video, ids_wanted_markers=ids_desejados)
Plot.plot_graphic_from_pickles_dicts(caminho_pasta_output+"Deslocamento_em_X_Tratado_x_Tempo", caminho_pasta_output+"times_to_each_marker.pkl", caminho_pasta_output+"cleaned_marker_x_positions.pkl", "Deslocamento em X x Tempo", "Tempo (s)", "Posicao (m)", video_duration=duracao_video, ids_wanted_markers=ids_desejados)
Plot.plot_graphic_from_pickles_dicts(caminho_pasta_output+"Velocidade_em_X_x_Tempo", caminho_pasta_output+"times_to_each_marker.pkl", caminho_pasta_output+"speed_markers_x.pkl", "Velocidade em X x Tempo", "Tempo (s)", "Velocidade (m/s)", video_duration=duracao_video, ids_wanted_markers=ids_desejados)

Plot.plot_graphic_from_pickles_dicts(caminho_pasta_output+"Velocidade_em_X_Tratada_x_Tempo", caminho_pasta_output+"times_to_each_marker.pkl", caminho_pasta_output+"cleaned_speed_markers_x.pkl", "Velocidade em X Tratada x Tempo", "Tempo (s)", "Velocidade (m/s)", video_duration=duracao_video, ids_wanted_markers=ids_desejados)
Plot.plot_graphic_from_pickles_dicts(caminho_pasta_output+"Velocidade_em_X_Tratatatatatada_x_Tempo", caminho_pasta_output+"times_to_each_marker.pkl", caminho_pasta_output+"cleaned_speed_markers_with_clean_x_positions.pkl", "Velocidade em X Tratatatatatada x Tempo", "Tempo (s)", "Velocidade (m/s)", video_duration=duracao_video, ids_wanted_markers=ids_desejados)

# Y
Plot.plot_graphic_from_pickles_dicts(caminho_pasta_output+"Deslocamento_em_Y_x_Tempo", caminho_pasta_output+"times_to_each_marker.pkl", caminho_pasta_output+"marker_y_positions.pkl", "Deslocamento em Y x Tempo", "Tempo (s)", "Posicao (m)", video_duration=duracao_video, ids_wanted_markers=ids_desejados)
Plot.plot_graphic_from_pickles_dicts(caminho_pasta_output+"Deslocamento_em_Y_Tratado_x_Tempo", caminho_pasta_output+"times_to_each_marker.pkl", caminho_pasta_output+"cleaned_marker_y_positions.pkl", "Deslocamento em Y x Tempo", "Tempo (s)", "Posicao (m)", video_duration=duracao_video, ids_wanted_markers=ids_desejados)

# Z
Plot.plot_graphic_from_pickles_dicts(caminho_pasta_output+"Posicao_Z_x_Tempo", caminho_pasta_output+"times_to_each_marker.pkl", caminho_pasta_output+"markers_z_positions.pkl", "Posicao em Z do Marcador x Tempo", "Tempo (s)", "Posicao (m)", video_duration=duracao_video, ids_wanted_markers=ids_desejados)
Plot.plot_graphic_from_pickles_dicts(caminho_pasta_output+"Velocidade_em_Z_x_Tempo", caminho_pasta_output+"times_to_each_marker.pkl", caminho_pasta_output+"speed_markers_z.pkl", "Velocidade em Z do Marcador x Tempo", "Tempo (s)", "Velocidade (m/s)", video_duration=duracao_video, ids_wanted_markers=ids_desejados)
Plot.plot_graphic_from_pickles_dicts(caminho_pasta_output+"Velocidade_em_Z_Tratatatatatada_x_Tempo", caminho_pasta_output+"times_to_each_marker.pkl", caminho_pasta_output+"cleaned_speed_markers_with_clean_z_positions.pkl", "Velocidade em Z Tratatatatatada x Tempo", "Tempo (s)", "Velocidade (m/s)", video_duration=duracao_video, ids_wanted_markers=ids_desejados)

Plot.plot_graphic_from_pickles_dicts(caminho_pasta_output+"Posicao_Z_Tratada_x_Tempo", caminho_pasta_output+"times_to_each_marker.pkl", caminho_pasta_output+"cleaned_markers_z_positions.pkl", "Posicao em Z do Marcador x Tempo", "Tempo (s)", "Posicao (m)", video_duration=duracao_video, ids_wanted_markers=ids_desejados)
Plot.plot_graphic_from_pickles_dicts(caminho_pasta_output+"Velocidade_em_Z_Tratada_x_Tempo", caminho_pasta_output+"times_to_each_marker.pkl", caminho_pasta_output+"cleaned_speed_markers_z.pkl", "Velocidade em Z do Marcador x Tempo", "Tempo (s)", "Velocidade (m/s)", video_duration=duracao_video, ids_wanted_markers=ids_desejados)

Manip.organize_aruco_proccessing_output_folder(caminho_pasta_output)