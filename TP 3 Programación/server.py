from flask import Flask, render_template, redirect, request, flash, url_for, abort
from flask_login import *
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_
from modules.forms import LoginForm, RegisterForm
import os
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

admin_list = [1,3] 
secretario_tecnico_list = [2]

def is_admin():
        if current_user.is_authenticated and current_user.id in admin_list:
            return True
        else:
            return False

@login_manager.user_loader
def user_loader(user_id):
    user = Usuario.query.get(user_id)
    if user:
        if user.id in secretario_tecnico_list:
            return Secretario_tecnico.query.get(user_id)
        elif user.id in admin_list:
            return Jefe_departamento.query.get(user_id)  #en base al id clasifica al usuario actual en jefe o usuario final
        else:
            return Usuario_final.query.get(user_id)

def admin_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.id not in admin_list:
            return abort(403)
        return f(*args, **kwargs)
    return decorated_function

def secretary_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.id not in secretario_tecnico_list:
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
            return render_template('adherirse_reclamo.html', reclamos=reclamos_similares)
        else:
            current_user.crear_reclamo(asunto, desc_reclamo)
            flash("Reclamo creado exitosamente.")
    return render_template('crear_reclamo.html')

@app.route("/adherir_reclamo/<int:reclamo_id>", methods=['POST'])
@login_required
def adherirse_reclamo(reclamo_id):
    adherido_reclamo = current_user.adherirse_reclamo(reclamo_id)

    if adherido_reclamo == True:
        flash("Adherido a reclamo existente.")
    elif adherido_reclamo == False:
        flash("Ya te encuentras adherido a este reclamo.")
    elif adherido_reclamo == "No se puede":
        flash("Tú hiciste este reclamo, no puedes ser un adherente.")
    return redirect(url_for('pantalla_principal'))


@app.route("/lista_reclamos", methods=['GET','POST'])
@login_required
def lista_reclamos():
    detalles = {}
    departamentos = Departamento.query.all()
    departamento_id = request.args.get('departamento_id',default=None)  # Obtener el ID del departamento seleccionado en el filtro
    reclamos_pendientes = Reclamo.query.filter_by(estado='Pendiente') # Obtener todos los reclamos pendientes
    if departamento_id:
        reclamos_pendientes = reclamos_pendientes.filter(Reclamo.departamento_id == departamento_id)  # Aplicar filtro por departamento
    reclamos = reclamos_pendientes.all()

    if request.method == 'POST':
        id = int(request.form['id'])
        creador = request.form['creador']
        fecha = request.form['fecha']
        estado = request.form['estado']
        adherente = request.form['adherente']
        departamento = request.form['departamento']
        detalles = {"id":id,"creador":creador,"fecha":fecha,"estado":estado,"adherente":adherente,"departamento":departamento}
    return render_template('lista_reclamos.html', reclamos=reclamos, detalles=detalles,user=current_user.email,departamentos=departamentos)

@app.route("/mis_reclamos", methods=['GET','POST'])
@login_required
def mis_reclamos():
    mis_reclamos = Reclamo.query.filter_by(usuario_creador=current_user.email)
    return render_template('mis_reclamos.html',mis_reclamos=mis_reclamos)



@app.route("/jefe_departamento", methods=['GET','POST'])
def jefe_departamento():
    login_form_d = LoginForm()
    if  login_form_d.validate_on_submit():
        email = login_form_d.email.data
        password = login_form_d.password.data
        user = Usuario.query.filter_by(email=email).first()
        if user.id not in admin_list:
            flash("El email que ingresaste no es de jefe de departamento, intenta de nuevo")
            return redirect(url_for('jefe_departamento'))
        elif not check_password_hash(user.password, password):
            flash("Contraseña incorrecta, intenta de nuevo")
            return redirect(url_for('jefe_departamento'))
        elif user.id in admin_list:
            login_user(user)
            return redirect('/departamento')
        elif user.id in secretario_tecnico_list:
            login_user(user)
            return redirect('/secretario_tecnico')
        
    return render_template('jefe_departamento.html',form_d=login_form_d)


@app.route("/departamento", methods=['GET','POST'])
@admin_only
def departamento():
    nombre1 = "Departamento de Coordinación Académica"
    jefe_depto1 = Usuario.query.filter_by(id=1).first().email
    current_user.crear_departamento(nombre1,jefe_depto1)
    nombre2 = "Departamento de Soporte Técnico"
    jefe_depto2 = Usuario.query.filter_by(id=2).first().email
    current_user.crear_departamento(nombre2,jefe_depto2)
    nombre3 = "Departamento de Servicios Estudiantiles"
    jefe_depto3 = Usuario.query.filter_by(id=3).first().email
    current_user.crear_departamento(nombre3,jefe_depto3) #crear los departamentos

    departamento = Departamento.query.filter_by(id=current_user.id).first()
    return render_template('departamento.html',departamento=departamento)

@app.route("/analitica", methods=['GET','POST'])
@admin_only
def analitica():
    # Eliminar la imagen existente si existe
    if os.path.exists('static\\grafico.png'):
        os.remove('static\\grafico.png')
    if os.path.exists('static\\grafico_palabras_claves.png'):
        os.remove('static\\grafico_palabras_claves.png')
    current_user.generar_graficos()
    return render_template('analitica.html')

@app.route("/manejar_reclamo", methods=['GET','POST'])
@admin_only
def manejar_reclamo():
    departamento = Departamento.query.filter_by(id=current_user.id).first()
    reclamos = Reclamo.query.filter_by(departamento_id=departamento.id).all()
    users = Usuario.query.all()
    usuarios = []
    for usuario in users:
        if usuario.id not in admin_list:
            usuarios.append(usuario)
    if request.method == 'POST':
        reclamo_id = request.form.get('reclamo_id')
        estado = request.form.get('estado')
        print("ID del reclamo:", reclamo_id)
        print("Nuevo estado:", estado)
        if reclamo_id is not None and estado is not None:
            current_user.cambiar_estado(reclamo_id,estado)

    return render_template('manejar_reclamo.html',reclamos=reclamos,usuarios=usuarios)

@app.route("/ayuda", methods=['GET','POST'])
@admin_only
def ayuda():
    return render_template('ayuda.html')

@app.route("/secretario_tecnico", methods=['GET','POST'])
@secretary_only
def secretario_tecnico():
    return render_template('secretario_tecnico.html')

if __name__ == '__main__':
   app.run(debug = True)
