from amb_pac import *
from LKS import LNS_metah
import matplotlib.pyplot as plt
import pandas as pd
import json
# import os
# os.chdir('D:\Ivonne\Documents\github\tesis\Tesis')
# parámetros de la heurística
area='1'
n_amb=9
L=10
I=20
nom_file='area_'+str(area)+'/'+'sol_area_'+str(area)+'_'+str(n_amb)+'amb.txt'

#importar los datasets
df_h_tot=pd.read_excel('datos/hosp_pulp_completo.xlsx')
df_h_tot['Area']=df_h_tot['Area'].astype(str)
df_h=df_h_tot.loc[df_h_tot['Area']==area]

df_pma_tot=pd.read_excel('datos/pma_completo.xlsx')
df_pma_tot['Area funcional']=df_pma_tot['Area funcional'].astype(str)
df_pma=df_pma_tot.loc[df_pma_tot['Area funcional']==area]
print(df_pma_tot['Area funcional'].value_counts()[0])
hospitales={h:cap_h for (h,cap_h) in zip(df_h['nom_pulp'],df_h['CAMAS'])}

# arreglo de 10 hospitales-ambulancias
h_arr=[h for h in list(hospitales.keys()) for i in range(n_amb)]
ambulancias=[ambulancia(num,hosp) for (num,hosp) in zip(range(n_amb*len(list(hospitales.keys()))),h_arr)]

#pacientes por cada PMA
# arreglo de pmas por cada paciente
pma_paciente={pma:cant_pac for (pma,cant_pac) in zip(df_pma['nom_pulp'],df_pma['heridos_hosp/pma'])}
pma_arr=[]
for pma in pma_paciente.keys():         # por cada cantidad de pacientes en todos los pma agregar el nombre del pma a la lista
    for cant_pac in range(pma_paciente[pma]):
        pma_arr.append(pma)

a=0
b=4
pacientes=[paciente(num,pma,a,b) for (num,pma) in zip(range(len(pma_arr)),pma_arr)]

with open('datos/distancias.json') as json_file:
    matrix_dist = json.load(json_file)


# probando Insertion_Heuristic
s,g=LNS_metah(10,5,ambulancias,matrix_dist,hospitales,pacientes)
data={}
data['g']=g
data['param']={'I':I,'L':L}
# guardar la solucion:
data['hospitales']=s['hospitales']
data['ambulancias']={}
for amb in s['ambulancias']:
    data['ambulancias'][str(amb.num)]={}
    data['ambulancias'][str(amb.num)]['hosp']=amb.hospital
    data['ambulancias'][str(amb.num)]['ruta']=amb.route
    data['ambulancias'][str(amb.num)]['tiempo_final']=amb.tiempo_final
data['pacientes']={}
for pac in s['pacientes']:
    data['pacientes'][str(pac.num)]={}
    data['pacientes'][str(pac.num)]['hosp']=pac.hosp
    data['pacientes'][str(pac.num)]['atendido']=pac.atendido
    data['pacientes'][str(pac.num)]['ambulancia']=pac.ambulancia
    data['pacientes'][str(pac.num)]['w']=pac.w


with open('solucion/'+nom_file, 'w') as outfile:
    json.dump(data, outfile)

plt.plot(g['i'],g['f(s)'])
plt.xlabel('i')
plt.ylabel('f(s)')
plt.title('valor de la funcion objetivo en cada iteracion')
plt.show()
# for i in range(len(s['ambulancias'])):
#     print('ambulancia nro: '+str(s['ambulancias'][i].num))
#     print('ambulancia hospital inicial: '+s['ambulancias'][i].hospital)
#     print('ambulancia ruta: '+str(s['ambulancias'][i].route))
#     print('_____________'*10)
# print('_____________'*20)

# for i in range(len(s['hospitales'])):
#     keys=list(s['hospitales'].keys())
#     print('hospital numero:'+keys[i])
#     print('capacidad restante de hospital:'+str(s['hospitales'][keys[i]]))
#     print('_____________'*10)
# print('_____________'*20)

# for i in range(len(s['pacientes'])):
#     print('paciente numero: '+str(s['pacientes'][i].num))
#     print('paciente estado: '+str(s['pacientes'][i].atendido))
#     print('hospital de atencion: '+s['pacientes'][i].hosp)
#     print('ambulancia del paciente: '+str(s['pacientes'][i].ambulancia))
#     print('tiempo de visita: '+str(s['pacientes'][i].w))
#     print('_____________'*10)