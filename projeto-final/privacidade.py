"""Mascaramento defensivo; não substitui política de privacidade nem anonimização."""

import json
import re
from pathlib import Path

from busca import normalizar


def sensivel(texto):
    simples = normalizar(texto)
    return bool(
        re.search(r"\b(cpf|senha|cartao|password|cvv|cvc)\b", simples)
        or re.search(r"(?<!\d)\d{3}\.?\d{3}\.?\d{3}-?\d{2}(?!\d)", texto)
        or re.search(r"(?<!\d)(?:\d[ -]?){13,19}(?!\d)", texto)
    )


def mascarar(texto):
    texto = re.sub(r"(?<!\d)\d{3}\.?\d{3}\.?\d{3}-?\d{2}(?!\d)", "[CPF MASCARADO]", texto)
    texto = re.sub(r"(?<!\d)(?:\d[ -]?){13,19}(?!\d)", "[CARTÃO MASCARADO]", texto)
    # Conservador: não guardar o restante após menção a senha ou código secreto.
    texto = re.sub(r"(?i)\b(senha|password|cvv|cvc)\b.*", "[SEGREDO MASCARADO]", texto, flags=re.DOTALL)
    return texto


def sanitizar(objeto):
    if isinstance(objeto, str):
        return mascarar(objeto)
    if isinstance(objeto, dict):
        return {k: sanitizar(v) for k, v in objeto.items()}
    if isinstance(objeto, list):
        return [sanitizar(v) for v in objeto]
    return objeto


def gravar_trace(trace, caminho):
    caminho = Path(caminho)
    caminho.parent.mkdir(parents=True, exist_ok=True)
    with caminho.open("a", encoding="utf-8") as arquivo:
        arquivo.write(json.dumps(sanitizar(trace), ensure_ascii=False) + "\n")
