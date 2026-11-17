"""Versões cumulativas do experimento; nenhuma delas usa modelo de linguagem."""

import re
import time

from busca import buscar, normalizar
from ferramentas import consultar_pedido
from privacidade import sanitizar, sensivel

VERSOES = {
    "inicial": {"radicais": False, "inteira": False, "limiar": 0.5},
    "radicais": {"radicais": True, "inteira": False, "limiar": 0.5},
    "politica": {"radicais": True, "inteira": True, "limiar": 0.5},
    "limiar": {"radicais": True, "inteira": True, "limiar": 0.3},
}
VERSOES["desempate"] = {**VERSOES["limiar"], "desempate": True}
VERSOES["entrada"] = {**VERSOES["desempate"], "entrada": True}
VERSOES["escopo"] = {**VERSOES["entrada"], "escopo": True}
VERSOES["segura"] = {**VERSOES["escopo"], "saida": True}


def encaminhar(motivo, trace):
    return {
        "resposta": "Vou encaminhar para um atendente. Não consigo responder com segurança.",
        "encaminhar": True, "fonte": None, "motivo": motivo, "trace": trace,
    }


def validar_saida(resultado):
    """Fonte deve estar presente no texto, não apenas nos metadados."""
    if not resultado["encaminhar"]:
        fonte = resultado.get("fonte")
        if not fonte or f"({fonte})" not in resultado["resposta"]:
            return encaminhar("fonte_ausente", resultado["trace"])
    return resultado


def responder(pergunta, versao="segura"):
    config = VERSOES[versao]
    inicio = time.perf_counter()
    trace = {"versao": versao, "pergunta": pergunta, "busca": None, "ferramenta": None}

    def finalizar(resultado):
        if config.get("saida"):
            resultado = validar_saida(resultado)
        trace.update({
            "resposta": resultado["resposta"], "fonte": resultado["fonte"],
            "encaminhar": resultado["encaminhar"], "motivo": resultado["motivo"],
            "latencia_ms": round((time.perf_counter() - inicio) * 1000, 3),
        })
        resultado["trace"] = sanitizar(trace)
        return resultado

    if not isinstance(pergunta, str) or not pergunta.strip() or len(pergunta) > 2000:
        return finalizar(encaminhar("entrada_invalida", trace))
    if config.get("entrada"):
        if sensivel(pergunta):
            return finalizar(encaminhar("dados_sensiveis", trace))
    if config.get("escopo"):
        # Defesa adicional de escopo. Não é uma proteção universal contra injection.
        if re.search(r"\b(parcel\w*|ignore|desconsidere)\b", normalizar(pergunta)):
            return finalizar(encaminhar("fora_do_escopo", trace))
    numeros = re.findall(r"\b\d{5}\b", pergunta)
    if "pedido" in normalizar(pergunta) and numeros:
        if len(numeros) != 1:
            return finalizar(encaminhar("pedidos_ambiguos", trace))
        dados = consultar_pedido(numeros[0])
        trace["ferramenta"] = {"nome": "consultar_pedido", "argumentos": {"numero": numeros[0]}, "resultado": dados}
        if "erro" in dados:
            return finalizar(encaminhar("pedido_nao_encontrado", trace))
        return finalizar({
            "resposta": f"Seu pedido está {dados['status']}, previsão {dados['previsao']}. (Consulta de pedidos)",
            "encaminhar": False, "fonte": "Consulta de pedidos", "motivo": "ferramenta", "trace": trace,
        })
    recuperacao = buscar(pergunta, config["radicais"], config["limiar"], desempate_exato=config.get("desempate", False))
    trace["busca"] = recuperacao
    if not recuperacao["encontrado"]:
        return finalizar(encaminhar("sem_evidencia", trace))
    melhor = recuperacao["candidatos"][0]
    texto = melhor["politica"] if config["inteira"] else melhor["texto"]
    return finalizar({
        "resposta": f"{texto} ({melhor['fonte']})", "fonte": melhor["fonte"],
        "encaminhar": False, "motivo": "politica", "trace": trace,
    })
