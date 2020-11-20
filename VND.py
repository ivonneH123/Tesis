
import random
def funcion_obj(s):
    try:
        return sum([ x.atendido for x in s['pacientes']])
    except:
        return 0
def sum_tiempo(s):
    return sum([a.tiempo_final for a in s['ambulancias']])
def verificar_tiempoLimite(s):
    # como todos los pacientes tienen el mismo tiempo límite:
    B=[p.b for p in s['pacientes'] ]
    condicion=[a.tiempo_final<B[0] for a in s['ambulancias']]
    resultado= True if sum(condicion)==len(s['ambulancias']) else False
    return resultado

# #debuggeo
# def debbug_pac_ruta(s):
#     rutas=[a.route for a in s['ambulancias']]
#     pac_in_ruta=[]
#     for ruta_pac in rutas:
#         pac_in_ruta=pac_in_ruta+[p for p in ruta_pac if isinstance(p,int)]
#     return pac_in_ruta


def VND(s,matrix_dist):
    f_s=sum_tiempo(s)
    s_optim=s.copy()
    f_Soptim=f_s
    lamb=[i_p_relocate, i_p_swap,e_p_swap, e_p_2opt,route_reasignment]
    i=0
    while i<len(lamb):
        s=lamb[i](s,matrix_dist)
        if (sum_tiempo(s)<f_Soptim and verificar_tiempoLimite(s)):
            s_optim=s
            f_Soptim=sum_tiempo(s)
            
            i=0
        else:
            i+=1
    return s_optim


def i_p_relocate(s,matrix_dist):
    # escoger ambulancia aleatoria
    index_amb_pac=[s['ambulancias'].index(a) for a in s['ambulancias'] if len(a.route)>3]
    index_amb=random.choice(index_amb_pac)
    ambulance=s['ambulancias'][index_amb]
    p=[ambulance.route.index(p) for p in s['ambulancias'][index_amb].route if isinstance(p,int)] # indices de pacientes en la ruta de la ambulancia
    pac_amb_index={str(p.num):s['pacientes'].index(p) for p in s['pacientes'] if p.num in ambulance.route} #indices de los pacientes en la lista de pacientes 
    num=[int(n) for n in pac_amb_index.keys()]

    #escoger paciente aleatorio
    index_pac=random.choice(p)
    # seleccionar paciente y el hospital al que se dirige
    num_pac=ambulance.route[index_pac]
    num_hosp=ambulance.route[index_pac+1]

    # extraer de la ruta de la ambulancia
    ambulance.route.pop(index_pac)
    ambulance.route.pop(index_pac)

    # indices de pacientes
    indices_p=[ambulance.route.index(p) for p in ambulance.route if isinstance(p,int)]

    #localizar en otro punto de la ruta
    
    nueva_loc=random.choice(indices_p)
    ambulance.route.insert(nueva_loc+2,num_pac)
    ambulance.route.insert(nueva_loc+3,num_hosp)
 
    ambulance.tiempo_final=ambulance.calc_tiempo_f(matrix_dist, s['pacientes'])#actualizar el tiempo final 
    
    # actualizar los tiempos de visita en los hospitales
    #posiciones de pacientes actualizados
    pos={str(p):ambulance.route.index(p) for p in ambulance.route if isinstance(p,int)}
    for i in range(len(pac_amb_index)):    
        s['pacientes'][pac_amb_index[str(num[i])]].w=ambulance.calc_tiempo(pos[str(num[i])],matrix_dist,s['pacientes'])
    
    # actualizar ambulancia
    s['ambulancias'][index_amb]=ambulance
    # if len(debbug_pac_ruta(s))>87:
    #     h=3
    return s

def i_p_swap(s,matrix_dist):
    # escoger una ruta e intercambiar dos pacientes
    index_amb_pac=[s['ambulancias'].index(a) for a in s['ambulancias'] if len(a.route)>3]
    index_amb=random.choice(index_amb_pac)
    ambulance=s['ambulancias'][index_amb]
    p=[ambulance.route.index(p) for p in s['ambulancias'][index_amb].route if isinstance(p,int)] # indices de pacientes en las rutas de las ambulancias
    pac_amb_index={str(p.num):s['pacientes'].index(p) for p in s['pacientes'] if p.num in ambulance.route} #indices de los pacientes en la lista de pacientes 
    num=[int(n) for n in pac_amb_index.keys()]

    index_pac1=random.choice(p)
    p2=p[:]
    p2.remove(index_pac1)

    #escoger otro paciente aleatoriamente
    index_pac2=random.choice(p2)
    # valores de paciente 1 (index_pac1)
    num_pac=ambulance.route[index_pac1]
    hosp=ambulance.route[index_pac1+1]
    # intercambiar los pacientes
    ambulance.route[index_pac1],ambulance.route[index_pac1+1]=ambulance.route[index_pac2],ambulance.route[index_pac2+1]
    ambulance.route[index_pac2],ambulance.route[index_pac2+1]=num_pac,hosp

    # actualizar los tiempos de llegada al paciente
    pos={str(p):ambulance.route.index(p) for p in ambulance.route if isinstance(p,int)}
    for i in range(len(pac_amb_index)):   
        s['pacientes'][pac_amb_index[str(num[i])]].w=ambulance.calc_tiempo(pos[str(num[i])],matrix_dist,s['pacientes'])
                
    s['ambulancias'][index_amb]=ambulance
    s['ambulancias'][index_amb].tiempo_final=s['ambulancias'][index_amb].calc_tiempo_f(matrix_dist,s['pacientes'])
    
    # if len(debbug_pac_ruta(s))>87:
    #     h=3
    return s

def e_p_swap(s,matrix_dist):
    index_ambulancias=[s['ambulancias'].index(a) for a in s['ambulancias'] if len(a.route)>3]#indice de ambulancias con pacientes intercambiables
    pac_index={str(p.num):s['pacientes'].index(p) for p in s['pacientes']} #indice de pacientes en dic

    index_amb1=random.choice(index_ambulancias)
    amb1=s['ambulancias'][index_amb1] #escoger la ambulancia 1
    index_2=index_ambulancias[:] # lista con ambulancias diferentes a la ambulancia 1
    index_2.remove(index_amb1)

    index_amb2=random.choice(index_2)
    amb2=s['ambulancias'][index_amb2] # escoger la ambulancia 2
    index_pac_amb1=[amb1.route.index(p) for p in amb1.route if isinstance(p,int)] # indice de pacientes en la ruta de la ambulancia 1
    index_pac_amb2=[amb2.route.index(p) for p in amb2.route if isinstance(p,int)] # indice de pacientes en la ruta de la ambulancia 2

    #rutas en blanco
    blank_route1=amb1.route[:]
    blank_route2=amb2.route[:]

    # paciente aleatorio de la ambulancia 1
    index_p1=random.choice(index_pac_amb1)
    index_p2=random.choice(index_pac_amb2)
        
    ruta_prueba1=blank_route1[:index_p1]+blank_route2[index_p2:index_p2+2]+blank_route1[index_p1+2:] #ruta con paciente cambiado en ambulancia 1
    ruta_prueba2=blank_route2[:index_p2]+blank_route1[index_p1:index_p1+2]+blank_route2[index_p2+2:] #ruta con paciente cambiado en ambulancia 2
    amb1.route=ruta_prueba1
    amb2.route=ruta_prueba2

    s['ambulancias'][index_amb2]=amb2 # guardar ambulancia 2
    s['ambulancias'][index_amb2].tiempo_final=s['ambulancias'][index_amb2].calc_tiempo_f(matrix_dist,s['pacientes'])
    s['ambulancias'][index_amb1]=amb1 # guardar ambulancia 1
    s['ambulancias'][index_amb1].tiempo_final=s['ambulancias'][index_amb1].calc_tiempo_f(matrix_dist,s['pacientes'])
    # actualizar los pacientes
    for index_amb in [index_amb1,index_amb2]:
        amb=s['ambulancias'][index_amb]
        for p_num in [p for p in amb.route if isinstance(p,int)]:
            s['pacientes'][pac_index[str(p_num)]].ambulancia=amb.num
            s['pacientes'][pac_index[str(p_num)]].w=amb.calc_tiempo(amb.route.index(p_num),matrix_dist,s['pacientes'])
    # if len(debbug_pac_ruta(s))>87:
    #     h=3
    return s

def e_p_2opt(s, matrix_dist):
    index_ambulancias=[s['ambulancias'].index(a) for a in s['ambulancias'] if len(a.route)>1]#indice de ambulancias
    pac_index={str(p.num):s['pacientes'].index(p) for p in s['pacientes']} #indice de pacientes en dic
    
    index_amb1=random.choice(index_ambulancias)
    amb1=s['ambulancias'][index_amb1] #escoger la ambulancia 1
    index_2=index_ambulancias[:] # lista con ambulancias diferentes a la ambulancia 1
    index_2.remove(index_amb1)

    index_amb2=random.choice(index_2)
    amb2=s['ambulancias'][index_amb2] # escoger la ambulancia 2
    index_pac_amb1=[amb1.route.index(p) for p in amb1.route if isinstance(p,int)] # indice de pacientes en la ruta de la ambulancia 1
    index_pac_amb2=[amb2.route.index(p) for p in amb2.route if isinstance(p,int)] # indice de pacientes en la ruta de la ambulancia 2

    #rutas en blanco
    blank_route1=amb1.route[:]
    blank_route2=amb2.route[:]

    index_p1=random.choice(index_pac_amb1)
    index_p2=random.choice(index_pac_amb2)
    
    ruta_prueba1=blank_route1[:index_p1]+blank_route2[index_p2:] #ruta con subruta cambiada desde el paciente p1 en ambulancia 1
    ruta_prueba2=blank_route2[:index_p2]+blank_route1[index_p1:] #ruta con subruta cambiada desde el paciente p2 en ambulancia 2
    amb1.route=ruta_prueba1
    amb2.route=ruta_prueba2

    s['ambulancias'][index_amb2]=amb2 # guardar ambulancia 2
    s['ambulancias'][index_amb2].tiempo_final=s['ambulancias'][index_amb2].calc_tiempo_f(matrix_dist,s['pacientes'])

    s['ambulancias'][index_amb1]=amb1 # guardar ambulancia 1
    s['ambulancias'][index_amb1].tiempo_final=s['ambulancias'][index_amb1].calc_tiempo_f(matrix_dist,s['pacientes'])
    # actualizar los pacientes
    for index_amb in [index_amb1,index_amb2]:
        s['ambulancias'][index_amb].tiempo_final=s['ambulancias'][index_amb].calc_tiempo_f(matrix_dist,s['pacientes'])
        amb=s['ambulancias'][index_amb]
        for p_num in [p for p in amb.route if isinstance(p,int)]:
            s['pacientes'][pac_index[str(p_num)]].ambulancia=amb.num
            s['pacientes'][pac_index[str(p_num)]].w=amb.calc_tiempo(amb.route.index(p_num),matrix_dist,s['pacientes'])                                               
    # if len(debbug_pac_ruta(s))>87:
    #     h=3
    return s

def route_reasignment(s,matrix_dist):
   index_amb=[s['ambulancias'].index(a) for a in s['ambulancias'] ]
   pac_index={str(p.num):s['pacientes'].index(p) for p in s['pacientes']} #indice de pacientes en dic
   
   index_amb1=random.choice(index_amb)
   amb1=s['ambulancias'][index_amb1]
   #lista de indices de ambulancias sin la ambulancia 1
   index_2=index_amb[:]
   index_2.remove(index_amb1)

   index_amb2=random.choice(index_2)
   amb2=s['ambulancias'][index_amb2]
   # intercambiar rutas
   route1_prueba=[amb1.route[0]]+amb2.route[1:]
   route2_prueba=[amb2.route[0]]+amb1.route[1:]
   # asignar rutas a las ambulancias
   amb1.route=route1_prueba[:]
   amb2.route=route2_prueba[:]
   #guardar rutas en solucion
   s['ambulancias'][index_amb1].route=route1_prueba
   s['ambulancias'][index_amb2].route=route2_prueba
    # actualizar las rutas de los pacientes
   for i_amb in [index_amb1,index_amb2]:
       s['ambulancias'][i_amb].tiempo_final=s['ambulancias'][i_amb].calc_tiempo_f(matrix_dist,s['pacientes'])
       amb=s['ambulancias'][i_amb]
       for p_num in [p for p in amb.route if isinstance(p,int)]:
           s['pacientes'][pac_index[str(p_num)]].ambulancia=amb.num
           s['pacientes'][pac_index[str(p_num)]].w=amb.calc_tiempo(amb.route.index(p_num),matrix_dist,s['pacientes'])                                               
#    if len(debbug_pac_ruta(s))>87:
#         h=3
   return s