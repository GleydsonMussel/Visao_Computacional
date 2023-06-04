import matplotlib.pyplot as plt
     
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
    if titulo=="Distancia x Tempo":
        print("Distancia Percorrida: "+str(sum(dado2)))
    
    
    
            
    