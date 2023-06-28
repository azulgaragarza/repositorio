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

admin_list = [1,5,6] 

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

def departamento1_jefe_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        departamento = Departamento.query.filter_by(id=1).first()
        if not current_user.is_authenticated or not current_user.email==departamento.jefe:
            return abort(403)  # Acceso no autorizado
        return f(*args, **kwargs)
    return decorated_function

def departamento2_jefe_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        departamento = Departamento.query.filter_by(id=5).first()
        if not current_user.is_authenticated or not current_user.email==departamento.jefe:
            return abort(403)  # Acceso no autorizado
        return f(*args, **kwargs)
    return decorated_function

def departamento3_jefe_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        departamento = Departamento.query.filter_by(id=6).first()
        if not current_user.is_authenticated or not current_user.email==departamento.jefe:
            return abort(403)  # Acceso no autorizado
        return f(*args, **kwargs)
    return decorated_function


@app.route("/jefe_departamento", methods=['GET','POST'])
@admin_only
def jefe_departamento():
    nombre1 = "Departamento de Coordinación Académica"
    jefe_depto1 = Usuario.query.filter_by(id=1).first().email
    current_user.crear_departamento(nombre1,jefe_depto1)
    nombre2 = "Departamento de Soporte Técnico"
    jefe_depto2 = Usuario.query.filter_by(id=5).first().email
    current_user.crear_departamento(nombre2,jefe_depto2)
    nombre3 = "Departamento de Servicios Estudiantiles"
    jefe_depto3 = Usuario.query.filter_by(id=6).first().email
    current_user.crear_departamento(nombre3,jefe_depto3)

    login_form_d1 = LoginForm()
    if  login_form_d1.validate_on_submit():
        email = login_form_d1.email.data
        password = login_form_d1.password.data
        user = Usuario.query.filter_by(email=email).first()

        if user.id not in admin_list:
            flash("El email que ingresaste no es de jefe de departamento, intenta de nuevo")
            return redirect(url_for('jefe_departamento'))
        elif not check_password_hash(user.password, password):
            flash("Contraseña incorrecta, intenta de nuevo")
            return redirect(url_for('jefe_departamento'))
        else:
            return redirect('/departamento_1')
        
    login_form_d2 = LoginForm() #cambiar estoooo
    if  login_form_d2.validate_on_submit():
        email = login_form_d1.email.data
        password = login_form_d1.password.data
        user = Usuario.query.filter_by(email=email).first()

        if user.id not in admin_list:
            flash("El email que ingresaste no es de jefe de departamento, intenta de nuevo")
            return redirect(url_for('jefe_departamento'))
        elif not check_password_hash(user.password, password):
            flash("Contraseña incorrecta, intenta de nuevo")
            return redirect(url_for('jefe_departamento'))
        else:
            return redirect('/departamento_2')

    return render_template('jefe_departamento.html',form_d1=login_form_d1,form_d2=login_form_d2)


@app.route("/departamento_1", methods=['GET','POST'])
@admin_only
@departamento1_jefe_only
def departamento_1():
    return render_template('departamento_1.html')

@app.route("/departamento_2", methods=['GET','POST'])
@admin_only
@departamento2_jefe_only
def departamento_2():
    return render_template('departamento_2.html')

if __name__ == '__main__':
   app.run(debug = True)
