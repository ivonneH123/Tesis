import matplotlib.pyplot as plt
import json

ruta_figs='D:/Ivonne/Documents/github/tesis/Tesis/solucion/plots'
ruta_json='D:/Ivonne/Documents/github/tesis/Tesis/solucion'

carpetas_json={'area_1_2':{'capacidad_20':'sol_area_1_2_1amb__cap20','capacidad_50':'sol_area_1_2_3amb__cap50','capacidad_70':'sol_area_1_2_4amb__cap70'},
               'area_3':{'capacidad_20':'sol_area_3_2amb__cap20','capacidad_50':'sol_area_3_4amb__cap50','capacidad_70':'sol_area_3_5amb__cap70'},
               'area_4':{'capacidad_20':'sol_area_4_2amb__cap20','capacidad_50':'sol_area_4_3amb__cap50','capacidad_70':'sol_area_4_6amb__cap70'},
               'area_5a_5b':{'capacidad_20':'sol_area_5a_5b_2amb__cap20','capacidad_50':'sol_area_5a_5b_6amb__cap50','capacidad_70':'sol_area_5a_5b_9amb__cap70'},
               'area_5c_5d':{'capacidad_20':'sol_area_5c_5d_4amb__cap20','capacidad_50':'sol_area_5c_5d_6amb__cap50','capacidad_70':'sol_area_5c_5d_9amb__cap70'},
               'area_6a_6b':{'capacidad_20':'sol_area_6a_6b_1amb__cap20','capacidad_50':'sol_area_6a_6b_4amb__cap50','capacidad_70':'sol_area_6a_6b_5amb__cap70'}}
areas=['area_1_2','area_3','area_4','area_5a_5b','area_5c_5d','area_6a_6b']
capacidades=['capacidad_20','capacidad_50','capacidad_70']

for area in range(len(areas)):
    for cap in range(len(capacidades)):
        file_json=ruta_json+'/'+areas[area]+'/'+capacidades[cap]+'/'+carpetas_json[areas[area]][capacidades[cap]]+'.txt'

        with open(file_json) as json_file:
            data = json.load(json_file)
        g=data['g']
        if cap==0:
            plt.figure(figsize=(15,3))
            plt.subplots_adjust(wspace = 0.6,hspace=0.5)
        plt.subplot(1,3,cap+1)
        plt.plot(g['i'],g['f(s)'])
        plt.xlabel('i')
        plt.ylabel('f(s)')
        plt.title(areas[area]+' y '+capacidades[cap])
        plt.savefig(ruta_figs+'/'+areas[area]+'.jpg')
        
        if cap==2:
            plt.clf()