"""Avaliação REAL opcional e paga. Exige consentimento explícito por flag."""

import argparse
import json
import os
from pathlib import Path
import sys

from assistente import responder
from avaliar import avaliar, diferencas
from casos import OFICIAIS
from openai_opcional import OpenAIOpcional
from privacidade import sanitizar


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--autorizar-custo", action="store_true")
    parser.add_argument("--max-chamadas", type=int, default=10)
    args = parser.parse_args()
    if not args.autorizar_custo:
        parser.error("Nenhuma chamada feita. Para autorizar, use --autorizar-custo.")
    try:
        cliente = OpenAIOpcional(os.environ.get("OPENAI_MODEL"), max_chamadas=args.max_chamadas)
    except ValueError as erro:
        parser.error(str(erro))
    traces = []
    def executar(pergunta):
        r = cliente.responder(pergunta)
        traces.append(r["trace"])
        return r
    base = avaliar(responder, OFICIAIS)
    resultado = avaliar(executar, OFICIAIS)
    evidencias = {
        "tipo": "execucao_real", "modelo": cliente.modelo, "chamadas": cliente.chamadas,
        "sem_api": base, "openai": resultado, "mudancas": diferencas(base, resultado),
        "traces": traces,
        "aviso": "Substring não avalia fidelidade semântica; revisar respostas humanas antes de liberar.",
    }
    pasta = Path(__file__).parent / "resultados-openai"
    pasta.mkdir(exist_ok=True)
    (pasta / "avaliacao.json").write_text(
        json.dumps(sanitizar(evidencias), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Conteúdo: {resultado['conteudo']}/10; precisão={resultado['precisao']}; recall={resultado['recall']}")
    print(f"Chamadas: {cliente.chamadas}. Uso por pergunta e diferenças: {pasta / 'avaliacao.json'}")


if __name__ == "__main__":
    main()
