from flask import Flask, render_template, request, redirect
from modules.classes import *
from modules.functions import *
import random
lista_objetos = []
aw_promedio_kiwi = 0
aw_promedio_manzana = 0
aw_promedio_zanahoria = 0
aw_promedio_papa = 0
aw_promedio_frutas = 0
aw_promedio_verduras = 0
aw_promedio_total = 0

app = Flask(__name__)
@app.route("/", methods=['GET','POST'])

def home():
    mensaje="Se recomienda inspeccion del cajon"

    if request.method == 'POST':
        cant_alimentos=request.form["cant_alimentos"]
        random.seed(1)
        sensor = DetectorAlimento()
        lista_pesos = []
        lista_alimentos = []
        lista_objetos=[]
        for i in range(cant_alimentos):
            lista_pesos.append(sensor.detectar_alimento()["peso"])
            lista_alimentos.append(sensor.detectar_alimento()["alimento"])
        
        crear_objetos(lista_pesos,lista_alimentos,lista_objetos)

        promedio = aw_promedio(obj_kiwi,obj_manzana,obj_zanahoria,obj_papa)
        promedio.aw_prom_kiwis()
        promedio.aw_prom_manzanas()
        promedio.aw_prom_papa()
        promedio.aw_prom_zanahorias()
        promedio.aw_prom_frutas()
        promedio.aw_prom_verduras()
        promedio.prom_total()

        global aw_promedio_kiwi 
        aw_promedio_kiwi = promedio.prom_k
        global aw_promedio_manzana 
        aw_promedio_manzana = promedio.prom_m
        global aw_promedio_zanahoria
        aw_promedio_zanahoria = promedio.prom_z
        global aw_promedio_papa
        aw_promedio_papa = promedio.prom_p
        global aw_promedio_frutas 
        aw_promedio_frutas = promedio.prom_frutas
        global aw_promedio_verduras
        aw_promedio_verduras = promedio.prom_verduras
        global aw_promedio_total 
        aw_promedio_total = promedio.promedio_total

    return render_template('Home.html',mensaje=mensaje,prom_kiwi=aw_promedio_kiwi, prom_manzana=aw_promedio_manzana, prom_zana=aw_promedio_zanahoria,prom_papa=aw_promedio_papa,prom_frutas=aw_promedio_frutas, prom_verdu=aw_promedio_verduras,prom_total=aw_promedio_total)

if __name__ == '__main__':
   app.run(debug = True)
