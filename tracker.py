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

# Tracker escolhido
tracker_key = 'kcf'
# Inicializa a região de interesse como None
roi = None
# Inicializa a variável que será responsável pelo tracking
tracker = trackers[tracker_key]()
# Capruta o video com base no caminho dado
video = cv2.VideoCapture('./videos/Aviao_de_Frente.mp4')

# Contador de frames lidos
cont = 0

# Controla se o ponto entrou ou não na zona de interesse
entrou = False

# REGIÃO 1
# Coordenadas pixel 1: 968, 459
# Coordenadas pixel 2: 1323, 500
# Coordenadas pixel 3: 727, 519
# Coordenadas pixel 4: 1100, 577

# REGIÃO 2
# Coordenadas pixel 1: 723, 525
# Coordenadas pixel 2: 1094, 579
# Coordenadas pixel 3: 364, 608
# Coordenadas pixel 4: 772, 698

# Cria as Áreas a serem desenhadas, extrair as coordenadas do promeiro frame da imagem que já é salvo
area1 = [(968, 459),(1323, 500),(727, 519),(1100, 577)]
area2 = [(723, 525),(1094, 579),(364, 608),(772, 698)]

# Começa a rodar o vídeo
while True:
    # Captura o grame atual
    frame = video.read()[1]
    # Checa se o frame atual não foi pego, se não foi, aborta o processamento
    if frame is None:
        break
    
    # Se leu o frame, já desenho as áreas nele
    funcoes.desenha_Area(frame, area1, (0,255,0))
    funcoes.desenha_Area(frame, area2, (128, 0, 128))
    
    # Salva o primeiro frame
    if cont==0:
        funcoes.salvaFrame(frame, "./frames/Primeiro_Frame.jpg")
    
    # Redimensiono o frame
    frame = cv2.resize(frame,(1220,720))

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
            funcoes.desenha_roi(frame, x,w,y,h)
            funcoes.desenha_centro(frame, x,w,y,h)
            # Checa se entrou em alguma área
            for area in [area1, area2]:
                contArea = 1
                entrou = funcoes.entrou_na_area(area, x,w,y,h) 
                if entrou:
                    print("Entrou na area: "+str(contArea)+"\n")
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

