
import random
def funcion_obj(s):
    return sum([ x.atendido for x in s['pacientes']])

def VND(s,matrix_dist):
    f_s=funcion_obj(s)
    s_optim=s
    f_Soptim=f_s
    lamb=[i_p_relocate, i_p_swap,e_p_swap, e_p_2opt,route_reasignment]
    i=0
    while i<len(lamb):
        s=lamb[i](s,matrix_dist)
        if (funcion_obj(s)>f_Soptim):
            s_optim=s
            f_Soptim=funcion_obj(s)
            
            i=0
        else:
            i+=i+1
    return s_optim


def i_p_relocate(s,matrix_dist):
    for index_amb in range(len(s['ambulancias'])): # iterar en todas las ambulancias
        ambulance=s['ambulancias'][index_amb]
        p=[ambulance.route.index(p) for p in s['ambulancias'][index_amb].route if isinstance(p,int)] # indices de pacientes en las rutas de las ambulancias
        B=[p.b for p in s['pacientes'] if p.num in ambulance.route]     # tiempo máximo de los pacientes
        pac_amb_index={str(p.num):s['pacientes'].index(p) for p in s['pacientes'] if p.num in ambulance.route} #indices de los pacientes en la lista de pacientes 
        num=[int(n) for n in pac_amb_index.keys()]

        for index_pac in p: # iterar en todos los pacientes
            # seleccionar paciente y el hospital al que se dirige
            num_pac=ambulance.route[index_pac]
            num_hosp=ambulance.route[index_pac+1]

            # extraer de la ruta de la ambulancia
            ambulance.route.pop(index_pac)
            ambulance.route.pop(index_pac)

            # indices de hospitales
            indices_h=[ambulance.route.index(h) for h in ambulance.route if isinstance(h,str)]

            #localizar en otro punto de la ruta
            for nueva_loc in indices_h:
                ambulance.route.insert(nueva_loc+1,num_pac)
                ambulance.route.insert(nueva_loc+2,num_hosp)
                
                #posiciones de pacientes actualizados
                pos={str(p):ambulance.route.index(p) for p in ambulance.route if isinstance(p,int)}

                if B[0]>=ambulance.calc_tiempo_f(matrix_dist,s['pacientes']):
                    # actualizar los tiempos de visita en los hospitales
                    for i in range(len(pac_amb_index)):    
                        s['pacientes'][pac_amb_index[str(num[i])]].w=ambulance.calc_tiempo(pos[str(num[i])],matrix_dist,s['pacientes'])
                    
        s['ambulancias'][index_amb]=ambulance
    
    return s

def i_p_swap(s,matrix_dist):
    # escoger una ruta e intercambiar dos pacientes
    for index_amb in range(len(s['ambulancias'])): # iterar en todas las ambulancias
        ambulance=s['ambulancias'][index_amb]
        p=[ambulance.route.index(p) for p in s['ambulancias'][index_amb].route if isinstance(p,int)] # indices de pacientes en las rutas de las ambulancias
        pac_amb_index={str(p.num):s['pacientes'].index(p) for p in s['pacientes'] if p.num in ambulance.route} #indices de los pacientes en la lista de pacientes 
        num=[int(n) for n in pac_amb_index.keys()]
        ruta_previa=ambulance.route
        tiempo_final_ans=ambulance.tiempo_final

        for index_pac1 in p: # iterar en todos los pacientes
            p2=p
            p2.remove(index_pac1)

            for index_pac2 in p2: # iterar en todos los pacientes diferentes al paciente a intercambiar
                # intercambiar los pacientes
                ambulance.route[index_pac1],ambulance.route[index_pac1+1]=ambulance.route[index_pac2],ambulance.route[index_pac2+1]
                pos={str(p):ambulance.route.index(p) for p in ambulance.route if isinstance(p,int)}
                #localizar en otro punto de la ruta
                if tiempo_final_ans>=ambulance.calc_tiempo_f(matrix_dist,s['pacientes']):
                    # actualizar los tiempos de visita en los hospitales
                    for i in range(len(pac_amb_index)):  
                        #ERRORRRR HELMP PLIS aiudaaaa  
                        s['pacientes'][pac_amb_index[str(num[i])]].w=ambulance.calc_tiempo(pos[str(num[i])],matrix_dist,s['pacientes'])
                else:
                    ambulance.route=ruta_previa
                    
        s['ambulancias'][index_amb]=ambulance
    
    return s

def e_p_swap(s,matrix_dist):
    pac_index={str(p.num):s['pacientes'].index(p) for p in s['pacientes']}
    for index_amb in range(len(s['ambulancias'])): # iterar en todas las ambulancias
        ambulance1=s['ambulancias'][index_amb]
        pac_amb1=[p for p in ambulance1.route if isinstance(p,int)]
        loc_1={str(p):ambulance1.route.index(p) for p in ambulance1.route if isinstance(p,int)}
        ruta1_actual= ambulance1.route
        ruta1_tiempo=ambulance1.tiempo_final

        for ambulance2 in s['ambulancias'][0:index_amb]+s['ambulancias'][index_amb+1:]:
            pac_amb2= [p for p in ambulance2.route if isinstance(p,int)]
            loc_2={str(p):ambulance2.route.index(p) for p in ambulance2.route if isinstance(p,int)}
            ruta2_actual= ambulance2.route
            ruta2_tiempo=ambulance2.tiempo_final
            index_amb2=s['ambulancias'].index(ambulance2)

            for p1 in pac_amb1:
                for p2 in pac_amb2:
                    hosp_1=ambulance1.route[loc_1[str(p1)]+1]
                    hosp_2=ambulance2.route[loc_2[str(p2)]+1]
                    ambulance1.route[loc_1[str(p1)]],ambulance1.route[loc_1[str(p1)]+1]=p2,hosp_2 # cambiar el paciente de la ambulancia1 en la ambulancia2
                    ambulance2.route[loc_2[str(p2)]],ambulance2.route[loc_2[str(p2)]+1]= p1,hosp_1 # cambiar el paciente de la ambulancia2 en la ambulancia1
                    if (ambulance1.calc_tiempo_f(matrix_dist,s['pacientes']) > ruta1_tiempo) and (ambulance2.calc_tiempo_f(matrix_dist,s['pacientes']) > ruta2_tiempo):
                        # actualizar los pacientes
                        for p in [p for p in ambulance1.route if isinstance(p,int)]:
                            s['pacientes'][pac_index[str(p)]].w=ambulance1.calc_tiempo(ambulance1.route.index(p),s['pacientes'])
                        for p in [p for p in ambulance2.route if isinstance(p,int)]:
                            s['pacientes'][pac_index[str(p)]].w=ambulance2.calc_tiempo(ambulance2.route.index(p),s['pacientes'])
                        s['ambulancias'][index_amb]=ambulance1
                        s['ambulancias'][index_amb2]=ambulance2
                        #actualizar las rutas actuales
                        ruta1_actual= ambulance1.route
                        ruta2_actual=ambulance2.route
                    else:
                        ambulance1.route=ruta1_actual
                        ambulance2.route=ruta2_actual
    return s

def e_p_2opt(s, matrix_dist):
    pac_index={str(p.num):s['pacientes'].index(p) for p in s['pacientes']}
    for index_amb in range(len(s['ambulancias'])): # iterar en todas las ambulancias
        ambulance1=s['ambulancias'][index_amb]
        pac_amb1=[p for p in ambulance1.route if isinstance(p,int)]
        ruta1_actual= ambulance1.route
        ruta1_tiempo=ambulance1.tiempo_final

        for ambulance2 in s['ambulancias'][0:index_amb]+s['ambulancias'][index_amb+1:]:
            pac_amb2= [p for p in ambulance2.route if isinstance(p,int)]
            ruta2_actual= ambulance2.route
            ruta2_tiempo=ambulance2.tiempo_final
            index_amb2=s['ambulancias'].index(ambulance2)

            for p1 in pac_amb1:
                for p2 in pac_amb2:
                    # cambiar las rutas desde el paciente 
                    if (pac_amb2.index(p2)!=len(pac_amb2)-1) and (pac_amb1.index(p1)!=len(pac_amb1)-1):# si no son los ultimos pacientes en la lista de pacientes en ambas ambulancias
                        ruta_1=ambulance1.route[:ambulance1.route.index(p1)+3]+ambulance2.route[ambulance2.route.index(p2)+3:]
                        ruta_2=ambulance2.route[:ambulance2.route.index(p2)+3]+ambulance1.route[ambulance1.route.index(p1)+3:]

                        ambulance1.route=ruta_1
                        ambulance1.route=ruta_2
                        if (ambulance1.calc_tiempo_f(matrix_dist,s['pacientes']) > ruta1_tiempo) and (ambulance2.calc_tiempo_f(matrix_dist,s['pacientes']) > ruta2_tiempo):
                            # actualizar los pacientes
                            for p in [p for p in ambulance1.route if isinstance(p,int)]:
                                s['pacientes'][pac_index[str(p)]].w=ambulance1.calc_tiempo(ambulance1.route.index(p),matrix_dist,s['pacientes'])
                                s['pacientes'][pac_index[str(p)]].ambulancia=ambulance1.num

                            for p in [p for p in ambulance2.route if isinstance(p,int)]:
                                s['pacientes'][pac_index[str(p)]].w=ambulance2.calc_tiempo(ambulance2.route.index(p),matrix_dist,s['pacientes'])
                                s['pacientes'][pac_index[str(p)]].ambulancia=ambulance2.num

                            s['ambulancias'][index_amb]=ambulance1
                            s['ambulancias'][index_amb2]=ambulance2
                            #actualizar las rutas actuales
                            ruta1_actual= ambulance1.route
                            ruta2_actual=ambulance2.route
                        else:
                            ambulance1.route=ruta1_actual
                            ambulance1.calc_tiempo_f(matrix_dist,s['pacientes'])
                            ambulance2.route=ruta2_actual
                            ambulance2.calc_tiempo_f(matrix_dist,s['pacientes'])
    return s

def route_reasignment(s,matrix_dist):
    index_amb={str(a.num): s['ambulancias'].index(a) for a in s['ambulancias']}
    index_pac={str(p.num): s['pacientes'].index(p) for p in s['pacientes']}
    for ambulance1 in s['ambulancias']:
        ruta1_actual=ambulance1.route
        tf1_actual=ambulance1.tiempo_final
        index_amb1=index_amb[str(ambulance1.num)]

        for ambulance2 in s['ambulancias']:
            ruta2_actual=ambulance2.route
            tf2_actual=ambulance2.tiempo_final
            index_amb2=index_amb[str(ambulance2.num)]
            
            # intercambiar ruta:
            ambulance1.route=[ambulance1.hospital]+ruta2_actual[1:]
            ambulance2.route=[ambulance2.hospital]+ruta1_actual[1:]

            if (ambulance1.calc_tiempo_f(matrix_dist,s['pacientes']) < tf1_actual) and (ambulance2.calc_tiempo_f(matrix_dist,s['pacientes']) < tf2_actual):
                
                # actualizar en todos los pacientes 
                for p in [p for p in ambulance2.route if isinstance(p,int)]:
                    s['pacientes'][index_pac[str(p)]].w=ambulance2.calc_tiempo(ambulance2.route.index(p),matrix_dist,s['pacientes'])
                    s['pacientes'][index_pac[str(p)]].ambulancia=ambulance2.num
                
                for p in [p for p in ambulance1.route if isinstance(p,int)]:
                    s['pacientes'][index_pac[str(p)]].w=ambulance1.calc_tiempo(ambulance1.route.index(p),matrix_dist,s['pacientes'])
                    s['pacientes'][index_pac[str(p)]].ambulancia=ambulance1.num
                ruta1_actual=ambulance1.route
                tf1_actual=ambulance1.tiempo_final

                #reasignar ambulancias
                s['ambulancias'][index_amb1]=ambulance1
                s['ambulancias'][index_amb2]=ambulance2

            else:
                ambulance1.route=ruta1_actual
                ambulance1.calc_tiempo_f(matrix_dist,s['pacientes'])
                ambulance2.route=ruta2_actual
                ambulance2.calc_tiempo_f(matrix_dist,s['pacientes'])
    return s