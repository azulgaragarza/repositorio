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

def opcionE(x):
    with open("apps\\opciones_elegidas.txt","a",encoding="utf-8") as elecciones:
        fecha=datetime.datetime.now()
        elecciones.write(str(x)+" "+str(fecha)+"\n")
    return 
listaEntera=[] #tiene frases y pelis
listaP=[] #tiene solo pelis
listaP2=[] #tiene pelis sin repeticion

with open("apps\\frases_de_peliculas.txt",encoding="utf-8") as archi:
    linea=archi.readlines()
    for i in linea:
        listaEntera.append(i.strip().split(";"))
for x in listaEntera:
    listaP.append(x[1])
listaP.sort()

for s in listaP:
    if s not in listaP2:
        listaP2.append(s)

while opcion!="5":
    if opcion=="1":
        for z in range(len(listaP2)):
            print(f"{z+1}. {listaP2[z]}")
        opcionE(opcion)
        opcion = input(OPCIONES)
    if opcion=="2":
       #print(listaEntera)
       Num=random.randint(0,len(listaEntera)-1)
       PeliCorrecta=listaEntera[Num][1]
       Frase=listaEntera[Num][0] 
       Num2=random.randint(0,len(listaEntera)-1)
       Peli2=listaEntera[Num2][1]
       while Peli2==PeliCorrecta:
            Num2=random.randint(0,len(listaEntera)-1)
            Peli2=listaEntera[Num2][1]
       Num3=random.randint(0,len(listaEntera)-1)
       Peli3=listaEntera[Num3][1]
       while Peli3==PeliCorrecta or Peli3==Peli2:
            Num3=random.randint(0,len(listaEntera)-1) 
            Peli3=listaEntera[Num3][1]
       Respuestas=[PeliCorrecta, Peli2, Peli3]
       random.shuffle(Respuestas)
       print("¿A que pelicula pertenece la frase?: ", Frase)
       print("1. "+Respuestas[0])
       print("2. "+Respuestas[1])
       print("3. "+Respuestas[2])
       op=int(input("Elija una opcion: "))
       if Respuestas[op-1]==PeliCorrecta:
           print("Felicitaciones, respuesta correcta!!")
       else:
           print("Respuesta incorrecta :(")
           
       opcionE(opcion)
       opcion = input(OPCIONES)
    if opcion=="3":
        opcionE(opcion)
        lista_elecciones=[]
        with open("apps\\opciones_elegidas.txt") as elecciones:
            l=elecciones.readlines()
            for a in l:
                lista_elecciones.append(a.strip().split(" "))
        for n in lista_elecciones:
            print(f"Opción {n[0]} el día {n[1]} a las {n[2]}")
        #print(lista_elecciones)
        opcion = input(OPCIONES)
    
    if opcion=="4":
        with open("apps\\opciones_elegidas.txt","w") as elecciones:
            elecciones.write("")
        opcion = input(OPCIONES)
if opcion=="5":
    print("¡Gracias por usar nuestro programa, vuelva pronto!")        

