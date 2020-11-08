
import random
from LKS import funcion_obj
def VND(s,matrix_dist):
    f_s=funcion_obj(s)
    s_optim=s
    f_Soptim=f_s
    lamb=[i_p_relocate, i_p_swap,s_h_change,e_p_swap, e_p_2opt, h_swap,route_reasignment]
    i=0
    while i<len(lamb):
        s=lamb[i](s,matrix_dist)
        if (funcion_obj(s)>f_Soptim):
            s_optim=s
            f_Soptim=funcion_obj(s)
            
            i=0
        else:
            i=+1
    return s_optim


def i_p_relocate(s,matrix_dist):
    # escoger una ruta e intercambiar dos pacientes
    rand=random