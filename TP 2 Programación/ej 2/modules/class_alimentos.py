import math

class Verduras():
    def aw_verduras(self):
        raise NotImplementedError("La subclase debe implementar el metodo") #este método no ha sido implementado 
                                    #en la clase actual y se espera que sea implementado en una subclase.

class Frutas():
    def aw_frutas(self):
        raise NotImplementedError("La subclase debe implementar el metodo")

class Kiwi(Frutas):
    def __init__(self):
        self.C=18
    def aw_frutas(self,m):
        self.masa=m
        self.aw_kiwi=round(0.96*((1-((math.e)**(-self.C*self.masa)))/(1+((math.e)**(-self.C*self.masa)))),2)
    
class Manzana(Frutas):
    def __init__(self):
        self.C=15
    def aw_frutas(self,m):
        self.masa=m
        self.aw_manzana=round(0.97*(((self.C*self.masa)**2)/(1+((self.C*self.masa)**2))),2)

class Papa(Verduras):
    def __init__(self):
        self.C=18
    def aw_verduras(self,m): #Polimorfismo
        self.masa=m
        self.aw_papa=round(0.66*(math.atan(self.C*self.masa)),2)

class Zanahoria(Verduras):
    def __init__(self):
        self.C=10
    def aw_verduras(self,m):
        self.masa=m
        self.aw_zanahoria=round(0.96*(1-(math.e**(-self.C*self.masa))),2)





    





