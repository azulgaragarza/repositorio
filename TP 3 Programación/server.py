from flask import Flask, render_template, redirect, request, flash, url_for, abort
from flask_login import *
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_
from modules.forms import LoginForm, RegisterForm
#from werkzeug.utils import secure_filename
#from flask_uploads import UploadSet, configure_uploads, IMAGES



db = SQLAlchemy()
from modules.classes import *
app = Flask(__name__)
app.secret_key = 'my_secret_key'
#photos = UploadSet('photos', IMAGES) #para subir fotos
#app.config['UPLOADED_PHOTOS_DEST'] = 'data'
#configure_uploads(app, photos)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)


login_manager = LoginManager()
login_manager.init_app(app)

with app.app_context():
    db.create_all() #crea la base de datos

admin_list = [1] 

def is_admin():
        if current_user.is_authenticated and current_user.id in admin_list:
            return True
        else:
            return False

@login_manager.user_loader
def user_loader(user_id):
    user = Usuario.query.get(user_id)
    if user:
        if user.id in admin_list:
            return Jefe_departamento.query.get(user_id)
        else:
            return Usuario_final.query.get(user_id)

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
        if not user:
            flash("El email que ingresaste no existe, intenta de nuevo")
            return redirect(url_for("Login"))
        elif not check_password_hash(user.password, password):
            flash("Contraseña incorrecta, intenta de nuevo")
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
            flash("Ya te registraste con ese email, puedes iniciar sesion!")
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
@admin_only
def jefe_departamento():
    return render_template('jefe_departamento.html')

@app.route("/pantalla_principal", methods=['GET','POST'])
@login_required
def pantalla_principal():
    return render_template('pantalla_principal.html')


@app.route("/crear_reclamo", methods=['GET','POST'])
@login_required
def crear_reclamo():
    if request.method == 'POST': #and 'photo' in request.files:
        asunto = request.form['asunto']
        desc_reclamo = request.form['reclamo']
        
        #file = request.files['imagen']
        #data = file.read()

        # Buscar reclamos similares en la base de datos
        reclamos_similares = Reclamo.query.filter(
            or_(
                Reclamo.asunto.ilike(f'%{asunto}%'),  # Búsqueda insensible a mayúsculas y minúsculas
                Reclamo.descripcion.ilike(f'%{desc_reclamo}%')
            )
        ).all()
        
        if reclamos_similares:
            # Hay reclamos similares, mostrar la opción de adherirse
        
            return render_template('adherirse_reclamo.html', reclamos=reclamos_similares)
        else:
            # Crear un nuevo reclamo
            current_user.crear_reclamo(asunto, desc_reclamo)

            flash("Reclamo creado exitosamente.")
    return render_template('crear_reclamo.html')

@app.route("/adherir_reclamo/<int:reclamo_id>", methods=['POST'])
@login_required
def adherir_reclamo(reclamo_id):
    reclamo = Reclamo.query.get(reclamo_id)

    if reclamo:
        reclamo.adherente = current_user.email
        current_user.crear_reclamo(reclamo.asunto, f'adherido a reclamo {reclamo.id}')
        db.session.commit()
        flash("Adherido a reclamo existente.")
    else:
        flash("El reclamo no existe.")
        return redirect(url_for('pantalla_principal'))
    return redirect(url_for('pantalla_principal'))

if __name__ == '__main__':
   app.run(debug = True)
