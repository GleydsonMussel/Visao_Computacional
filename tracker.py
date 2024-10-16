import cv2
import sys
sys.path.append("./Classes")
from Classes.CameraData import CameraData
from Drawer import Drawer
from Manipulate_Files import Manipulate_Files as Manip
from Calculator import Calculator
from Graphics import Graphics as Plot
from Calibration import Calibration

# Garante que as pastas necessárias existem
Manip.create_folders()
# Limpa tudo que for necessário para realizar o processamento
Manip.clean_tracker_processing()

#-----------------------------PREENCHER-----------------------------------

# SETAR NOME VÍDEO
nome_video = 'Voo10Editado'; extencao = '.mp4'

# Caminho para importar os dados da câmera utilizada
dados_camera = CameraData('./Cameras_Data/celular_Gleydson2/testeCharuco.npz')

# SETAR O VALOR DO FATOR DE CONVERSÃO
fatConvPxM = 4.2/873
fatConvPxM = 4.2/826 # ChArUco voo 10

# Se desejar aplicar a calibração de câmera, True, se não, False
aplicaCalib = True

# Define se os coeficientes foram obtidos pela calibração usando tabuleiro de xadrez ou ChArUco 
ChArUco = True

#--------------------------------------------------------------------------

# Cria pasta para exportar os dados necessários para a realização dessa análise
caminho_pasta_output = "./dados_extraidos/"+nome_video+"_Tracker"
caminho_pasta_output = Manip.create_folder(caminho_pasta_output)

# Lista de trackers disponíveis
trackers = {
    'csrt' : cv2.legacy.TrackerCSRT.create(),  # hight accuracy ,slow
    'mosse' : cv2.legacy.TrackerMOSSE.create(),  # fast, low accuracy
    'kcf' : cv2.legacy.TrackerKCF.create(),   # moderate accuracy and speed
    'medianflow' : cv2.legacy.TrackerMedianFlow.create(),
    'mil' : cv2.legacy.TrackerMIL.create(),
    'tld' : cv2.legacy.TrackerTLD.create(),
    'boosting' : cv2.legacy.TrackerBoosting.create()
}
tracker_key = 'csrt'
tracker = trackers[tracker_key]

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

distancia_acumulada_X = 0; altura_acumulada = 0
contFrame = 0
roi = None                              

#-----------------Começo Processamento------------------
while True:
    # Tenta coletar o frame a ser processado
    frame = video.read()[1]
    
    if frame is None:
        break
    cv2.imwrite('./frames/frameCRU_'+str(contFrame)+'.png', frame)
    
    # Caso se deseje aplicar a calibração
    if aplicaCalib:
        frame = Calibration.aply_calib(frame, dados_camera, ChArUco)
        cv2.imwrite('./frames/frameCALIB_'+str(contFrame)+'.png', frame)
    
    # Se há uma região de interesse para o rastreador rastrear
    if roi is not None:
        
        localizou, caixaInteresse = tracker.update(frame)
        
        if localizou:
            # x -> cood x do canto superior direito, w -> largura da roi
            # y -> cood y do canto superior direito, h -> altura da roi
            x,y,w,h = [int(c) for c in caixaInteresse]
            if contFrame>1:
                distancia_acumulada_X, altura_acumulada = Calculator.calc_speed(x, y, w, h, cx, cy, contFrame, video.get(cv2.CAP_PROP_FPS), distancia_acumulada_X, altura_acumulada, fatConvPxM, caminho_pasta_output)
            
            cx, cy = Calculator.get_center_roi(x,w,y,h)
            Drawer.draw_roi(frame, x, w, y, h, cx, cy)

        else:
            break
    
    Drawer.write_on_video(frame, "Fps: "+str(round(video.get(cv2.CAP_PROP_FPS))),(0,25), (255,0,0))
    Drawer.write_on_video(frame, "Frame: "+str(contFrame),(0,60), (0,255,0))
    Drawer.write_on_video(frame, "Tempo: "+str(round(contFrame/round(video.get(cv2.CAP_PROP_FPS)), 2)),(0,95), (0,0,255))
     
    cv2.imshow('Rastreando',frame)   
    
    k = cv2.waitKey(30)
    
    if k == ord('s'):
        
        # Inicializando selecionando com o mouse
        roi = cv2.selectROI('Rastreando',frame)
        # Inicializando por coordenada
        #roi = 
        
        # Inicializa o tracker no frame no qual se selecionou a roi
        tracker.init(frame,roi)
        Manip.save_data(roi, caminho_pasta_output+"roi.txt")
        
        # Atualização do Rastreador
        x,y,w,h = [int(c) for c in tracker.update(frame)[1]]
        cx, cy = Calculator.get_center_roi(x,w,y,h)
        Drawer.draw_roi(frame, x, w, y, h, cx, cy)
    
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
with open("./Textual_Inputs_Tracker_Processing/graphics_titles.txt", 'r') as arquivo:
    titles = arquivo.readlines()
    titles = [title.replace("\n", "") for title in titles]
    arquivo.close()

# Dados
caminhos_dados_eixo_x = caminho_pasta_output+"tempo_decorrido.txt"
with open("./Textual_Inputs_Tracker_Processing/paths_data_to_plot_graphics.txt", 'r') as arquivo:
    caminhos_dados_eixo_y = arquivo.readlines()
    caminhos_dados_eixo_y = [caminho_pasta_output+(caminho.split(" ")[0].replace("\n", "")) for caminho in caminhos_dados_eixo_y]
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
    Plot.plot_graphic(caminhos_dados_eixo_x, path_data_y_axis, title, xlabel, ylabel, pasta_output=caminho_pasta_output)
    
with open(caminho_pasta_output+"distancias_cumulativas.txt", 'r') as arquivo:
    distsCumulativasDiag = [abs(float(linha)) for linha in arquivo.readlines()]
    arquivo.close()
print('Distância Percorrida Diagonalmente (m): '+str(max(distsCumulativasDiag)))

with open(caminho_pasta_output+"poscoes_y_centro_atuais.txt", 'r') as arquivo:
    alturas = [abs(float(linha)) for linha in arquivo.readlines()]
    arquivo.close()
print("Queda da Mesa (m): "+str(abs(alturas[0]*fatConvPxM - min(alturas)*fatConvPxM)))    


