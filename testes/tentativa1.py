import cv2
import sys

# Inicializa o tracker
tracker = cv2.TrackerKCF_create()

# Captura o vídeo
video = cv2.VideoCapture("videos/Teste1.mp4")

# Testa se o vídeo abriu
if not video.isOpened():
    print("Could not open video")
    sys.exit()

# Tenta ler o primeiro frame do arquivo
ok, frame = video.read()

# Testa se foi possível ler o frame
if not ok:
    print('Cannot read video file')
    sys.exit()

# Selecionando o retangulo de seleção
bbox = cv2.selectROI("Inicio Rastreio",frame, False)

# Inicializa o tracker com a primeira área de interesse
ok = tracker.init(frame, bbox)
frames=[]
cont = 0
# Comeá a de fato ler os frames
while True:
    # Le um novo frame
    ok, frame = video.read()
    
    # Interrompe a leitura se perdeu 1 frame
    if not ok:
        break
        
    # Inicializa o timer
    timer = cv2.getTickCount()

    # Faz o tracker ler o próximo frame
    ok, bbox = tracker.update(frame)

    # Calcula o fps
    fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer)

    # Redesenha a área de interesse para o frame atual caso o frame seja pego com sucesso
    if ok:
        # Tracking success
        p1 = (int(bbox[0]), int(bbox[1]))
        p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
        cv2.rectangle(frame, p1, p2, (255,0,0), 2, 1)
        # Display result
        cv2.imshow("Rastreando", frame)
        frames.append(cv2.CAP_PROP_FPS)
        print(frames[cont])
        print("\n")
        cont+=1
    else :
        # Tracking failure
        cv2.putText(frame, "Falha no Tracking", (100,80), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(0,0,255),2)

        # Display tracker type on frame
        cv2.putText(frame, " KCS Tracker", (100,20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50),2);
    
        # Display FPS on frame
        cv2.putText(frame, "FPS : " + str(int(fps)), (100,50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50), 2);

        # Display result
        cv2.imshow("Rastreando", frame)

        # Exit if ESC pressed
        k = cv2.waitKey(1) & 0xff
        
        # Interrompe a leitura dos vídeos caso se pressione esc ou o vídeo acabe
        if k == 27 : break
