"""Chat no terminal. Este programa não abre chamados nem atende clientes reais."""

import argparse
import json
import os
from pathlib import Path
import sys
import uuid

from assistente import responder
from privacidade import gravar_trace


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pergunta", help="Responder uma pergunta e sair")
    parser.add_argument("--json", action="store_true", help="Ler pergunta JSON de stdin e devolver resultado JSON, sem persistência")
    parser.add_argument("--sem-trace", action="store_true")
    parser.add_argument("--mostrar-trace", action="store_true")
    parser.add_argument("--openai", action="store_true", help="Autorizar API paga para esta sessão")
    parser.add_argument("--max-chamadas", type=int, default=10)
    args = parser.parse_args()
    funcao = responder
    if args.json and args.openai:
        parser.error("--json é reservado à comparação sem API")
    if args.openai:
        from openai_opcional import OpenAIOpcional
        try:
            cliente = OpenAIOpcional(os.environ.get("OPENAI_MODEL"), max_chamadas=args.max_chamadas)
        except ValueError as erro:
            parser.error(str(erro))
        funcao = cliente.responder
        print(f"API paga habilitada: no máximo {args.max_chamadas} chamadas; sem retries.")
    if args.json:
        sys.stdout.reconfigure(encoding="utf-8")
        print(json.dumps(responder(json.load(sys.stdin)), ensure_ascii=False))
        return
    arquivo = Path(__file__).parent / "traces" / f"sessao-{uuid.uuid4().hex}.jsonl"

    def executar(pergunta):
        r = funcao(pergunta)
        if not args.sem_trace:
            gravar_trace(r["trace"], arquivo)
        print(r["resposta"])
        if r["encaminhar"]:
            print("[Encaminhamento simulado: nenhum chamado foi aberto.]")
        if args.mostrar_trace:
            print(json.dumps(r["trace"], ensure_ascii=False, indent=2))

    if args.pergunta is not None:
        executar(args.pergunta)
        return
    print("Assistente didático de IA — dados fictícios. Não informe CPF, senha ou cartão.")
    print("Sem memória entre perguntas. Digite /sair para terminar.")
    if not args.sem_trace:
        print(f"Traces locais com mascaramento parcial: {arquivo}")
    try:
        while True:
            pergunta = input("Você: ")
            if pergunta.strip().lower() == "/sair":
                break
            executar(pergunta)
    except (EOFError, KeyboardInterrupt):
        print("\nSessão encerrada.")


if __name__ == "__main__":
    main()
