"""Guardrails: verificações em volta do modelo, em código, que não dependem do modelo acertar.

- entrada (before_model_callback): mensagem com segredo ou dado sensível nem chega ao modelo;
- ferramenta (before_tool_callback): argumentos inválidos não executam a ferramenta.
"""
import re

from google.adk.models import LlmResponse
from google.genai import types

# Chaves de API comuns (Groq, OpenAI, Anthropic, Google), cartão de crédito, CPF e senha.
PADROES_SENSIVEIS = {
    "chave de API": re.compile(r"\b(gsk_|sk-|sk-ant-|AIza)[A-Za-z0-9_\-]{10,}"),
    "CPF": re.compile(r"\b\d{3}\.?\d{3}\.?\d{3}-?\d{2}\b"),
    "senha": re.compile(r"\bsenha\s*[:=]", re.IGNORECASE),
}

PADRAO_CARTAO = re.compile(r"(?<!\d)(?:\d[ .-]?){12,18}\d(?!\d)")


def _cartao_valido_luhn(numero: str) -> bool:
    digitos = [int(d) for d in numero if d.isdigit()]
    if not 13 <= len(digitos) <= 19:
        return False
    soma = 0
    for posicao, digito in enumerate(reversed(digitos)):
        if posicao % 2:
            digito *= 2
            if digito > 9:
                digito -= 9
        soma += digito
    return soma % 10 == 0


def encontrar_dado_sensivel(texto: str) -> str | None:
    """Devolve o tipo de dado sensível encontrado no texto, ou None."""
    for nome, padrao in PADROES_SENSIVEIS.items():
        if padrao.search(texto):
            return nome
    if any(_cartao_valido_luhn(match.group()) for match in PADRAO_CARTAO.finditer(texto)):
        return "número de cartão"
    return None


def _ultima_mensagem_do_usuario(llm_request) -> str:
    for conteudo in reversed(llm_request.contents or []):
        if conteudo.role == "user":
            return " ".join(p.text for p in (conteudo.parts or []) if p.text)
    return ""


def guardrail_entrada(callback_context, llm_request):
    """Bloqueia a mensagem antes do modelo se ela tiver segredo ou dado sensível.

    Devolver uma resposta aqui faz o ADK pular a chamada ao modelo: o dado não sai da sua máquina.
    """
    achado = encontrar_dado_sensivel(_ultima_mensagem_do_usuario(llm_request))
    if achado is None:
        return None  # segue para o modelo
    callback_context.state["bloqueios"] = callback_context.state.get("bloqueios", 0) + 1
    texto = (f"Sua mensagem parece conter {achado}. Por segurança, ela não foi enviada ao modelo. "
             "Nunca cole chaves, senhas ou dados pessoais no chat; envie a pergunta sem eles.")
    return LlmResponse(content=types.Content(role="model", parts=[types.Part(text=texto)]))


def guardrail_ferramenta(tool, args, tool_context):
    """Valida os argumentos antes de executar a ferramenta. Devolver um dict substitui a execução."""
    if tool.name == "estimar_custo":
        numeros = {k: v for k, v in args.items() if isinstance(v, (int, float))}
        if any(v < 0 for v in numeros.values()):
            return {"erro": "Os valores não podem ser negativos. Peça à pessoa para conferir os números."}
        if args.get("chamadas_por_dia", 1) > 10_000_000:
            return {"erro": "Quantidade de chamadas por dia fora do razoável. Confirme o número com a pessoa."}
    if tool.name == "converter_moeda":
        if args.get("valor_usd", 0) < 0:
            return {"erro": "O valor em dólares não pode ser negativo."}
        if args.get("cotacao", 0) <= 0:
            return {"erro": "A cotação precisa ser maior que zero."}
    if tool.name in {"ask_wiki_question", "read_wiki_structure"} and tool_context is not None:
        tool_context.state["consultou_deepwiki"] = True
    return None  # segue com a execução normal


def guardrail_saida(callback_context, llm_response):
    """Acrescenta um lembrete se a resposta final do DeepWiki não trouxer fonte ou link."""
    if not callback_context.state.get("consultou_deepwiki") or not llm_response.content:
        return None
    partes = llm_response.content.parts or []
    if any(parte.function_call for parte in partes):
        return None  # ainda há outra ferramenta a executar

    texto = "".join(parte.text or "" for parte in partes)
    callback_context.state["consultou_deepwiki"] = False
    if re.search(r"https?://|\bfontes?\s*:", texto, re.IGNORECASE):
        return None

    complemento = (
        "\n\n⚠️ Esta resposta usou o DeepWiki, mas não identificou uma fonte. "
        "Confira a documentação original antes de confiar nela."
    )
    llm_response.content.parts.append(types.Part(text=complemento))
    return llm_response
