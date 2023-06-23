from flask import Flask, render_template, redirect, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import *
from modules.forms import LoginForm, SignupForm


app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///usuarios.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
from modules.classes import *

login_manager = LoginManager()
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return Usuario.get_by_id(int(user_id))

user= None
@app.route("/", methods=['GET','POST'])
def Login():
    form = LoginForm()
    if form.validate_on_submit():
        global user
        user = Usuario.get_by_email(form.email.data)
    if user is not None and user.check_password(form.password.data):
        login_user(user, remember=form.remember_me.data)
    return render_template("login.html", form=form)

@app.route("/crear_usuario", methods=['GET','POST'])
def crear_usuario():
    if current_user.is_authenticated:
        return redirect('pantalla_principal.html')
    form = SignupForm()
    error = None
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        password = form.password.data
        # Comprobamos que no hay ya un usuario con ese email
        user = Usuario.get_by_email(email)
        if user is not None:
            error = f'El email {email} ya está siendo utilizado por otro usuario'
        else:
            # Creamos el usuario y lo guardamos
            user = Usuario(name=name, email=email)
            user.set_password(password)
            user.save()
            # Dejamos al usuario logueado
            login_user(user, remember=True)
    return render_template('crear_usuario.html',form=form, error=error)

@app.route("/pantalla_principal", methods=['GET','POST'])
def pantalla_principal():
    return render_template('pantalla_principal.html')

@app.route("/crear_reclamo", methods=['GET','POST'])
def crear_reclamo():
    return render_template('crear_reclamo.html')


if __name__ == '__main__':
   app.run(debug = True)
