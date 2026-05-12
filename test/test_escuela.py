import unittest
from escuela.modelos import Asignatura
from escuela.common import Validator


class TestPrograma(unittest.TestCase):

    # NOTA VALIDA
    def test_nota_valida(self):
        a = Asignatura("matematicas", 8)
        self.assertEqual(a.nota, 8)

    # NOTA NO VALIDA
    def test_nota_negativa(self):
        with self.assertRaises(ValueError):
            Asignatura("matematicas", -1)

    # NOTA NO VALIDA 
    def test_nota_mayor(self):
        with self.assertRaises(ValueError):
            Asignatura("matematicas", 11)

    # DNI MAL
    def test_dni_mal(self):
        self.assertFalse(
            Validator.validar_dni("12345678A")
        )