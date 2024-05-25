import cv2
import pickle

def generate_detector_params(caminho_pasta_output):
    
    arucoParams = cv2.aruco.DetectorParameters()
    # DETECÇÃO
    arucoParams.adaptiveThreshWinSizeMin = 3                            # Padrão = 5  (pixels), Mínimo = 3 pixels
    arucoParams.adaptiveThreshWinSizeMax = 60                           # Padrão = 23 (pixels)
    arucoParams.adaptiveThreshWinSizeStep = 1                           # Padrão = 10 (pixels)
    arucoParams.adaptiveThreshConstant = 8.5                              # Padrão = 7  
    arucoParams.minMarkerPerimeterRate = 0.01                           # Padrão = 0.03 (%) 
    arucoParams.maxMarkerPerimeterRate = 4.0                            # Padrão = 4.0 (%)
    arucoParams.perspectiveRemovePixelPerCell = 6                       # Padrão = 4 pixels
    arucoParams.perspectiveRemoveIgnoredMarginPerCell = 0.11            # Padrão = 0.13 (%)
    arucoParams.maxErroneousBitsInBorderRate = 0.31                     # Padrão = 0.35 (%) 
    arucoParams.errorCorrectionRate = 0.51                               # Padrão = 0.6 (%)   

    # REFINAMENTO DO DESENHO DO ARUCO
    arucoParams.polygonalApproxAccuracyRate = 0.020                     # Padrão = 0.03 (pixels)
    arucoParams.cornerRefinementMethod = cv2.aruco.CORNER_REFINE_SUBPIX
    arucoParams.cornerRefinementWinSize =  14                           # Padrão = 5 pixels
    arucoParams.cornerRefinementMaxIterations = 50                      # Padrão = 30 iterações
    arucoParams.cornerRefinementMinAccuracy = 0.005                     # Padrão = 0.01 pixels
    
    arucoParamsDict = {
        'adaptiveThreshWinSizeMin': arucoParams.adaptiveThreshWinSizeMin,
        'adaptiveThreshWinSizeMax': arucoParams.adaptiveThreshWinSizeMax,
        'adaptiveThreshWinSizeStep': arucoParams.adaptiveThreshWinSizeStep,
        'adaptiveThreshConstant': arucoParams.adaptiveThreshConstant,
        'minMarkerPerimeterRate': arucoParams.minMarkerPerimeterRate,
        'maxMarkerPerimeterRate': arucoParams.maxMarkerPerimeterRate,
        'perspectiveRemovePixelPerCell': arucoParams.perspectiveRemovePixelPerCell,
        'perspectiveRemoveIgnoredMarginPerCell': arucoParams.perspectiveRemoveIgnoredMarginPerCell,
        'maxErroneousBitsInBorderRate': arucoParams.maxErroneousBitsInBorderRate,
        'errorCorrectionRate': arucoParams.errorCorrectionRate,
        'polygonalApproxAccuracyRate': arucoParams.polygonalApproxAccuracyRate,
        'cornerRefinementMethod': arucoParams.cornerRefinementMethod,
        'cornerRefinementWinSize': arucoParams.cornerRefinementWinSize,
        'cornerRefinementMaxIterations': arucoParams.cornerRefinementMaxIterations,
        'cornerRefinementMinAccuracy': arucoParams.cornerRefinementMinAccuracy
    }
    
    # Salvando os parâmetros usando pickle
    with open(caminho_pasta_output+"arucoParams.pkl", 'wb') as arquivo:
        pickle.dump(arucoParamsDict, arquivo)
        arquivo.close()
    
        
    return arucoParams