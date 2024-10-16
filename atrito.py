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

roi = None

nome_video = 'Atrito1Editado'
extencao = '.mp4'
video = cv2.VideoCapture('./videos/Teste_Atrito/'+nome_video+extencao)
alturaVideo = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT)); larguraVideo = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
fps = video.get(cv2.CAP_PROP_FPS)
videoSaida = cv2.VideoWriter('./videos/Outputs/'+nome_video+'_output'+extencao, cv2.VideoWriter_fourcc('m', 'p', '4', 'v'), fps, (larguraVideo, alturaVideo), isColor=True)

contFrame = 0

dadosCalib = np.load('./coeficientes/celular_Ronaldo/coeficientes.npz')

dist = dadosCalib['distortion']; mtx = dadosCalib['camera']; newcameramtx = dadosCalib['new_camera']; 
distpercorridaPassada = 0; alturapercorridaPassada = 0

aplicaCalib = False; redimensionaJanela = False; rodaVideo = True

if rodaVideo:  
    
    funcs_manip_arq.limpa_frames_logs()                        

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
                    distpercorridaPassada, alturapercorridaPassada, h0 = funcs_velocidade.calc_velocidades_diagonalmente(x,y,w,h, cx, cy, contFrame, video.get(cv2.CAP_PROP_FPS), distpercorridaPassada, alturapercorridaPassada, h0)
                    #distpercorridaPassada, alturapercorridaPassada, h0 = funcs_velocidade.calc_velocidades(x,y,w,h, cx, cy, contFrame, video.get(cv2.CAP_PROP_FPS), distpercorridaPassada, alturapercorridaPassada, h0)
                
                cx, cy = Drawer.calc_centro_roi(x,w,y,h)
                Drawer.desenha_roi(frame, x,w,y,h)
                Drawer.desenha_centro(frame, cx, cy)
            
            else:
                break
        
        Drawer.escreve_no_video(frame, "Fps: "+str(round(video.get(cv2.CAP_PROP_FPS))),(0,25), (255,0,0))
        Drawer.escreve_no_video(frame, "Frame: "+str(contFrame),(0,60), (0,255,0))
        
        cv2.imshow('Rastreando',frame)   
        
        k = cv2.waitKey(30)
        
        if k == ord('s') or contFrame==0:
            
            #roi = cv2.selectROI('Rastreando',frame)
            roi = (1682, 216, 58, 40)
            
            tracker.init(frame,roi)
            funcs_manip_arq.salva_dado(roi, 1, './rois/roi'+str("Atrito1")+'.txt')
            
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
print("Altura Percorrida(m): "+str(max(alturas)))

# Massa do objeto (kg)
m = 0.410
# Força atuante no eixo x (N)
Px = 1.95
# Angulo (graus)
theta = 29
# Gravidade
g = 9.81

# Aceleração desconsiderando o atrito (m/s2)
ax = Px/m
# Pega os Dados
velocidades = plot_graficos.get_dados("./logs/velocidade_percorrida_em_cada_frame.txt")
tempos = plot_graficos.get_dados("./logs/tempo_decorrido.txt")
distancias = plot_graficos.get_dados("./logs/distancias_cumulativas.txt")

distancias = [abs(float(distancia)) for distancia in distancias]
velocidades = [abs(float(velocidade)) for velocidade in velocidades]
tempos = [float(tempo) for tempo in tempos]

polinomio = np.polyfit(tempos, distancias, 2)
aceleracaoMedia = polinomio[0]*2

u = ((Px/m) - aceleracaoMedia)/g*np.cos(np.pi/180*theta)

plot_graficos.plot_grafico_atrito(tempos, distancias, np.polyval(polinomio, tempos), "Distancia x Tempo Atrito Poli", "Tempo (s)", "Distancia (m)")
print("O coeficiente de atrito é: "+str(u))   


