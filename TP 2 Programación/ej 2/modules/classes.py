import math
import numpy as np
import random
import matplotlib.pyplot as plt


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

class Cinta_Transportadora():
    def __init__(self,pesos,alimentos):
        self.pesos=pesos
        self.alimentos=alimentos
        self.lista_objetos=[]
    def crear_objetos(self):
        for x in range(len(self.alimentos)):
            if self.alimentos[x]=="undefined":
                next
            else:
                if self.alimentos[x]=="kiwi":
                    objeto=Kiwi()
                    objeto.aw_frutas(self.pesos[x]) #le asigna un peso a al objeto
                    self.lista_objetos.append(objeto)
                elif self.alimentos[x]=="manzana":
                    objeto=Manzana()
                    objeto.aw_frutas(self.pesos[x])
                    self.lista_objetos.append(objeto)
                elif self.alimentos[x]=="zanahoria":
                    objeto=Zanahoria()
                    objeto.aw_verduras(self.pesos[x])
                    self.lista_objetos.append(objeto)
                elif self.alimentos[x]=="papa":
                    objeto=Papa()
                    objeto.aw_verduras(self.pesos[x])
                    self.lista_objetos.append(objeto)

class Cajon(Cinta_Transportadora):
    def aw_prom_kiwis(self):
        suma=0
        contador=0
        for k in range(len(self.lista_objetos)):
            if isinstance(self.lista_objetos[k],Kiwi)==True:
                suma=suma+self.lista_objetos[k].aw_kiwi
                contador=contador+1
        if contador!=0:
            self.prom_k=round(suma/contador,2)
        else:
            self.prom_k=0
        
    def aw_prom_manzanas(self):
        suma=0
        contador=0
        for m in range(len(self.lista_objetos)):
            if isinstance(self.lista_objetos[m],Manzana)==True:
                suma=suma+self.lista_objetos[m].aw_manzana
                contador=contador+1
        if contador!=0:
            self.prom_m=round(suma/contador,2)
        else:
            self.prom_m=0
        
    def aw_prom_zanahorias(self):
        suma=0
        contador=0
        for z in range(len(self.lista_objetos)):
            if isinstance(self.lista_objetos[z],Zanahoria)==True:
                suma=suma+self.lista_objetos[z].aw_zanahoria
                contador=contador+1
        if contador!=0:
            self.prom_z=round(suma/contador,2)
        else:
            self.prom_z=0
        
    def aw_prom_papas(self):
        suma=0
        contador=0
        for p in range(len(self.lista_objetos)):
            if isinstance(self.lista_objetos[p],Papa)==True:
                suma=suma+self.lista_objetos[p].aw_papa
                contador=contador+1
        if contador!=0:
            self.prom_p=round(suma/contador,2)
        else:
            self.prom_p=0
    
    def aw_prom_verduras(self):
        suma=0
        contador=0
        for v in range(len(self.lista_objetos)):
            if isinstance(self.lista_objetos[v],Verduras):
                if isinstance(self.lista_objetos[v],Papa):
                    suma=suma+self.lista_objetos[v].aw_papa
                    contador=contador+1
                else:
                    suma=suma+self.lista_objetos[v].aw_zanahoria
                    contador=contador+1
        if contador!=0:
            self.prom_verduras=round(suma/contador,2)
        else:
            self.prom_verduras=0

    def aw_prom_frutas(self):
        suma=0
        contador=0
        for f in range(len(self.lista_objetos)):
            if isinstance(self.lista_objetos[f],Frutas):
                if isinstance(self.lista_objetos[f],Kiwi):
                    suma=suma+self.lista_objetos[f].aw_kiwi
                    contador=contador+1
                else:
                    suma=suma+self.lista_objetos[f].aw_manzana
                    contador=contador+1
        if contador!=0:
            self.prom_frutas=round(suma/contador,2)
        else:
            self.prom_frutas=0
        
    def aw_prom_total(self,cant_alimentos):
        suma=0
        for t in self.lista_objetos:
            if isinstance(t,Kiwi):
                suma=suma+t.aw_kiwi
            elif isinstance(t,Manzana):
                suma=suma+t.aw_manzana
            elif isinstance(t,Zanahoria):
                suma=suma+t.aw_zanahoria
            else:
                suma=suma+t.aw_papa
        self.promedio_total= round((suma/cant_alimentos),2)


class DetectorAlimento:
    """clase que representa un conjunto de sensores de la cinta transportadora
    para detectar el tipo de alimento y su peso.
    """
    def __init__(self):
        self.alimentos = ["kiwi", "manzana", "papa", "zanahoria", "undefined"]
        self.peso_alimentos = np.round(np.linspace(0.05, 0.6, 12),2)
        self.prob_pesos = np.round(self.__softmax(self.peso_alimentos)[::-1], 2)

    def __softmax(self, x):
        """función softmax para crear vector de probabilidades 
        que sumen 1 en total
        """
        return (np.exp(x - np.max(x)) / np.exp(x - np.max(x)).sum())

    def detectar_alimento(self):
        """método que simula la detección del alimento y devuelve un diccionario
        con la información del tipo y el peso del alimento.
        """
        n_alimentos = len(self.alimentos)
        alimento_detectado = self.alimentos[random.randint(0, n_alimentos-1)]
        peso_detectado = random.choices(self.peso_alimentos, self.prob_pesos)[0]
        return {"alimento": alimento_detectado, "peso": peso_detectado}
    


    





