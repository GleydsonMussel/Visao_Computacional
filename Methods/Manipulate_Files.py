import os

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
      

        