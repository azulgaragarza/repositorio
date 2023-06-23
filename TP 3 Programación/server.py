from flask import Flask, render_template, redirect, request

app = Flask(__name__)
@app.route("/", methods=['GET','POST'])
def ingreso():
    return render_template('ingreso.html')

@app.route("/crear_usuario", methods=['GET','POST'])
def crear_usuario():
    return render_template('crear_usuario.html')

@app.route("/pantalla_principal", methods=['GET','POST'])
def pantalla_principal():
    return render_template('pantalla_principal.html')

@app.route("/crear_reclamo", methods=['GET','POST'])
def crear_reclamo():
    return render_template('crear_reclamo.html')


if __name__ == '__main__':
   app.run(debug = True)
