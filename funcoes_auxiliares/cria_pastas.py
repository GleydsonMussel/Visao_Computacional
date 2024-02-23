import os

def arruma_ambiente():
    if not os.path.exists("./frames"):
        os.mkdir("./frames/")
    if not os.path.exists("./logs"):
        os.mkdir("./logs")
    if not os.path.exists("./graficos"):
        os.mkdir("./graficos")