# Provas de revisão

Abra `abrir-provas.bat` e escolha uma das sete provas: seis gerais e uma específica de precisão e recall. Cada uma contém 30 questões, com quatro alternativas e uma única correta. As explicações de todas as alternativas aparecem somente depois de confirmar a resposta.

As questões são embaralhadas a cada início de prova, sem agrupamento por módulo. A interface não exibe a aula ou o módulo de origem da questão; as referências ficam apenas no banco para rastreabilidade.

## Escopo real do material

As seis provas gerais cobrem as 22 aulas técnicas **1.1 a 3.4**: fundamentos de IA, LLMs, prompts, treino e contexto, embeddings, RAG, ferramentas, agentes, MCP, guardrails, avaliação, observabilidade, versões, segurança, loops, agentes de código, contexto, especificações e escolha de modelos. Além disso, as provas **3 a 6** cobrem as aulas **4.1 a 6.2**, incluindo Python, Git, APIs, containers, padrões e frameworks de agentes, ADK, tendências e prontidão para produção. A aula **0.1 — Como a trilha funciona** e a aula **6.3 — Projeto final** estão excluídas. As provas mantêm 30 questões, combinando conteúdos em questões integradoras quando necessário.

As provas 1 e 2 continuam no escopo de 1.1 a 3.4. As provas 3 a 6 usam também o material extraído das aulas 4.1 a 6.2; a aula 6.3 não é avaliada.

O arquivo `modulo-1-aulas.txt` contém navegação duplicada na seção inicialmente identificada como aula 1.1. Para os conceitos dessa aula, foram usados também os registros em `quizes/quiz-aula-1.1.md`. A elaboração foi feita com arquivos locais; não houve envio de respostas à Academy nesta etapa.

## Organização

| Prova | Ênfase dos cenários | Cobertura adicional | Questões |
| --- | --- | --- |
| 1 — Conceitos e decisões de projeto | Escolha de abordagens, componentes e controles | — | 30 |
| 2 — Diagnóstico e melhoria de soluções | Identificação de falhas, medições e ajustes | — | 30 |
| 3 — Integração, riscos e operação | Contratos entre componentes, segurança e revisão | Aulas 4.1 a 6.2 | 30 |
| 4 — Evidências e escolhas de arquitetura | Evidências, recuperação de informação e desenho de componentes | Aulas 4.1 a 6.2 | 30 |
| 5 — Qualidade e investigação de falhas | Diagnóstico, contexto, métricas e controles de qualidade | Aulas 4.1 a 6.2 | 30 |
| 6 — Entrega e controle de soluções | Custos, contratos, liberação e responsabilidade operacional | Aulas 4.1 a 6.2 | 30 |
| 7 — Precisão e recall | Prova temática: interpretação, cálculos, erros e decisões | Aula 2.4 e guia | 30 |

**As provas gerais não são partes sequenciais.** Cada uma cobre as 22 aulas de 1.1 a 3.4; as provas 3 a 6 também cobrem todas as aulas de 4.1 a 6.2. As questões integradoras preservam as 30 questões por prova. Os 180 enunciados são diferentes. Consulte `aulas` e `referencia` em cada questão no banco para rastrear a origem.

A **prova 7 é temática** e acrescenta 30 enunciados diferentes, totalizando 210 questões. Ela avalia precisão e recall em diferentes cenários, a distinção entre falsos positivos e negativos, a diferença para acurácia, dados insuficientes, limiares e casos de denominador zero. Não é uma sétima revisão de todas as aulas.

## Guia de precisão e recall

Leia [Precisão e recall — explicações simples](GUIA-PRECISAO-RECALL.md). O documento resolve passo a passo a questão dos 100 atendimentos, explica as duas bases da divisão, traz uma analogia, uma matriz de confusão e exercícios comentados. O conteúdo parte da aula 2.4 e desenvolve exemplos e casos-limite didáticos.

Na prova 7, tente justificar qual grupo está usando como denominador antes de escolher uma alternativa. Leia as explicações depois de confirmar. Para evitar acerto apenas por memória das alternativas, explique também a conta sem olhar as opções.

## Arquivos e manutenção

- `provas.json`: conteúdo consumido diretamente pelo frontend.
- `REGRAS-PROVAS.md`: critérios pedagógicos e de revisão obrigatórios.
- `scripts/prova-1.cjs` a `scripts/prova-6.cjs`: conteúdo autoral usado para publicar o JSON. Na fonte, a primeira alternativa é a correta; o gerador distribui as posições no JSON.
- `scripts/prova-7.cjs`: banco específico de precisão e recall, com a mesma convenção de gabarito na fonte.
- `scripts/gerar-provas.cjs`: publica os bancos no formato da interface, com posições de gabarito equilibradas e sem aleatoriedade na geração.
- `scripts/validar-provas.cjs`: confere as sete provas, correspondência com os bancos e gabaritos, IDs, enunciados únicos, referências, cobertura geral ou temática, exclusão da aula 0.1, alternativas, explicações e compatibilidade com o validador da interface.

Para alterar as provas de forma permanente, edite os bancos e execute:

```powershell
node scripts/gerar-provas.cjs
node scripts/validar-provas.cjs
```

Editar apenas o JSON funciona para visualizar mudanças, mas elas serão sobrescritas caso o gerador seja executado novamente. Node é necessário apenas para gerar/validar; o frontend continua lendo o JSON pronto.
