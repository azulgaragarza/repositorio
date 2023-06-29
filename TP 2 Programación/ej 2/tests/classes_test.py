import unittest
from unittest.mock import patch
from modules.classes import Kiwi,Manzana,Papa,Zanahoria,Cinta_Transportadora,Cajon,DetectorAlimento
import numpy as np


class TestClasses(unittest.TestCase):
    def test_aw_frutas_kiwi(self):
        kiwi = Kiwi()
        kiwi.aw_frutas(0.5)
        self.assertAlmostEqual(kiwi.aw_kiwi, 0.96)
    def test_aw_frutas_manzana(self):
        manzana = Manzana()
        manzana.aw_frutas(0.5)
        self.assertAlmostEqual(manzana.aw_manzana, 0.95)
    def test_aw_verduras_papa(self):
        papa = Papa()
        papa.aw_verduras(0.5)
        self.assertAlmostEqual(papa.aw_papa, 0.96)
    def test_aw_verduras_zanahoria(self):
        zanahoria = Zanahoria()
        zanahoria.aw_verduras(0.5)
        self.assertAlmostEqual(zanahoria.aw_zanahoria, 0.95)

class TestCintaTransportadora(unittest.TestCase):
    def test_crear_objetos(self):
        #vacio
        cinta = Cinta_Transportadora([],[])
        cinta.crear_objetos()
        self.assertEqual(cinta.lista_objetos,[])
        #con datos 
        alimentos = ["kiwi","manzana","papa","undefined","zanahoria"]
        pesos = [0.550,0.600,0.400,0.300,0.400]
        cinta2 = Cinta_Transportadora(pesos,alimentos)
        cinta2.crear_objetos()
        #comprobar que se creen los objetos sin los elementos undefined
        self.assertEqual(len(cinta2.lista_objetos), len(alimentos)-1)
        #si los objetos son instancias de las clases
        self.assertIsInstance(cinta2.lista_objetos[0], Kiwi)
        self.assertIsInstance(cinta2.lista_objetos[1], Manzana)
        self.assertIsInstance(cinta2.lista_objetos[2], Papa)
        self.assertIsInstance(cinta2.lista_objetos[3], Zanahoria)
        #que los pesos se asignen
        self.assertEqual(cinta2.lista_objetos[0].masa, pesos[0])
        self.assertEqual(cinta2.lista_objetos[1].masa, pesos[1])
        self.assertEqual(cinta2.lista_objetos[2].masa, pesos[2])
        self.assertEqual(cinta2.lista_objetos[3].masa, pesos[4])

class TestCajon(unittest.TestCase):
    def test_aw_prom_kiwis(self):
        cajon = Cajon([], [])
        kiwi1 = Kiwi()
        kiwi1.aw_kiwi = 0.5
        kiwi2 = Kiwi()
        kiwi2.aw_kiwi = 0.8
        kiwi3 = Kiwi()
        kiwi3.aw_kiwi = 0.6
        cajon.lista_objetos = [kiwi1, kiwi2, kiwi3]
        cajon.aw_prom_kiwis()
        self.assertEqual(cajon.prom_k, 0.63)
        cajon2 = Cajon([], [])
        cajon2.aw_prom_kiwis()
        self.assertEqual(cajon2.prom_k, 0)

    def test_aw_prom_manzanas(self):
        cajon = Cajon([], [])
        manzana1 = Manzana()
        manzana1.aw_manzana = 0.9
        manzana2 = Manzana()
        manzana2.aw_manzana = 0.7
        manzana3 = Manzana()
        manzana3.aw_manzana = 0.8
        cajon.lista_objetos = [manzana1, manzana2, manzana3]
        cajon.aw_prom_manzanas()
        self.assertEqual(cajon.prom_m, 0.80)
        cajon2 = Cajon([], [])
        cajon2.aw_prom_manzanas()
        self.assertEqual(cajon2.prom_m, 0)

    def test_aw_prom_papas(self): #partes de una prueba unitaria (AAA)
        cajon = Cajon([], []) #arrange
        papa1 = Papa()
        papa1.aw_papa = 0.7
        papa2 = Papa()
        papa2.aw_papa = 0.7
        papa3 = Papa()
        papa3.aw_papa = 0.9
        cajon.lista_objetos = [papa1, papa2, papa3] #act
        cajon.aw_prom_papas()
        self.assertEqual(cajon.prom_p, 0.77) #assert 
        cajon2 = Cajon([], [])
        cajon2.aw_prom_papas()
        self.assertEqual(cajon2.prom_p, 0)
    
    def test_aw_prom_zanahorias(self):
        cajon = Cajon([], [])
        zanahoria1 = Zanahoria()
        zanahoria1.aw_zanahoria = 0.7
        zanahoria2 = Zanahoria()
        zanahoria2.aw_zanahoria = 0.8
        zanahoria3 = Zanahoria()
        zanahoria3.aw_zanahoria = 0.8
        cajon.lista_objetos = [zanahoria1, zanahoria2, zanahoria3]
        cajon.aw_prom_zanahorias()
        self.assertEqual(cajon.prom_z, 0.77)
        cajon2 = Cajon([], [])
        cajon2.aw_prom_zanahorias()
        self.assertEqual(cajon2.prom_z, 0)

    def test_aw_prom_verduras(self):
        #sin objetos en la lista
        cajon = Cajon([], [])
        self.assertEqual(cajon.aw_prom_verduras(), None)
        #objetos de prueba
        papa1 = Papa()
        papa1.aw_verduras(0.5)
        zanahoria1 = Zanahoria()
        zanahoria1.aw_verduras(0.4)
        papa2 = Papa()
        papa2.aw_verduras(0.3)
        cajon.lista_objetos = [papa1, zanahoria1, papa2]
        #promedio de verduras
        promedio = (papa1.aw_papa + zanahoria1.aw_zanahoria + papa2.aw_papa) / 3
        promedio_redondeado = round(promedio, 2)
        cajon.aw_prom_verduras()
        self.assertEqual(cajon.prom_verduras, promedio_redondeado) 

    def test_aw_prom_frutas(self):
        #sin objetos en la lista
        cajon = Cajon([], [])
        self.assertEqual(cajon.aw_prom_frutas(), None)
        #objetos de prueba
        kiwi1 = Kiwi()
        kiwi1.aw_frutas(0.5)
        manzana1 = Manzana()
        manzana1.aw_frutas(0.4)
        kiwi2 = Kiwi()
        kiwi2.aw_frutas(0.3)
        cajon.lista_objetos = [kiwi1, manzana1, kiwi2]
        #promedio de frutas
        promedio = (kiwi1.aw_kiwi + manzana1.aw_manzana + kiwi2.aw_kiwi) / 3
        promedio_redondeado = round(promedio, 2)
        cajon.aw_prom_frutas()
        self.assertEqual(cajon.prom_frutas, promedio_redondeado) 
    
    def test_aw_prom_total(self):
        cajon = Cajon([], [])
        kiwi = Kiwi()
        kiwi.aw_frutas(0.4)
        manzana = Manzana()
        manzana.aw_frutas(0.5)
        papa = Papa()
        papa.aw_verduras(0.2)
        cajon.lista_objetos = [kiwi,manzana,papa]
        cantidad_alimentos = 4 #se agrega uno para probar cuando el alimento da undefined
        promedio_calculado = round((kiwi.aw_kiwi+manzana.aw_manzana+papa.aw_papa)/cantidad_alimentos,2)
        cajon.aw_prom_total(cantidad_alimentos)
        self.assertEqual(cajon.promedio_total,promedio_calculado)

def softmax(x):
        return (np.exp(x - np.max(x)) / np.exp(x - np.max(x)).sum())

class TestDetectorAlimento(unittest.TestCase):
    def test_softmax(self):
        detector = DetectorAlimento()
        #entrada de ejemplo
        x = np.array([1, 2, 3])
        resultado_esperado = np.array([0.09003057, 0.24472847, 0.66524096])
        #calcular el resultado actual
        resultado_actual = softmax(x)
        #comparar el resultado actual con el resultado esperado
        np.testing.assert_allclose(resultado_actual, resultado_esperado, rtol=1e-6)

    def test_detectar_alimento(self):
        detector = DetectorAlimento()
        # Mockear la función random para controlar el resultado
        with patch('random.randint', return_value=0) as mock_randint, \
            patch('random.choices', return_value=[0.05]) as mock_choices:
            
            resultado = detector.detectar_alimento()
            
            mock_randint.assert_called_once_with(0, 4) 
            
            expected_seq = np.round(np.linspace(0.05, 0.6, 12), 2).tolist()
            expected_weights = np.round(softmax(expected_seq)[::-1], 2).tolist()
            
            actual_seq, actual_weights = mock_choices.call_args[0]
            
            self.assertTrue(np.array_equal(actual_seq, expected_seq))
            self.assertTrue(np.array_equal(actual_weights, expected_weights))
            self.assertEqual(resultado["alimento"], "kiwi")
            self.assertEqual(resultado["peso"], 0.05)


if __name__ == '__main__':
    unittest.main()