import pandas as pd
from scipy import stats
from scipy.signal import butter, filtfilt
import numpy as np
from Manipulate_Files import Manipulate_Files

class Data_Cleaner:
    
    @staticmethod
    def remove_outliers(data_frame, key):

        z_scores = np.abs(stats.zscore(data_frame[key]))
            
        # Baseado na distribuição normal:
        # 68.0% dos dados estão dentro de 1 desvio padrão da média
        # 95.0% dos dados estão dentro de 2 desvios padrão da média
        # 99.7% dos dados estão dentro de 3 desvios padrão da média.
        # limite então dita a quantos desvios padrões da média o dado ainda é considerado daod e não ruído
        limite = 2
            
        data_frame.loc[z_scores >= limite, key] = np.nan
        # Remove todas as linhas que estão com NaN, isso afeta todas as colunas
        data_frame = data_frame.dropna()
            
        return data_frame

    @staticmethod
    def aply_rolling_mean(data_frame):
        # Aplicar média móvel com window=3 para suavização
        data_frame_suavizado = data_frame.rolling(window=3, min_periods=1).mean()  # min_periods=1 para incluir todas as linhas
        data_frame_suavizado = data_frame_suavizado.dropna()
        
        return data_frame_suavizado 
    
    @staticmethod    
    def clean_data(destiny_folder, file_name, path_to_picke_dict, keys_to_clean):
        pickle_dict_import = Manipulate_Files.load_pickle_data(path_to_picke_dict)
        pickle_dict_export = {}
        for key in keys_to_clean:
            data_to_clean = pd.DataFrame({key:pickle_dict_import[key]})
            data_to_clean = Data_Cleaner.remove_outliers(data_to_clean, key)
            data_to_clean = Data_Cleaner.aply_rolling_mean(data_to_clean)
            data_to_clean.to_excel(destiny_folder+file_name+".xlsx", index=False)
            for colum in data_to_clean.columns:
                pickle_dict_export[colum] = data_to_clean[colum].to_list()
            
        Manipulate_Files.save_as_pickle_data(pickle_dict_export, destiny_folder, file_name+".pkl")
        
        print("Go Go Maniac !")
    

    
    