import os
import pickle
import cv2
import glob
import shutil

class Manipulate_Files:
    
    # Cria pastas necessárias para o funcionamento do código
    @staticmethod
    def create_folders():
        if not os.path.exists("./frames"):
            os.mkdir("./frames/")
        if not os.path.exists("./logs"):
            os.mkdir("./logs")
        if not os.path.exists("./graficos"):
            os.mkdir("./graficos")
        if not os.path.exists("./Calibration/Res_Calib/"):
            os.mkdir("./Calibration/Res_Calib/")
        if not os.path.exists("./Calibration/Samples/"):
            os.mkdir("./Calibration/Samples/")
    
    @staticmethod
    def create_folder(path_to_folder):
        if not os.path.exists(path_to_folder):
            os.mkdir(path_to_folder)
            return path_to_folder+"/"
        else:
            cont = 2
            while os.path.exists(path_to_folder+"_take_"+str(cont)):
                cont += 1
            os.mkdir(path_to_folder+"_take_"+str(cont))
            return path_to_folder+"_take_"+str(cont)+"/"
    
    @staticmethod
    def clean_folder(folder):
        for file in os.listdir(folder):
                os.remove(os.path.join(folder, file))
    @staticmethod            
    def save_data(dado, caminho):
        with open(caminho, 'a') as arquivo:
            arquivo.write(str(dado))
            arquivo.write('\n')
    @staticmethod    
    def clean_tracker_processing():
        dirs_to_clean = ['./frames', './logs/', './graficos/']
        [Manipulate_Files.clean_folder(dir) for dir in dirs_to_clean]
    
    @staticmethod          
    def clean_calibrations_processing():
        dirs_to_clean = ['./Calibration/Res_Calib/', './Calibration/Samples/']
        [Manipulate_Files.clean_folder(dir) for dir in dirs_to_clean]
   
    @staticmethod
    def save_as_pickle_data(data, destiny_folder, file_name):
        with open(destiny_folder+file_name, "wb") as arquivo:
            pickle.dump(data, arquivo)
            arquivo.close()
    
    @staticmethod         
    def load_pickle_data(path_to_data): 
        with open(path_to_data, 'rb') as arquivo:
            data = pickle.load(arquivo)
            arquivo.close()
        return data

    @staticmethod
    def load_arucoParams(path_to_file):
        
        arucoParamsDict = Manipulate_Files.load_pickle_data(path_to_file)
        
        arucoParams = cv2.aruco.DetectorParameters()
        arucoParams.adaptiveThreshWinSizeMin = arucoParamsDict['adaptiveThreshWinSizeMin']
        arucoParams.adaptiveThreshWinSizeMax = arucoParamsDict['adaptiveThreshWinSizeMax']
        arucoParams.adaptiveThreshWinSizeStep = arucoParamsDict['adaptiveThreshWinSizeStep']
        arucoParams.adaptiveThreshConstant = arucoParamsDict['adaptiveThreshConstant']
        arucoParams.minMarkerPerimeterRate = arucoParamsDict['minMarkerPerimeterRate']
        arucoParams.maxMarkerPerimeterRate = arucoParamsDict['maxMarkerPerimeterRate']
        arucoParams.perspectiveRemovePixelPerCell = arucoParamsDict['perspectiveRemovePixelPerCell']
        arucoParams.perspectiveRemoveIgnoredMarginPerCell = arucoParamsDict['perspectiveRemoveIgnoredMarginPerCell']
        arucoParams.maxErroneousBitsInBorderRate = arucoParamsDict['maxErroneousBitsInBorderRate']
        arucoParams.errorCorrectionRate = arucoParamsDict['errorCorrectionRate']
        arucoParams.polygonalApproxAccuracyRate = arucoParamsDict['polygonalApproxAccuracyRate']
        arucoParams.cornerRefinementMethod = arucoParamsDict['cornerRefinementMethod']
        arucoParams.cornerRefinementWinSize = arucoParamsDict['cornerRefinementWinSize']
        arucoParams.cornerRefinementMaxIterations = arucoParamsDict['cornerRefinementMaxIterations']
        arucoParams.cornerRefinementMinAccuracy = arucoParamsDict['cornerRefinementMinAccuracy']
        
        return arucoParams
    
    @staticmethod
    def organize_aruco_proccessing_output_folder(path_to_folder):
        
        caminho_arquivos_pickle = path_to_folder+"Arquivos_Pickle"
        caminho_arquivos_excel = path_to_folder+"Excel_Saga"
        caminho_arquivos_graficos = path_to_folder+"Graficos"
        caminho_arquivos_txt = path_to_folder+"Textos"
        
        arquivo_pickle = glob.glob(path_to_folder+"*.pkl")
        arquivos_excel = glob.glob(path_to_folder+"*.xlsx")
        graficos = glob.glob(path_to_folder+"*.png")
        arquivos_txt = glob.glob(path_to_folder+"*.txt")
        
        if not os.path.exists(caminho_arquivos_pickle) and len(arquivo_pickle)>0:
            os.mkdir(caminho_arquivos_pickle)
            [shutil.move(local_atual, caminho_arquivos_pickle) for local_atual in arquivo_pickle]
        
        if not os.path.exists(caminho_arquivos_excel) and len(arquivos_excel)>0:
            os.mkdir(caminho_arquivos_excel)
            [shutil.move(local_atual, caminho_arquivos_excel) for local_atual in arquivos_excel]
        
        if not os.path.exists(caminho_arquivos_graficos) and len(graficos)>0:
            os.mkdir(caminho_arquivos_graficos)
            [shutil.move(local_atual, caminho_arquivos_graficos) for local_atual in graficos]
        
        if not os.path.exists(caminho_arquivos_txt) and len(arquivos_txt)>0:
            os.mkdir(caminho_arquivos_txt) 
            [shutil.move(local_atual, caminho_arquivos_txt) for local_atual in arquivos_txt]

        print("\nSaturday Night is a Good Night for Fighting\n")

    

