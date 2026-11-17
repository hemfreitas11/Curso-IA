import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from assistente import responder, validar_saida
from avaliar import avaliar
from casos import ADICIONAIS, OFICIAIS
from privacidade import gravar_trace, mascarar


class AssistenteTest(unittest.TestCase):
    def test_aceite_oficial(self):
        r = avaliar(responder, OFICIAIS)
        self.assertGreaterEqual(r["completos"], 9)
        self.assertEqual(r["recall"], 1)

    def test_adicionais(self):
        r = avaliar(responder, ADICIONAIS)
        self.assertEqual(r["fn"], 0)

    def test_bloqueio_antes_de_busca_e_ferramenta(self):
        with patch("assistente.buscar") as busca, patch("assistente.consultar_pedido") as ferramenta:
            for texto in (
                "Meu CPF é 123.456.789-00, cadê o pedido 48213?",
                "senha teste-ficticio pedido 48213",
                "cartão 4111 1111 1111 1111 frete", "12345678900 frete",
            ):
                r = responder(texto)
                self.assertTrue(r["encaminhar"])
                self.assertIsNone(r["trace"]["busca"])
            busca.assert_not_called()
            ferramenta.assert_not_called()

    def test_fonte_ausente(self):
        for fonte, resposta in ((None, "7 dias"), ("Frete", "Grátis")):
            r = validar_saida({"resposta": resposta, "fonte": fonte, "encaminhar": False, "trace": {}})
            self.assertEqual(r["motivo"], "fonte_ausente")

    def test_regressao_prefixo_corrigida(self):
        self.assertIn("10 dias úteis", responder("Quando recebo o reembolso?")["resposta"])

    def test_mascaramento_persistido(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "trace.jsonl"
            r = responder("Meu CPF é 123.456.789-00, frete?")
            gravar_trace(r["trace"], path)
            texto = path.read_text(encoding="utf-8")
            self.assertNotIn("123.456.789-00", texto)
            self.assertIn("CPF MASCARADO", texto)
            json.loads(texto)
        self.assertNotIn("teste-ficticio", mascarar("senha teste-ficticio"))
        self.assertNotIn("4111", mascarar("cartão 4111 1111 1111 1111"))

    def test_limites_e_ambiguidade(self):
        for pergunta in ("", "a" * 2001, "pedido 48213 e pedido 99999"):
            self.assertTrue(responder(pergunta)["encaminhar"])

    def test_metricas_sem_denominador(self):
        r = avaliar(responder, [("Frete grátis?", "200 reais", False)])
        self.assertIsNone(r["precisao"])
        self.assertIsNone(r["recall"])

    def test_experimento_reproduzivel_e_regressao_visivel(self):
        esperados = {"inicial": 7, "radicais": 7, "politica": 8, "limiar": 9, "segura": 10}
        for versao, acertos in esperados.items():
            r = avaliar(lambda p: responder(p, versao), OFICIAIS)
            self.assertEqual(r["completos"], acertos, versao)
        self.assertNotIn("10 dias úteis", responder(OFICIAIS[3][0], "radicais")["resposta"])
        self.assertIn("10 dias úteis", responder(OFICIAIS[3][0], "desempate")["resposta"])


if __name__ == "__main__":
    unittest.main()
