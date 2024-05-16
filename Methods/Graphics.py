import matplotlib.pyplot as plt
import numpy as np

# Formatação das fontes
font_title={  
    "fontsize":14,
    "fontweight": 'bold',
    "fontname":'Times New Roman',
}
font_label={
    "fontsize":12,
    "fontweight":'bold',
    'fontname':'Times New Roman',
}
font_lgd={
    "size":9,
    "weight":'normal',
    'family':'Times New Roman',
}

def get_dados(caminho_dado):
    with open(caminho_dado, 'r') as arquivo:
        dados = arquivo.readlines()
        dados = [float(dado) for dado in dados]
        arquivo.close()
    return dados 

def plot_graphic(path_data_1, path_data_2, title, lgdX, lgdY, limX=None, limY=None):
    dado1=get_dados(path_data_1); dado2 = get_dados(path_data_2)
    plt.plot(dado1, dado2)
    plt.title(title, fontdict=font_title); plt.xlabel(lgdX, fontdict=font_label); plt.ylabel(lgdY, fontdict=font_label)
    plt.grid()
    if limX != None and limY!=None:
        plt.axes([limX[0], limX[1], limY[0], limY[1]]) 
    plt.savefig("./graficos/"+title+".png")
    plt.close()

def plot_interpolation(path_data_1, path_data_2, title, lgdX, lgdY,  lim_inf_dados1, lim_sup_dados1, limX=None, limY=None):
    dados1 = get_dados(path_data_1); dados2 = get_dados(path_data_2)
    polinomio = np.polyfit(dados1, dados2, 3)
    vetDados1 = np.arange(lim_inf_dados1, lim_sup_dados1, 0.01)
    valsDados2 = np.polyval(polinomio, vetDados1)  
    plt.plot(vetDados1, valsDados2)
    plt.title(title, fontdict=font_title); plt.xlabel(lgdX, fontdict=font_label); plt.ylabel(lgdY, fontdict=font_label)
    plt.grid()
    if limX != None and limY!=None:
        plt.axes([limX[0], limX[1], limY[0], limY[1]]) 
    plt.savefig("./graficos/"+title+"POLI.png")
    plt.close()

def plot_friction_test(tempos, distsCru, distsPoli,title, batizaX, batizaY):
    plt.title(title)
    plt.xlabel(batizaX); plt.ylabel(batizaY)
    plt.plot(tempos, distsCru, label='Cru')
    plt.plot(tempos, distsPoli, label='Poli')
    plt.legend()
    plt.grid()
    plt.savefig("./graficos/"+title+".png")
        
        

    
            
    