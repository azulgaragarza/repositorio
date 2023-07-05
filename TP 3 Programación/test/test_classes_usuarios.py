import unittest
from flask_login import login_user
from server import app, db
import os

from modules.classes_usuarios import Usuario_final, Jefe_departamento
from modules.class_reclamo import Reclamo
from modules.class_departamento import Departamento

class TestUsuarioFinal(unittest.TestCase):
    def test_crear_reclamo(self):
        with app.app_context():
            asunto="asunto de prueba"
            descripcion="descripcion de prueba"
            #defino un usuario cualquiera (que no sea jefe de departamento)
            usuario_final = Usuario_final.query.filter_by(id=4).first()
            usuario_final.crear_reclamo(asunto,descripcion)
            reclamo_creado = Reclamo.query.filter_by(asunto=asunto).first()
            self.assertIsNotNone(reclamo_creado)
            self.assertEqual(reclamo_creado.asunto,asunto)
            self.assertEqual(reclamo_creado.descripcion,descripcion)
            self.assertEqual(reclamo_creado.usuario_creador,usuario_final.email)
            self.assertEqual(reclamo_creado.departamento_id,None)
            #elimino elemento de prueba de la base de datos
            db.session.delete(reclamo_creado)
            db.session.commit()

    def test_adherirse_a_reclamo(self):
        with app.app_context():
            asunto="asunto de prueba"
            descripcion="descripcion de prueba"
            #defino un usuario cualquiera (que no sea jefe de departamento)
            usuario_final1 = Usuario_final.query.filter_by(id=4).first()
            usuario_final2 = Usuario_final.query.filter_by(id=5).first()
            #creo un reclamo
            usuario_final1.crear_reclamo(asunto,descripcion)
            #obtengo el reclamo
            reclamo = Reclamo.query.filter_by(asunto=asunto).first()
            #defino el usuario 2 como current_user 
            with app.test_request_context():
                login_user(usuario_final2)
                resultado_1 = usuario_final2.adherirse_reclamo(reclamo.id)
                resultado_3 = usuario_final2.adherirse_reclamo(reclamo.id)
                self.assertEqual(resultado_1,True)
                self.assertEqual(resultado_3,False)
            #defino el usuario 1 como current_user
            with app.test_request_context():
                login_user(usuario_final1)
                resultado_2 = usuario_final1.adherirse_reclamo(reclamo.id)
                self.assertEqual(resultado_2,"No se puede")
            db.session.delete(reclamo)
            db.session.commit()

class TestJefeDepartamento(unittest.TestCase):
    def test_crear_departamento(self):
        with app.app_context():
            usuario_jefe = Jefe_departamento.query.filter_by(id=2).first() #usuario secretario tecnico
            nombre_departamento = "departamento prueba"
            jefe = "jefe prueba"
            resultado = usuario_jefe.crear_departamento(nombre_departamento,jefe)
            departamento_nuevo = Departamento.query.filter_by(nombre=nombre_departamento).first()
            self.assertIsNotNone(departamento_nuevo)
            self.assertEqual(departamento_nuevo.nombre,nombre_departamento)
            self.assertEqual(departamento_nuevo.jefe,jefe)
            self.assertEqual(resultado,"Departamento creado")
            #borro los cambios
            db.session.delete(departamento_nuevo)
            db.session.commit()
            #prueba cuando el departamento ya existe
            nombre_departamento2 = "Departamento de Coordinación Académica"
            resultado2 = usuario_jefe.crear_departamento(nombre_departamento2,jefe)
            self.assertEqual(resultado2,"El departamento ya existe")

    def test_cambiar_estado(self):
        with app.app_context():
            usuario_jefe = Jefe_departamento.query.filter_by(id=1).first()
            #creo un reclamo
            asunto="asunto de prueba"
            descripcion="descripcion de prueba"
            usuario_final = Usuario_final.query.filter_by(id=4).first()
            usuario_final.crear_reclamo(asunto,descripcion)
            #busco el reclamo
            reclamo = Reclamo.query.filter_by(asunto=asunto).first()
            #cambiar de pendiente a resuelto
            usuario_jefe.cambiar_estado(reclamo.id,"Resuelto")
            self.assertEqual(reclamo.estado,"Resuelto")
            #cambiar de pendiente a en proceso
            usuario_jefe.cambiar_estado(reclamo.id,"En proceso")
            self.assertEqual(reclamo.estado,"En proceso")
            #cambiar de pendiente a invalido
            usuario_jefe.cambiar_estado(reclamo.id,"Invalido")
            self.assertEqual(reclamo.estado,"Invalido")
            #borro los cambios
            db.session.delete(reclamo)
            db.session.commit()
   
    def test_derivar_reclamo(self):
        with app.app_context():
            usuario_jefe = Jefe_departamento.query.filter_by(id=2).first() #secretario tecnico
            #creo un reclamo
            asunto="asunto de prueba"
            descripcion="descripcion de prueba"
            usuario_final = Usuario_final.query.filter_by(id=4).first()
            usuario_final.crear_reclamo(asunto,descripcion)
            #busco el reclamo
            reclamo = Reclamo.query.filter_by(asunto=asunto).first()
            #derivar al primer departamento
            usuario_jefe.derivar_reclamo(reclamo.id,"1")
            self.assertEqual(reclamo.departamento_id,1)
            #derivar al segundo departamento
            usuario_jefe.derivar_reclamo(reclamo.id,"2")
            self.assertEqual(reclamo.departamento_id,2)
            #derivar al tercer departamento
            usuario_jefe.derivar_reclamo(reclamo.id,"3")
            self.assertEqual(reclamo.departamento_id,3)
            db.session.delete(reclamo)
            db.session.commit()
    def test_generar_graficos(self):
        with app.app_context():
            usuario_jefe = Jefe_departamento.query.filter_by(id=1).first()
            with app.test_request_context():
                login_user(usuario_jefe)
                usuario_jefe.generar_graficos()
                self.assertTrue(os.path.exists('static\\grafico.png'))
                self.assertTrue(os.path.exists('static\\grafico_palabras_claves.png'))

if __name__ == '__main__':
    unittest.main()