import unittest
from server import app
from modules.class_departamento import Departamento

class TestDepartamento(unittest.TestCase):
    def test_cambiar_jefe(self):
        with app.app_context():
            departamento = Departamento.query.filter_by(id=1).first()
            jefe_anterior = departamento.jefe
            jefe_nuevo="jefe_nuevo@gmail.com"
            departamento.cambiar_jefe(jefe_nuevo,1)
            self.assertEqual(departamento.jefe,jefe_nuevo)
            #volver al jefe anterior
            departamento.cambiar_jefe(jefe_anterior,1)

if __name__ == '__main__':
    unittest.main()