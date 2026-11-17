// Conteúdo autoral baseado nos módulos locais. A primeira opção de cada item
// é o gabarito na fonte; a publicação distribui as posições de forma determinística.
const fs = require('node:fs');
const path = require('node:path');
const bancos = Array.from({ length: 7 }, (_, i) => require(`./prova-${i + 1}.cjs`));
const titulos = {
  '1.1': 'O que é inteligência artificial',
  '1.2': 'O que é engenharia de IA',
  '1.3': 'IA, Machine Learning, Deep Learning e IA generativa',
  '1.4': 'Como funciona um LLM: tokens, contexto, amostragem e alucinação',
  '1.5': 'Prompt engineering: papel, contexto, exemplos e formato',
  '1.6': 'Treino vs contexto: fine-tuning ou RAG?',
  '1.7': 'Embeddings: como a IA representa significado',
  '1.8': 'RAG do zero: chunking, banco vetorial, retrieval e top-k',
  '1.9': 'RAG melhor: reranking, busca híbrida e citações',
  '1.10': 'Tool calling: como o modelo chama APIs',
  '2.1': 'Agentes e harness: o que existe em volta do modelo',
  '2.2': 'MCP: o padrão que liga a IA aos sistemas',
  '2.3': 'Guardrails: limites para o que o agente diz e faz',
  '2.4': 'Evals: como saber se o agente está bom',
  '2.5': 'Observabilidade: traces, custo, latência e qualidade',
  '2.6': 'Versionar e liberar: prompt também tem versão',
  '2.7': 'Segurança, ética e governança',
  '2.8': 'Loop engineering: planejar, executar, verificar',
  '3.1': 'Agentes de código: o Claude e as outras ferramentas',
  '3.2': 'Recursos do Claude e contexto para agentes de código',
  '3.3': 'Spec-driven development: especificar antes de gerar código',
  '3.4': 'Foundation models: como nascem e como escolher',
  '4.1': 'Python o suficiente para IA',
  '4.2': 'Git do zero, e Git com agentes',
  '4.3': 'APIs e middleware: o agente conversando com os sistemas',
  '4.4': 'Containers e deploy: do notebook ao servidor',
  '5.1': 'Padrões de agentes e como escolher um framework',
  '5.2': 'LangChain: componentes e integrações',
  '5.3': 'LangGraph: agente como grafo de estados',
  '5.4': 'Google ADK: agentes, sub-agentes e A2A',
  '6.1': 'Para onde vai: tendências e o papel do Analista de IA',
  '6.2': 'Checklist de um agente pronto para produção'
};
// Sequências sem ciclo simples; cada prova tem 7 ou 8 gabaritos por posição.
const posicoes = [
  [1,3,0,2,2,0,3,1,0,2,1,3,3,1,2,0,1,0,3,2,0,3,1,2,2,1,0,3,1,2],
  [2,0,3,1,1,3,0,2,3,1,2,0,0,2,1,3,2,3,0,1,3,0,2,1,1,2,3,0,2,1],
  [3,1,2,0,0,2,1,3,2,0,3,1,1,3,0,2,3,2,1,0,2,1,3,0,0,3,2,1,3,0],
  [0,2,1,3,1,0,2,3,3,1,0,2,0,3,2,1,2,0,1,3,1,2,3,0,3,0,2,1,0,2],
  [1,0,3,2,0,2,1,3,2,3,1,0,1,2,0,3,0,1,3,2,2,0,3,1,3,2,1,0,1,3],
  [2,3,0,1,3,1,2,0,1,0,2,3,2,1,3,0,3,2,0,1,1,3,0,2,0,1,2,3,2,0],
  [0,2,3,1,2,1,0,3,1,3,2,0,3,0,1,2,2,0,3,1,0,1,2,3,1,2,0,3,2,0]
];
const nomes = ['Conceitos e decisões de projeto', 'Diagnóstico e melhoria de soluções', 'Integração, riscos e operação', 'Evidências e escolhas de arquitetura', 'Qualidade e investigação de falhas', 'Entrega e controle de soluções', 'Precisão e recall'];
const provas = bancos.map((banco, pi) => {
  const tematica = pi === 6;
  if (banco.length !== 30) throw new Error(`Prova ${pi + 1}: ${banco.length} questões, esperado 30`);
  const questoes = banco.map(([aulas, pergunta, ...opcoes], qi) => {
    const refs = aulas.split(',');
    if (refs.some(a => !titulos[a])) throw new Error(`Referência desconhecida: ${aulas}`);
    if (opcoes.length !== 4 || opcoes.some(o => o.length !== 2 || o.some(s => typeof s !== 'string' || !s.trim()))) throw new Error(`Opções inválidas: ${pi}/${qi}`);
    const itens = opcoes.map(([texto, explicacao], i) => ({ texto, explicacao, correta: i === 0 }));
    const correta = itens.shift();
    // Alternar a ordem dos distratores sem aleatoriedade na publicação.
    if ((qi + pi) % 2) itens.reverse();
    itens.splice(posicoes[pi][qi], 0, correta);
    return {
      id: `p${pi + 1}-q${String(qi + 1).padStart(2, '0')}`,
      aulas: refs,
      referencia: refs.map(a => `Aula ${a} — ${titulos[a]}`).join(' · '),
      pergunta,
      alternativas: itens.map((a, i) => ({ id: 'abcd'[i], ...a }))
    };
  });
  const cobertas = new Set(questoes.flatMap(q => q.aulas));
  const coberturaEsperada = tematica
    ? ['2.4']
    : Object.keys(titulos).filter(a => pi >= 2 || Number(a.split('.')[0]) <= 3);
  for (const aula of coberturaEsperada) if (!cobertas.has(aula)) throw new Error(`Prova ${pi + 1} não cobre ${aula}`);
  if (tematica && [...cobertas].some(a => !coberturaEsperada.includes(a))) throw new Error('Prova temática fora do escopo de precisão e recall');
  return {
    id: `prova-${pi + 1}`,
    titulo: `Prova ${pi + 1} — ${nomes[pi]}`,
    descricao: tematica
      ? '30 questões específicas de precisão e recall: interpretação, cálculos, falsos positivos e negativos, comparação de sistemas e limites das métricas. Estudo complementar: GUIA-PRECISAO-RECALL.md.'
      : pi < 2
        ? '30 questões de aplicação sobre as aulas 1.1 a 3.4. Não inclui a aula 0.1 nem módulos posteriores.'
        : '30 questões de aplicação sobre as aulas 1.1 a 3.4 e 4.1 a 6.2. A aula 0.1 e a aula 6.3 estão excluídas.',
    questoes
  };
});
const perguntas = provas.flatMap(p => p.questoes.map(q => q.pergunta));
if (new Set(perguntas).size !== perguntas.length) throw new Error('Enunciados duplicados');
fs.writeFileSync(path.join(__dirname, '..', 'provas.json'), JSON.stringify({ versao: 1, escopo: 'Material local: provas 1-2 cobrem aulas 1.1 a 3.4; provas 3-6 cobrem aulas 1.1 a 3.4 e 4.1 a 6.2; aula 0.1 excluída e aula 6.3 fora das provas gerais; prova 7 temática de precisão e recall', provas }, null, 2) + '\n', 'utf8');
console.log(`Publicadas ${provas.length} provas, ${perguntas.length} questões, ${perguntas.length * 4} alternativas com explicações. Provas 1-2 cobrem 1.1-3.4; provas 3-6 também cobrem 4.1-6.2; prova 7 é temática.`);
