def crear_lista(listaEntera):
    ruta="D:\\Azul\\repositorio\\TP 1 Programación\\ej 2\\apps\\frases_de_peliculas.txt"
    with open(ruta) as archi:
        linea=archi.readlines()
        for i in linea:
            listaEntera.append(i.strip().split(";"))
    return listaEntera
 
def pelis_frase(listaEntera):
    import random
    Num=random.randint(0,len(listaEntera)-1)
    PeliCorrecta=listaEntera[Num][1]
    Frase=listaEntera[Num][0] 
    Num2=random.randint(0,len(listaEntera)-1)
    while Num2==Num:
        Num2=random.randint(0,len(listaEntera)-1)
    Peli2=listaEntera[Num2][1]
    Num3=random.randint(0,len(listaEntera)-1)
    while Num3==Num or Num3==Num2:
        Num3=random.randint(0,len(listaEntera)-1) 
    Peli3=listaEntera[Num3][1]     
    matriz=[PeliCorrecta, Peli2, Peli3]
    random.shuffle(matriz) #mezcla las respuestas para que la opcion correcta no sea siempre la misma
    matriz.append(Frase)
    matriz.append(PeliCorrecta) #se agrega un quinto elemento que contiene siempre la respuesta correcta
    return matriz

ruta="D:\\Azul\\repositorio\\TP 1 Programación\\ej 2\\"
def guardar_nombre_en_archivo(nombre):  
    import datetime
    with open(ruta+"nombres.txt", "a", encoding="UTF-8") as archi:
        fecha=datetime.datetime.now()
        archi.write(str(nombre)+" "+str(fecha))

def escribir_mensaje(Respuesta,Correcta,intentos):
    with open(ruta+"mensaje.txt","w") as mensaje:
        suma=0
        if Respuesta==Correcta:
            mens="Respuesta correcta :)"
            mensaje.write(mens+"\n")
            intentos.append(1)
        else:
            mens="Respuesta incorrecta :("
            mensaje.write(mens+"\n")
            intentos.append(0)
        if len(intentos)==5:
            for x in intentos:
                suma=suma+x
        mensaje.write(str(suma))

        


