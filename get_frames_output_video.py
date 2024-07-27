import cv2

caminho_video = "./dados_extraidos/Voo10Editado_ArUco_take_3/Voo10Editado_Output.mp4"
video = cv2.VideoCapture(caminho_video)
cont = 0

while(True):
    ok, frame = video.read()
    cv2.imwrite("./frames_video_processado/frame"+str(cont)+".png", frame)
    cont+=1
    cv2.imshow("Lendo", frame)
    k = cv2.waitKey(30)
    # Aborta o vídeo
    if k == ord('q'):
        break
        