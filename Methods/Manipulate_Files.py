import os
import pickle
import cv2

# Cria pastas necessárias para o funcionamento do código
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

def clean_folder(folder):
    for file in os.listdir(folder):
            os.remove(os.path.join(folder, file))
            
def save_data(dado, caminho):
    with open(caminho, 'a') as arquivo:
        arquivo.write(str(dado))
        arquivo.write('\n')
    
def clean_tracker_processing():
    dirs_to_clean = ['./frames', './logs/', './graficos/']
    [clean_folder(dir) for dir in dirs_to_clean]
            
def clean_calibrations_processing():
    dirs_to_clean = ['./Calibration/Res_Calib/', './Calibration/Samples/']
    [clean_folder(dir) for dir in dirs_to_clean]
      
def create_folder(path_to_folder):
    if not os.path.exists(path_to_folder):
        os.mkdir(path_to_folder)
        return path_to_folder
    else:
        cont = 2
        while os.path.exists(path_to_folder+"_take_"+str(cont)):
            cont += 1
        os.mkdir(path_to_folder+"_take_"+str(cont))
        return path_to_folder+"_take_"+str(cont)+"/"

def load_arucoParams(path_to_file):
    
    with open(path_to_file, 'rb') as arquivo:
        arucoParamsDict = pickle.load(arquivo)
        arquivo.close()
    
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