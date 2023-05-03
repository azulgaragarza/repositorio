from flask import Flask, render_template, request, redirect
from module.funciones import *
app = Flask(__name__)
contador=0

@app.route("/", methods=['GET','POST'])
def home():
        global contador
        contador=0
        if request.method == 'POST':
              nombre=request.form["nombre"]
              guardar_nombre_en_archivo(nombre)
        return render_template('home.html')


@app.route("/pag1", methods=['GET','POST'])
def pag1():
      listaEntera=[] #tiene frases y pelis
      listaP=[] #tiene solo pelis
      listaP2=[] #tiene pelis con indice y ordenadas
      crear_lista(listaEntera,listaP,listaP2)
      matriz=pelis_frase(listaEntera)
      if request.method == 'POST' :
            Respuesta=request.form["valor-boton"]
            Correcta=request.form["valor-boton2"]
            escribir_mensaje(Respuesta,Correcta)
            return redirect('/pag2')
      return render_template('pag1.html', matriz=matriz)

@app.route("/pag2")
def pag2():
      global contador
      contador=contador+1
      with open("mensaje.txt") as m:
            linea=m.readlines()
            for msj in linea:
                  mensaje=str(msj)
      return render_template('pag2.html',mensaje=mensaje,contador=contador)

@app.route("/resultados")
def resultados():
      lista_participantes=[]
      with open("D:\\Azul\\TP 1 Programación\\ej 2\\nombres.txt") as f:
            linea=f.readlines()
      for i in linea:
            lista_participantes.append(i.strip().split(" "))
      return render_template('resultados.html',lista_participantes=lista_participantes)
        
if __name__ == '__main__':
   app.run(debug = True)
