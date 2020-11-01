class ambulancia:
    def _init_(self,num, hospital,velocidad=50):
        self.num=num
        self.hospital=hospital
        self.tiempo_final=0
        self.velocidad=velocidad
        self.route=[hospital]
    
    def add_point(self,point):
        self.route.append(point)
    
    def delete_point(self,position_point):
        self.route.pop()

class paciente:
    def _init_(self, num,pma,a,b):
        self.num=num
        self.pma=pma
        self.a=a
        self.b=b
        self.atendido=0
        self.ambulancia=None
        self.w=0
    
    def atender_paciente(self,ambulancia, matriz_dist):
        self.w=ambulancia.tiempo_final+matriz_dist[ambulancia.route[-1]][self.pma]*ambulancia.velocidad
        ambulancia.add_point(self.pma)
        ambulancia.tiempo_final=self.w
        self.ambulancia=ambulancia.num
        self.atendido=1

    