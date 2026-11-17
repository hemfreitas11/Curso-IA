"""Recuperação lexical pequena e inspecionável, sem embeddings ou rede."""

import re
import unicodedata

from base import trechos


def normalizar(texto):
    return "".join(
        c for c in unicodedata.normalize("NFD", texto.lower())
        if unicodedata.category(c) != "Mn"
    )


IGNORAR = set("""
a o as os um uma uns umas de do da dos das em no na nos nas para por pelo pela
e ou que qual quais como quando onde meu minha meus minhas seu sua seus suas
eu voce voces posso pode podem ser estar se com sem ao aos ate nao sim isso
esse essa este esta foi tem ter quanto quantos quantas sobre falar quero
""".split())


def palavras(texto, radicais=False):
    tokens = {
        p for p in re.findall(r"[a-z0-9]+", normalizar(texto))
        if p not in IGNORAR
    }
    return {p[:5] for p in tokens} if radicais else tokens


def buscar(pergunta, radicais=False, limiar=0.5, desempate_exato=False):
    consulta = palavras(pergunta, radicais)
    candidatos = []
    for trecho in trechos():
        comuns = consulta & palavras(trecho["texto"], radicais)
        score = len(comuns) / len(consulta) if consulta else 0
        exatos = palavras(pergunta) & palavras(trecho["texto"])
        candidatos.append({**trecho, "score": score, "comuns": sorted(comuns), "exatos": len(exatos)})
    candidatos.sort(key=lambda c: (c["score"], c["exatos"] if desempate_exato else 0), reverse=True)
    melhor = candidatos[0]
    return {
        "encontrado": melhor["score"] >= limiar,
        "limiar": limiar,
        "consulta": sorted(consulta),
        "candidatos": candidatos,
    }
