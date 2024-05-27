import numpy as np
import matplotlib.pyplot as plt

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

marker_z_positions_1m_55cm = np.load("./Quick_Codigos/Marker_z_PositionsTeste_ArUco_Casa_1m_55cm.npy")
marker_z_positions_2m_20cm = np.load("./Quick_Codigos/Marker_z_PositionsTeste_ArUco_Casa_2m_20cm.npy")
marker_z_positions_2m_97cm = np.load("./Quick_Codigos/Marker_z_PositionsTeste_ArUco_Casa_2m_97cm.npy")

marker_z_positions_1m_55cm_ERRO = [(dist - 1.55)/1.55 for dist in marker_z_positions_1m_55cm]
marker_z_positions_2m_20cm_ERRO = [(dist - 2.20)/2.20 for dist in marker_z_positions_2m_20cm]
marker_z_positions_2m_97cm_ERRO = [(dist - 2.97)/2.97 for dist in marker_z_positions_2m_97cm]

coletas_1m_55cm = np.arange(1,len(marker_z_positions_1m_55cm)+1, 1)
coletas_2m_20cm = np.arange(1,len(marker_z_positions_2m_20cm)+1, 1)
coletas_2m_97cm = np.arange(1,len(marker_z_positions_2m_97cm)+1, 1)

plt.title("Erro Relativo para Testes")
plt.xlabel("Coletas"); plt.ylabel("Erro Relativo")
plt.plot(coletas_1m_55cm[0:300], marker_z_positions_1m_55cm_ERRO[0:300], label='Ref: 1.55m')
plt.plot(coletas_2m_20cm[0:300], marker_z_positions_2m_20cm_ERRO[0:300], label='Ref: 2.20m')
plt.plot(coletas_2m_97cm[0:300], marker_z_positions_2m_97cm_ERRO[0:300], label='Ref: 2.97m')
plt.legend()
plt.grid()
plt.savefig("./Quick_Codigos/Erros_Relativos_Ensaios.png")