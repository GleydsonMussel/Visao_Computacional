import matplotlib.pyplot as plt
import numpy as np
import os

def get_dados(caminho_dado):
    dado = []
    with open(caminho_dado, 'r') as arquivo:
        linhas = arquivo.readlines()
        for linha in linhas:
            dado.append(float(linha))
        arquivo.close()
    return dado 

def plot_grafico(caminho_dado1, caminho_dado2, titulo, lgdX, lgdY, limX=None, limY=None):
    dado1=get_dados(caminho_dado1); dado2 = get_dados(caminho_dado2)
    plt.plot(dado1, dado2)
    plt.title(titulo); plt.xlabel(lgdX); plt.ylabel(lgdY)
    plt.grid()
    if limX != None and limY!=None:
        plt.axes([limX[0], limX[1], limY[0], limY[1]]) 
    plt.savefig("./graficos/"+titulo+".png")
    plt.close()

def plot_polinomio(caminho_dado1, caminho_dado2, titulo, lgdX, lgdY,  lim_inf_dados1, lim_sup_dados1, limX=None, limY=None):
    dados1 = get_dados(caminho_dado1); dados2 = get_dados(caminho_dado2)
    polinomio = np.polyfit(dados1, dados2, 3)
    vetDados1 = np.arange(lim_inf_dados1, lim_sup_dados1, 0.01)
    valsDados2 = np.polyval(polinomio, vetDados1)  
    plt.plot(vetDados1, valsDados2)
    plt.title(titulo); plt.xlabel(lgdX); plt.ylabel(lgdY)
    plt.grid()
    if limX != None and limY!=None:
        plt.axes([limX[0], limX[1], limY[0], limY[1]]) 
    plt.savefig("./graficos/"+titulo+"POLI.png")
    plt.close()

def plot_grafico_atrito(tempos, distsCru, distsPoli,titulo, batizaX, batizaY):
    plt.title(titulo)
    plt.xlabel(batizaX); plt.ylabel(batizaY)
    plt.plot(tempos, distsCru, label='Cru')
    plt.plot(tempos, distsPoli, label='Poli')
    plt.legend()
    plt.grid()
    plt.savefig("./graficos/"+titulo+".png")
        
        

    
            
    