"""Adaptador para o contrato do AGENTS.md da referência, sem colisão de imports.

Copiado pelo comparador para a raiz da referência. Executa nossa versão em um
processo separado, porque os dois projetos possuem base.py e casos.py diferentes.
"""

import json
from pathlib import Path
import subprocess
import sys


def assistente(pergunta: str) -> dict:
    pasta = Path(__file__).resolve().parent
    if not (pasta / "chat.py").exists():
        pasta = pasta.parent
    processo = subprocess.run(
        [sys.executable, str(pasta / "chat.py"), "--json"],
        input=json.dumps(pergunta), capture_output=True, text=True,
        encoding="utf-8", check=True, timeout=10,
    )
    r = json.loads(processo.stdout)
    return {
        "pergunta": r["trace"]["pergunta"], "passos": [r["trace"]],
        "resposta": r["resposta"], "encaminhou": r["encaminhar"],
    }
