from flask_login import UserMixin
from server import db
from datetime import datetime
from flask_login import current_user

class Usuario(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    apellido = db.Column(db.String(1000))
    claustro = db.Column(db.String(100))

    def __init__(self, email, password, name, apellido,claustro):
        self.email = email
        self.password = password
        self.name = name
        self.apellido = apellido
        self.claustro = claustro


class Usuario_final(Usuario):
    def crear_reclamo(self, asunto, descripcion):
        departamento = Clasificador_reclamos.clasificar_reclamo(asunto, descripcion)
        if departamento is None:
            departamento = "Esperando asignacion de departamento"
        reclamo = Reclamo(
        id = None,
        usuario_creador=self.email,
        asunto=asunto,
        descripcion=descripcion,
        departamento=departamento,
        estado='Pendiente',
        adherente='',
        fecha=datetime.utcnow(),
        departamento_id=departamento.id
        )
        db.session.add(reclamo)
        db.session.commit()
    
    def adherirse_reclamo(self, reclamo_id):
        reclamo = Reclamo.query.get(reclamo_id)
        if reclamo:
            if reclamo.usuario_creador == current_user.email:
                return "No se puede"
            else:
                if reclamo.adherente == '':
                    reclamo.adherente = current_user.email
                else:
                    if current_user.email not in reclamo.adherente:
                        reclamo.adherente = reclamo.adherente + f', { current_user.email}'
                    else:
                        return False
            db.session.commit()
            return True
        else:
            return False
    

class Reclamo(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    usuario_creador = db.Column(db.String(100))
    asunto = db.Column(db.String(1000))
    descripcion = db.Column(db.String(1000))
    departamento_id = db.Column(db.Integer, db.ForeignKey('departamento.id'))
    departamento = db.relationship('Departamento', backref=db.backref('reclamos'))
    estado =  db.Column(db.String(100))
    adherente = db.Column(db.String(100))
    fecha = db.Column(db.DateTime, default=datetime.utcnow)
    #imagen = db.Column(db.LargeBinary)
    
    def __init__(self, id, asunto, descripcion, fecha, usuario_creador, departamento, departamento_id, estado, adherente):
        self.id = id
        self.asunto = asunto
        self.descripcion = descripcion
        self.fecha = fecha
        self.usuario_creador = usuario_creador
        self.departamento = departamento
        self.departamento_id = departamento_id
        self.estado = estado
        self.adherente = adherente

class Jefe_departamento(Usuario):
    def crear_departamento(self,nombre,jefe):
        departamento = Departamento.query.filter_by(nombre=nombre).first()
        if not departamento:
            departamento = Departamento(nombre=nombre,jefe=jefe)
            db.session.add(departamento)
            db.session.commit()

class Departamento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    jefe = db.Column(db.String(200))

    def __init__(self, nombre, jefe):
        self.nombre = nombre
        self.jefe = jefe
        
    def cambiar_jefe(self,jefe_nuevo,id_depto):
        departamento = Departamento.query.filter_by(id=id_depto).first()
        departamento.jefe = jefe_nuevo
        db.session.commit()

class Clasificador_reclamos():
    @staticmethod
    def clasificar_reclamo(asunt, description):
        palabras_clave_dpto1 = ['plan de estudio','currículo académico','programas académicos','carrera','horarios','aulas','calificación','calificaciones','catedra','profesor','examen','asignaturas','pasantías','materia']
        palabras_clave_dpto2 = ['campus','correo electrónico institucional','software institucional','gestión académica',' aula virtual','conexion','wifi']
        palabras_clave_dpto3 = ['beca', 'salud', 'residencia', 'transporte','inscripcion','bienestar estudiantil','atención médica','Actividades extracurriculares']

        asunto = asunt.lower()
        descripcion = description.lower()

        for palabra in palabras_clave_dpto1:
            if palabra in asunto or palabra in descripcion:
                return Departamento.query.filter_by(id=1).first()

        for palabra in palabras_clave_dpto2:
            if palabra in asunto or palabra in descripcion:
                return Departamento.query.filter_by(id=2).first()
    
        for palabra in palabras_clave_dpto3:
            if palabra in asunto or palabra in descripcion:
                return Departamento.query.filter_by(id=3).first()
        
        # Si no se cumple ninguna regla, clasificar en un departamento por defecto
        return None