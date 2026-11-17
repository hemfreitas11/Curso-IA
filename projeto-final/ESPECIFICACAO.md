# Escopo e critérios de aceite

## Decisões do usuário

Terminal; Python sem dependências; base determinística e OpenAI opcional; sem
chamadas pagas agora; execução completa das etapas; traces com texto mascarado.

## Contrato do assistente

Responde somente às quatro políticas integrais da aula 6.3 e consulta o pedido
fictício 48213 (em transporte; previsão 12/11). Outros pedidos não existem.
Não cancela, reembolsa, agenda nem modifica nada. Não interpreta dados financeiros,
não pede dados sensíveis e não promete condições não descritas nas políticas.
Falta de evidência, fonte ausente, dado sensível ou falha no modelo opcional
encaminham para atendente. Encaminhamento é apenas sinalização local, sem fila real.
Não há identidade real: a ferramenta é exclusivamente uma simulação didática.

## Métricas e aceite

- Conteúdo correto em pelo menos 9 dos 10 casos oficiais.
- Recall de encaminhamento de 100% nos casos oficiais (positivo = precisa de humano).
- Precisão = VP/(VP+FP); recall = VP/(VP+FN). Denominador zero é `null`, não 100%.
- Mostrar conteúdo e decisão separadamente; um acerto textual não prova correção semântica.
- Preservar linha de base e três melhorias cumulativas, com comparação caso a caso.
- Adicionar casos de risco e de guardrails; não ocultar regressões.
- Registrar um trace de falha e diagnóstico.
- Comparar implementação própria com referência apenas após construí-la.
- Relatório curto com checklist da aula 6.2 e lacunas para produção.

## Experimento planejado (antes dos resultados)

1. `inicial`: interseção de palavras significativas; frase mais parecida e fonte.
2. `radicais`: mesma busca, comparando prefixos de cinco caracteres.
3. `politica`: mesma recuperação, mas devolver a política inteira.
4. `limiar`: reduzir limiar de sobreposição de 0,5 para 0,3; medir riscos.
5. Iterações de correção e proteção isoladas: `desempate`, `entrada`, `escopo`
   e `segura` (validação de fonte). As três melhorias acima permanecem reproduzíveis.

O limiar é heurístico, não probabilidade. Se a redução causar falsos negativos nos
casos de risco, rejeitar a variante desprotegida como configuração final. Uma
configuração protegida só é aceita depois de repetir os casos de risco.

## OpenAI opcional

Só reescreve uma resposta já fundamentada. Não escolhe ferramentas nem amplia
escopo. Recebe a pergunta mascarada e a política recuperada, nunca histórico nem
segredos. Modelo configurado explicitamente; timeout, teto de chamadas/tokens,
sem retries automáticos. Registrar uso, sem expor chave. Validar fonte e contrato
de saída; tais validações não demonstram fidelidade semântica de um LLM.

## Privacidade e limites

Traces JSONL locais fora do Git; mascaramento é defesa parcial e não anonimização.
Retenção operacional curta deve ser definida antes de uso real. Há opção de não
persistir traces. Testes e evidências publicados usam apenas exemplos fictícios.
Perguntas não têm memória entre turnos. Limite de tamanho de entrada e uma única
consulta/busca por pergunta; sem loop autônomo.
