import random
from amb_pac import hosp_cercano
from VND import VND, funcion_obj
import tqdm

def LNS_metah(I,L,ambulancias,matrix_dist,hospitales,pacientes):
    s_optim={} # inicializar soluciones en vacio
    s={}

    # f_optim=0 # funcion objetivo de la solución óptima hasta el momento
    # f_actual=0 # funcion objetivo de la solución actual
    
    i=0 #contador de iteraciones
    l=0 #contador de iteraciones sin mejoras
    g={}#datos para los graficos
    g['i']=[]
    g['f(s)']=[]
    pbar=tqdm.tqdm(total=I, initial=1)
    # #debbuging
    # d=[]
    while (i<I):
        if (i == 0 or l == L):
            rand = random.randint(0,1)
            alpha = random.randint(2,5)
            if rand ==0:
                s=Insertion_Heuristic(ambulancias,matrix_dist,hospitales,pacientes, alpha)
            elif rand==1:
                s=Constructive_heuristic(ambulancias,matrix_dist,hospitales,pacientes, alpha)
            l=0
        else:
            rand=random.randint(0,2)
            # #debbuging
            # d.append(rand)
            if rand==0:
                s=Rem2(s,matrix_dist)
            elif rand==1:
                s=Rem_rand(s,matrix_dist)
            else:
                s=Rem_all(s,matrix_dist)

            s=Constructive_heuristic(s['ambulancias'],matrix_dist, s['hospitales'],s['pacientes'],1) # reparar las rutas

        
        s=VND(s, matrix_dist)
        s=Constructive_heuristic(s['ambulancias'],matrix_dist, s['hospitales'],s['pacientes'],1) #añadir más pacientes si el tiempo se redujo
        # if len(debbug_pac_ruta(s))>87:
        #         h=3

        if funcion_obj(s) > funcion_obj(s_optim):
            s_optim=s
            l=0
        else:
            l+=1
        g['i'].append(i)
        g['f(s)'].append(funcion_obj(s_optim))
        i+=1
        pbar.update(1)
    pbar.close()
    return s,g

# def debbug_pac_ruta(s):
#     rutas=[a.route for a in s['ambulancias']]
#     pac_in_ruta=[]
#     for ruta_pac in rutas:
#         pac_in_ruta=pac_in_ruta+[p for p in ruta_pac if isinstance(p,int)]
#     return pac_in_ruta




"""
ambulancias= lista con objetos de clase ambulancia
matrix_dist= diccionario con las distancias
hospitales= diccionario con key= hospitales y values= capacidad de camas
pacientes= lista con objetos de clase pacientes
alpha= número aleatorio entre 2 y 5
"""
def Insertion_Heuristic(ambulancias, matrix_dist, hospitales, pacientes, alpha):
    a=ambulancias[random.randint(0,len(ambulancias)-1)]
    ambulancias_no_usadas=[a.num for a in ambulancias]
    h=a.hospital
    Chsum=sum(hospitales.values()) # suma de las capacidades en los hospitales
    B=max([x.b for x in pacientes]) # ventana de tiempo tardío para la atención de los pacientes
    t=a.tiempo_final
    pacientes_no_atendidos=[p for p in pacientes if p.atendido==0]

    while ((Chsum>0 and t<B )and len(pacientes_no_atendidos)>0 and len(ambulancias_no_usadas)>0):
        index_a=ambulancias.index(a)
        index_p_no=random.randint(0,len(pacientes_no_atendidos)-1)
        j=pacientes_no_atendidos[index_p_no] # paciente seleccionado al azar
        index_p=pacientes.index(j)
        C=a.posiciones_baratas(j.pma, matrix_dist,pacientes, alpha) # las posiciones baratas solo evaluan hospitales
        # seleccionar una posición de inserción
        i=random.randint(0,len(C)-1)
        # seleccionar hospital
        hosp=hosp_cercano(j.pma, hospitales, matrix_dist)[0]
        # agregar j en la posición i y añadir el hospital a la ruta y actualizar el tiempo final en la ambulancia
        j.atender_paciente(a,hosp, int(C[i]), matrix_dist,pacientes)
        # quitar el numero de paciente de la lista de pacientes no atendidos
        pacientes_no_atendidos.pop(index_p_no)
        # actualizar pacientes
        pacientes[index_p]=j
        # actualizar hospital
        hospitales[hosp]=hospitales[hosp]-1
        # actualizar ambulancias
        ambulancias[index_a]=a
        # actualizar la suma de capacidades
        Chsum=sum(hospitales.values())
        # actualizar el tiempo final de la ambulancia en la heuristica
        t=a.tiempo_final

        if t>B and len(ambulancias_no_usadas)>1:
            ambulancias_no_usadas.remove(a.num) #añadimos a la lista de ambulancias usadas
            a_new_num=ambulancias_no_usadas[random.randint(0,len(ambulancias_no_usadas)-1)]
            a_nueva=[a for a in ambulancias if a.num==a_new_num][0] # seleccionar nueva ambulancia
            a=a_nueva
            # actualizar el tiempo final
            t=a.tiempo_final

    s={"ambulancias":ambulancias,"hospitales":hospitales,"pacientes":pacientes}
    return s


def Constructive_heuristic (ambulancias, matrix_dist, hospitales, pacientes, alpha):
    Chsum=sum(hospitales.values()) # suma de las capacidades en los hospitales
    B=max([x.b for x in pacientes]) # ventana de tiempo tardío para la atención de los pacientes
    T =[a.tiempo_final for a in ambulancias]
    condicion_tiempo=sum([x<B for x in T])
    pacientes_no_atendidos=[p for p in pacientes if p.atendido==0]

    while (Chsum>0 and condicion_tiempo>0 and len(pacientes_no_atendidos)>0):
        index_a=T.index(min(T))
        a=ambulancias[index_a]
        Cp=a.pac_cercanos(matrix_dist,[p for p in pacientes if p in pacientes_no_atendidos],alpha) #lista de pacientes mas cercanos
        i=Cp[random.randint(0,alpha-1)] # paciente aleatorio
        index_P_na=pacientes_no_atendidos.index(i) #indice del paciente en la lista de no atendido
        index_p=pacientes.index(i) # indice del paciente en la lista de pacientes
        Ch= hosp_cercano(i.pma,hospitales,matrix_dist,alpha) # lista de hospitales alpha más cercanos
        hosp= Ch[random.randint(0,(alpha if alpha<len(Ch) else len(Ch))-1 )]  #hospital aleatorio
        i.atender_paciente(a, hosp, len(a.route), matrix_dist,pacientes)
        # actualizar lista de pacientes no atendidos
        pacientes_no_atendidos.pop(index_P_na)
        # actualizar lista de pacientes
        pacientes[index_p]=i
        #actualizar lista de ambulancias
        ambulancias[index_a]=a
        #actualizar capacidad de hospitales
        hospitales[hosp]=hospitales[hosp]-1

        # actualizar las variables de tiempo final
        T =[a.tiempo_final for a in ambulancias]
        condicion_tiempo=sum([x<B for x in T])
        Chsum=sum(hospitales.values())
        
        #escoger otra ambulancia con el menor tiempo final
        index_a=T.index(min(T))
        a_nueva=ambulancias[index_a]
        a=a_nueva
    s={"ambulancias":ambulancias,"hospitales":hospitales,"pacientes":pacientes}
    # if len(debbug_pac_ruta(s))>87:
    #     h=3
    return s


def Rem2(s,matrix_dist):
    # removemos 2 rutas de las ambulancias con mayor tiempo final
    i=0 
    while i<2:
        i+=1
        T=[a.tiempo_final for a in s['ambulancias']]
        Tmax=max(T)
        index_a=T.index(Tmax)
        a=s['ambulancias'][index_a]
        # removemos el último paciente de la ruta  
        s['ambulancias'][index_a],s['hospitales'],s['pacientes']=remove_route(a,matrix_dist,s['hospitales'], s['pacientes'])
    # if len(debbug_pac_ruta(s))>87:
    #     h=3
        # s['ambulancias'][index_a]=a
        # s['hospitales']=hosp
        # s['pacientes']=pac
        
    
    return s

def Rem_rand(s,matrix_dist):
    # seleccionar la ambulancia con mayor tiempo
    T=[a.tiempo_final for a in s['ambulancias']]
    Tmax=max(T)
    index_a=T.index(Tmax)
    a=s['ambulancias'][index_a]
    rand=random.randint(0,len([p_num for p_num in a.route if isinstance(p_num,int)])-1)
    # removemos el  paciente aleatorio de la ruta  
    s['ambulancias'][index_a],s['hospitales'],s['pacientes']=remove_route(a,matrix_dist,s['hospitales'], s['pacientes'],rand)
    # if len(debbug_pac_ruta(s))>87:
    #     h=3
    return s

def Rem_all(s,matrix_dist):
    T=[a.tiempo_final for a in s['ambulancias']]
    Tmax=max(T)
    index_a=T.index(Tmax)
    a=s['ambulancias'][index_a]
    # quitar a los pacientes atendidos:
    while len(s['ambulancias'][index_a].route)>1:
        s['ambulancias'][index_a],s['hospitales'],s['pacientes']=remove_route(a,matrix_dist,s['hospitales'], s['pacientes'])

    # pacientes_a=[s['pacientes'].index(p) for p in s['pacientes'] if p.ambulancia==a.num]
    # for p in pacientes_a:
    #     s['pacientes'][p].atendido=0
    #     s['pacientes'][p].hosp=''
    #     s['pacientes'][p].ambulancia=None
    #     s['pacientes'][p].w=0
    # hosp_usados=[h for h in a.route[1:] if isinstance(h, str)]
    # hosp_unico=list(set(hosp_usados))
    # for h in hosp_unico:
    #     s['hospitales'][h]=s['hospitales'][h]+hosp_usados.count(h)
    # # modificar los parametros de la ambulancia
    # a.tiempo_final=0
    # h=a.route[0]
    # a.route=[h]
    # s['ambulancias'][index_a]=a
    # if len(debbug_pac_ruta(s))>87:
    #     h=3
    return s


def remove_route(ambulancia,matrix_dist,hospitales, pacientes,paciente=-1):
    pacientes_a=[p for p in ambulancia.route if isinstance(p,int)] # pacientes atendidos por la ambulancia a
    if paciente==-1:
        w_pacientes=[p.w for p in pacientes if p.num in pacientes_a]                   # tiempo de visita de la ambulancia a los pacientes
        p_index=w_pacientes.index(max(w_pacientes))
        p_num=pacientes_a[p_index]                    # paciente con mayor tiempo
    else:
        p_num=pacientes_a[paciente]
    
    p=[p for p in pacientes if p.num==p_num][0]
    # devolver la capacidad a los hospitales 
    hospitales[p.hosp]=hospitales[p.hosp]+1

    # actualizar el estado del paciente
    p_index=pacientes.index(p)
    p.ambulancia=None
    p.hosp=''
    p.atendido=0
    p.w=0
    pacientes[p_index]=p
    
    # actualizar ruta de ambulancia
    item=ambulancia.route.index(p.num)
    ambulancia.route.pop(item)
    ambulancia.route.pop(item)
    # ambulancia.route=ambulancia.route[:item]+ambulancia.route[item+2:]

    # actualizar el tiempo de la ambulancia
    ambulancia.calc_tiempo_f(matrix_dist,pacientes)
    
    #removemos el paciente de la lista de pacientes
    pacientes_a=[p_num for p_num in ambulancia.route if isinstance(p_num,int)]

    #actualizar los tiempos de los pacientes
    for i in pacientes_a: # iterar en los pacientes de la ambulancia a para actualizar los tiempos de visita a los pacientes
        index_route=ambulancia.route.index(i)
        w=ambulancia.calc_tiempo(index_route,matrix_dist,pacientes)
        index_pac=pacientes.index([p for p in pacientes if p.num==i][0])
        pacientes[index_pac].w=w
        
    
    return ambulancia,hospitales,pacientes
