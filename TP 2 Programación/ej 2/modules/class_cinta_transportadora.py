from modules.class_alimentos import Kiwi, Manzana, Papa, Zanahoria
from modules.class_detector_alimentos import DetectorAlimento

class Cinta_Transportadora():
    def __init__(self):
        self.pesos=[]
        self.alimentos=[]
        self.lista_objetos=[]
    def crear_listas(self,cant_alimentos):
        sensor = DetectorAlimento()
        for i in range(int(cant_alimentos)):
            self.pesos.append(sensor.detectar_alimento()["peso"])
            self.alimentos.append(sensor.detectar_alimento()["alimento"])
        while "undefined" in self.alimentos:
            for alimento in range(len(self.alimentos)):
                if self.alimentos[alimento] == "undefined":
                    del self.alimentos[alimento]
                    del self.pesos[alimento]
                    self.alimentos.append(sensor.detectar_alimento()["alimento"])
                    self.pesos.append(sensor.detectar_alimento()["peso"])
                    break
    def crear_objetos(self):
        for x in range(len(self.alimentos)):
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


