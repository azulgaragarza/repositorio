from flask import Flask, render_template, request, redirect
from modules.classes import *
app = Flask(__name__)
@app.route("/", methods=['GET','POST'])
def home():
    mensaje="Se recomienda inspeccion del cajon"
    if request.method == 'POST':
        cant_alimentos=request.form["cant_alimentos"]
    return render_template('Home.html',mensaje=mensaje)

if __name__ == '__main__':
   app.run(debug = True)
