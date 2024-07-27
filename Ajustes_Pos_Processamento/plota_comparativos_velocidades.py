import numpy as np
import matplotlib.pyplot as plt
import sys

# Adicione o diretório "Methods" ao sys.path
sys.path.append('./Classes')

# Agora você pode importar os módulos diretamente
from Manipulate_Files import Manipulate_Files as Manip
from Graphics import Graphics

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
    "size":12,
    "weight":'normal',
    'family':'Times New Roman',
}

posicoes = {}
velocidades_tracker = []
with open("./Ajustes_Pos_Processamento/Velocidades_Tracker.txt", 'r') as arquivo:
    velocidades_tracker = arquivo.readlines()
velocidades_tracker = [float(velocidade) for velocidade in velocidades_tracker]

velocidades = Manip.load_pickle_data("./Ajustes_Pos_Processamento/Velocidades_ArUcO.pkl")[37]
tempo = Manip.load_pickle_data("./Ajustes_Pos_Processamento/Tempos.pkl")[37]

plt.plot(tempo[0:len(velocidades)], velocidades, label="ArUco")
plt.plot(tempo[0:len(velocidades_tracker)], velocidades_tracker, label="Rastreador")
plt.xlim(2.5,4.5)
plt.title("Velocidades Extraídas x Tempo", fontdict=font_title); plt.xlabel("Tempo (s)", fontdict=font_label); plt.ylabel("Velocidade (m/s)", fontdict=font_label)
plt.grid()
plt.legend(prop=font_lgd)
plt.savefig("./Ajustes_Pos_Processamento/Comparativo_Coleta_Velocidades.png")
plt.show()
plt.close() 