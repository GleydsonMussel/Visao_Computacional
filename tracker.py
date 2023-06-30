import cv2
import numpy as np
import funcoes_auxiliares.funcs_draw as funcs_draw
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

# Limpa a pasta de frames
funcs_manip_arq.limpa_pastas()
# Tracker escolhido
tracker_key = 'csrt'
# Inicializa a região de interesse como None
roi = None
# Inicializa a variável que será responsável pelo tracking
tracker = trackers[tracker_key]()
# Capruta o video com base no caminho dado
video = cv2.VideoCapture('./videos/Voo.mp4')
# Contador de frames lidos
cont = 0
# Carregar os coeficientes do arquivo
data = np.load('./coeficientes/celular_Gleydson/coeficientes.npz')
# Acessar os coeficientes salvos                                                    Acumulador de distâncias percorridas
dist = data['distortion']; mtx = data['camera']; newcameramtx = data['new_camera']; distpercorridaPassada = 0
# Controlo se vou aplicar ou não a calibração   Controlo se precisa redimensionar o vídeo para
aplicaCalib = True                                 
# Começa a rodar o vídeo
while True:
    # Captura o grame atual
    frame = video.read()[1]
    # Checa se o frame atual não foi pego, se não foi, aborta o processamento
    if frame is None:
        break
    # resize image
    #frame = redimensiona.redimensiona(50, frame)
    funcs_manip_arq.salvaFrame('./frames/frameCRU'+str(cont)+'.png', frame)
    if aplicaCalib:
        frame = cv2.undistort(frame, mtx, dist, None, newcameramtx)
        funcs_manip_arq.salvaFrame('./frames/frameCALIB'+str(cont)+'.png', frame)
    # Salva o primeiro frame
    if cont==0:
       funcs_manip_arq.salvaFrame("./frames/Primeiro_Frame.jpg",frame)
    
    # Checa se a região de interesse foi definida
    if roi is not None:
        # Atualiza o frame a ser pego pelo tracker
        success, box = tracker.update(frame)
        # Caso conseguiu atualizar
        if success:
            # x -> cood x do canto superior direito, w -> largura da roi
            # y -> cood y do canto superior direito, h -> altura da roi
            x,y,w,h = [int(c) for c in box]
            if cont>1:
                distpercorridaPassada = funcs_velocidade.calc_velocidades_saida_chao(x,y,w,h, cx, cy, cont, video.get(cv2.CAP_PROP_FPS), distpercorridaPassada)
            # Atualiza os centros 
            cx, cy = funcs_draw.calc_centro_roi(x,w,y,h)
            funcs_draw.desenha_roi(frame, x,w,y,h)
            funcs_draw.desenha_centro(frame, cx, cy)
        # Caso não consiga atualizar
        else:
            funcs_draw.escreve_no_video(frame, "PERDEU DE VISTA", (0,50), (0,0,255))
            roi = None
            tracker = trackers[tracker_key]()
    
    # Escreve o fps na tela
    funcs_draw.escreve_no_video(frame, "Fps: "+str(round(video.get(cv2.CAP_PROP_FPS))),(0,25), (255,0,0))
    # Mostra a janela com o vídeo executando 
    cv2.imshow('Rastreando',redimensiona.redimensiona(50, frame))   
    # Fica no aguardo do usuáqrio digitar algo
    k = cv2.waitKey(30)
    # Garanto que a roi é sempre selecionada logo no primeiro frame
    if cont==0:
        k = 's'    
    # Digita-se s para pausar o video e se selecionar a região de interesse, roi
    if k == ord('s') or k=='s':
        # Chama a função para permitir que a roi seja selecionada
        #roi = cv2.selectROI('Rastreando',frame)
        roi = (109, 1651, 235, 120)
        # Inicializa o tracker no frame no qual se selecionou a roi
        tracker.init(frame,roi)
        # Salvo o frame no qual selecionei a roi
        funcs_manip_arq.salvaFrame( "./frames/Frame_da_Roi.jpg", frame)
        # Reseto o k
        k="g"
    # Fecha o vídeo
    elif k == ord('q'):
        break
    
    # Atualiza o contador
    cont+=1
    print("Li o frame: "+str(cont))
    
# Encerra vídeo e fecha janelas
video.release();cv2.destroyAllWindows() 
sourceDados1 =["./logs/tempo_decorrido.txt", "./logs/tempo_decorrido.txt", "./logs/tempo_decorrido.txt", "./logs/tempo_decorrido.txt", "./logs/tempo_decorrido.txt", "./logs/tempo_decorrido.txt", "./logs/tempo_decorrido.txt", "./logs/tempo_decorrido.txt"] 
sourceDados2 =["./logs/velocidade_percorrida_em_cada_frame.txt", "./logs/distancia_percorrida_x_em_cada_frame.txt", "./logs/distancia_percorrida_em_cada_frame.txt", "./logs/distancia_percorrida_y_em_cada_frame.txt", "./logs/velocidade_percorrida_em_cada_frame.txt", "./logs/distancia_percorrida_x_em_cada_frame.txt",  "./logs/distancia_percorrida_y_em_cada_frame.txt", "./logs/distancias_cumulativas.txt"]
titulos = ["Velocidade x Tempo", "Distancia_X x Tempo", "Distancia x Tempo", "Altura x Tempo", "Velocidade x Tempo", "Distancia x Tempo", "Altura x Tempo", "Distancia x Tempo"]
labelsX = ["Tempo (s)", "Tempo (s)", "Tempo (s)", "Tempo (s)", "Tempo (s)", "Tempo (s)", "Tempo (s)", "Tempo (s)"]
labelsY = ["Velocidade (m/s)", "Distancia (m)", "Distancia (m)",  "Altura (m)", "Velocidade (m/s)", "Distancia (m)", "Altura (m)", "Distancia (m)"]
funcs_velocidade.salvaGraficosVelocidade(sourceDados1, sourceDados2, titulos, labelsX, labelsY)
# Output no terminal
print("Frames Lidos: "+str(cont))
print("Salvando Graficos...")

