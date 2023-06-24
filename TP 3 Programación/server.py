from flask import Flask, render_template, redirect, request, flash, url_for, abort
from flask_login import *
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

from modules.forms import LoginForm, RegisterForm
from modules.classes import Usuario
from modules.config import app, db, login_manager


with app.app_context():
    db.create_all() #crea la base de datos


@login_manager.user_loader
def user_loader(user_id):
    return Usuario.query.get(user_id)


admin_list = [1] 

def is_admin():
    if current_user.is_authenticated and current_user.id in admin_list:
        return True
    else:
        return False

def admin_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.id not in admin_list:
            return abort(403)
        return f(*args, **kwargs)
    return decorated_function

@app.route("/", methods=['GET','POST'])
def Login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        email = login_form.email.data
        password = login_form.password.data
        user = Usuario.query.filter_by(email=email).first()
        if not user: #controlar porque no hace esto
            flash("That email does not exist, please try again")
            return redirect(url_for("Login"))
        elif not check_password_hash(user.password, password):
            flash("Password incorrect, please try again.")
            return redirect(url_for("Login"))
        else:
            login_user(user)
            if is_admin():
                return redirect(url_for('jefe_departamento')) 
            else:
                return redirect(url_for('pantalla_principal'))   
    return render_template("login.html", form=login_form)

@app.route("/crear_usuario", methods=['GET','POST'])
def crear_usuario():
    register_form = RegisterForm()
    if register_form.validate_on_submit():
        if Usuario.query.filter_by(email=register_form.email.data).first():
            flash("You've already signed up with that email, log in instead!")
            return redirect(url_for('Login'))

        encripted_pass = generate_password_hash(
            password= register_form.password.data,
            method= 'pbkdf2:sha256',
            salt_length=8
        )
        new_user = Usuario(
            email = register_form.email.data,
            password = encripted_pass,
            name = register_form.name.data,
            apellido = register_form.apellido.data,
            claustro = register_form.claustro.data
            )
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for("Login"))
    return render_template('crear_usuario.html', form=register_form)

@app.route("/jefe_departamento", methods=['GET','POST'])
def jefe_departamento():
    return render_template('jefe_departamento.html')

@app.route("/pantalla_principal", methods=['GET','POST'])
@login_required
def pantalla_principal():
    return render_template('pantalla_principal.html')

@app.route("/crear_reclamo", methods=['GET','POST'])
def crear_reclamo():
    return render_template('crear_reclamo.html')


if __name__ == '__main__':
   app.run(debug = True)
