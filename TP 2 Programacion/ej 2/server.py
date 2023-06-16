from flask import Flask, render_template, request
from modules.classes import *
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
    mensaje=""
    if request.method == 'POST':
        cant_alimentos=request.form["cant_alimentos"]
        random.seed(1)
        sensor = DetectorAlimento()
        lista_pesos = []
        lista_alimentos = []
        for i in range(int(cant_alimentos)):
            lista_pesos.append(sensor.detectar_alimento()["peso"])
            lista_alimentos.append(sensor.detectar_alimento()["alimento"])

        cajon = Cajon(lista_pesos,lista_alimentos)
        cajon.crear_objetos()
        cajon.aw_prom_kiwis()
        cajon.aw_prom_manzanas()
        cajon.aw_prom_papa()
        cajon.aw_prom_zanahorias()
        cajon.aw_prom_frutas()
        cajon.aw_prom_verduras()
        cajon.aw_prom_total(int(cant_alimentos))

        global aw_promedio_kiwi 
        aw_promedio_kiwi = cajon.prom_k
        global aw_promedio_manzana 
        aw_promedio_manzana = cajon.prom_m
        global aw_promedio_zanahoria
        aw_promedio_zanahoria = cajon.prom_z
        global aw_promedio_papa
        aw_promedio_papa = cajon.prom_p
        global aw_promedio_frutas 
        aw_promedio_frutas = cajon.prom_frutas
        global aw_promedio_verduras
        aw_promedio_verduras = cajon.prom_verduras
        global aw_promedio_total 
        aw_promedio_total = cajon.promedio_total

        if aw_promedio_kiwi>=0.95 or aw_promedio_manzana>=0.95 or aw_promedio_zanahoria>=0.95 or aw_promedio_papa>=0.95:
            mensaje="Se recomienda inspeccion del cajon" 

    return render_template('Home.html', mensaje=mensaje, prom_kiwi=aw_promedio_kiwi, prom_manzana=aw_promedio_manzana, prom_zana=aw_promedio_zanahoria,prom_papa=aw_promedio_papa,prom_frutas=aw_promedio_frutas, prom_verdu=aw_promedio_verduras,prom_total=aw_promedio_total)

if __name__ == '__main__':
   app.run(debug = True)
