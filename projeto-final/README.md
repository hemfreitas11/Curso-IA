# Assistente da loja — projeto final da aula 6.3

Projeto didático completo, **sem dependências externas**, com políticas exatas da
aula, consulta fictícia de pedidos, busca lexical, testes, experimentos e relatório.
O modo padrão não usa modelo, chave ou rede. OpenAI é uma extensão opcional.

## Executar

Precisa de Python 3.12 ou mais recente (validado aqui no Python 3.14.4/Windows).
A partir da pasta `projeto-final`:

```powershell
python chat.py
python chat.py --pergunta "Onde está meu pedido 48213?" --sem-trace
python chat.py --pergunta "Posso trocar um produto usado?" --mostrar-trace
python avaliar.py
python -m unittest discover -s tests -v
python verificar.py
```

No chat, `/sair` encerra. Não há memória entre perguntas. Use apenas dados fictícios.
Encaminhamentos são **simulados**, sem fila real. O sistema informa que é IA.

Traces vão para `traces/sessao-*.jsonl`, fora do Git; `--sem-trace` desativa gravação.
Há mascaramento de padrões de CPF, cartão e senha, mas **não anonimização garantida**.
Não use dados pessoais reais. Apague traces que não precisar; não há expurgo
automático, criptografia nem controle de acesso implementados neste protótipo.

## Resultados e entregáveis

- [Relatório curto](RELATORIO.md): escopo, linha de base, três melhorias, falha,
  comparação e checklist de prontidão.
- [Especificação](ESPECIFICACAO.md) e [instruções](AGENTS.md).
- `evidencias/experimentos.json`: métricas e respostas por caso de cada variante.
- `evidencias/traces-didaticos.json`: falha inicial, regressão, correção e bloqueio.
- `evidencias/comparacao-referencia.{json,txt}`: comparação real com avaliador oficial.
- `evidencias/verificacao.json`: ambiente, comandos e saída da última verificação;
  `python verificar.py --comparar` repete testes, experimentos e comparação offline.

Resultado observado: **10/10 oficiais**, **12/12 adicionais próprios** e **14/15 no
conjunto da referência**, com recall 100% nesses conjuntos. Isso não é estimativa
de desempenho em produção: os casos são poucos, conhecidos e usados no desenvolvimento.

As variantes em `assistente.VERSOES` reproduzem cada etapa: `inicial`, `radicais`,
`politica`, `limiar`, `desempate`, `entrada`, `escopo`, `segura`. Só `segura` é usada
pelo chat. As demais têm falhas intencionais preservadas para medir mudanças.

O avaliador mede substring esperada e decisão de encaminhar **separadamente**.
`completos` exige ambos. Precisão/recall usam humano como classe positiva;
denominador zero aparece como `null`. Não se trata de verificação semântica.

## Comparar novamente com a referência

A referência foi aberta somente após construir e testar nossa versão. Ela não é
vendorizada; os resultados guardam o commit usado. Revise o código externo antes
de executar. Na primeira preparação:

```powershell
git clone https://github.com/paulo-atsinformatica/projeto-final-analista-ia.git referencia
git -C referencia switch --detach 42ad8168b2452838869d13c57dcb87208316ba91
python comparar.py
```

O comparador adiciona **apenas** `minha_versao.py` à raiz da referência, sem mudar
seus dados, casos ou implementações. O adaptador respeita o contrato
`assistente(pergunta) -> {pergunta, passos, resposta, encaminhou}` e isola imports
em subprocesso, pois ambos os projetos têm módulos chamados `base` e `casos`.
Ele só funciona como copiado na pasta `referencia` ou na própria pasta do projeto.

Para usar diretamente o avaliador oficial:

```powershell
python referencia/avaliar.py --comparar minha_versao versao_final
```

## OpenAI opcional — não executado com API real nesta entrega

Sem SDK: `urllib` chama a Responses API HTTPS oficial. Configure as variáveis na
sua sessão, sem colar a chave em arquivos versionados ou conversas:

```powershell
$env:OPENAI_API_KEY = Read-Host "Chave da OpenAI" -MaskInput
$env:OPENAI_MODEL = "IDENTIFICADOR_DO_MODELO_DA_SUA_CONTA"
python chat.py --openai --max-chamadas 10
python avaliar_openai.py --autorizar-custo --max-chamadas 10
```

`-MaskInput` requer PowerShell 7. Não inclua chaves literais no histórico do shell.
Escolha um modelo que suporte Responses API e JSON Schema; prefira uma versão
datada para reproduzir resultados. A conta do ChatGPT não implica crédito de API.

O modelo recebe só pergunta mascarada e política já recuperada. Não recebe senha,
cartão ou CPF reconhecido pelos guardrails, não chama ferramentas e não decide o
encaminhamento inicial. Consulta de pedido continua determinística. A saída exige
fonte recuperada e pode recusar; erro/timeout leva a humano, sem retry automático.

Limites por processo: 10 tentativas por padrão (máximo configurável 100), 300 tokens
de saída por chamada, entrada até 2.000 caracteres, timeout de 20 s. Não é teto de
custo em reais/dólares; configure orçamento/alertas no provedor. Reiniciar o processo
reinicia o contador. `store=false` não equivale a garantia contratual de retenção zero.

`avaliar_openai.py` grava resultados reais, diferenças e uso por pergunta em
`resultados-openai/avaliacao.json`, ignorado pelo Git. Reescritas podem falhar na
checagem textual mesmo quando corretas — e conter a substring mesmo estando erradas.
Revise semanticamente antes de qualquer uso. Citar a fonte não prova fidelidade.

## Arquitetura e conceitos do curso

```text
terminal → validação/guardrail de entrada → consulta de pedido OU busca lexical
         → política + fonte → [OpenAI opcional] → guardrail de saída → resposta
         → trace mascarado; sem evidência/erro → encaminhamento simulado
```

`base.py` conserva os documentos; `busca.py` faz chunking por frase e recuperação
lexical; `ferramentas.py` valida argumentos; `assistente.py` organiza o fluxo;
`privacidade.py` mascara/persiste traces; `avaliar.py` mede conteúdo e decisão.

Conceitos aplicados: contexto vs treino (1.6), RAG/recuperação/citações (1.8–1.9),
ferramentas (1.10), harness e limites (2.1/2.8), guardrails (2.3), evals (2.4),
observabilidade (2.5), versões (2.6), segurança (2.7), especificação (3.3), Python
e Git (4.1–4.2). Conforme 5.1, um workflow previsível resolve: adicionar framework,
multiagente ou MCP aqui aumentaria a complexidade sem necessidade.

**Não está pronto para clientes reais.** Veja prioridades e lacunas no relatório.
