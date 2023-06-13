import math

class Kiwi():
    def __init__(self,m):
        self.C=18
        self.aw_kiwi=(0.96*((1-((math.e)**(-self.C*m)))/(1+((math.e)**(-self.C*m)))))
    
class aw_prom_kiwi():
    def __init__(self,listaAws):
        self.listaKiwi=listaAws
    def aw_prom_kiwis(self):
        suma=0
        for k in range(len(self.listaKiwi)):
            suma=suma+self.listaKiwi[k].aw_kiwi
        promedio=round(suma/len(self.listaKiwi),2)
        return promedio
    
kiwi1=Kiwi(0.3)  #Pruebas
kiwi2=Kiwi(0.2)
kiwi3=Kiwi(0.6)  #si en el programa server se hace una iteracion que cree una lista con objetos kiwi
lista=[kiwi1,kiwi2,kiwi3]
kiwis=aw_prom_kiwi(lista)
print("El aw promedio del kiwi es: ", kiwis.aw_prom_kiwis())

class Manzana():
    def __init__(self,m):
        self.C=15
        self.aw_manzana=(0.97*(((self.C*m)**2)/(1+((self.C*m)**2))))

class aw_prom_manzana():
    def __init__(self,listaAws):
        self.listaManzana=listaAws
    def aw_prom_manzanas(self):
        suma=0
        for m in range(len(self.listaManzana)):
            suma=suma+self.listaManzana[m].aw_manzana
        promedio=round(suma/len(self.listaManzana),2)
        return promedio

class Alimentos():
    def __init__(self):
        pass

class Verduras(Alimentos):
    def aw_verduras(self):
        raise NotImplementedError("La subclase debe implementar el metodo")

class Papa(Verduras):
    def __init__(self,m):
        self.C=18
        self.masa=m
    def aw_verduras(self): #Polimorfismo
        self.aw_papa=0.66*(math.atan(self.C*self.masa))
        return self.aw_papa

class Zanahoria(Verduras):
    def __init__(self,m):
        self.C=10
        self.masa=m
    def aw_verduras(self): #Polimorfismo
        self.aw_zanahoria=0.96*(1-(math.e**(-self.C*self.masa)))
        return self.aw_zanahoria

# Función que interactúa con objetos de la clase Verduras
def obtener_aw(verdura):
    return round(verdura.aw_verduras(),2)

papa1=Papa(0.5)
zanahoria1=Zanahoria(0.3)
print("El aw de la papa es:",obtener_aw(papa1))
print("El aw de la zanahoria es:",obtener_aw(zanahoria1))

class aw_prom_papa():
    def __init__(self,listaAws):
        self.listaPapa=listaAws
    def aw_prom_papas(self):
        suma=0
        for p in range(len(self.listaPapa)):
            suma=suma+self.listaPapa[p].aw_papa
        promedio=round(suma/len(self.listaPapa),2)
        return promedio
    
class aw_prom_zanahoria():
    def __init__(self,listaAws):
        self.listaZanahoria=listaAws
    def aw_prom_zanahorias(self):
        suma=0
        for z in range(len(self.listaZanahoria)):
            suma=suma+self.listaZanahoria[z].aw_zanahoria
        promedio=round(suma/len(self.listaZanahoria),2)
        return promedio
    






