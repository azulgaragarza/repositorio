from server import db

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
