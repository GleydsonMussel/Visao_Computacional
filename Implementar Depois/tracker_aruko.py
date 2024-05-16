import cv2
import numpy as np
import funcoes_auxiliares.Drawer as Drawer
import funcoes_auxiliares.funcs_manip_arq as funcs_manip_arq
import funcoes_auxiliares.funcs_velocidade as funcs_velocidade
import funcoes_auxiliares.plot_graficos as plot_graficos
import funcoes_auxiliares.redimensiona as redimensiona

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

video = cv2.VideoCapture('./videos/Voos/Voo1.mp4')

contFrame = 0

dadosCalib = np.load('./coeficientes/celular_Vitor/coeficientes.npz')

dist = dadosCalib['distortion']; mtx = dadosCalib['camera']; newcameramtx = dadosCalib['new_camera']; distpercorridaPassada = 0; alturapercorrisaPassada = 0

aplicaCalib = False; redimensionaJanela = False                              

while True:
    
    frame = video.read()[1]
    
    if frame is None:
        break
    
    frameJanela = frame
    
    if redimensionaJanela:
        frameJanela = redimensiona.redimensiona(50, frame)  
    
    funcs_manip_arq.salvaFrame('./frames/frameCRU'+str(contFrame)+'.png', frame)
           
    if aplicaCalib:
        frame = cv2.undistort(frame, mtx, dist, None, newcameramtx)
        funcs_manip_arq.salvaFrame('./frames/frameCALIB'+str(contFrame)+'.png', frame)
        
    if roi is not None:
        
        localizou, caixaInteresse = tracker.update(frame)
        
        if localizou:
            # x -> cood x do canto superior direito, w -> largura da roi
            # y -> cood y do canto superior direito, h -> altura da roi
            x,y,w,h = [int(c) for c in caixaInteresse]
            if contFrame>1:
                distpercorridaPassada, alturapercorrisaPassada = funcs_velocidade.calc_velocidades_saida_chao(x,y,w,h, cx, cy, contFrame, video.get(cv2.CAP_PROP_FPS), distpercorridaPassada, alturapercorrisaPassada)
                #distpercorridaPassada, alturapercorrisaPassada = funcs_velocidade.calc_velocidades(x,y,w,h, cx, cy, contFrame, video.get(cv2.CAP_PROP_FPS), distpercorridaPassada, alturapercorrisaPassada)
            
            cx, cy = Drawer.calc_centro_roi(x,w,y,h)
            Drawer.desenha_roi(frame, x,w,y,h)
            Drawer.desenha_centro(frame, cx, cy)
        
        else:
            break
    
    Drawer.escreve_no_video(frame, "Fps: "+str(round(video.get(cv2.CAP_PROP_FPS))),(0,25), (255,0,0))
     
    cv2.imshow('Rastreando',frameJanela)   
    
    k = cv2.waitKey(30)
    
    if k == ord('s') or contFrame==0:
        
        roi = cv2.selectROI('Rastreando',frame)
        # VOO 1
        #roi = (109, 1651, 235, 120)
        # VOO2
        #roi = (2801,1253,141,109)
        # Teste de atrito
        #roi = (3289,271,112,49)
        # Atrito 2 
        #roi = (3309, 303, 113, 62)
        # Inicializa o tracker no frame no qual se selecionou a roi
        tracker.init(frame,roi)
        
    elif k == ord('q'):
        break
    
    contFrame+=1
    
    print("Li o frame: "+str(contFrame))
    
video.release();cv2.destroyAllWindows() 
sourceDados1 =["./logs/tempo_decorrido.txt", "./logs/tempo_decorrido.txt", "./logs/tempo_decorrido.txt", "./logs/tempo_decorrido.txt", "./logs/tempo_decorrido.txt", "./logs/tempo_decorrido.txt", "./logs/tempo_decorrido.txt", "./logs/tempo_decorrido.txt", "./logs/tempo_decorrido.txt"] 
sourceDados2 =["./logs/velocidade_percorrida_em_cada_frame.txt", "./logs/distancia_percorrida_x_em_cada_frame.txt", "./logs/distancia_percorrida_em_cada_frame.txt", "./logs/distancia_percorrida_y_em_cada_frame.txt", "./logs/velocidade_percorrida_em_cada_frame.txt", "./logs/distancia_percorrida_x_em_cada_frame.txt",  "./logs/distancia_percorrida_y_em_cada_frame.txt", "./logs/distancias_cumulativas.txt", "./logs/alturasCumulativas.txt"]
titulos = ["Velocidade x Tempo", "Distancia_X x Tempo", "Distancia x Tempo", "Altura x Tempo", "Velocidade x Tempo", "Distancia x Tempo", "Altura Nao Cumulativa x Tempo", "Distancia x Tempo", "Altura x Tempo "]
labelsX = ["Tempo (s)", "Tempo (s)", "Tempo (s)", "Tempo (s)", "Tempo (s)", "Tempo (s)", "Tempo (s)", "Tempo (s)", "Tempo (s)"]
labelsY = ["Velocidade (m/s)", "Distancia (m)", "Distancia (m)",  "Altura (m)", "Velocidade (m/s)", "Distancia (m)", "Altura (m)", "Distancia (m)", "Altura (m)"]
funcs_velocidade.salvaGraficosVelocidade(sourceDados1, sourceDados2, titulos, labelsX, labelsY)

print("Frames Lidos: "+str(contFrame))
print("Salvando Graficos...")

