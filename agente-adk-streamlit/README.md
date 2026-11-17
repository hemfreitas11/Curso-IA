# Agente de exemplo: Google ADK + Streamlit + Groq + MCP

Um projeto pequeno e completo para estudar como se monta um agente de IA de verdade: um assistente de estudos para quem quer ser **Analista de IA**, com tela de chat, modelo de linguagem, uma **ferramenta própria**, um **servidor MCP local em Python**, um **MCP público** e **guardrails** em código. Tudo com plano gratuito.

```text
Você (tela em Streamlit)
   │
   ▼
Runner do Google ADK ──► guardrail de entrada ──► (barra chave, senha, cartão, CPF: não chega ao modelo)
   │
   ▼
Modelo da Groq (via LiteLLM) ◄──► ferramentas
                                    ├─ estimar_custo (própria) ◄── guardrail de ferramenta valida os argumentos
                                    ├─ MCP local "analista-ia" (Python, stdio): glossário, competências e roteiro de estudos
                                    └─ DeepWiki (MCP público, HTTP): perguntas sobre repositórios do GitHub
   │
   ▼
Resposta + "passos do agente" (cada chamada de ferramenta e o resultado)
```

## O que você vai ver funcionando

| Peça | Onde está | Tema |
|---|---|---|
| Agente com instruções e ferramentas | `agente/agent.py` | agentes e harness |
| Ferramentas próprias (custo e conversão de moeda) | `agente/ferramentas.py` | tool calling |
| Servidor MCP próprio, em Python, iniciado pelo agente | `mcp_analista/servidor.py` | criar um MCP |
| MCP público, com só as ferramentas de leitura liberadas | `criar_mcp_publico()` em `agente/agent.py` | MCP e menor privilégio |
| Guardrail de entrada e guardrail de ferramenta | `agente/guardrails.py` | guardrails |
| Passos do agente na tela | `agente/conversa.py` e `app.py` | observabilidade |
| Perguntas de entrevista | `perguntas_de_entrevista` no MCP local | prática |
| Guardrail de saída para respostas do DeepWiki | `agente/guardrails.py` | citações |
| MCP Context7 opcional | `criar_mcp_context7()` em `agente/agent.py` | documentação atual |
| Histórico de sessão em SQLite | `conversas.db` (criado ao rodar) | memória |
| Testes simulados e avaliação de respostas | `tests/`, `avaliar.py` | evals |

## Antes de começar

1. **uv.** Ele instala o Python certo (3.12) e as bibliotecas num ambiente virtual; veja a seção abaixo.
2. **Chave gratuita da Groq.** Crie em [console.groq.com/keys](https://console.groq.com/keys). Trate como senha: não cole em chat, issue, print nem commit.
3. **Opcional — Context7.** Para consultar documentação atual de bibliotecas, crie uma chave no Context7 e configure `CONTEXT7_API_KEY` e `MCP_CONTEXT7_ATIVO=true` no `.env`. Sem isso, o MCP fica desligado.

## Ambiente virtual e bibliotecas com uv

Cada projeto Python deve ter o seu **ambiente virtual** (venv): uma pasta com um Python e as bibliotecas só daquele projeto, para um projeto não quebrar o outro. Aqui quem cuida disso é o [uv](https://docs.astral.sh/uv/), que cria o venv, instala as bibliotecas e garante que todo mundo use as mesmas versões.

**1. Instale o uv** (uma vez por computador):

```bash
# Windows (PowerShell)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# macOS e Linux
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Feche e abra o terminal e confira com `uv --version`.

**2. Crie o venv e instale as bibliotecas** (na pasta do projeto):

```bash
uv sync
```

Esse comando lê o `.python-version` (Python 3.12; se você não tiver, o uv baixa), cria a pasta `.venv` e instala exatamente as versões do `uv.lock`. As bibliotecas do projeto estão listadas no `pyproject.toml`; o `uv.lock` guarda as versões exatas, para o projeto funcionar igual em qualquer máquina.

**3. Rode comandos dentro do venv.** O jeito mais simples é pôr `uv run` na frente; não é preciso ativar nada:

```bash
uv run python --version
uv run streamlit run app.py
uv run pytest -q
```

Se preferir ativar o venv e usar os comandos direto:

```bash
# Windows (PowerShell)
.venv\Scripts\activate

# macOS e Linux
source .venv/bin/activate

python --version      # agora é o Python do projeto
streamlit run app.py
deactivate            # sai do venv
```

**4. Adicione, remova e atualize bibliotecas** sempre com o uv, para o `pyproject.toml` e o `uv.lock` ficarem certos:

```bash
uv add pandas                        # adiciona uma biblioteca ao projeto
uv add --dev ruff                    # só para desenvolvimento (testes, formatação)
uv remove pandas                     # remove
uv lock --upgrade-package litellm    # atualiza uma biblioteca para a versão mais nova
uv sync                              # aplica o que está no uv.lock
```

Evite `pip install` direto: a biblioteca entra no venv, mas não fica registrada no projeto, e quem clonar depois não a terá. Se algo der muito errado, apague a pasta `.venv` e rode `uv sync` de novo; ela é recriada do zero.

## Como rodar

Neste repositório de estudos, execute os comandos dentro de `agente-adk-streamlit/`.
Se estiver na raiz `Provas-Curso-IA`, entre primeiro com `cd agente-adk-streamlit`.
O ambiente virtual é local: rode `uv sync` nessa pasta para criá-lo.

Para obter o projeto original separadamente:

```bash
git clone https://github.com/paulo-atsinformatica/agente-adk-streamlit.git
cd agente-adk-streamlit
uv sync                     # cria o .venv e instala as bibliotecas (veja a seção acima)
cp .env.example .env        # no Windows (PowerShell): copy .env.example .env
```

Abra o `.env` e preencha `GROQ_API_KEY`. Depois:

```bash
uv run streamlit run app.py
```

Abra o endereço que aparecer (normalmente http://localhost:8501) e experimente as perguntas da barra lateral:

- *O que é RAG?* e *Monte um roteiro de estudos de 14 dias* → usam o MCP local.
- *Quanto custa 2.000 tokens de entrada e 500 de saída, a 0,59 e 0,79 dólares por milhão, 3.000 vezes por dia?* → usa a ferramenta própria.
- *Converta US$ 25 para reais com cotação de 5,20* → usa a ferramenta de conversão.
- *Faça perguntas de entrevista sobre RAG* → usa o MCP local.
- *No repositório google/adk-python, o que é um callback?* → usa o MCP do DeepWiki.
- *Minha chave é gsk_abc123...* → o guardrail barra antes de chegar ao modelo.

Abra "Passos do agente" embaixo de cada resposta para ver quais ferramentas ele chamou e o que voltou.

**Alternativa:** a interface do próprio ADK, com o rastro detalhado de cada evento: `uv run adk web` e escolha o agente `agente`.

## Testes

```bash
uv run pytest -q              # sem chave: ferramenta, guardrails e o agente com um modelo simulado
uv run python testar_groq.py  # com a chave: perguntas de ponta a ponta no modelo de verdade
uv run python avaliar.py      # com a chave: 10 casos; consulta Groq e DeepWiki
```

O teste do agente usa um **modelo simulado**: um "LLM de mentira" que pede a ferramenta e depois responde. Assim dá para testar o fluxo inteiro sem gastar nada. Os testes de MCP acessam a internet para listar ferramentas públicas e o servidor local. `avaliar.py` envia dez perguntas reais à Groq e inclui uma consulta ao DeepWiki, então pode consumir sua cota gratuita.

## Como cada peça funciona

- **Modelo.** O ADK fala com a Groq pelo LiteLLM (`LiteLlm(model="groq/...")`). Trocar de fornecedor é trocar esse texto. O modelo padrão é `groq/openai/gpt-oss-20b`; os modelos da Groq mudam com o tempo, então confira a [lista](https://console.groq.com/docs/models) e ajuste `GROQ_MODEL` no `.env`.
- **Raciocínio escondido.** Modelos de raciocínio devolvem o "pensamento" junto da resposta, e a Groq recusa receber esse pensamento de volta no turno depois de uma ferramenta. Por isso o projeto pede `reasoning_format: hidden`. Se usar um modelo sem raciocínio, deixe `GROQ_REASONING_FORMAT` vazio.
- **Ferramenta própria.** Uma função Python comum. O modelo não lê o código: lê o nome, a docstring e os tipos dos argumentos para decidir quando usar.
- **MCP local.** `mcp_analista/servidor.py` é um servidor MCP de verdade, escrito em Python com o SDK oficial (`MCPServer`). Ele oferece três ferramentas: `consultar_glossario`, `competencias_analista_ia` e `roteiro_de_estudos`. O agente inicia esse servidor como um processo e conversa com ele por **stdio** (entrada e saída padrão), sem precisar de porta nem de outro terminal. Para subi-lo sozinho como serviço HTTP e testar com outro cliente MCP: `uv run python -m mcp_analista.servidor --http` (fica em `http://127.0.0.1:8001/mcp`).
- **MCP público.** O agente também se conecta ao servidor público do DeepWiki por HTTP. `tool_filter` libera só duas ferramentas de leitura, mesmo que o servidor ofereça mais.
- **Nome de ferramenta importa.** A ferramenta do glossário se chamava `explicar_conceito`, e o modelo pequeno da Groq insistia em chamá-la de `explain_conceito`, um nome que não existe; a Groq recusava a chamada. Trocar o nome para `consultar_glossario` resolveu. Nomes curtos e sem parecença com palavras em inglês ajudam modelos pequenos.
- **Guardrails.** `guardrail_entrada` roda antes de cada chamada ao modelo: se a mensagem tiver chave, senha, cartão ou CPF, devolve uma resposta pronta e o modelo nem é chamado. `guardrail_ferramenta` roda antes da ferramenta e recusa argumentos inválidos. São regras em código: valem mesmo que o modelo seja enganado.

## Limites do plano gratuito

A Groq limita requisições e tokens por minuto. Cada pergunta envia as instruções, o histórico e a descrição de todas as ferramentas, então algumas perguntas seguidas já podem bater no limite. A tela avisa quando isso acontece: espere cerca de um minuto e tente de novo. Começar uma "Nova conversa" também ajuda, porque o histórico enviado fica menor.

O modelo padrão, `openai/gpt-oss-20b`, tem mais limite por minuto. O `openai/gpt-oss-120b` erra menos ao escolher ferramentas, mas bate no limite gratuito mais rápido. Troque em `GROQ_MODEL`.

## Use um agente de código para ir além

Este repositório foi preparado para você trabalhar junto com um agente de código, como **Google Antigravity**, **Claude Code** ou **OpenAI Codex**. O arquivo `AGENTS.md` (lido pelo Codex e pelo Antigravity; o `CLAUDE.md` aponta para ele) já explica ao agente os comandos, a estrutura e as regras.

Como trabalhar bem com ele:

1. Abra a pasta do projeto no agente e peça primeiro para ele **explicar** o código: *"Leia o projeto e me explique, em poucas linhas, o caminho de uma mensagem do chat até a resposta."*
2. Peça **uma mudança por vez**, com critério de pronto: *"Adicione uma ferramenta que converte dólar para real com uma taxa fixa, com validação no guardrail e um teste. Rode os testes no final."*
3. **Leia o diff** antes de aceitar. Você precisa conseguir explicar cada linha.
4. Rode `uv run pytest -q` e teste na tela.
5. **Nunca cole a sua chave no chat do agente.** Ela fica só no `.env`.

## Exercícios desenvolvidos neste clone

1. `converter_moeda` calcula a conversão com a cotação informada e tem validação e teste.
2. O MCP local oferece `perguntas_de_entrevista` para os temas geral, RAG e agentes.
3. O guardrail valida cartões com Luhn; um número de pedido inválido como cartão não deve ser bloqueado.
4. O guardrail de saída alerta quando uma resposta que usou DeepWiki não inclui link ou indicação de fonte.
5. O MCP opcional Context7 consulta documentação; libera apenas `resolve-library-id` e `query-docs`.
6. `avaliar.py` roda dez casos e confere ferramenta esperada e trecho da resposta.
7. O app usa SQLite e guarda o identificador da conversa localmente para retomar o contexto após reinício. Os arquivos locais são ignorados pelo Git.

## Segurança

- A chave fica no `.env`, que está no `.gitignore`. Nunca a coloque no código.
- Se uma chave vazar, revogue em [console.groq.com/keys](https://console.groq.com/keys) e crie outra; apagar o arquivo não basta, porque o histórico do Git guarda tudo.
- Os guardrails deste projeto são didáticos. Num sistema real, combine regras, classificadores e revisão humana.

## Licença

MIT. Use, copie e adapte à vontade.
