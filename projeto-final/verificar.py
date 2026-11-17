"""Executar a verificação offline completa e guardar o resultado dos testes."""

import argparse
import json
from pathlib import Path
import platform
import subprocess
import sys


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--comparar", action="store_true", help="Também executar referência já clonada e revisada")
    args = parser.parse_args()
    raiz = Path(__file__).parent
    passos = [
        ["-m", "unittest", "discover", "-s", "tests", "-v"],
        ["avaliar.py"],
    ]
    if args.comparar:
        passos.append(["comparar.py"])
    registros = []
    for argumentos in passos:
        processo = subprocess.run(
            [sys.executable, "-X", "utf8", *argumentos], cwd=raiz,
            capture_output=True, text=True, encoding="utf-8", timeout=120,
        )
        registros.append({"comando": ["python", *argumentos], "codigo": processo.returncode,
                          "stdout": processo.stdout, "stderr": processo.stderr})
        print(processo.stdout, end="")
        print(processo.stderr, end="")
        if processo.returncode:
            break
    pasta = raiz / "evidencias"
    pasta.mkdir(exist_ok=True)
    (pasta / "verificacao.json").write_text(json.dumps({
        "python": platform.python_version(), "sistema": platform.system(),
        "api_real_executada": False, "passos": registros,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return 0 if all(r["codigo"] == 0 for r in registros) else 1


if __name__ == "__main__":
    raise SystemExit(main())
