from modules.classes import *

def crear_objetos(pesos,alimentos,lista_objetos):
    for x in range(len(alimentos)):
        if alimentos[x]=="kiwi":
            objeto=Kiwi()
            objeto.aw_frutas(pesos[x]) #le asigna un peso a al objeto
            lista_objetos.append(objeto.aw_kiwi)
        elif alimentos[x]=="manzana":
            objeto=Manzana()
            objeto.aw_frutas(pesos[x])
            lista_objetos.append(objeto.aw_manzana)
        elif alimentos[x]=="zanahoria":
            objeto=Zanahoria()
            objeto.aw_verduras(pesos[x])
            lista_objetos.append(objeto.aw_zanahoria)
        elif alimentos[x]=="papa":
            objeto=Papa()
            objeto.aw_verduras(pesos[x])
            lista_objetos.append(objeto.aw_papa)
        else:
            next

def obtener_aw(lista_objetos):
    for s in range(len(lista_objetos)):
        if isinstance(lista_objetos[s], Kiwi):
            

            


