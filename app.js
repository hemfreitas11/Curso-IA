const state = { provas: [], prova: null, indice: 0, selecionada: null, confirmada: false, acertos: 0 };

const $ = (id) => document.getElementById(id);
const selecao = $('selecao');
const area = $('area-prova');
const resultado = $('resultado');

async function carregarProvas() {
  try {
    const resposta = await fetch('provas.json');
    if (!resposta.ok) throw new Error(`Não foi possível ler provas.json (${resposta.status}).`);
    const dados = await resposta.json();
    if (!Array.isArray(dados.provas) || dados.provas.length === 0) throw new Error('O arquivo não contém provas.');
    dados.provas.forEach(validarProva);
    state.provas = dados.provas;
    const select = $('prova-select');
    select.replaceChildren(new Option('Selecione…', ''));
    state.provas.forEach((prova, i) => select.add(new Option(prova.titulo, String(i))));
    select.addEventListener('change', atualizarDescricao);
    $('iniciar').addEventListener('click', iniciar);
    $('confirmar').addEventListener('click', confirmar);
    $('proxima').addEventListener('click', avancar);
    $('voltar-selecao').addEventListener('click', voltarSelecao);
    $('nova-prova').addEventListener('click', voltarSelecao);
    $('alternativas').addEventListener('change', (event) => {
      if (!state.confirmada && event.target.name === 'resposta') {
        state.selecionada = Number(event.target.value);
        $('confirmar').disabled = false;
      }
    });
  } catch (erro) {
    $('erro').textContent = `${erro.message} Abra esta página por um servidor local (não direto como arquivo).`;
  }
}

function validarProva(prova) {
  if (!prova.titulo || !Array.isArray(prova.questoes) || !prova.questoes.length) throw new Error('Uma prova está sem título ou questões.');
  prova.questoes.forEach((questao, qi) => {
    if (!questao.pergunta || !Array.isArray(questao.alternativas) || questao.alternativas.length < 2) throw new Error(`Questão ${qi + 1} inválida.`);
    if (questao.alternativas.filter((a) => a.correta === true).length !== 1) throw new Error(`Questão ${qi + 1} deve ter exatamente uma alternativa correta.`);
    if (questao.alternativas.some((a) => !a.texto || !a.explicacao || typeof a.correta !== 'boolean')) throw new Error(`Alternativas da questão ${qi + 1} incompletas.`);
  });
}

function atualizarDescricao() {
  const prova = state.provas[Number($('prova-select').value)];
  $('descricao-prova').textContent = prova ? `${prova.descricao || ''} ${prova.questoes.length} questões.` : '';
  $('iniciar').disabled = !prova;
}

function iniciar() {
  const prova = state.provas[Number($('prova-select').value)];
  state.prova = { ...prova, questoes: embaralhar(prova.questoes) };
  state.indice = 0;
  state.acertos = 0;
  selecao.classList.add('hidden');
  resultado.classList.add('hidden');
  area.classList.remove('hidden');
  renderizarQuestao();
}

function embaralhar(questoes) {
  const copia = [...questoes];
  for (let i = copia.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [copia[i], copia[j]] = [copia[j], copia[i]];
  }
  return copia;
}

function renderizarQuestao() {
  const q = state.prova.questoes[state.indice];
  state.selecionada = null;
  state.confirmada = false;
  $('progresso').textContent = `Questão ${state.indice + 1} de ${state.prova.questoes.length}`;
  $('pergunta').textContent = q.pergunta;
  $('aviso').textContent = '';
  $('confirmar').disabled = true;
  $('confirmar').classList.remove('hidden');
  $('proxima').classList.add('hidden');
  const form = $('alternativas');
  form.replaceChildren();
  q.alternativas.forEach((alt, i) => {
    const label = document.createElement('label');
    label.className = 'option';
    const input = document.createElement('input');
    input.type = 'radio'; input.name = 'resposta'; input.value = String(i);
    const body = document.createElement('span'); body.className = 'option-content';
    const text = document.createElement('span'); text.textContent = alt.texto;
    body.append(text);
    label.append(input, body);
    form.append(label);
  });
}

function confirmar() {
  if (state.selecionada === null || state.confirmada) return;
  state.confirmada = true;
  const q = state.prova.questoes[state.indice];
  const acertou = q.alternativas[state.selecionada].correta;
  if (acertou) state.acertos++;
  $('aviso').textContent = acertou ? 'Resposta correta.' : 'Resposta incorreta. Veja as explicações abaixo.';
  $('alternativas').querySelectorAll('input').forEach((input, i) => {
    input.disabled = true;
    const alt = q.alternativas[i];
    const label = input.closest('.option');
    if (alt.correta) label.classList.add('correct');
    if (i === state.selecionada && !alt.correta) label.classList.add('incorrect-selected');
    const explanation = document.createElement('p');
    explanation.className = 'explanation';
    explanation.textContent = `${alt.correta ? 'Correta' : 'Incorreta'}: ${alt.explicacao}`;
    label.querySelector('.option-content').append(explanation);
  });
  $('confirmar').classList.add('hidden');
  $('proxima').textContent = state.indice + 1 === state.prova.questoes.length ? 'Ver resultado' : 'Próxima questão';
  $('proxima').classList.remove('hidden');
}

function avancar() {
  if (!state.confirmada) return;
  state.indice++;
  if (state.indice < state.prova.questoes.length) return renderizarQuestao();
  area.classList.add('hidden');
  resultado.classList.remove('hidden');
  $('pontuacao').textContent = `Você acertou ${state.acertos} de ${state.prova.questoes.length} questões.`;
}

function voltarSelecao() {
  area.classList.add('hidden');
  resultado.classList.add('hidden');
  selecao.classList.remove('hidden');
}

carregarProvas();
