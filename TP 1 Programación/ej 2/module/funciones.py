def crear_lista(listaEntera,listaP,listaP2):
    ruta="D:\\Azul\\TP 1 Programación\\ej 2\\apps\\frases_de_peliculas.txt"
    with open(ruta) as archi:
        linea=archi.readlines()
        for i in linea:
            listaEntera.append(i.strip().split(";"))
    for x in listaEntera:
        listaP.append(x[1])
    listaP.sort()
    for z in range(len(listaP)):
        m=[z+1,listaP[z]]
        listaP2.append(m)
    return listaEntera,listaP,listaP2
 
def pelis_frase(listaEntera):
    import random
    Num=random.randint(0,len(listaEntera)-1)
    PeliCorrecta=listaEntera[Num][1]
    Frase=listaEntera[Num][0] 
    Num2=random.randint(0,len(listaEntera)-1)
    Peli2=listaEntera[Num2][1]
    Num3=random.randint(0,len(listaEntera)-1) 
    Peli3=listaEntera[Num3][1]     
    matriz=[PeliCorrecta, Peli2, Peli3]
    random.shuffle(matriz) #mezcla las respuestas para que la opcion correcta no sea siempre la misma
    matriz.append(Frase)
    matriz.append(PeliCorrecta) #se agrega un quinto elemento que contiene siempre la respuesta correcta
    return matriz


def guardar_nombre_en_archivo(nombre):  
    import datetime
    with open("nombres.txt", "a", encoding="UTF-8") as archi:
        fecha=datetime.datetime.now()
        archi.write(str(nombre)+" "+str(fecha)+"\n")

def escribir_mensaje(Respuesta,Correcta):
    with open("mensaje.txt","w") as mensaje:
        if Respuesta==Correcta:
            mens="Respuesta correcta :)"
            mensaje.write(mens)
        else:
            mens="Respuesta incorrecta :("
            mensaje.write(mens)
        


