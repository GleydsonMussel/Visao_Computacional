import cv2
from funcoes_auxiliares import funcoes

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
funcoes.limpa_pasta()

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
    
    # Se leu o frame, já desenho as áreas nele
    funcoes.desenha_Area(frame, area1, (0,255,0))
    #funcoes.desenha_Area(frame, area2, (128, 0, 128))
    
    # Salva o primeiro frame
    if cont==0:
        funcoes.salvaFrame(frame, "./frames/Primeiro_Frame.jpg")
    
    # Redimensiono o frame
    #frame = cv2.resize(frame,(1220,720))

    # Checa se a região de interesse foi definida
    if roi is not None:
        # Atualiza o frame a ser pego pelo tracker
        success, box = tracker.update(frame)
        # Caso conseguiu atualizar
        if success:
            # x -> cood x do canto superior direito, w -> largura da roi
            # y -> cood y do canto superior direito, h -> altura da roi
            x,y,w,h = [int(c) for c in box]
            # Desenha
            cx, cy = funcoes.calc_centro_roi(x,w,y,h)
            coordenadas_centro_x.append(cx); coordenadas_centro_y.append(cy)
            funcoes.desenha_roi(frame, x,w,y,h)
            funcoes.desenha_centro(frame, x,w,y,h)
            # Checa se entrou em alguma área
            for area in [area1]:
                contArea = 1
                entrou = funcoes.entrou_na_area(area, x,w,y,h) 
                if entrou:
                    funcoes.salvaFrame(frame, "./frames/frames_na_area/"+str(contArea)+"_"+str(cont)+".jpg")
                    break
                    
        # Caso não consiga atualizar
        else:
            funcoes.escreve_no_video(frame, "PERDEU DE VISTA", (0,50), (0,0,255))
            roi = None
            tracker = trackers[tracker_key]()
    
    # Escreve o fps na tela
    funcoes.escreve_no_video(frame, "Fps: "+str(round(video.get(cv2.CAP_PROP_FPS))),(0,25), (255,0,0))
    
    # Mostra a janela com o vídeo executando 
    cv2.imshow('Rastreando',frame)
    
    # Fica no aguardo do usuáqrio digitar algo
    k = cv2.waitKey(30)
    
    # Digita-se s para pausar o video e se selecionar a região de interesse, roi
    if k == ord('s'):
        # Chama a função para permitir que a roi seja selecionada
        roi = cv2.selectROI('Rastreando',frame)
        # Inicializa o tracker no frame no qual se selecionou a roi
        tracker.init(frame,roi)
        # Salvo o frame no qual selecionei a roi
        funcoes.salvaFrame(frame, "./frames/Frame_da_Roi.jpg")
    # Fecha o vídeo
    elif k == ord('q'):
        break
    
    # Atualiza o contador
    cont+=1

video.release()
cv2.destroyAllWindows()
print("Frames lidos: "+str(cont)) 
