import cv2
import numpy as np
import funcoes_auxiliares.funcs_draw as funcs_draw
import funcoes_auxiliares.funcs_manip_arq as funcs_manip_arq
import funcoes_auxiliares.funcs_velocidade as funcs_velocidade
import funcoes_auxiliares.plot_graficos as plot_graficos


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
video = cv2.VideoCapture('./videos/Aviao_de_Perfil.mp4')
# Contador de frames lidos
cont = 0
# Carrego as variáveis da camera
mtx = np.load('./coeficientes/celular_Gleydson/mtx.npy')
newcameramtx = np.load('./coeficientes/celular_Gleydson/newcameramtx.npy')
dist = np.load('./coeficientes/celular_Gleydson/dist.npy') 
# Começa a rodar o vídeo
while True:
    # Captura o grame atual
    frame = video.read()[1]
    # Checa se o frame atual não foi pego, se não foi, aborta o processamento
    if frame is None:
        break
    cv2.imwrite('./frames/frameCRU'+str(cont)+'.png', frame)
    frame = cv2.undistort(frame, mtx, dist, None, newcameramtx)
    cv2.imwrite('./frames/frameCALIB'+str(cont)+'.png', frame)
    # Salva o primeiro frame
    if cont==0:
       funcs_manip_arq.salvaFrame(frame, "./frames/Primeiro_Frame.jpg")
    
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
                funcs_velocidade.calc_velocidades(x,y,w,h, cx, cy, cont, video.get(cv2.CAP_PROP_FPS))
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
    cv2.imshow('Rastreando',frame)
    
    # Fica no aguardo do usuáqrio digitar algo
    k = cv2.waitKey(30)
    
    # Garanto que a roi é sempre selecionada logo no primeiro frame
    if cont==0:
        k = 's'
    
    # Digita-se s para pausar o video e se selecionar a região de interesse, roi
    if k == ord('s') or k=='s':
        # Chama a função para permitir que a roi seja selecionada
        roi = cv2.selectROI('Rastreando',frame)
        # Inicializa o tracker no frame no qual se selecionou a roi
        tracker.init(frame,roi)
        # Salvo o frame no qual selecionei a roi
        funcs_manip_arq.salvaFrame(frame, "./frames/Frame_da_Roi.jpg")
        # Reseto o k
        k="g"
    # Fecha o vídeo
    elif k == ord('q'):
        break
    
    # Atualiza o contador
    cont+=1
    
# Encerra vídeo e fecha janelas
video.release();cv2.destroyAllWindows()    
# PLOTS GRÁFICOS
plot_graficos.plot_grafico("./logs/tempo_decorrido.txt", "./logs/velocidade_percorrida_em_cada_frame.txt", "Velocidade x Tempo", "Tempo (s)", "Velocidade (m/s)", [0,12], [0,1])
plot_graficos.plot_grafico("./logs/tempo_decorrido.txt", "./logs/distancia_percorrida_x_em_cada_frame.txt", "Distancia x Tempo", "Tempo (s)", "Distancia (m)")
plot_graficos.plot_grafico("./logs/tempo_decorrido.txt", "./logs/distancia_percorrida_y_em_cada_frame.txt", "Altura x Tempo", "Tempo (s)", "Altura (m)")
plot_graficos.plot_polinomio("./logs/tempo_decorrido.txt", "./logs/velocidade_percorrida_em_cada_frame.txt", "Velocidade x Tempo", "Tempo (s)", "Velocidade (m/s)", 0, 14)
plot_graficos.plot_polinomio("./logs/tempo_decorrido.txt", "./logs/distancia_percorrida_x_em_cada_frame.txt", "Distancia x Tempo", "Tempo (s)", "Distancia (m)", 0, 14)
plot_graficos.plot_polinomio("./logs/tempo_decorrido.txt", "./logs/distancia_percorrida_y_em_cada_frame.txt", "Altura x Tempo", "Tempo (s)", "Altura (m)", 0, 14)
# Output no terminal
print("Frames Lidos: "+str(cont))
print("Salvando Graficos...")
 
