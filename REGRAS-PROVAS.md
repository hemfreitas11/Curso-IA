# Regras para criar provas e questões

Estas regras devem ser consultadas e seguidas sempre que forem criadas ou alteradas provas deste projeto.

## Objetivo pedagógico

- As questões devem avaliar entendimento e aplicação dos conceitos, não apenas memorização de frases ou definições.
- Sempre que possível, apresentar uma situação concreta e pedir que a pessoa escolha, compare, diagnostique ou justifique uma decisão.
- Distratores devem ser plausíveis e representar confusões comuns entre conceitos; evitar alternativas absurdas ou obviamente incompatíveis com o caso.
- Não tornar a correta óbvia pelo contraste: evitar distratores caricatos, descuidados ou claramente irresponsáveis enquanto a correta é a única sensata.
- Evitar absolutos que entreguem o distrator, como “sempre”, “nunca”, “obrigatoriamente”, “sem avaliação” ou “sem teste”, exceto quando o absoluto for o próprio conceito avaliado.
- Todas as alternativas devem responder ao mesmo problema e ser parecidas em nível de detalhe, tom, especificidade e extensão. A correta não deve ser a única longa, cautelosa ou bem elaborada.
- Distratores devem representar escolhas que alguém razoável poderia fazer, mas conter uma falha conceitual identificável.
- Antes de aprovar, perguntar: “Uma pessoa competente, mas com compreensão parcial, poderia escolher cada distrator?” Se não, reescrever as alternativas fracas.
- Não usar como distrator uma solução alternativa que também seja defensável no cenário. Delimitar melhor o enunciado quando necessário (por exemplo, perguntar qual abordagem aproveita diretamente dados rotulados ou qual é a escolha inicial típica para aquele tipo de problema).
- Fazer uma revisão sem olhar o gabarito: verificar se a correta pode ser identificada apenas pelo tamanho, tom, vocabulário, ressalvas ou uso de absolutos. Se puder, equilibrar o conjunto.
- Deve existir exatamente uma alternativa correta por questão.
- Usar linguagem clara, direta e adequada a quem está aprendendo.

## Explicações

- Cada alternativa deve ter sua própria explicação, inclusive as incorretas.
- A explicação da correta deve dizer por que ela resolve o caso ou aplica corretamente o conceito.
- A explicação de cada incorreta deve apontar o erro de raciocínio e, quando útil, distinguir o conceito confundido.
- Manter as explicações curtas e fáceis de ler; usar exemplos simples quando ajudarem.
- As explicações não podem aparecer antes da confirmação da resposta.

## Formato e experiência

- O conteúdo da prova deve ser armazenado em JSON válido, sem comentários e sem vírgulas finais.
- Uma prova contém questões com enunciado e alternativas; a interface deve embaralhar todas as questões a cada início de prova, sem agrupamento por aula ou módulo e sem alterar a ordem no banco original.
- A interface mostra uma questão por vez e oculta todas as explicações até a pessoa selecionar uma alternativa e clicar em **Confirmar**.
- Depois da confirmação, mostrar as explicações de todas as alternativas e indicar visualmente a correta.
- Não permitir confirmar sem selecionar uma alternativa nem trocar resposta após confirmar.
- Deve haver exatamente uma alternativa marcada como correta (`correta: true`) por questão.
- Incluir referências às aulas/fontes no banco quando disponíveis, para rastreabilidade, mas não exibir a aula ou o módulo de origem na interface da questão, para não dar pistas.

## Revisão antes de publicar

- Validar que o JSON pode ser carregado.
- Conferir que cada questão tem pelo menos duas alternativas e exatamente uma correta.
- Conferir que todas as alternativas têm texto e explicação.
- Revisar a qualidade dos distratores e confirmar que a resposta não depende de informação ausente da aula ou do enunciado.

## Cobertura e equilíbrio de provas completas

- Avaliar apenas conteúdos efetivamente recuperados e lidos. Declarar o escopo disponível; links ou títulos de módulos posteriores não equivalem ao conteúdo dessas aulas.
- As seis provas gerais têm 30 questões cada e cobrem todas as 22 aulas técnicas de 1.1 a 3.4. Além disso, as provas 3 a 6 cobrem todas as aulas extraídas de 4.1 a 6.2; as aulas 4.1 a 6.2 podem ser combinadas em questões integradoras para preservar o total de 30. A aula 0.1, sobre organização da trilha, não deve ser avaliada; a aula 6.3 também fica fora das provas gerais. Ao remover uma questão, preservar o total e a cobertura prevista para aquela prova.
- Provas temáticas são adicionais às seis provas gerais e cobrem apenas o tema declarado. A prova 7 tem 30 questões de precisão e recall, vinculadas à aula 2.4 e ao guia complementar `GUIA-PRECISAO-RECALL.md`; não se exige dela cobertura das outras aulas. Cada questão deve definir o alvo positivo quando necessário e fornecer os dados para uma resposta única. Nos casos de denominador zero, explicitar se a pergunta usa apenas a fórmula ou alguma convenção de software.
- Criar cenários e perguntas diferentes entre as provas; não apenas trocar nomes, números ou a posição da resposta de uma questão existente.
- Acrescentar questões que conectem componentes e conceitos, além das questões focadas em cada aula.
- Distribuir as posições corretas sem ciclos simples nem concentração em uma letra. Com 30 questões e quatro alternativas, usar sete ou oito gabaritos por posição.
- Conferir o conjunto quanto a pistas de extensão: a correta não pode ser sistematicamente a alternativa mais longa ou a única que inclui testes, limites e ressalvas.
- As verificações automáticas de estrutura não substituem revisão pedagógica da plausibilidade dos distratores e da unicidade conceitual da resposta.
