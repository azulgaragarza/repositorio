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

    

class Jefe_departamento(Usuario):
    pass

class Usuario_final(Usuario):
    def crear_reclamo(self, asunto, descripcion):
        departamento = Clasificador_reclamos.clasificar_reclamo(asunto, descripcion)

        reclamo = Reclamo(
        usuario_creador=self.email,
        asunto=asunto,
        descripcion=descripcion,
        departamento=departamento,
        estado='Pendiente',
        adherente='',
        fecha=datetime.utcnow()
        )
        db.session.add(reclamo)
        db.session.commit()
    
    def adherirse_reclamo(self, reclamo_id):
        reclamo = Reclamo.query.get(reclamo_id)
        if reclamo:
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
    
    def __innit__(self, id, descripcion, fecha_hora, usuario_creador, departamento_id):
        self.id = id
        self.descripcion = descripcion
        self.fecha_hora = fecha_hora
        self.usuario_creador = usuario_creador
        self.departamento_id = departamento_id

class Departamento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.String(200))

    def __init__(self,nombre, descripcion):
        self.nombre = nombre
        self.descripcion = descripcion

    def crear_departamento(nombre, descripcion):
        departamento = Departamento(nombre=nombre, descripcion=descripcion)
        db.session.add(departamento)
        db.session.commit()

class Clasificador_reclamos():
    @staticmethod
    def clasificar_reclamo(asunto, descripcion):
       # Lógica de clasificación del reclamo en un departamento específico
        # Puedes implementar tus propias reglas de clasificación aquí
        # Por ejemplo, puedes utilizar palabras clave en el asunto o descripción del reclamo

        if 'facturación' in asunto.lower() or 'facturación' in descripcion.lower():
            return Departamento.query.filter_by(nombre='Departamento de Facturación').first()

        if 'soporte técnico' in asunto.lower() or 'soporte técnico' in descripcion.lower():
            return Departamento.query.filter_by(nombre='Departamento de Soporte Técnico').first()

        # Otras reglas de clasificación según tus necesidades

        # Si no se cumple ninguna regla, clasificar en un departamento por defecto
        return Departamento.query.filter_by(nombre='Departamento por Defecto').first()