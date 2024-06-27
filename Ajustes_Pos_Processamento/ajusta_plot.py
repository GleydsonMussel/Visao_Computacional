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
posicoes["charuco"] = load_pickle_data("./Ajustes_Pos_Processamento/markers_z_positions_90cm_CHARUCO.pkl")[37]
posicoes["xadrez"] = load_pickle_data("./Ajustes_Pos_Processamento/markers_z_positions_90cm_XADREZ.pkl")[37]
posicoes["xadrez"] = [dado for dado in posicoes["xadrez"] if dado < 2]
tempo = load_pickle_data("./Ajustes_Pos_Processamento/times_to_each_marker.pkl")[37]
posicao_ref = []
for i in range(len(tempo)):
    posicao_ref.append(0.9)
    
print(len(posicoes["charuco"]))

#plot_graphic_with_direct_values("./Ajustes_Pos_Processamento/Comparativo_Posicoes_Z", tempo, posicoes, "Posicao em Z x Tempo", "Tempo (s)", "Posicao (m)")

plt.plot(tempo, posicoes["charuco"][0:len(tempo)], label="37 ChArUco")
plt.plot(tempo[0:len(posicoes["xadrez"])], posicoes["xadrez"][0:len(tempo)], label="37 Xadrez")
plt.plot(tempo, posicao_ref, label="Posição Real")

plt.title("Posicao em Z x Tempo", fontdict=font_title); plt.xlabel("Tempo (s)", fontdict=font_label); plt.ylabel("Posicao (m)", fontdict=font_label)
plt.grid()
plt.legend()
plt.savefig("./Ajustes_Pos_Processamento/Comparativo_2.png")
plt.close() 