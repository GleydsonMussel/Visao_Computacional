import cv2
import numpy as np
import funcoes_auxiliares.funcs_draw as funcs_draw
import funcoes_auxiliares.funcs_manip_arq as funcs_manip_arq
import funcoes_auxiliares.funcs_velocidade as funcs_velocidade
import funcoes_auxiliares.cria_pastas as cria_pastas

# Grante que as pastas necessárias existam
cria_pastas.arruma_ambiente()

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

funcs_manip_arq.limpa_frames_logs()

roi = None

# Pegando vídeo e preparando output do mesmo
nome_video = 'Voo6Editado'
extencao = '.mp4'
video = cv2.VideoCapture('./videos/Voos/'+nome_video+extencao)
alturaVideo = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT)); larguraVideo = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
fps = video.get(cv2.CAP_PROP_FPS)
videoSaida = cv2.VideoWriter('./videos/Outputs/'+nome_video+'_output'+extencao, cv2.VideoWriter_fourcc('m', 'p', '4', 'v'), fps, (larguraVideo, alturaVideo))

contFrame = 0

dadosCalib = np.load('./coeficientes/celular_Ronaldo/coeficientes.npz')

dist = dadosCalib['distortion']; mtx = dadosCalib['camera']; newcameramtx = dadosCalib['new_camera']; 
distpercorridaPassada = 0; alturapercorridaPassada = 0

aplicaCalib = True; redimensionaJanela = False                              

while True:
    
    frame = video.read()[1]
    
    if frame is None:
        break
    
    funcs_manip_arq.salvaFrame('./frames/frameCRU_'+str(contFrame)+'.png', frame)
           
    if aplicaCalib:
        frame = cv2.undistort(frame, mtx, dist, None, newcameramtx)
        funcs_manip_arq.salvaFrame('./frames/frameCALIB_'+str(contFrame)+'.png', frame)
        
    if roi is not None:
        
        localizou, caixaInteresse = tracker.update(frame)
        
        if localizou:
            # x -> cood x do canto superior direito, w -> largura da roi
            # y -> cood y do canto superior direito, h -> altura da roi
            x,y,w,h = [int(c) for c in caixaInteresse]
            if contFrame == 1:
                h0 = -999999999999
            if contFrame>1:
                #distpercorridaPassada, alturapercorridaPassada, h0 = funcs_velocidade.calc_velocidades_diagonalmente(x,y,w,h, cx, cy, contFrame, video.get(cv2.CAP_PROP_FPS), distpercorridaPassada, alturapercorridaPassada, h0)
                distpercorridaPassada, alturapercorridaPassada, h0 = funcs_velocidade.calc_velocidades(x,y,w,h, cx, cy, contFrame, video.get(cv2.CAP_PROP_FPS), distpercorridaPassada, alturapercorridaPassada, h0)
            
            cx, cy = funcs_draw.calc_centro_roi(x,w,y,h)
            funcs_draw.desenha_roi(frame, x,w,y,h)
            funcs_draw.desenha_centro(frame, cx, cy)
        
        else:
            break
    
    funcs_draw.escreve_no_video(frame, "Fps: "+str(round(video.get(cv2.CAP_PROP_FPS))),(0,25), (255,0,0))
    funcs_draw.escreve_no_video(frame, "Frame: "+str(contFrame),(0,60), (0,255,0))
     
    cv2.imshow('Rastreando',frame)   
    
    k = cv2.waitKey(30)
    
    if k == ord('s') or contFrame==0:
        
        # Inicializando selecionando com o mouse
        roi = cv2.selectROI('Rastreando',frame)

        # Inicializa o tracker no frame no qual se selecionou a roi
        tracker.init(frame,roi)
        funcs_manip_arq.salva_dado(roi, 1, './rois/roi'+str(nome_video)+'.txt')
        
    elif k == ord('q'):
        break
    
    contFrame+=1
    
    videoSaida.write(frame)
    
    print("Li o frame: "+str(contFrame))
    
video.release();cv2.destroyAllWindows() 
sourceDados1 =["./logs/tempo_decorrido.txt", 
               "./logs/tempo_decorrido.txt", 
               "./logs/tempo_decorrido.txt", 
               "./logs/tempo_decorrido.txt", 
               "./logs/tempo_decorrido.txt", 
               "./logs/tempo_decorrido.txt", 
               "./logs/tempo_decorrido.txt", 
               "./logs/tempo_decorrido.txt", 
               "./logs/tempo_decorrido.txt"
               ] 
sourceDados2 =["./logs/velocidade_percorrida_em_cada_frame.txt", 
               "./logs/distancia_percorrida_x_em_cada_frame.txt", 
               "./logs/distancia_percorrida_em_cada_frame.txt", 
               "./logs/alturaPercorrida_Ref_h0.txt", 
               "./logs/velocidade_percorrida_em_cada_frame.txt", 
               "./logs/distancia_percorrida_x_em_cada_frame.txt",  
               "./logs/distancia_percorrida_y_em_cada_frame.txt", 
               "./logs/distancias_cumulativas.txt", 
               "./logs/alturasCumulativas.txt"
               ]
titulos = ["Velocidade x Tempo", 
           "Distancia Nao Cumulativa x Tempo", 
           "Distancia x Tempo", 
           "Altura Baseada em H0 x Tempo", 
           "Velocidade x Tempo", 
           "Distancia x Tempo", 
           "Altura Nao Cumulativa x Tempo", 
           "Distancia x Tempo", 
           "Altura Cumulativa x Tempo "
           ]
labelsX = ["Tempo (s)", 
           "Tempo (s)", 
           "Tempo (s)", 
           "Tempo (s)", 
           "Tempo (s)", 
           "Tempo (s)", 
           "Tempo (s)", 
           "Tempo (s)", 
           "Tempo (s)"
           ]
labelsY = ["Velocidade (m/s)", 
           "Distancia (m)", 
           "Distancia (m)",  
           "Altura (m)", 
           "Velocidade (m/s)", 
           "Distancia (m)", 
           "Altura (m)", 
           "Distancia (m)", 
           "Altura (m)"
           ]

funcs_velocidade.salvaGraficosVelocidade(sourceDados1, sourceDados2, titulos, labelsX, labelsY)

print("Frames Lidos: "+str(contFrame))
print("Salvando Graficos...")

with open("./logs/distancias_cumulativas.txt", 'r') as arquivo:
    distsCumulativasDiag = [abs(float(linha)) for linha in arquivo.readlines()]
    arquivo.close()
print('Distância Percorrida Diagonalmente (m): '+str(max(distsCumulativasDiag)))

with open("./logs/alturaPercorrida_Ref_h0.txt", 'r') as arquivo:
    alturas = [abs(float(linha)) for linha in arquivo.readlines()]
    arquivo.close()
print("Queda da Mesa (m): "+str(max(alturas)))    


