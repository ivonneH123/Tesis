import random
from amb_pac import hosp_cercano
def LNS_metah(I,L,ambulancias,matrix_dist,hospitales,pacientes):
    s_optim={} # inicializar soluciones en vacio
    s={}

    f_optim=0 # funcion objetivo de la solución óptima hasta el momento
    f_actual=0 # funcion objetivo de la solución actual
    
    i=0 #contador de iteraciones
    l=0 #contador de iteraciones sin mejoras
    while (i<l):
        if (i == 0 or l == L):
            rand = random.randint(0,1)
            alpha = random.randint(2,5)
            if rand ==0:
                s=Insertion_Heuristic(ambulancias,matrix_dist,hospitales,pacientes, alpha)
            elif rand==1:
                s=Constructive_heuristic(ambulancias,matrix_dist,hospitales,pacientes, alpha)
            l=1
        else:
            rand=random.randint(0,2)
            if rand==0:
                s=Rem2(s,matrix_dist)
            elif rand==1:
                s=Rem_rand(s,matrix_dist)
            else:
                s=Rem_all(s)
            s=Constructive_heuristic(s['ambulancias'],matrix_dist, s['hospitales'],s['pacientes'],1) # reparar las rutas






def funcion_obj(s):
    return sum([ x.atendido for x in s['pacientes']])

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

    while ((Chsum>0 or t<B )and len(pacientes_no_atendidos)>0):
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

        if t>B:
            a.route.append(h) # cerramos la ruta
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

    while ((Chsum>0 or condicion_tiempo>0) and len(pacientes_no_atendidos)>0):
        index_a=T.index(min(T))
        a=ambulancias[index_a]
        Cp=a.pac_cercanos(matrix_dist,[p for p in pacientes if p.num in pacientes_no_atendidos],alpha) #lista de pacientes mas cercanos
        i=Cp[random.randint(0,alpha-1)] # paciente aleatorio
        index_P_na=pacientes_no_atendidos.index(i)
        index_p=pacientes.index(i)
        Ch= hosp_cercano(i.pma,hospitales,matrix_dist,alpha) # lista de hospitales alpha más cercanos
        hosp= Ch[random.randint(0,alpha-1)]  #hospital aleatorio
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
    return s


def Rem2(s,matrix_dist):
    # removemos 2 rutas de las ambulancias con mayor tiempo final
    i=0 
    while i<2:
        T=[a.tiempo_final for a in s['ambulancias']]
        Tmax=max(T)
        index_a=T.index(Tmax)
        a=s['ambulancias'][index_a]
        # removemos el último paciente de la ruta  
        s['ambulancias'][index_a],s['hospitales'],s['pacientes']=remove_route(a,matrix_dist,s['hospitales'], s['pacientes'])
        
        i=+1
    
    return s

def Rem_rand(s,matrix_dist):
    # seleccionar la ambulancia con mayor tiempo
    T=[a.tiempo_final for a in s['ambulancias']]
    Tmax=max(T)
    index_a=T.index(Tmax)
    a=s['ambulancias'][index_a]
    rand=random.randint(0,len(a.pacientes))
    # removemos el  paciente aleatorio de la ruta  
    s['ambulancias'][index_a],s['hospitales'],s['pacientes']=remove_route(a,matrix_dist,s['hospitales'], s['pacientes'],rand)
    return s

def Rem_all(s):
    T=[a.tiempo_final for a in s['ambulancias']]
    Tmax=max(T)
    index_a=T.index(Tmax)
    a=s['ambulancias'][index_a]
    # quitar a los pacientes atendidos:
    for p in a.pacientes:
        s['pacientes'][p].atendido=0
        s['pacientes'][p].hosp=''
        s['pacientes'][p].ambulancia=None
        s['pacientes'][p].w=0
    hosp_usados=[h for h in a.route[1:] if h[:4]=="HOSP"]
    hosp_unico=list(set(hosp_usados))
    for h in hosp_unico:
        s['hospitales'][h]=s['hospitales'][h]+hosp_usados.count(h)
    # modificar los parametros de la ambulancia
    a.pacientes=[]
    a.tiempo_final=0
    h=a.route[0]
    a.route=[h]
    s['ambulancias'][index_a]=a
    return s


def remove_route(ambulancia,matrix_dist,hospitales, pacientes,paciente=-1):
    a_num=ambulancia.num
    pacientes_a=[p for p in pacientes if p.ambulancia==a_num] # pacientes atendidos por la ambulancia a
    if paciente==-1:
        w_pacientes=[p.w for p in pacientes_a]                   # tiempo de visita de la ambulancia a los pacientes
        p_index=pacientes_a.index(max(w_pacientes))
        p=pacientes_a[p_index]                    # paciente con mayor tiempo
    else:
        p=pacientes_a[paciente]
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
    index_route=ambulancia.pacientes.index(p.num)
    cant_pacientes=0
    item=0
    while cant_pacientes!=index_route:
        if ambulancia.route[item][:3]=='PMA':
            cant_pacientes=+1
        item=+1                             # item se vuelve la posición en donde se encuentra el PMA al que el paciente p pertenece
    
    ambulancia.route=ambulancia.route[:item]+ambulancia.route[item+2:]
    
    #actualizarl los tiempos de los pacientes
    num_pac=[p.num for p in ambulancia.pacientes]
    index_pma=[i for i in range(len(ambulancia.route)) if ambulancia.route[i][:3]=="PMA"] # indices de los pmas en la ruta de la ambulancia a
    index_pac=[pacientes.index(p) for p in pacientes if p.num in num_pac] # indices de los pacientes en la lista de pacientes

    for i in range(len(ambulancia.pacientes)): # iterar en los pacientes de la ambulancia a para actualizar los tiempos de visita a los pacientes
        w=ambulancia.calc_tiempo(ambulancia.route[index_pma[i]],matrix_dist,pacientes)
        pacientes[index_pac[i]].w=w

    return ambulancia,hospitales,pacientes

# def VND(s,matrix_dist):
#     f_s=funcion_obj(s)
#     s_optim=s
#     f_Soptim=f_s
#     lamb=[i_p_relocate, i_p_swap,s_h_change,e_p_swap, e_p_2opt, h_swap,route_reasignment]
#     i=0
#     while i<len(lamb):
#         s=lamb[i](s,matrix_dist)
#         if (funcion_obj(s)>f_Soptim):
#             s_optim=s
#             f_Soptim=funcion_obj(s)
            
#             i=0
#         else:
#             i=+1
#     return s_optim


# def i_p_relocate(s,matrix_dist):
#     # escoger una 