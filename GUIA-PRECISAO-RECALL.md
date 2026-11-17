# Precisão e recall — um guia para entender de verdade

## 1. A ideia em duas perguntas

Imagine que um assistente decide quais atendimentos enviar para uma pessoa.

- **Precisão:** dos atendimentos que ele **enviou**, quantos realmente precisavam de uma pessoa?
- **Recall:** dos atendimentos que **precisavam** de uma pessoa, quantos ele conseguiu enviar?

Os dois olham para os mesmos acertos, mas comparam esses acertos com **grupos diferentes**.

> **Precisão olha para o que o sistema selecionou. Recall olha para o que ele deveria encontrar.**

Recall também é chamado de **sensibilidade**. Neste guia, pense nele como a capacidade de encontrar os casos que não poderiam ficar de fora.

## 2. Resolvendo a questão da imagem, sem pular etapas

O enunciado diz:

> De 100 casos, 20 exigiam humano. O sistema encaminhou 25, e 15 desses realmente exigiam humano.

Separe as informações em três grupos:

| Informação | Quantidade | O que significa |
| --- | ---: | --- |
| Precisavam de humano | 20 | A necessidade real, conferida por uma referência confiável |
| Foram encaminhados | 25 | A escolha do sistema |
| Foram encaminhados e precisavam | 15 | Os acertos dentro dos encaminhamentos |

### Precisão: olhe para os 25 encaminhados

Dos **25 enviados**, **15 precisavam**.

**Precisão = 15 ÷ 25 = 0,60 = 60%.**

Em linguagem simples: de cada dez encaminhamentos, seis eram necessários e quatro não eram, considerando a proporção desse conjunto.

Os outros **10 encaminhamentos** eram desnecessários: 25 − 15 = 10.

### Recall: olhe para os 20 que precisavam

Dos **20 que precisavam**, o sistema encontrou e enviou **15**.

**Recall = 15 ÷ 20 = 0,75 = 75%.**

Em linguagem simples: encontrou três de cada quatro casos que precisavam de ajuda humana.

Os outros **5 casos necessários ficaram de fora**: 20 − 15 = 5.

**Resposta da questão: precisão de 60% e recall de 75%.**

### Por que não dividir por 100?

Porque 100 é o total de atendimentos. Nenhuma das duas perguntas está perguntando “do total de atendimentos”.

- Precisão pergunta **dos encaminhados**: a base é 25.
- Recall pergunta **dos que precisavam**: a base é 20.

O número 15 aparece nas duas contas porque representa os casos que o sistema encontrou **e** que eram necessários.

## 3. Os quatro resultados possíveis

Primeiro defina o que você quer detectar. Neste exemplo, o alvo é **“precisa de humano”**. Chamaremos esse alvo de **positivo**.

“Positivo” não significa bom. É apenas o nome do grupo que queremos detectar. Em um detector de fraude, por exemplo, positivo pode significar “é fraude”.

| Decisão do sistema | Realmente precisava | Não precisava | Total |
| --- | ---: | ---: | ---: |
| Encaminhou | 15: verdadeiro positivo (VP) | 10: falso positivo (FP) | 25 |
| Não encaminhou | 5: falso negativo (FN) | 70: verdadeiro negativo (VN) | 75 |
| Total | 20 | 80 | 100 |

Leia os nomes em duas partes:

- **Positivo/negativo:** o que o sistema decidiu sobre o alvo.
- **Verdadeiro/falso:** se a decisão estava certa ou errada.

Exemplos:

- **Verdadeiro positivo:** enviou e precisava. Encontrou um caso real.
- **Falso positivo:** enviou, mas não precisava. Gerou um alarme indevido.
- **Falso negativo:** não enviou, mas precisava. Deixou um caso passar.
- **Verdadeiro negativo:** não enviou e não precisava. Acertou ao não agir.

Os 70 verdadeiros negativos vêm dos 80 que não precisavam, menos os 10 encaminhados indevidamente.

## 4. As fórmulas depois de entender a história

```text
Precisão = VP / (VP + FP)
         = acertos selecionados / tudo que o sistema selecionou

Recall   = VP / (VP + FN)
         = acertos selecionados / tudo que realmente era alvo
```

Para escrever como porcentagem, multiplique o resultado por 100.

**Macete:**

- **Precisão:** “Quando o sistema apontou, acertou quanto?”
- **Recall:** “Do que precisava achar, achou quanto?”

Se esquecer a fórmula, reconstrua a pergunta. É mais seguro do que decorar letras.

## 5. Uma analogia: procurar frutas estragadas

Há **10 frutas estragadas** em uma caixa. Você retira **8 frutas**, mas apenas **6 das retiradas estão estragadas**.

- Precisão: das 8 retiradas, 6 estavam estragadas → **6/8 = 75%**.
- Recall: das 10 estragadas, você encontrou 6 → **6/10 = 60%**.
- Falsos positivos: 2 frutas boas retiradas à toa.
- Falsos negativos: 4 frutas estragadas que ficaram na caixa.

Observe: trocar “encaminhar atendimentos” por “retirar frutas” não muda o raciocínio.

## 6. É possível ser muito bom em uma métrica e ruim na outra

### Precisão alta, recall baixo

Existem 100 casos necessários. O sistema seleciona só 10, e os 10 são necessários.

- Precisão: 10/10 = **100%**.
- Recall: 10/100 = **10%**.

Ele raramente aponta à toa, mas deixa muitos casos importantes para trás.

### Recall alto, precisão baixa

Existem 10 casos necessários em 100 atendimentos. O sistema encaminha todos os 100.

- Precisão: 10/100 = **10%**.
- Recall: 10/10 = **100%**.

Ele não perde nenhum caso necessário, mas encaminha muita gente sem necessidade.

**Logo, 100% em uma métrica não garante 100% na outra.**

## 7. Qual erro custa mais?

Não existe uma escolha ideal para todos os problemas.

| Situação | Falso positivo | Falso negativo |
| --- | --- | --- |
| Encaminhar para humano | Envia um caso que o assistente poderia resolver | Deixa sem humano um caso que precisava |
| Detectar fraude | Sinaliza uma compra legítima | Deixa uma fraude passar |
| Bloquear dados sensíveis | Bloqueia uma mensagem legítima | Deixa um dado sensível passar |
| Buscar documentos | Recupera um documento irrelevante | Deixa de recuperar um documento relevante |

Se deixar um vazamento passar é muito grave, é importante buscar **recall alto**, sem ignorar os bloqueios indevidos.

Se os alarmes indevidos estão sobrecarregando a equipe, é importante investigar a **precisão**, sem esconder os casos necessários que estão ficando de fora.

**A decisão depende do custo dos dois erros, não apenas da porcentagem mais bonita.**

## 8. O que acontece ao mudar o limiar?

Imagine que um filtro dá uma pontuação de risco e bloqueia mensagens a partir de certo valor.

- Um limiar **mais baixo** aceita mais mensagens como suspeitas: tende a encontrar mais riscos, mas também pode gerar mais alarmes indevidos.
- Um limiar **mais alto** seleciona menos mensagens: pode reduzir alarmes indevidos, mas também deixar riscos passarem.

Isso precisa ser medido em mensagens com classificação de referência. **Bloquear mais não prova, por si só, que a precisão melhorou.**

No mesmo conjunto, com as mesmas pontuações e apenas o limiar mudando, ampliar os selecionados não perde os verdadeiros positivos que já estavam selecionados. O recall não cai nesse caso. Já a precisão depende de quantos dos novos selecionados são realmente alvo: pode cair, subir ou ficar igual.

## 9. Precisão não é acurácia

**Acurácia** pergunta: “De todas as decisões, quantas estavam certas?”. Ela inclui os acertos de não encaminhar.

Na questão da imagem:

```text
Acurácia = (VP + VN) / total
         = (15 + 70) / 100
         = 85%
```

Por isso a alternativa “precisão de 85%” está errada: 85% é a **acurácia**, não a precisão.

Um exemplo do perigo: em mil casos, só dez são perigosos. Um sistema que libera todos acerta os 990 comuns e tem **99% de acurácia**, mas encontra **zero dos dez perigosos**: recall de **0%**.

## 10. Quando falta informação, não invente uma porcentagem

- “O sistema encaminhou 25 casos.” → não basta para calcular precisão nem recall.
- “Dos 25 encaminhados, 15 precisavam.” → permite calcular precisão, mas ainda falta saber quantos precisavam no total para calcular recall.
- “Havia 20 necessários e 15 foram encontrados.” → permite calcular recall, mas ainda falta o total encaminhado para calcular precisão.

### E quando o denominador é zero?

- Nenhum caso selecionado: precisão seria 0/0, então fica **indefinida nessa conta**.
- Nenhum caso realmente positivo: recall também fica **indefinido nessa conta**.

Ferramentas podem adotar convenções, como mostrar zero ou não apresentar a métrica. É preciso declarar a convenção. Não trate uma divisão por zero como prova de desempenho perfeito.

## 11. Um roteiro para qualquer questão

1. **Defina o alvo.** O que é “positivo” nesse problema?
2. **Separe realidade e decisão.** Quantos eram alvo? Quantos foram selecionados?
3. **Encontre a interseção.** Quantos selecionados realmente eram alvo? Esse é o VP.
4. **Escolha a pergunta.** Dos selecionados (precisão) ou dos alvos reais (recall)?
5. **Faça a divisão e interprete.** Não pare na porcentagem: diga o que ficou de fora e o que foi selecionado à toa.

## 12. Exercícios curtos para fazer antes da prova

Tente responder sem olhar as soluções abaixo.

1. Existem 12 mensagens perigosas. O filtro bloqueia 10 mensagens, das quais 9 são perigosas. Qual é a precisão? E o recall?
2. Um detector acerta todos os cinco alertas que emite, mas havia 25 problemas reais. O que está alto e o que está baixo?
3. Uma busca retorna 20 documentos, dos quais 8 são relevantes. Você consegue calcular recall apenas com isso? Por quê?
4. Um filtro gera 30 alarmes: 18 corretos e 12 indevidos. Há 6 riscos que passaram sem alarme. Identifique VP, FP e FN; depois calcule as métricas.

### Soluções comentadas

1. **Precisão de 90%** (9/10) e **recall de 75%** (9/12). Uma mensagem legítima foi bloqueada; três perigosas passaram.
2. Precisão de **100%** (5/5), mas recall de **20%** (5/25). Os poucos alertas são bons, mas vinte problemas ficaram sem alerta.
3. Não. A precisão é **40%** (8/20), mas falta saber quantos documentos relevantes existiam no conjunto avaliado para calcular recall.
4. VP = 18, FP = 12, FN = 6. Precisão = 18/30 = **60%**. Recall = 18/(18 + 6) = **75%**.

## 13. Como usar a prova específica

Na página de provas, escolha **Prova 7 — Precisão e recall**. São 30 questões embaralhadas, com interpretação, cálculos, comparação de sistemas, erros de classificação e limites das métricas.

Antes de marcar, tente dizer em voz alta: **“Estou dividindo por este número porque a pergunta fala deste grupo.”**

Depois de confirmar, leia também as explicações das alternativas incorretas. Elas mostram confusões comuns: inverter as bases, usar o total de casos ou confundir precisão com acurácia.

Refazer e acertar pela posição da alternativa não prova compreensão. Para conferir se fixou, explique a conta sem olhar as opções e aplique o raciocínio a outro cenário.

---

Base: aula 2.4 de `modulo-2-aulas.txt` (avaliação, matriz de confusão, precisão e recall). Os exemplos, exercícios e casos-limite deste guia são complementos didáticos; não pressupõem conteúdo de módulos posteriores.
