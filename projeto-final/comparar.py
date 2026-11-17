"""Executar somente após revisar o código do repositório de referência."""

import argparse
import json
from pathlib import Path
import shutil
import subprocess
import sys

from assistente import responder
from avaliar import avaliar
from base import POLITICAS
from casos import OFICIAIS
from privacidade import sanitizar


def comparar(referencia):
    raiz = Path(__file__).parent
    if not (referencia / "versao_final.py").is_file():
        raise SystemExit("Clone e revise a referência conforme o README antes de comparar.")
    # Só adiciona o adaptador; não muda dados, casos ou código original.
    destino = referencia / "minha_versao.py"
    fonte = raiz / "minha_versao.py"
    if destino.exists() and destino.read_bytes() != fonte.read_bytes():
        raise SystemExit("Já existe minha_versao.py diferente na referência; preserve-o antes de continuar.")
    shutil.copyfile(fonte, destino)
    def executar(args):
        return subprocess.run(
            [sys.executable, *args], cwd=referencia, capture_output=True,
            text=True, encoding="utf-8", check=True, timeout=60,
        ).stdout
    saida = executar(["avaliar.py", "--comparar", "minha_versao", "versao_final"])
    print(saida)
    codigo = (
        "import json; from casos import CASOS,CASOS_EXTRAS; "
        "from base import DOCUMENTOS; from versao_final import assistente; "
        "print(json.dumps({'documentos':DOCUMENTOS,'oficiais':CASOS,'casos':CASOS+CASOS_EXTRAS,"
        "'respostas':[assistente(c['pergunta']) for c in CASOS+CASOS_EXTRAS]},ensure_ascii=True))"
    )
    dados = json.loads(executar(["-c", codigo]))
    oficiais = [(c["pergunta"], c["contem"], c["humano"]) for c in dados["oficiais"]]
    if dados["documentos"] != POLITICAS or oficiais != OFICIAIS:
        raise SystemExit("A referência mudou os dados/casos; revise antes de interpretar a comparação.")
    casos = [(c["pergunta"], c["contem"], c["humano"]) for c in dados["casos"]]
    respostas = dict(zip((c[0] for c in casos), dados["respostas"]))
    def referencia_responder(pergunta):
        r = respostas[pergunta]
        return {"resposta": r["resposta"], "encaminhar": r["encaminhou"]}
    commit = subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=referencia, capture_output=True,
        text=True, check=True,
    ).stdout.strip()
    resultado = {"referencia_commit": commit, "grupos": {}}
    for nome, conjunto in (("oficiais", casos[:10]), ("todos", casos)):
        resultado["grupos"][nome] = {
            "nossa": avaliar(responder, conjunto),
            "referencia": avaliar(referencia_responder, conjunto),
        }
    pasta = raiz / "evidencias"
    pasta.mkdir(exist_ok=True)
    (pasta / "comparacao-referencia.txt").write_text(saida, encoding="utf-8")
    (pasta / "comparacao-referencia.json").write_text(
        json.dumps(sanitizar(resultado), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--referencia", type=Path, default=Path(__file__).parent / "referencia")
    comparar(parser.parse_args().referencia.resolve())
