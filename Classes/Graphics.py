import matplotlib.pyplot as plt
import numpy as np
import pickle
import sys
sys.path.append('./Classes')
from Manipulate_Files import Manipulate_Files

# Formatação das fontes
font_title={"fontsize":14, "fontweight": 'bold', "fontname":'Times New Roman',}
font_label={"fontsize":12, "fontweight":'bold', 'fontname':'Times New Roman',}
font_lgd={"size":9, "weight":'normal', 'family':'Times New Roman',}

class Graphics:
    
    # Importador Genérico de Dados
    @staticmethod
    def get_data(caminho_dado):
        with open(caminho_dado, 'r') as arquivo:
            dados = arquivo.readlines()
            dados = [float(dado) for dado in dados]
            arquivo.close()
        return dados 
        
    # Plotador Genérico
    @staticmethod
    def plot_graphic(path_data_1, path_data_2, title, lgdX, lgdY, limX=None, limY=None, pasta_output=""):
        dado1= Graphics.get_data(path_data_1); dado2 = Graphics.get_data(path_data_2)
        plt.plot(dado1, dado2)
        plt.title(title, fontdict=font_title); plt.xlabel(lgdX, fontdict=font_label); plt.ylabel(lgdY, fontdict=font_label)
        plt.grid()
        if limX != None:
            plt.xlim([limX[0], limX[1]])
        if limY != None:
            plt.ylim([limY[0], limY[1]]) 
        plt.savefig(pasta_output+title+".png")
        plt.close()

    # Plotador Genérico para a interpolação do dado passado
    @staticmethod
    def plot_interpolation(path_data_1, path_data_2, title, lgdX, lgdY,  lim_inf_dados1, lim_sup_dados1, limX=None, limY=None):
        dados1 = Graphics.get_data(path_data_1); dados2 = Graphics.get_data(path_data_2)
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
    @staticmethod
    def plot_friction_test(tempos, distsCru, distsPoli,title, batizaX, batizaY):
        plt.title(title)
        plt.xlabel(batizaX); plt.ylabel(batizaY)
        plt.plot(tempos, distsCru, label='Cru')
        plt.plot(tempos, distsPoli, label='Poli')
        plt.legend()
        plt.grid()
        plt.savefig("./graficos/"+title+".png")
            
    # Plotador Genérico
    @staticmethod
    def plot_graphic_with_direct_values(path_to_save_figura, values_x_axis, values_y_axis, title, lgdX, lgdY, limX=None, limY=None):
        plt.plot(values_x_axis[0:len(values_y_axis)], values_y_axis)
        plt.title(title, fontdict=font_title); plt.xlabel(lgdX, fontdict=font_label); plt.ylabel(lgdY, fontdict=font_label)
        plt.grid()
        if limX != None:
            plt.xlim([limX[0], limX[1]])
        if limY != None:
            plt.ylim([limY[0], limY[1]]) 
        plt.savefig(path_to_save_figura)
        plt.close()  

    @staticmethod
    def plot_graphic_from_pickles_dicts(path_to_save_figura, data_1_path, data_2_path, title, lgdX, lgdY, limX=None, limY=None, path_to_reference_positions = None, video_duration = None, ids_wanted_markers = None):
        
        data_1 = Manipulate_Files.load_pickle_data(data_1_path)
        data_2 = Manipulate_Files.load_pickle_data(data_2_path)
        
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
        plt.close()

