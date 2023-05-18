from flask import Flask, render_template, request, redirect
from module.funciones import *
app = Flask(__name__)
contador=0
intentos=[]
listaPrueba=[] #lista que guarda las frases en cada intento
Comparacion=[]

@app.route("/", methods=['GET','POST'])
def home():
        global contador
        contador=0
        global intentos
        intentos=[]
        global listaPrueba
        listaPrueba=[] #se vuelven las variables a cero y las listas a vacias
        if request.method == 'POST':
              nombre=request.form["nombre"]
              guardar_nombre_en_archivo(nombre)
        return render_template('home.html')


@app.route("/pag1", methods=['GET','POST'])
def pag1():
      global intentos
      global listaPrueba
      global Comparacion
      if len(listaPrueba)==0:
            listaEntera=[] #tiene frases y pelis
            crear_lista(listaEntera)
            matriz=pelis_frase(listaEntera)
      else:
            listaEntera=[] #tiene frases y pelis
            crear_lista(listaEntera)
            matriz=pelis_frase(listaEntera)
            for i in listaPrueba:
                  while i==matriz[3]:
                        listaEntera=[] #tiene frases y pelis
                        crear_lista(listaEntera)
                        matriz=pelis_frase(listaEntera)
      Comparacion=matriz[3] #guarda la frase utilizada
      if request.method == 'POST' :
            Respuesta=request.form["valor-boton"]
            Correcta=request.form["valor-boton2"]
            escribir_mensaje(Respuesta,Correcta,intentos)
            return redirect('/pag2')
      return render_template('pag1.html', matriz=matriz)

@app.route("/pag2")
def pag2():
      global listaPrueba
      global contador
      global Comparacion
      listaPrueba.append(Comparacion)
      contador=contador+1 #cuenta los intentos que se van jugando
      mensj=[]
      with open("D:\\Azul\\repositorio\\TP 1 Programación\\ej 2\\mensaje.txt") as m:
            linea=m.readlines()
            for msj in linea:
                 mensj.append(msj) 
            mensaje=str(mensj[0])
      return render_template('pag2.html',mensaje=mensaje,contador=contador)

@app.route("/resultados")
def resultados():
      lista_participantes=[]
      mensj=[]
      with open("D:\\Azul\\repositorio\\TP 1 Programación\\ej 2\\mensaje.txt") as m:
            linea=m.readlines()
            for msj in linea:
                 mensj.append(msj)
            resultados=mensj[1]
      with open("D:\\Azul\\repositorio\\TP 1 Programación\\ej 2\\nombres.txt","a") as n:
            n.write(" "+str(resultados)+"\n")
      with open("D:\\Azul\\repositorio\\TP 1 Programación\\ej 2\\nombres.txt") as f:
            linea=f.readlines()
      for i in linea:
            lista_participantes.append(i.strip().split(" "))
      return render_template('resultados.html',lista_participantes=lista_participantes)
        
if __name__ == '__main__':
   app.run(debug = True)
