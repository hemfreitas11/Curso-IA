"""Ferramenta somente de leitura: simulação, nunca dados de clientes reais."""

import re


def consultar_pedido(numero):
    if not isinstance(numero, str) or not re.fullmatch(r"\d{5}", numero):
        return {"erro": "Número de pedido inválido; use cinco dígitos."}
    if numero != "48213":
        return {"erro": "Pedido não encontrado; procure um atendente."}
    return {"numero": "48213", "status": "em transporte", "previsao": "12/11"}
