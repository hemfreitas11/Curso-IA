"""Dados fictícios transcritos da aula 6.3, sem alterar as políticas."""

POLITICAS = {
    "Prazo de troca": (
        "Produtos podem ser trocados em até 7 dias corridos após o recebimento. "
        "O produto precisa estar sem uso e na embalagem original."
    ),
    "Garantia": (
        "Eletrônicos têm garantia de 12 meses a partir da data da nota fiscal. "
        "A garantia não cobre quedas nem contato com líquidos."
    ),
    "Frete": (
        "O frete é grátis para compras acima de 200 reais. "
        "Abaixo disso, o valor aparece no carrinho antes de pagar."
    ),
    "Reembolso": (
        "O reembolso é feito na mesma forma de pagamento em até 10 dias úteis "
        "depois que o produto devolvido chega ao nosso centro."
    ),
}


def trechos():
    """Cada frase guarda a fonte e a política completa a que pertence."""
    return [
        {"fonte": fonte, "texto": frase.strip() + ".", "politica": texto}
        for fonte, texto in POLITICAS.items()
        for frase in texto.split(".") if frase.strip()
    ]
