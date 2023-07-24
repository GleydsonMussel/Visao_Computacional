import numpy as np
import matplotlib.pyplot as plt
import statistics

def get_dados(caminho_dado):
    dado = []
    with open(caminho_dado, 'r') as arquivo:
        linhas = arquivo.readlines()
        for linha in linhas:
            dado.append(float(linha))
        arquivo.close()
    return dado

def plot_polinomio(dado1, dado2, titulo, lgdX, lgdY,  lim_inf_dados, lim_sup_dados1=None, limX=None, limY=None):
    polinomio = np.polyfit(dado1, dado2, 2)
    vetDados1 = np.arange(lim_inf_dados, lim_sup_dados1, 0.01)
    valsDados2 = np.polyval(polinomio, vetDados1)  
    plt.plot(vetDados1, valsDados2, label="Interpolação")
    plt.plot(dado1, dado2, label = "Bruto")
    plt.title(titulo); plt.xlabel(lgdX); plt.ylabel(lgdY)
    plt.grid()
    plt.legend()
    if limX != None and limY!=None:
        plt.axes([limX[0], limX[1], limY[0], limY[1]]) 
    plt.savefig("./graficos/"+titulo+"POLI.png")

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
# Variação do tempo entre um frame e outro (s)
deltaT = 0.0166
# Pega os Dados
velocidades = get_dados("./logs/velocidade_percorrida_em_cada_frame.txt")
tempos = get_dados("./logs/tempo_decorrido.txt")
distancias = get_dados("./logs/distancias_cumulativas.txt")

temposGrafico = []
distancias_grafico = []

for i in range(len(distancias)): 
    if i>27 and i<111:
        temposGrafico.append(tempos[i])
        distancias_grafico.append(distancias[i])

distanciasAdap = [i - distancias_grafico[0] for i in distancias_grafico]
tempoAdap = [i-temposGrafico[0] for i in temposGrafico]

distanciasPoli = np.polyfit(tempoAdap, distanciasAdap, 2)
aceleracaoMedia = distanciasPoli[0]*2

u = ((Px/m) - aceleracaoMedia)/g*np.cos(np.pi/180*theta)

plot_polinomio(tempoAdap, distanciasAdap, "Distancia x Tempo Atrito Poli", "Tempo (s)", "Distancia (m)", 0, tempoAdap[len(tempoAdap)-1])
print("O coeficiente de atrito é: "+str(u))