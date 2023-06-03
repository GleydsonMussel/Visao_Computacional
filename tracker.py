import cv2
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
coordenadas_centro_x = []
coordenadas_centro_y = []
# Contador de frames lidos
cont = 0

# Controla se o ponto entrou ou não na zona de interesse
entrou = False

# Cria as Áreas a serem desenhadas, extrair as coordenadas do promeiro frame da imagem que já é salvo
area1 = [(1439, 739),(1314,664), (942, 730), (942, 664)]
area2 = [(942, 728), ]

# Começa a rodar o vídeo
while True:
    # Captura o grame atual
    frame = video.read()[1]
    # Checa se o frame atual não foi pego, se não foi, aborta o processamento
    if frame is None:
        break
    
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
            # Calcula velocidade
            if cont>1:
                funcs_velocidade.calc_velocidades(frame, x,y,w,h, cx, cy, cont, video.get(cv2.CAP_PROP_FPS))
            # Atualiza os centros
            cx, cy = funcs_draw.calc_centro_roi(x,w,y,h)
            coordenadas_centro_x.append(cx); coordenadas_centro_y.append(cy)
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
    
plot_graficos.plot_grafico("./log/tempo_decorrido.txt", "./log/velocidade_percorrida_em_cada_frame.txt", "Velocidade x Tempo")
video.release()
cv2.destroyAllWindows()
print("Frames lidos: "+str(cont)) 
