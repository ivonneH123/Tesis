import random

class ambulancia:
    def __init__(self,num, hospital,velocidad=50):
        self.num=num
        self.hospital=hospital
        self.tiempo_final=0
        self.velocidad=velocidad
        self.route=[hospital]
        #self.pacientes=[] # numeros de pacientes atendidos por la ambulancia
    
    def add_point(self,point):
        self.route.append(point)
    
    def delete_point(self,position_point):
        self.route.pop()

    def calc_tiempo(self, i, matrix_distance,pacientes):
        puntos=traducir_ruta(self.route[:i+1],pacientes)
        
        trayectoria=0
        for punto in range(1,len(puntos)):
            trayectoria=trayectoria+matrix_distance[puntos[punto-1]][puntos[punto]]
        return trayectoria/self.velocidad

    def calc_tiempo_f(self, matrix_distance,pacientes):
        if len(self.route)<=1:
            self.tiempo_final=0
            return self.tiempo_final
        trayectoria=0
        puntos=traducir_ruta(self.route,pacientes)
        for punto in range(1,len(self.route)):
            trayectoria=trayectoria+matrix_distance[puntos[punto-1]][puntos[punto]]
        self.tiempo_final=trayectoria/ self.velocidad
        return self.tiempo_final

    def posiciones_baratas(self,point, matrix_dist,pacientes, alpha):
        if len(self.route)==1:
            return [1]
        ruta=traducir_ruta(self.route, pacientes)
        index_hosp=[i for i in range(len(ruta[1:])) if ruta[i][:4]=='HOSP']
        distancias = {str(p):matrix_dist[ruta[p]][point] for p in index_hosp}
        sorted_dist = sorted(distancias, key=distancias.get)        
        return [int(x)+1 for x in sorted_dist[:(alpha+1)]]
    
    def pac_cercanos(self,matrix_dist,pacientes, alpha):
        hosp=self.route[-1]
        lista_pmas=[x.pma for x in pacientes]
        pmas=list(set(lista_pmas))
        distancias={ pma: matrix_dist[hosp][pma] for pma in pmas}
        sorted_dist = sorted(distancias, key=distancias.get)[:alpha+1] # distancias de PMA
        Cp=[]
        for i in range(alpha):
            a= random.randint(0,alpha-1)
            Cp.append(pacientes[lista_pmas.index(sorted_dist[a])])
        return Cp
def traducir_ruta(lista, pacientes):
    trad_ruta=[]
    for punto in lista:
        if isinstance(punto, int):
            trad_ruta.append([p.pma for p in pacientes if p.num==punto][0])
        else:
            trad_ruta.append(punto)
    return trad_ruta      




class paciente:
    def __init__(self, num,pma,a,b):
        self.num=num
        self.pma=pma
        self.a=a
        self.b=b
        self.atendido=0
        self.ambulancia=None
        self.w=0
        self.hosp=""
    
    def atender_paciente(self,ambulancia, hosp, posicion, matriz_dist,pacientes):
        ambulancia.route.insert(posicion,self.num)
        self.w=ambulancia.calc_tiempo(posicion,matriz_dist, pacientes)
        # ambulancia.pacientes.insert(len([x for x in ambulancia.route[:posicion] if x[:3]=="PMA"]),self.num)
        ambulancia.route.insert(posicion+1,hosp)
        ambulancia.tiempo_final=ambulancia.calc_tiempo_f(matriz_dist,pacientes)
        self.hosp=hosp
        self.ambulancia=ambulancia.num
        self.atendido=1

def hosp_cercano(pma, hospitales, matrix_dist, alpha=1):
    hosp_con_cap= [hosp for hosp in list(hospitales.keys()) if hospitales[hosp]>0]
    distancias = {str(hosp):matrix_dist[pma][hosp] for hosp in hosp_con_cap}
    sorted_dist = sorted(distancias, key=distancias.get)
    # actualizando capacidad
    hosp=sorted_dist[:alpha]
    return   hosp

    