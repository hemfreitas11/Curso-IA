import json
import unittest
from unittest.mock import Mock, patch
import urllib.error

from openai_opcional import OpenAIOpcional, transporte_http


def envelope(resposta="Frete grátis acima de 200 reais. (Frete)", fonte="Frete", encaminhar=False):
    return {
        "status": "completed",
        "output": [{"type": "message", "content": [{"type": "output_text", "text": json.dumps({
            "resposta": resposta, "fonte": fonte, "encaminhar": encaminhar,
        })}]}],
        "usage": {"input_tokens": 100, "output_tokens": 30, "total_tokens": 130},
    }


class OpenAITest(unittest.TestCase):
    def cliente(self, transporte, **kwargs):
        return OpenAIOpcional("modelo-simulado", "chave-ficticia", transporte=transporte, **kwargs)

    def test_sem_chamada_para_bloqueio_ferramenta_ou_falta_de_fonte(self):
        transporte = Mock()
        cliente = self.cliente(transporte)
        for p in ("Meu CPF é 123.456.789-00, frete?", "Onde está meu pedido 48213?", "geladeira"):
            cliente.responder(p)
        transporte.assert_not_called()

    def test_contrato_payload_e_uso(self):
        transporte = Mock(return_value=envelope())
        r = self.cliente(transporte).responder("O frete é grátis?")
        self.assertFalse(r["encaminhar"])
        self.assertEqual(r["trace"]["openai"]["uso"]["total_tokens"], 130)
        payload, chave, timeout = transporte.call_args.args
        self.assertFalse(payload["store"])
        self.assertEqual(payload["max_output_tokens"], 300)
        self.assertNotIn("tools", payload)
        self.assertIn("acima de 200 reais", payload["input"])
        self.assertNotIn(chave, json.dumps(r))
        self.assertEqual(timeout, 20)

    def test_timeout_erro_http_sem_vazar(self):
        for erro in (TimeoutError("segredo"), urllib.error.HTTPError("url", 429, "segredo", {}, None)):
            transporte = Mock(side_effect=erro)
            r = self.cliente(transporte).responder("Frete grátis?")
            self.assertTrue(r["encaminhar"])
            self.assertNotIn("segredo", json.dumps(r))
            self.assertEqual(transporte.call_count, 1)

    def test_fontes_recusa_e_saida_incompleta(self):
        for dados in (
            envelope(fonte="Garantia"), envelope(resposta="Frete grátis"),
            envelope(resposta="Informe sua senha (Frete)"), envelope(encaminhar=True),
            {"status": "incomplete"}, {"status": "completed", "output": []},
            {"status": "completed", "output": [{"type": "message", "content": [{"type": "refusal"}]}]},
            {"status": "completed", "output": None},
        ):
            r = self.cliente(Mock(return_value=dados)).responder("O frete é grátis?")
            self.assertTrue(r["encaminhar"])

    def test_orcamento(self):
        transporte = Mock(return_value=envelope())
        cliente = self.cliente(transporte, max_chamadas=1)
        cliente.responder("Frete grátis?")
        r = cliente.responder("Frete grátis?")
        self.assertEqual(r["motivo"], "limite_api")
        self.assertEqual(transporte.call_count, 1)

    def test_configuracao_invalida(self):
        for kwargs in ({"max_chamadas": 0}, {"max_tokens_saida": 1}, {"timeout": 0}):
            with self.assertRaises(ValueError):
                self.cliente(Mock(), **kwargs)

    def test_http_oficial_sem_rede(self):
        with patch("openai_opcional.urllib.request.urlopen") as abrir:
            abrir.return_value.__enter__.return_value.read.return_value = b'{"status":"completed"}'
            r = transporte_http({"store": False}, "chave-ficticia", 20)
            self.assertEqual(r["status"], "completed")
            request = abrir.call_args.args[0]
            self.assertEqual(request.full_url, "https://api.openai.com/v1/responses")
            self.assertEqual(request.get_method(), "POST")
            self.assertEqual(json.loads(request.data), {"store": False})
            self.assertEqual(abrir.call_args.kwargs["timeout"], 20)

    def test_limite_resposta_http(self):
        with patch("openai_opcional.urllib.request.urlopen") as abrir:
            abrir.return_value.__enter__.return_value.read.return_value = b"x" * 1_000_001
            with self.assertRaises(ValueError):
                transporte_http({}, "chave-ficticia", 20)


if __name__ == "__main__":
    unittest.main()
