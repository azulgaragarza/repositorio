# -*- coding: utf-8 -*-
"""
Created on Tue Mar 21 17:36:45 2023

@author: NOTEBOOK-HP
"""

OPCIONES="""
#######################################
#  Películas: Preguntas y respuestas  #
#######################################
Elige una opción
1 - Mostrar lista de películas.
2 - ¡Trivia de película!
3 - Mostrar secuencia de opciones seleccionadas previamente.
4 - Borrar historial de opciones.
5 - Salir

"""
opcion = input(OPCIONES)
import random
import datetime
from module.funciones import *
def opcionE(x):
    with open("opciones_elegidas.txt","a") as elecciones:
        fecha=datetime.datetime.now()
        elecciones.write(str(x)+" "+str(fecha)+"\n")
    return 
listaEntera=[] #tiene frases y pelis
listaP=[] #tiene solo pelis
listaP2=[] #tiene pelis con indice y ordenadas
crear_lista(listaEntera,listaP,listaP2) #abre el archivo y crea las listas
while opcion!="5":
    if opcion=="1":
        print(listaP2)
        opcionE(opcion)
        opcion = input(OPCIONES)
    if opcion=="2":
       #print(listaEntera)
       Num=random.randint(0,len(listaEntera)-1)
       PeliCorrecta=listaEntera[Num][1]
       Frase=listaEntera[Num][0] 
       Num2=random.randint(0,len(listaEntera)-1)
       Peli2=listaEntera[Num2][1]
       Num3=random.randint(0,len(listaEntera)-1) 
       Peli3=listaEntera[Num3][1]     
       Respuestas=[PeliCorrecta, Peli2, Peli3]
       random.shuffle(Respuestas)
       print("¿A que pelicula pertenece la frase?: ", Frase)
       print(Respuestas)
       op=int(input("Elija una opcion del 1 al 3: "))
       if Respuestas[op-1]==PeliCorrecta:
           print("Felicitaciones, respuesta correcta!!")
       else:
           print("Respuesta incorrecta :(")
           
       opcionE(opcion)
       opcion = input(OPCIONES)
    if opcion=="3":
        opcionE(opcion)
        lista_elecciones=[]
        with open("opciones_elegidas.txt") as elecciones:
            l=elecciones.readlines()
            for a in l:
                lista_elecciones.append(a.strip())
        print(lista_elecciones)
        opcion = input(OPCIONES)
    
    if opcion=="4":
        with open("opciones_elegidas.txt","w") as elecciones:
            elecciones.write("")
        opcion = input(OPCIONES)
if opcion=="5":
    print("¡Gracias por usar nuestro programa, vuelva pronto!")        

