import unittest
import numpy as np
from unittest.mock import patch
from modules.class_detector_alimentos import DetectorAlimento

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
