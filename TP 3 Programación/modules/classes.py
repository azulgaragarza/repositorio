from flask_login import UserMixin
from config import db

class Usuario(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    apellido = db.Column(db.String(1000))
    claustro = db.Column(db.String(100))

    def __init__(self, email, password, name, apellido,claustro):
        self.email = email
        self.contraseña = password
        self.nombre = name
        self.apellido = apellido
        self.claustro = claustro


class Jefe_departamento(Usuario):
    pass

