import random


def LNS_metah(I,L):
    s_optim={} # inicializar soluciones en vacio
    s={}

    f_optim=0 # funcion objetivo de la solución óptima hasta el momento
    f_actual=0 # funcion objetivo de la solución actual
    
    i=0 #contador de iteraciones
    l=0 #contador de iteraciones sin mejoras
    while (i<l):
        if (i == 0 or l == L):
            rand = random.randint(0,1)
            if rand ==0:
                s=Insertion_Heuristic()



def funcion_obj(s_optim):
