import numpy as np
import matplotlib.pyplot as plt
import sys

# Adicione o diretório "Methods" ao sys.path
sys.path.append('./Methods')

# Agora você pode importar os módulos diretamente
from Manipulate_Files import load_pickle_data
from Graphics import plot_graphic_with_direct_values

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

posicoes = {}
posicoes["charuco"] = load_pickle_data("./Ajustes_Pos_Processamento/Marcador_Z_CHARUCO.pkl")[37]
posicoes["xadrez"] = load_pickle_data("./Ajustes_Pos_Processamento/Marcador_Z_XADREZ.pkl")[37]
tempo = load_pickle_data("./Ajustes_Pos_Processamento/Tempo.pkl")[37]
print(len(posicoes["charuco"]))

#plot_graphic_with_direct_values("./Ajustes_Pos_Processamento/Comparativo_Posicoes_Z", tempo, posicoes, "Posicao em Z x Tempo", "Tempo (s)", "Posicao (m)")

plt.plot(tempo, posicoes["charuco"][0:len(tempo)], label="37 ChArUco")
plt.plot(tempo[0:len(posicoes["xadrez"])], posicoes["xadrez"][0:len(tempo)], label="37 Xadrez")
plt.title("Posicao em Z x Tempo", fontdict=font_title); plt.xlabel("Tempo (s)", fontdict=font_label); plt.ylabel("Posicao (m)", fontdict=font_label)
plt.grid()
plt.legend()
plt.savefig("./Ajustes_Pos_Processamento/Comparativo.png")
plt.close() 