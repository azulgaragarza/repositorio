import math
import numpy as np
import random
import matplotlib.pyplot as plt

class Kiwi():
    def __init__(self,m):
        self.C=18
        self.aw_kiwi=(0.96*((1-((math.e)**(-self.C*m)))/(1+((math.e)**(-self.C*m)))))
    
class Manzana():
    def __init__(self,m):
        self.C=15
        self.aw_manzana=(0.97*(((self.C*m)**2)/(1+((self.C*m)**2))))

class Papa():
    def __init__(self,m):
        self.C=18
        self.aw_papa=0.66*(math.atan(self.C*m))

class Zanahoria():
    def __init__(self,m):
        self.C=10
        self.aw_zanahoria=0.96*(1-(math.e**(-self.C*m)))

class aw_promedio():
    def __init__(self,lista_k,lista_m,lista_z,lista_p):
        self.kiwis=lista_k
        self.manzanas=lista_m
        self.zanahorias=lista_z
        self.papas=lista_p
        self.aw_kiwis = []
        self.aw_manzanas = []
        self.aw_zanahorias = []
        self.aw_papas = []

    def aw_prom_kiwis(self):
        for obj in self.kiwis:
            self.aw_kiwis.append(obj.aw_kiwi)
        suma=0
        for k in range(len(self.aw_kiwis)):
            suma=suma+self.aw_kiwis[k]
        promedio_k=round(suma/len(self.aw_kiwis),2)
        self.prom_k=promedio_k

    def aw_prom_manzanas(self):
        for obj in self.manzanas:
            self.aw_manzanas.append(obj.aw_manzana)
        suma=0
        for m in range(len(self.aw_manzanas)):
            suma=suma+self.aw_manzanas[m]
        promedio_m=round(suma/len(self.aw_manzanas),2)
        self.prom_m=promedio_m
        
    def aw_prom_zanahorias(self):
        for obj in self.zanahorias:
            self.aw_zanahorias.append(obj.aw_zanahoria)
        suma=0
        for z in range(len(self.aw_zanahorias)):
            suma=suma+self.aw_zanahorias[z]
        promedio_z=round(suma/len(self.aw_zanahorias),2)
        self.prom_z=promedio_z

    def aw_prom_papa(self):
        for obj in self.papas:
            self.aw_papas.append(obj.aw_papa)
        suma=0
        for p in range(len(self.aw_papas)):
            suma=suma+self.aw_papas[p]
        promedio_p=round(suma/len(self.aw_papas),2)
        self.prom_p=promedio_p

    def aw_prom_verduras(self):
        self.prom_verduras= round(((self.prom_p + self.prom_z)/2),2)
    
    def aw_prom_frutas(self):
        self.prom_frutas= round(((self.prom_k + self.prom_m)/2),2)

    def prom_total(self):
        self.promedio_total= round(((self.prom_verduras + self.prom_frutas)/2),2)

class DetectorAlimento:
    """clase que representa un conjunto de sensores de la cinta transportadora
    para detectar el tipo de alimento y su peso.
    """
    def __init__(self):
        self.alimentos = ["kiwi", "manzana", "papa", "zanahoria", "undefined"]
        self.peso_alimentos = round(np.linspace(0.05, 0.6, 12),2)
        self.prob_pesos = round(self.__softmax(self.peso_alimentos)[::-1], 2)

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
    

    





