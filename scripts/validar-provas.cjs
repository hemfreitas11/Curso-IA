const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const raiz = path.join(__dirname, '..');
const dados = JSON.parse(fs.readFileSync(path.join(raiz, 'provas.json'), 'utf8'));
const aulasBase = [...Array.from({ length: 10 }, (_, i) => `1.${i + 1}`), ...Array.from({ length: 8 }, (_, i) => `2.${i + 1}`), ...Array.from({ length: 4 }, (_, i) => `3.${i + 1}`)];
const aulasNovas = ['4.1', '4.2', '4.3', '4.4', '5.1', '5.2', '5.3', '5.4', '6.1', '6.2'];
const aulas = [...aulasBase, ...aulasNovas];
const perguntas = new Set();
const ids = new Set();
assert.equal(dados.provas.length, 7);
assert.equal(new Set(dados.provas.map(p => p.id)).size, 7);
assert.deepEqual(dados.provas.map(p => p.id), Array.from({ length: 7 }, (_, i) => `prova-${i + 1}`));

// Executa também o validador real da interface, sem carregar a página.
const contexto = { document: { getElementById: () => ({}) } };
vm.createContext(contexto);
const app = fs.readFileSync(path.join(raiz, 'app.js'), 'utf8');
assert.match(app, /\ncarregarProvas\(\);\s*$/);
vm.runInContext(app.replace(/\ncarregarProvas\(\);\s*$/, ''), contexto);

// Verifica o embaralhamento sem depender de um resultado aleatório específico.
const originais = dados.provas[0].questoes;
const ordemOriginal = originais.map(q => q.id);
vm.runInContext('Math.random = () => 0;', contexto);
const embaralhadas = contexto.embaralhar(originais);
assert.notEqual(embaralhadas, originais);
assert.notDeepEqual(Array.from(embaralhadas, q => q.id), ordemOriginal);
assert.deepEqual(Array.from(embaralhadas).sort((a, b) => a.id.localeCompare(b.id)), [...originais].sort((a, b) => a.id.localeCompare(b.id)));
assert.deepEqual(originais.map(q => q.id), ordemOriginal, 'O banco original não deve ser reordenado');
vm.runInContext('Math.random = () => 0.999999;', contexto);
const outraOrdem = contexto.embaralhar(originais);
assert.notDeepEqual(Array.from(outraOrdem, q => q.id), Array.from(embaralhadas, q => q.id));
assert.equal(contexto.embaralhar([]).length, 0);
assert.equal(contexto.embaralhar([originais[0]])[0], originais[0]);
const html = fs.readFileSync(path.join(raiz, 'index.html'), 'utf8');
assert.doesNotMatch(html, /id="referencia"/);
assert.doesNotMatch(app, /\$\('referencia'\)/);

for (const prova of dados.provas) {
  assert.equal(prova.questoes.length, 30, prova.id);
  contexto.validarProva(prova);
  const banco = require(path.join(__dirname, `${prova.id}.cjs`));
  assert.equal(banco.length, 30);
  assert.deepEqual(prova.questoes.map(q => q.pergunta), banco.map(q => q[1]), 'JSON deve corresponder ao banco autoral');
  const cobertura = new Set();
  const posicoes = [0, 0, 0, 0];
  for (const [qi, q] of prova.questoes.entries()) {
    assert(!ids.has(q.id), `ID repetido: ${q.id}`);
    ids.add(q.id);
    assert(!perguntas.has(q.pergunta), `Enunciado repetido: ${q.id}`);
    perguntas.add(q.pergunta);
    assert.equal(q.alternativas.length, 4);
    assert.equal(new Set(q.alternativas.map(a => a.id)).size, 4);
    assert.equal(new Set(q.alternativas.map(a => a.texto)).size, 4);
    assert.equal(q.alternativas.filter(a => a.correta === true).length, 1);
    for (const a of q.alternativas) {
      assert.equal(typeof a.correta, 'boolean');
      assert(a.texto.trim() && a.explicacao.trim());
      const fonte = banco[qi].slice(2).find(opcao => opcao[0] === a.texto);
      assert(fonte, `${q.id}: alternativa não encontrada na fonte`);
      assert.equal(a.explicacao, fonte[1], `${q.id}: explicação diferente da fonte`);
      assert.equal(a.correta, a.texto === banco[qi][2][0], `${q.id}: gabarito diferente da fonte`);
    }
    posicoes[q.alternativas.findIndex(a => a.correta)]++;
    assert(q.referencia.trim());
    assert(Array.isArray(q.aulas) && q.aulas.length > 0);
    assert(!q.aulas.includes('0.1'), `${prova.id}: aula 0.1 excluída do escopo`);
    assert(!q.referencia.includes('Aula 0.1'), `${q.id}: referência à aula excluída`);
    for (const aula of q.aulas) {
      assert(aulas.includes(aula), `Aula fora do escopo: ${aula}`);
      cobertura.add(aula);
    }
  }
  const tematica = prova.id === 'prova-7';
  const expandida = ['prova-3', 'prova-4', 'prova-5', 'prova-6'].includes(prova.id);
  const coberturaEsperada = tematica ? ['2.4'] : expandida ? aulas : aulasBase;
  for (const aula of coberturaEsperada) assert(cobertura.has(aula), `${prova.id}: falta aula ${aula}`);
  if (tematica) {
    assert.deepEqual([...cobertura], ['2.4']);
    assert.match(prova.titulo, /Precisão e recall/);
    assert.match(prova.descricao, /GUIA-PRECISAO-RECALL\.md/);
    assert(fs.existsSync(path.join(raiz, 'GUIA-PRECISAO-RECALL.md')));
  }
  assert(posicoes.every(n => n >= 7 && n <= 8), 'Gabaritos desequilibrados');
  console.log(`${prova.id}: 30 questões, ${tematica ? 'tema precisão e recall' : `${expandida ? '32' : '22'} aulas técnicas`}, 120 explicações; gabaritos A/B/C/D: ${posicoes.join('/')}.`);
}
assert.equal(perguntas.size, 210);
console.log('Validação concluída, incluindo compatibilidade com o validador do frontend.');
