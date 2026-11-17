# Instruções do projeto — aula 6.3

- Objetivo: assistente didático da loja para políticas e consulta do pedido fictício 48213.
- Usar apenas Python e biblioteca padrão. A base funciona sem chave, rede ou LLM.
- Não alterar as provas nem outros materiais do repositório.
- Explicar mudanças e documentação em português.
- Preservar políticas e dez casos exatamente como fornecidos pela aula.
- Desenvolver em passos verificáveis: base, ferramenta, decisão/trace, avaliação,
  três melhorias isoladas, guardrails e só então comparar com a referência.
- Não copiar a referência para implementar nossa solução.
- Versionar as variantes experimentais; não fabricar resultados nem ajustar testes para passar.
- Dados sensíveis bloqueados antes de busca, ferramenta ou API; traces com mascaramento.
- Nunca pedir senhas, CPF ou dados de cartão, nem inventar compromissos da loja.
- Encaminhar é uma decisão local simulada, não um atendimento realmente aberto.
- OpenAI é opcional; chave somente em variável de ambiente; nenhuma chamada paga
  durante este desenvolvimento. Testes da integração usam transporte simulado.
- Após cada mudança relevante, executar testes e registrar evidências.

## Comandos (a partir desta pasta)

- `python -m unittest discover -s tests -v`
- `python avaliar.py`
- `python chat.py`

Não declarar prontidão para produção: faltam autenticação, integração real,
validação de privacidade e operação por responsável humano.
