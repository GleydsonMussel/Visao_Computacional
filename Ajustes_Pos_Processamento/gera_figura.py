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
    "size":9,
    "weight":'normal',
    'family':'Times New Roman',
}

posicoes = {}
velocidades = Manip.load_pickle_data("./Ajustes_Pos_Processamento/cleaned_speed_markers_x_Voo_10.pkl")[37]
tempo = Manip.load_pickle_data("./Ajustes_Pos_Processamento/times_to_each_marker_Voo10.pkl")[37]

plt.plot(tempo[0:len(velocidades)], velocidades)
plt.title("Velocidade em X Tratada x Tempo", fontdict=font_title); plt.xlabel("Tempo (s)", fontdict=font_label); plt.ylabel("Velocidade (m/s)", fontdict=font_label)
plt.grid()
plt.legend()
plt.show()
#plt.savefig("./Ajustes_Pos_Processamento/Comparativo_2.png")
#plt.close() 