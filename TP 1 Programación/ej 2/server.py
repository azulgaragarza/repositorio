from flask import Flask, render_template, request, redirect
from module.funciones import *
app = Flask(__name__)
contador=0
intentos=[]

@app.route("/", methods=['GET','POST'])
def home():
        global contador
        contador=0
        global intentos
        intentos=[]
        if request.method == 'POST':
              nombre=request.form["nombre"]
              guardar_nombre_en_archivo(nombre)
        return render_template('home.html')


@app.route("/pag1", methods=['GET','POST'])
def pag1():
      global intentos
      listaEntera=[] #tiene frases y pelis
      listaP=[] #tiene solo pelis
      listaP2=[] #tiene pelis con indice y ordenadas
      crear_lista(listaEntera,listaP,listaP2)
      matriz=pelis_frase(listaEntera)
      if request.method == 'POST' :
            Respuesta=request.form["valor-boton"]
            Correcta=request.form["valor-boton2"]
            escribir_mensaje(Respuesta,Correcta,intentos)
            return redirect('/pag2')
      return render_template('pag1.html', matriz=matriz)

@app.route("/pag2")
def pag2():
      global contador
      contador=contador+1
      mensj=[]
      with open("mensaje.txt") as m:
            linea=m.readlines()
            for msj in linea:
                 mensj.append(msj) 
            mensaje=str(mensj[0])
      return render_template('pag2.html',mensaje=mensaje,contador=contador)

@app.route("/resultados")
def resultados():
      lista_participantes=[]
      mensj=[]
      with open("mensaje.txt") as m:
            linea=m.readlines()
            for msj in linea:
                 mensj.append(msj)
            resultados=mensj[1]
      with open("nombres.txt","a") as n:
            n.write(" "+str(resultados)+"\n")
      with open("nombres.txt") as f:
            linea=f.readlines()
      for i in linea:
            lista_participantes.append(i.strip().split(" "))
      return render_template('resultados.html',lista_participantes=lista_participantes)
        
if __name__ == '__main__':
   app.run(debug = True)
