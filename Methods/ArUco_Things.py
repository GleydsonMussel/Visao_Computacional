import cv2
import pickle

def generate_detector_params(caminho_pasta_output):
    
    arucoParams = cv2.aruco.DetectorParameters()

    # minimun standard deviation in pixels values during the decodification step to apply Otsu thresholding (otherwise, all the bits are set to 0 or 1 depending on mean higher than 128 or not)
    arucoParams.minOtsuStdDev = 7
    
    # DETECÇÃO
    
    arucoParams.adaptiveThreshWinSizeMin = 3                            # Padrão = 5  (pixels), Mínimo = 3 pixels
    arucoParams.adaptiveThreshWinSizeMax = 120                           # Padrão = 23 (pixels)
    arucoParams.adaptiveThreshWinSizeStep = 1                           # Padrão = 10 (pixels)
    
    # valores de 7 a 13 fazem alguns marcadores serem detectados e outros não! Valores >= 11 melhoram a qualidade da forma
    arucoParams.adaptiveThreshConstant = 1.5                           # Padrão = 7  
    arucoParams.minDistanceToBorder = 3                                 # Padrão = x (pixels)

    # Minimum distance between any pair of corners in the same marker
    arucoParams.minCornerDistanceRate = 0.001                           # Padrão = x (%)

    # This parameter indicates the width of the marker border. It is relative to the size of each bit. So, a value of 2 indicates the border has the width of two internal bits.
    arucoParams.markerBorderBits = 1                                   # Padrão = x ()
    
    arucoParams.minMarkerPerimeterRate = 0.01                           # Padrão = 0.03 (%) 
    arucoParams.maxMarkerPerimeterRate = 4.0                            # Padrão = 4.0 (%)
    
    # This parameter determines the number of pixels (per cell) in the obtained image after removing perspective distortion (including the border)
    arucoParams.perspectiveRemovePixelPerCell = 4                       # Padrão = 4 pixels
    
    # width of the margin of pixels on each cell not considered for the determination of the cell bit
    arucoParams.perspectiveRemoveIgnoredMarginPerCell = 0.15            # Padrão = 0.13 (%)
    arucoParams.maxErroneousBitsInBorderRate = 0.3                      # Padrão = 0.35 (%) 
    arucoParams.errorCorrectionRate = 1.0                            # Padrão = 0.6 (%)   

    # REFINAMENTO DO DESENHO DO ARUCO
    arucoParams.polygonalApproxAccuracyRate = 0.017                     # Padrão = 0.03 (pixels)
    arucoParams.cornerRefinementMethod = cv2.aruco.CORNER_REFINE_SUBPIX
    arucoParams.cornerRefinementWinSize =  20                           # Padrão = 5 pixels
    arucoParams.cornerRefinementMaxIterations = 2000000                      # Padrão = 30 iterações
    arucoParams.cornerRefinementMinAccuracy = 0.001                     # Padrão = 0.01 pixels
    
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