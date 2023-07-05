import unittest
from modules.class_alimentos import Kiwi, Manzana, Papa, Zanahoria

class TestClassesAlimentos(unittest.TestCase):
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


if __name__ == '__main__':
    unittest.main()

