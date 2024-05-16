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
nome_video = 'Voo7Editado'; extencao = '.mp4'

# SETAR O VALOR DO FATOR DE CONVERSÃO
fatConvPxM = 0.078

# Se desejar aplicar a calibração de câmera, True, se não, False
aplicaCalib = True

#--------------------------------------------------------------------------

# Lista de trackers disponíveis
trackers = {
    'csrt' : cv2.legacy.TrackerCSRT_create,  # hight accuracy ,slow
    'mosse' : cv2.legacy.TrackerMOSSE_create,  # fast, low accuracy
    'kcf' : cv2.legacy.TrackerKCF_create,   # moderate accuracy and speed
    'medianflow' : cv2.legacy.TrackerMedianFlow_create,
    'mil' : cv2.legacy.TrackerMIL_create,
    'tld' : cv2.legacy.TrackerTLD_create,
    'boosting' : cv2.legacy.TrackerBoosting_create
}
tracker_key = 'csrt'
tracker = trackers[tracker_key]()

video = cv2.VideoCapture('./videos/Voos/'+nome_video+extencao)
alturaVideo = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT)); 
larguraVideo = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
videoSaida = cv2.VideoWriter('./videos/Outputs/'+nome_video+'_output'+extencao, cv2.VideoWriter_fourcc('m', 'p', '4', 'v'), video.get(cv2.CAP_PROP_FPS), (larguraVideo, alturaVideo))

dados_camera = CameraData('./Cameras_Data/celular_Gleydson/coeficientes.npz')
 
distancia_acumulada_X = 0; altura_acumulada = 0
contFrame = 0
roi = None                              

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
    
    # Se há uma região de interesse para o rastreador rastrear
    if roi is not None:
        
        localizou, caixaInteresse = tracker.update(frame)
        
        if localizou:
            # x -> cood x do canto superior direito, w -> largura da roi
            # y -> cood y do canto superior direito, h -> altura da roi
            x,y,w,h = [int(c) for c in caixaInteresse]
            if contFrame>1:
                distancia_acumulada_X, altura_acumulada = Calculator.calc_speed(x, y, w, h, cx, cy, contFrame, video.get(cv2.CAP_PROP_FPS), distancia_acumulada_X, altura_acumulada, fatConvPxM)
            
            cx, cy = Calculator.get_center_roi(x,w,y,h)
            Drawer.draw_roi(frame, x, w, y, h, cx, cy)

        else:
            break
    
    Drawer.write_on_video(frame, "Fps: "+str(round(video.get(cv2.CAP_PROP_FPS))),(0,25), (255,0,0))
    Drawer.write_on_video(frame, "Frame: "+str(contFrame),(0,60), (0,255,0))
     
    cv2.imshow('Rastreando',frame)   
    
    k = cv2.waitKey(30)
    
    if k == ord('s') or contFrame==0:
        
        # Inicializando selecionando com o mouse
        roi = cv2.selectROI('Rastreando',frame)
        # Inicializando por coordenada
        #roi = ()
        
        # Inicializa o tracker no frame no qual se selecionou a roi
        tracker.init(frame,roi)
        Manip.save_data(roi, './rois/roi'+str(nome_video)+'.txt')
    
    # Habilita dar pause no vídeo
    elif k == ord('p'):
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
video.release();cv2.destroyAllWindows() 

# Títulos
with open("./Methods/Textual_Inputs/graphics_titles.txt", 'r') as arquivo:
    titles = arquivo.readlines()
    titles = [title.replace("\n", "") for title in titles]
    arquivo.close()
    
# Dados
caminhos_dados_eixo_x = "./logs/tempo_decorrido.txt"
with open("./Methods/Textual_Inputs/paths_data_to_plot_graphics.txt", 'r') as arquivo:
    caminhos_dados_eixo_y = arquivo.readlines()
    caminhos_dados_eixo_y = [caminho.split(" ")[0].replace("\n", "") for caminho in caminhos_dados_eixo_y]
    arquivo.close()

# Labels
xlabel = "Tempo (s)"
ylabels = ["Velocidade (m/s)", 
           "Distancia (m)", 
           "Distancia (m)",
           "Distancia (m)",
           "Distancia (m)",  
           ]

print("Frames Lidos: "+str(contFrame))

print("Salvando Graficos...")
for path_data_y_axis, title, ylabel in zip(caminhos_dados_eixo_y, titles, ylabels):
    Plot.plot_graphic(caminhos_dados_eixo_x, path_data_y_axis, title, xlabel, ylabel)
    
with open("./logs/distancias_cumulativas.txt", 'r') as arquivo:
    distsCumulativasDiag = [abs(float(linha)) for linha in arquivo.readlines()]
    arquivo.close()
print('Distância Percorrida Diagonalmente (m): '+str(max(distsCumulativasDiag)))

with open("./logs/poscoes_y_centro_atuais.txt", 'r') as arquivo:
    alturas = [abs(float(linha)) for linha in arquivo.readlines()]
    arquivo.close()
print("Queda da Mesa (m): "+str(abs(alturas[0]*fatConvPxM - min(alturas)*fatConvPxM)))    


