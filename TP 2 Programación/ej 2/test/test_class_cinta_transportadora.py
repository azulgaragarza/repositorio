import unittest
from modules.class_cinta_transportadora import Cinta_Transportadora
from modules.class_alimentos import *

class TestCintaTransportadora(unittest.TestCase):
    def test_crear_listas(self):
        cinta = Cinta_Transportadora()
        cant_alimentos = 4
        cinta.crear_listas(cant_alimentos)
        self.assertEqual(len(cinta.alimentos),4)
        self.assertEqual(len(cinta.pesos),4)
        self.assertNotIn("undefined", cinta.alimentos)
        
    def test_crear_objetos(self):
        #vacio
        cinta = Cinta_Transportadora()
        cinta.alimentos = []
        cinta.pesos = []
        cinta.crear_objetos()
        self.assertEqual(cinta.lista_objetos,[])
        #con datos 
        cinta2 = Cinta_Transportadora()
        cinta2.alimentos = ["kiwi","manzana","papa","zanahoria"]
        cinta2.pesos = [0.550,0.600,0.400,0.300]
        cinta2.crear_objetos()
        #si los objetos son instancias de las clases
        self.assertIsInstance(cinta2.lista_objetos[0], Kiwi)
        self.assertIsInstance(cinta2.lista_objetos[1], Manzana)
        self.assertIsInstance(cinta2.lista_objetos[2], Papa)
        self.assertIsInstance(cinta2.lista_objetos[3], Zanahoria)
        #que los pesos se asignen
        self.assertEqual(cinta2.lista_objetos[0].masa, cinta2.pesos[0])
        self.assertEqual(cinta2.lista_objetos[1].masa, cinta2.pesos[1])
        self.assertEqual(cinta2.lista_objetos[2].masa, cinta2.pesos[2])
        self.assertEqual(cinta2.lista_objetos[3].masa, cinta2.pesos[3])

if __name__ == '__main__':
    unittest.main()
