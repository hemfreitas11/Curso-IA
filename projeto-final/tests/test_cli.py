import json
from pathlib import Path
import subprocess
import sys
import unittest

from minha_versao import assistente

RAIZ = Path(__file__).resolve().parents[1]


class CLITest(unittest.TestCase):
    def executar(self, *args, entrada=None):
        return subprocess.run(
            [sys.executable, *args], cwd=RAIZ, input=entrada,
            capture_output=True, text=True, encoding="utf-8", timeout=10,
        )

    def test_pergunta_sem_trace(self):
        r = self.executar("chat.py", "--pergunta", "Frete grátis?", "--sem-trace")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("200 reais", r.stdout)

    def test_interativo(self):
        r = self.executar("chat.py", "--sem-trace", entrada="Frete grátis?\n/sair\n")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("200 reais", r.stdout)

    def test_json_e_adaptador(self):
        r = self.executar("chat.py", "--json", entrada=json.dumps("Frete grátis?"))
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertFalse(json.loads(r.stdout)["encaminhar"])
        adaptado = assistente("Quando recebo o reembolso?")
        self.assertEqual(set(adaptado), {"pergunta", "passos", "resposta", "encaminhou"})
        self.assertIn("10 dias úteis", adaptado["resposta"])

    def test_api_avaliacao_exige_consentimento(self):
        r = self.executar("avaliar_openai.py")
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("--autorizar-custo", r.stderr)


if __name__ == "__main__":
    unittest.main()
