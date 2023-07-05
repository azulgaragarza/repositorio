from modules.class_cinta_transportadora import Cinta_Transportadora
from modules.class_alimentos import Kiwi, Manzana, Zanahoria, Papa, Verduras, Frutas

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
