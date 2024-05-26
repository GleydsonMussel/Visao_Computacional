import matplotlib.pyplot as plt
import numpy as np
import pickle
from Calculator import calc_speed_in_Z_axis
from Methods.Data_Cleaner import clean_data
from Manipulate_Files import load_pickle_data

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

# Importador Genérico de Dados
def get_dados(caminho_dado):
    with open(caminho_dado, 'r') as arquivo:
        dados = arquivo.readlines()
        dados = [float(dado) for dado in dados]
        arquivo.close()
    return dados 
    
# Plotador Genérico
def plot_graphic(path_data_1, path_data_2, title, lgdX, lgdY, limX=None, limY=None):
    dado1=get_dados(path_data_1); dado2 = get_dados(path_data_2)
    plt.plot(dado1, dado2)
    plt.title(title, fontdict=font_title); plt.xlabel(lgdX, fontdict=font_label); plt.ylabel(lgdY, fontdict=font_label)
    plt.grid()
    if limX != None:
        plt.xlim([limX[0], limX[1]])
    if limY != None:
        plt.ylim([limY[0], limY[1]]) 
    plt.savefig("./graficos/"+title+".png")
    plt.close()

# Plotador Genérico para a interpolação do dado passado
def plot_interpolation(path_data_1, path_data_2, title, lgdX, lgdY,  lim_inf_dados1, lim_sup_dados1, limX=None, limY=None):
    dados1 = get_dados(path_data_1); dados2 = get_dados(path_data_2)
    polinomio = np.polyfit(dados1, dados2, 3)
    vetDados1 = np.arange(lim_inf_dados1, lim_sup_dados1, 0.01)
    valsDados2 = np.polyval(polinomio, vetDados1)  
    plt.plot(vetDados1, valsDados2)
    plt.title(title, fontdict=font_title); plt.xlabel(lgdX, fontdict=font_label); plt.ylabel(lgdY, fontdict=font_label)
    plt.grid()
    if limX != None:
        plt.xlim([limX[0], limX[1]])
    if limY != None:
        plt.ylim([limY[0], limY[1]]) 
    plt.savefig("./graficos/"+title+"POLI.png")
    plt.close()

# Plotador de gráfico do ensaio do teste de atrito
def plot_friction_test(tempos, distsCru, distsPoli,title, batizaX, batizaY):
    plt.title(title)
    plt.xlabel(batizaX); plt.ylabel(batizaY)
    plt.plot(tempos, distsCru, label='Cru')
    plt.plot(tempos, distsPoli, label='Poli')
    plt.legend()
    plt.grid()
    plt.savefig("./graficos/"+title+".png")
        
# Plotador Genérico
def plot_graphic_with_direct_values(values_x_axis, values_y_axis, title, lgdX, lgdY, limX=None, limY=None):
    plt.plot(values_x_axis, values_y_axis)
    plt.title(title, fontdict=font_title); plt.xlabel(lgdX, fontdict=font_label); plt.ylabel(lgdY, fontdict=font_label)
    plt.grid()
    if limX != None:
        plt.xlim([limX[0], limX[1]])
    if limY != None:
        plt.ylim([limY[0], limY[1]]) 
    plt.savefig("./graficos/"+title+".png")
    plt.close()  

def plot_graphic_from_pickles_dicts(path_to_save_figura, data_1_path, data_2_path, title, lgdX, lgdY, limX=None, limY=None, path_to_reference_positions = None, video_duration = None, ids_wanted_markers = None):
    
    data_1 = load_pickle_data(data_1_path)
    data_2 = load_pickle_data(data_2_path)
    
    for key in ids_wanted_markers:
        plt.plot(data_1[key][0:len(data_2[key])], data_2[key], label="Id_"+str(key))
    # Se passar as disntâncias de referência para cada marcador
    if path_to_reference_positions is not None:
        with open(path_to_reference_positions, 'rb') as file3:
            reference_distances = pickle.load(file3)
            file3.close()
        for key3 in list(reference_distances.keys()):
            tempos_video = np.arange(0, video_duration+1, 1)
            distancia_referencia = [reference_distances[key3] for i in range(len(tempos_video))]
            plt.plot(tempos_video, distancia_referencia, label="Pos_Ref_Id_"+str(key3))
         
    plt.title(title, fontdict=font_title)
    plt.xlabel(lgdX, fontdict=font_label)
    plt.ylabel(lgdY, fontdict=font_label)
    plt.grid()
    plt.legend()    
    if limX != None:
        plt.xlim([limX[0], limX[1]])
    if limY != None:
        plt.ylim([limY[0], limY[1]])
    plt.savefig(path_to_save_figura)

with open("./dados_extraidos/Teste_Arthur_2x_take_8/markers_z_positions.pkl", "rb") as file1, open("./dados_extraidos/Teste_Arthur_2x_take_8/times_to_each_marker.pkl", "rb") as file2:
        marker_z_postions = pickle.load(file1)
        tempos = pickle.load(file2)
        file1.close()
        file2.close()
#calc_speed_in_Z_axis("./dados_extraidos/Teste_Arthur_2x_take_8/", "speed_markers.pkl", marker_z_postions, tempos, [0])
#clean_data("./dados_extraidos/Teste_Arthur_2x_take_8/", "cleaned_speed", "./dados_extraidos/Teste_Arthur_2x_take_8/speed_markers.pkl", [0])
plot_graphic_from_pickles_dicts("./dados_extraidos/Teste_Arthur_2x_take_8/Velocidade_em_Z_x_Tempo_TRATADO.png", "./dados_extraidos/Teste_Arthur_2x_take_8/times_to_each_marker.pkl", "./dados_extraidos/Teste_Arthur_2x_take_8/cleaned_speed.pkl",  "Velocidade em Z Tratada do Marcador x Tempo", "Tempo (s)", "Velocidade (m/s)",video_duration=20, ids_wanted_markers=[0])
    
            
    