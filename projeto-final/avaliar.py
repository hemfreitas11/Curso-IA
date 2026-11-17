"""Avaliação local reproduzível: conteúdo por substring NÃO é avaliação semântica."""

import argparse
import json
from pathlib import Path

from assistente import VERSOES, responder
from busca import normalizar
from casos import ADICIONAIS, OFICIAIS
from privacidade import sanitizar


def avaliar(funcao, casos):
    linhas = []
    vp = fp = fn = vn = 0
    for i, (pergunta, contem, esperado) in enumerate(casos, 1):
        resultado = funcao(pergunta)
        resposta = resultado["resposta"]
        previsto = resultado["encaminhar"]
        conteudo = normalizar(contem) in normalizar(resposta)
        if previsto and esperado:
            vp += 1
        elif previsto:
            fp += 1
        elif esperado:
            fn += 1
        else:
            vn += 1
        linhas.append({
            "caso": i, "pergunta": pergunta, "contem": contem,
            "humano_esperado": esperado, "humano_previsto": previsto,
            "conteudo_ok": conteudo, "decisao_ok": previsto == esperado,
            "completo_ok": conteudo and previsto == esperado,
            "resposta": resposta, "motivo": resultado.get("motivo"),
        })
    return {
        "total": len(linhas), "conteudo": sum(l["conteudo_ok"] for l in linhas),
        "decisao": sum(l["decisao_ok"] for l in linhas),
        "completos": sum(l["completo_ok"] for l in linhas),
        "vp": vp, "fp": fp, "fn": fn, "vn": vn,
        "precisao": vp / (vp + fp) if vp + fp else None,
        "recall": vp / (vp + fn) if vp + fn else None,
        "casos": linhas,
    }


def diferencas(antes, depois):
    return [
        {"caso": b["caso"], "antes": a["completo_ok"], "depois": b["completo_ok"],
         "tipo": "melhora" if b["completo_ok"] else "regressao"}
        for a, b in zip(antes["casos"], depois["casos"])
        if a["completo_ok"] != b["completo_ok"]
    ]


def executar(pasta):
    resultados = {}
    anterior = None
    for versao in VERSOES:
        funcao = lambda p, v=versao: responder(p, v)
        dados = {"oficiais": avaliar(funcao, OFICIAIS), "adicionais": avaliar(funcao, ADICIONAIS)}
        if anterior:
            dados["mudancas"] = {
                grupo: diferencas(resultados[anterior][grupo], dados[grupo])
                for grupo in ("oficiais", "adicionais")
            }
        resultados[versao] = dados
        anterior = versao
        r = dados["oficiais"]
        extra = dados["adicionais"]
        print(f"{versao:10} oficiais: {r['completos']}/{r['total']}; "
              f"precisao={r['precisao']} recall={r['recall']}; "
              f"adicionais: {extra['completos']}/{extra['total']}, FN={extra['fn']}")
    pasta.mkdir(parents=True, exist_ok=True)
    (pasta / "experimentos.json").write_text(
        json.dumps(resultados, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    traces = {
        "nota": "Exemplos fictícios. Registros de falha e correção; sem dados reais.",
        "falha_inicial": responder(OFICIAIS[0][0], "inicial")["trace"],
        "regressao_radicais": responder(OFICIAIS[3][0], "radicais")["trace"],
        "correcao_desempate": responder(OFICIAIS[3][0])["trace"],
        "bloqueio_sensivel": responder(ADICIONAIS[2][0])["trace"],
    }
    (pasta / "traces-didaticos.json").write_text(
        json.dumps(sanitizar(traces), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return resultados


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--saida", type=Path, default=Path(__file__).parent / "evidencias")
    args = parser.parse_args()
    executar(args.saida)
