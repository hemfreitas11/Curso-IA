import unittest

from base import POLITICAS, trechos
from busca import buscar, normalizar, palavras
from ferramentas import consultar_pedido


class BaseTest(unittest.TestCase):
    def test_base_exata(self):
        self.assertEqual(len(POLITICAS), 4)
        self.assertEqual(len(trechos()), 7)
        self.assertIn("acima de 200 reais", POLITICAS["Frete"])
        for t in trechos():
            self.assertIn(t["texto"], POLITICAS[t["fonte"]])

    def test_recuperacao_com_fonte(self):
        r = buscar("O frete é grátis?")
        self.assertTrue(r["encontrado"])
        self.assertEqual(r["candidatos"][0]["fonte"], "Frete")

    def test_sem_evidencia(self):
        self.assertFalse(buscar("Vocês vendem geladeira?")["encontrado"])
        self.assertFalse(buscar("")["encontrado"])

    def test_normalizacao_e_radicais(self):
        self.assertEqual(normalizar("LÍQUIDOS"), "liquidos")
        self.assertEqual(palavras("trocar trocados", True), {"troca"})

    def test_ferramenta_validada(self):
        self.assertEqual(consultar_pedido("48213")["status"], "em transporte")
        for numero in ("99999", "48213 OR 1=1", "123", 48213):
            self.assertIn("erro", consultar_pedido(numero))


if __name__ == "__main__":
    unittest.main()
