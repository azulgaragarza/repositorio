import unittest
from server import app
from modules.class_clasificador_reclamos import Clasificador_reclamos
from modules.class_departamento import Departamento

class TestClasificador(unittest.TestCase):
    def test_departamento_1(self):  #(coordinacion academica)
        with app.app_context(): 
            departamento = Clasificador_reclamos()
            asunto="plan de estudio"
            descripcion="no encuentro el plan de estudio"
            resultado_obtenido = departamento.clasificar_reclamo(asunto,descripcion)
            #comparar si hace lo esperado
            palabras_clave_dpto1 = ['plan de estudio','currículo académico','programas académicos','carrera','horarios','aulas','calificación','calificaciones','catedra','profesor','examen','asignaturas','pasantías','materia']
            for palabra in palabras_clave_dpto1:
                if palabra in asunto or palabra in descripcion:
                    resultado_esperado = Departamento.query.filter_by(id=1).first()
                    return resultado_esperado
            self.assertEqual(resultado_obtenido,resultado_esperado)

    def test_departamento_2(self):
        with app.app_context():
            departamento = Clasificador_reclamos()
            asunto="no funciona el campus"
            descripcion="el campus esta caido"
            resultado_obtenido = departamento.clasificar_reclamo(asunto,descripcion)
            #comparar si hace lo esperado
            palabras_clave_dpto2 = ['campus','correo electrónico institucional','software institucional','gestión académica',' aula virtual','conexion','wifi']
            for palabra in palabras_clave_dpto2:
                if palabra in asunto or palabra in descripcion:
                    resultado_esperado = Departamento.query.filter_by(id=2).first()
                    return resultado_esperado
            self.assertEqual(resultado_obtenido,resultado_esperado)

    def test_departamento_3(self):
        with app.app_context():
            departamento = Clasificador_reclamos()
            asunto="beca estudiantil"
            descripcion="quisiera saber porque motivos no pude acceder a la beca estudiantil"
            resultado_obtenido = departamento.clasificar_reclamo(asunto,descripcion)
            #comparar si hace lo esperado
            palabras_clave_dpto3 = ['beca', 'salud', 'residencia', 'transporte','inscripcion','bienestar estudiantil','atención médica','actividades extracurriculares']
            for palabra in palabras_clave_dpto3:
                if palabra in asunto or palabra in descripcion:
                    resultado_esperado = Departamento.query.filter_by(id=3).first()
                    return resultado_esperado
            self.assertEqual(resultado_obtenido,resultado_esperado)

    def test_departamento_indefinido(self):
        with app.app_context():
            departamento = Clasificador_reclamos()
            asunto="llamo y no me contestan"
            descripcion="llamo a la facultad y nadie contesta"
            resultado_obtenido = departamento.clasificar_reclamo(asunto,descripcion)
            self.assertEqual(resultado_obtenido,None)

if __name__ == '__main__':
    unittest.main()
