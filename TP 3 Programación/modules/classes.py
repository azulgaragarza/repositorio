from flask_login import UserMixin
from server import db
from datetime import datetime

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
    pass

class Reclamo(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    usuario_creador = db.Column(db.String(100))
    asunto = db.Column(db.String(1000))
    descripcion = db.Column(db.String(1000))
    departamento = db.Column(db.String(100))
    estado =  db.Column(db.String(100))
    adherente = db.Column(db.String(100))
    fecha = db.Column(db.DateTime, default=datetime.utcnow)
    imagen = db.Column(db.LargeBinary)
    
    def __innit__(self, id, descripcion, fecha_hora, usuario_creador):
        self.id = id
        self.descripcion = descripcion
        self.fecha_hora = fecha_hora
        self.usuario_creador = usuario_creador

