import numpy as np
import matplotlib.pyplot as plt
import sys

# Adicione o diretório "Methods" ao sys.path
sys.path.append('./Methods')

# Agora você pode importar os módulos diretamente
from Manipulate_Files import load_pickle_data
from Graphics import plot_graphic_with_direct_values

# Formatação das fontes
font_title = {  
    "fontsize": 14,
    "fontweight": 'bold',
    "fontname": 'Times New Roman',
}
font_label = {
    "fontsize": 12,
    "fontweight": 'bold',
    'fontname': 'Times New Roman',
}
font_lgd = {
    "size": 9,
    "weight": 'normal',
    'family': 'Times New Roman',
}

tempos = load_pickle_data("./dados_extraidos/Teste_Arthur_2x_take_2/times_to_each_marker.pkl")
velocidades_z = load_pickle_data("./dados_extraidos/Teste_Arthur_2x_take_2/cleaned_speed_markers_with_clean_z_positions.pkl")

plot_graphic_with_direct_values("./dados_extraidos/Teste_Arthur_2x_take_2/Velocidade_em_Z_Tratatatatatada_x_Tempo", tempos[0], velocidades_z[0], "Velocidade em Z Tratatada x Tempo", "Tempo (s)", "Velocidade (m/s)")
