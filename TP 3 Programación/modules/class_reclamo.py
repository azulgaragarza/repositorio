from server import db
from datetime import datetime

class Reclamo(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    usuario_creador = db.Column(db.String(100))
    asunto = db.Column(db.String(1000))
    descripcion = db.Column(db.String(1000))
    departamento_id = db.Column(db.Integer, db.ForeignKey('departamento.id'), nullable=True)
    estado =  db.Column(db.String(100))
    adherente = db.Column(db.String(100))
    fecha = db.Column(db.DateTime, default=datetime.utcnow)

    
    def __init__(self, id, asunto, descripcion, fecha, usuario_creador, estado, adherente, departamento_id):
        self.id = id
        self.asunto = asunto
        self.descripcion = descripcion
        self.fecha = fecha
        self.usuario_creador = usuario_creador
        self.departamento_id = departamento_id
        self.estado = estado
        self.adherente = adherente
