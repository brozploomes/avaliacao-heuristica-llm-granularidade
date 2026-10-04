/**
 * Gera as N definicoes de avaliador a partir de uma fonte unica.
 *
 * Por que N arquivos e nao um agente so: cada avaliador precisa enxergar APENAS o seu
 * servidor MCP. Um agente unico com os dez namespaces alcancaria o navegador dos outros,
 * e isso e canal de contaminacao do estado do objeto — exatamente a independencia que os
 * Formatos A e B manipulam.
 *
 * As N definicoes tem de ser identicas byte a byte, exceto as duas linhas do frontmatter
 * que precisam diferir: `name:` e o namespace de `tools:`. O passo 0 das skills e a conferencia 6 do
 * fechamento verificam isso com `--verificar`.
 *
 *   node .claude/gerar_avaliadores.mjs              gera
 *   node .claude/gerar_avaliadores.mjs --verificar  so confere
 */
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';

const AQUI = path.dirname(fileURLToPath(import.meta.url));
const MODELO = path.join(AQUI, 'avaliador_modelo.template');
const AGENTS = path.join(AQUI, 'agents');
const N = 10;
const NS_MODELO = 'mcp__chrome-devtools__';
const NOME_MODELO = 'avaliador-heuristico';

const slot = i => String(i).padStart(2, '0');
const nomeDe = i => `${NOME_MODELO}-${slot(i)}`;
const nsDe = i => `mcp__cdp-${slot(i)}__`;
const arquivoDe = i => path.join(AGENTS, `${nomeDe(i)}.md`);

function render(modelo, i) {
  return modelo
    .replace(new RegExp(`^name: ${NOME_MODELO}$`, 'm'), `name: ${nomeDe(i)}`)
    .replaceAll(NS_MODELO, nsDe(i));
}

/** desfaz as duas diferencas permitidas, para comparar os corpos */
function normalizar(texto, i) {
  return texto
    .replace(new RegExp(`^name: ${nomeDe(i)}$`, 'm'), `name: ${NOME_MODELO}`)
    .replaceAll(nsDe(i), NS_MODELO);
}

function verificar() {
  const faltando = [];
  const normalizados = [];
  for (let i = 1; i <= N; i++) {
    if (!fs.existsSync(arquivoDe(i))) { faltando.push(nomeDe(i)); continue; }
    const bruto = fs.readFileSync(arquivoDe(i), 'utf8');
    if (bruto.includes(NS_MODELO)) {
      console.error(`REPROVA: ${nomeDe(i)} ainda cita o namespace do modelo`);
      process.exit(1);
    }
    if (!bruto.includes(nsDe(i))) {
      console.error(`REPROVA: ${nomeDe(i)} nao cita o proprio namespace ${nsDe(i)}`);
      process.exit(1);
    }
    normalizados.push({nome: nomeDe(i), corpo: normalizar(bruto, i)});
  }
  if (faltando.length) { console.error('REPROVA: faltam', faltando.join(', ')); process.exit(1); }

  const ref = normalizados[0];
  const divergentes = normalizados.filter(x => x.corpo !== ref.corpo).map(x => x.nome);
  if (divergentes.length) {
    console.error('REPROVA: divergem do primeiro alem de name/namespace:', divergentes.join(', '));
    process.exit(1);
  }

  const modelo = fs.readFileSync(MODELO, 'utf8');
  if (ref.corpo !== modelo) {
    console.error('REPROVA: os avaliadores divergem de avaliador_modelo.template — regere');
    process.exit(1);
  }
  console.log(`OK: ${N} avaliadores identicos ao modelo, exceto name e namespace`);
}

if (process.argv.includes('--verificar')) {
  verificar();
} else {
  const modelo = fs.readFileSync(MODELO, 'utf8');
  for (let i = 1; i <= N; i++) fs.writeFileSync(arquivoDe(i), render(modelo, i));
  console.log(`gerados ${N} avaliadores em .claude/agents/`);
  verificar();
}
