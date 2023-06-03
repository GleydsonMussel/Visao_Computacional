import matplotlib.pyplot as plt

def plot_grafico(caminho_dado1, caminho_dado2, titulo):
    dado1=get_dados(caminho_dado1); dado2 = get_dados(caminho_dado2)
    plt.plot(dado1, dado2)
    plt.title(titulo)
    plt.xlabel("Tempo decorrido (s)")
    plt.ylabel("Velocidade (m/s)")
    plt.grid()
    plt.axes([0,12, 0,1]) 
    plt.show()
    
    
     
def get_dados(caminho_dado):
    dado = []
    with open(caminho_dado, 'r') as arquivo:
        linhas = arquivo.readlines()
        for linha in linhas:
            dado.append(float(linha))
        arquivo.close()
    return dado             
    