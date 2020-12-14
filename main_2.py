from amb_pac import *
from LKS import LNS_metah
import matplotlib.pyplot as plt
import pandas as pd
import json
import time
# import os
# os.chdir('D:\Ivonne\Documents\github\tesis\Tesis')
# parámetros de la heurística
#capacidades a evaluar: 70,50 y 20 %
areas=['6a','6b']
capacidad=20
n_amb=1
I=160
L=I/10
nom_file_1='area'
nom_file_2='/'+'sol_area_'
for area in areas:
    nom_file_1=nom_file_1+'_'+str(area)
    nom_file_2=nom_file_2+str(area)+'_'
# nom_file='area_'+str(areas[0])+'_'+str(areas[1])+'_'+str(areas[2])+'_'+str(areas[3])+'_'+str(areas[4])+'/'+'sol_area_'+str(areas[0])+'_'+str(areas[1])+'_'+str(areas[2])+'_'+str(areas[3])+'_'+str(areas[4])+'_'+str(n_amb)+'amb.txt'
nom_file_2=nom_file_2+str(n_amb)+'amb_'+'_cap'+str(capacidad)+'.txt'
nom_file=nom_file_1+'/capacidad_'+str(capacidad)+nom_file_2
print(nom_file)
#importar los datasets
df_h_tot=pd.read_excel('datos/hosp_pulp_completo.xlsx')
df_h_tot['Area']=df_h_tot['Area'].astype(str)

df_pma_tot=pd.read_excel('datos/pma_completo.xlsx')
df_pma_tot['Area funcional']=df_pma_tot['Area funcional'].astype(str)

condicion1=False
condicion2=False
for area in areas:
    condicion1=condicion1 | (df_h_tot['Area']==area)
    condicion2=condicion2 | (df_pma_tot['Area funcional']==area)
df_h=df_h_tot.loc[condicion1]
df_pma=df_pma_tot.loc[condicion2]  
# df_h=df_h_tot.loc[(df_h_tot['Area']==areas[0]) | (df_h_tot['Area']==areas[1]) | (df_h_tot['Area']==areas[2]) | (df_h_tot['Area']==areas[3]) | (df_h_tot['Area']==areas[4])]

# df_pma=df_pma_tot.loc[(df_pma_tot['Area funcional']==areas[0]) | (df_pma_tot['Area funcional']==areas[1]) | (df_pma_tot['Area funcional']==areas[2]) | (df_h_tot['Area']==areas[3]) | (df_h_tot['Area']==areas[4])]

hospitales={h:round(cap_h*capacidad/100) for (h,cap_h) in zip(df_h['nom_pulp'],df_h['CAMAS'])}

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



start_time=time.time()
s,g=LNS_metah(I,L,ambulancias,matrix_dist,hospitales,pacientes)
data={}
data['capacidad']=capacidad
data['tiempo_ejecucion']=time.time()-start_time
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
    data['pacientes'][str(pac.num)]['pma']=pac.pma
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