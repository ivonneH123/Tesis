from amb_pac import *
from LKS import *

hospitales={'HOSP_1':30,'HOSP_2':30}

h_arr=[h for h in list(hospitales.keys()) for i in range(3)]
ambulancias=[ambulancia(num,hosp) for (num,hosp) in zip(range(3*len(list(hospitales.keys()))),h_arr)]

pma_1=['PMA_1','PMA_2']
a=0
b=4
pma_arr=[pma for pma in pma_1 for i in range(3)]

pacientes=[paciente(num,pma,a,b) for (num,pma) in zip(range(len(pma_1)*3),pma_arr) ]
L=10
I=20
matrix_dist={'PMA_1':{'HOSP_1':10, 'HOSP_2':10,'PMA_2':10},
            'PMA_2':{'HOSP_1':10, 'HOSP_2':10,'PMA_1':10},
            'HOSP_1':{'PMA_1':10, 'HOSP_2':10,'PMA_2':10},
            'HOSP_2':{'PMA_1':10, 'HOSP_1':10,'PMA_2':10}}

# probando Insertion_Heuristic
s=Constructive_heuristic(ambulancias, matrix_dist, hospitales, pacientes,1)

s1=Rem_all(s)

for i in range(len(s['ambulancias'])):
    print('ambulancia nro: '+str(s['ambulancias'][i].num))
    print('ambulancia hospital inicial: '+s['ambulancias'][i].hospital)
    print('ambulancia ruta: '+str(s['ambulancias'][i].route))
    print('_____________'*10)
print('_____________'*20)

for i in range(len(s['hospitales'])):
    keys=list(s['hospitales'].keys())
    print('hospital numero:'+keys[i])
    print('capacidad restante de hospital:'+str(s['hospitales'][keys[i]]))
    print('_____________'*10)
print('_____________'*20)

for i in range(len(s['pacientes'])):
    print('paciente numero: '+str(s['pacientes'][i].num))
    print('paciente estado: '+str(s['pacientes'][i].atendido))
    print('hospital de atencion: '+s['pacientes'][i].hosp)
    print('ambulancia del paciente: '+str(s['pacientes'][i].ambulancia))
    print('tiempo de visita: '+str(s['pacientes'][i].w))
    print('_____________'*10)