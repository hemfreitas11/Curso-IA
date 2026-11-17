# Projeto final — assistente da loja

## 1. Escopo e sucesso

Assistente de terminal para troca, garantia, frete, reembolso e consulta fictícia
do pedido 48213. Não altera pedidos nem solicita dados sensíveis. Dúvida sem
evidência, dado sensível ou falha encaminha para humano **de forma simulada**.
Políticas e dez casos foram preservados integralmente. Python padrão, sem API
na base; extensão OpenAI separada, sem chamadas reais autorizadas nesta entrega.

Aceite: conteúdo ≥9/10 e recall de encaminhamento 100%. Positivo = precisa de
humano. Precisão = VP/(VP+FP); recall = VP/(VP+FN); base zero = indefinido.
Conteúdo é checado por substring; decisão é independente; ambos são necessários
para o acerto completo. Os conjuntos conhecidos não demonstram generalização.

## 2. Linha de base e três melhorias, uma por vez

Resultados reproduzidos por `python avaliar.py`:

| Versão cumulativa | Oficiais completos | Precisão / recall | Próprios adicionais |
|---|---:|---:|---:|
| Inicial: palavras e frase | 7/10 | 60% / 100% | 8/12 |
| 1. Prefixos de cinco caracteres | 7/10 | 75% / 100% | 8/12 |
| 2. Responder política inteira | 8/10 | 75% / 100% | 10/12 |
| 3. Limiar 0,5 → 0,3 | 9/10 | 100% / 100% | 9/12 |

**Melhoria 1:** associa trocar/trocados. Corrige caso 1, mas regride caso 4:
recebo/recebimento colidem em `receb`, empatando com reembolso. O total esconde
a troca de acertos. **Melhoria 2:** retorna a condição “sem uso” e a informação
vizinha sobre frete; corrige caso 10 e dois adicionais. **Melhoria 3:** permite
responder a garantia/água (caso 9), mas passa a aceitar uma instrução fora de
escopo. A variante desprotegida foi rejeitada: tem três falsos negativos nos
adicionais. As regressões e respostas estão em `evidencias/experimentos.json`.

## 3. Trace de falha, correções e guardrails

Na primeira pergunta (“Em quantos dias posso trocar um produto?”), a base encontra
palavras genéricas e devolve a política de **reembolso**. Há fonte, mas é a fonte
errada: citar não basta. O trace mostra candidatos, palavras comuns, score e limiar.
Na regressão de reembolso, o prefixo empata políticas distintas. A correção
`desempate` prioriza palavras exatas em empates; chega a 10/10 oficiais.

Depois, passos isolados: `entrada` bloqueia cartão/senha/CPF **antes** de busca,
ferramenta ou rede; `escopo` recusa parcelamento e padrões de manipulação conhecidos;
`segura` exige fonte também no texto da saída. Fonte removida é testada por injeção
de falha. Não há regressões nos dez casos oficiais. Resultado final: **10/10**,
VP=3, FP=0, FN=0, VN=7; nos 12 adicionais, **12/12**, sem falso negativo.
Isso é evidência limitada, não proteção universal contra prompt injection.

Traces de falha, regressão, correção e bloqueio ficam em
`evidencias/traces-didaticos.json`. Traces operacionais usam texto mascarado, conforme
decisão do usuário; mascaramento parcial não é anonimização e não remove todo PII.

## 4. Comparação com a referência e OpenAI

Nossa solução foi construída antes de abrir a referência. Adaptador conforme
`AGENTS.md`; avaliador oficial executado sem mudar base ou casos.
Referência: `paulo-atsinformatica/projeto-final-analista-ia`, commit
`42ad8168b2452838869d13c57dcb87208316ba91`.

| Avaliador oficial | Nossa versão | Referência |
|---|---:|---:|
| Conteúdo original | 10/10 | 9/10 |
| Precisão / recall original | 100% / 100% | 75% / 100% |
| Conteúdo com extras oficiais | 14/15 | 13/15 |
| Precisão / recall com extras | 85,7% / 100% | 75% / 100% |

A referência encaminha reembolso e garantia de queda no chão: dois falsos
positivos seguros (humano em vez de resposta inventada). Resolvemos reembolso;
queda no chão continua encaminhada, por falta de correspondência lexical suficiente.
Nossa busca pontua frases e desempata por palavras exatas; a referência pontua
documentos inteiros e usa contagem absoluta. Ambas citam fonte e protegem entrada.
Dados completos: `evidencias/comparacao-referencia.{txt,json}`.

OpenAI opcional implementada com fonte recuperada, contrato JSON, timeout, orçamento
de tentativas/tokens e uso por pergunta. **Só testes simulados**, sem avaliação de
qualidade real nem gasto de API. Não afirmamos melhoria de naturalidade/fidelidade.
Validação de fonte não detecta toda alucinação. A avaliação real está disponível
por comando com autorização explícita; requer revisão humana das respostas.

## 5. Checklist 6.2 e decisão de prontidão

| Área | Aplicado no protótipo | Falta para produção |
|---|---|---|
| Problema | Escopo, público e métricas; workflow fixo suficiente | Validar demanda e custo do erro com a loja |
| Contexto | Base/fonte rastreável; recuperação testada; instruções claras | Dono/atualização da base; eval independente de recuperação e cobertura |
| Ferramentas | Função pequena, validada e somente leitura | API real, autenticação por cliente e autorização; ações futuras exigem aprovação/idempotência |
| Qualidade | Baseline, mudanças isoladas, casos de risco, fonte na saída | Conjunto cego maior, revisão semântica, métricas de produção e eval OpenAI real |
| Segurança/LGPD | Guardrails, mascaramento, aviso de IA e humano | Base legal, minimização/retencão, expurgo, acesso seguro, testes adversariais e atendimento humano real |
| Operação | Traces locais, latência, variantes, limites e chave fora do código | Pipeline/deploy/rollback, versão fixa de modelo, orçamento global/alertas e responsável por revisão |

**Não liberar a clientes.** Prioridade 1: identidade/autorização, privacidade e fila
humana real. Prioridade 2: evals independentes e adversariais, recuperação melhor e
validação da API opcional. Prioridade 3: deploy por pipeline, observabilidade com
alertas, responsável e piloto interno gradual com rollback. O aceite didático foi
atingido; prontidão operacional e revisão humana ainda não.
