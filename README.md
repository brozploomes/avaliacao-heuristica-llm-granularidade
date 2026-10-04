# Avaliação heurística com LLM e granularidade do prompt: instrumento, coleta e análise

Repositório da pesquisa citada como "repositório da pesquisa (Damião, 2026)" no trabalho de conclusão de
curso do MBA USP/Esalq. Aqui estão o objeto avaliado, o instrumento de coleta completo, os resultados das
nove execuções com os registros visuais de cada achado e o caminho da revisão e da análise até as
métricas.

## A pesquisa

Um LLM, o Claude Opus 5, fez avaliações heurísticas de uma aplicação web que ele próprio operava num
navegador, usando as dez heurísticas de Nielsen. A única coisa que variou foi a maneira de repartir as
heurísticas entre as chamadas ao modelo: uma por chamada (Formato A), quatro grupos de heurísticas afins
(Formato B) ou todas numa chamada só (Formato C), cada formato rodado três vezes sobre o mesmo objeto. Da
coleta saíram 476 achados; a IA, sem saber a origem de cada um, juntou os que tratavam do mesmo problema
em 93 achados unificados, e o pesquisador julgou 83 deles defeitos e 10 falsos positivos, ponto de
partida das métricas que comparam os formatos.

## Conteúdo

```
.
├── objeto/tarefas_crm.html           aplicação avaliada
├── instrumento/                      instrumento de coleta e scripts da análise
│   ├── .mcp.json                     os dez servidores do navegador (cdp-01 a cdp-10)
│   ├── .gitignore                    mantém as saídas de uma nova coleta fora do git
│   ├── .claude/
│   │   ├── settings.json             modelo e permissões da sessão de coleta
│   │   ├── avaliador_modelo.template definição do subagente avaliador
│   │   ├── gerar_avaliadores.mjs     gera e confere as dez cópias do avaliador
│   │   ├── agents/                   caracterizador-objeto.md
│   │   └── skills/                   formato-a, formato-b, formato-c, caracterizar
│   ├── protocolo/                    nucleo_heuristico.md, unificacao.md, analise.md
│   ├── contexto/contexto.md          material de contexto
│   ├── analise/                      sete scripts Python da revisão e da análise
│   ├── evidencias/_incoming/         pasta de trabalho dos avaliadores (vazia)
│   └── resultados/                   destino de uma nova execução (vazia)
├── .claude/                          skill e subagente da unificação, que rodam da raiz
│   ├── skills/unificar/SKILL.md
│   └── agents/unificador.md
├── coleta-2026-09-24/                o que as nove execuções e a caracterização gravaram
│   ├── resultados/                   nove JSONL e caracterizacao_79f2e33c.json
│   ├── exec-1/  exec-2/  exec-3/     registros visuais, por formato e heurística
│   └── caracterizacao_79f2e33c/      instantâneos e exploração da caracterização
├── analise-2026-09-24/               revisão e métricas
├── LICENSE.md
└── MANIFESTO.sha256                  SHA-256 de cada arquivo do repositório
```

## Vocabulário

| Termo | Sentido neste repositório |
|---|---|
| **achado** | item produzido por um subagente avaliador, sempre sob uma única heurística |
| **achado unificado** | conjunto de achados que a IA reuniu por descreverem o mesmo problema da interface; é o que o pesquisador classifica |
| **defeito** | achado unificado que o pesquisador julgou problema real |
| **falso positivo** | achado unificado cujo problema não se verifica no objeto |
| **duplicata** | achado a mais, além do primeiro, de um mesmo defeito dentro de uma mesma execução |
| **defeito exclusivo** | defeito encontrado por um só formato |
| **conjunto agregado (D)** | união dos defeitos de todas as execuções, usada como denominador do recall |
| **unificação** | a operação, feita pela IA sem conhecer formato nem execução, que produz os achados unificados |
| **revisão** | a unificação cega pela IA seguida da classificação e da severidade dadas pelo pesquisador, que é o revisor único |
| **ponto de manifestação** | tela ou estado em que um defeito aparece |
| **leitura** | texto que a IA escreve, para cada heurística presente num achado unificado, representando os achados daquela heurística |

A definição completa, com os termos que o estudo evita, está em `instrumento/protocolo/analise.md`, §1.

## Como o instrumento está organizado

### Objeto

`objeto/tarefas_crm.html`, SHA-256 `79f2e33c8caab3d0c0475f4516480f78b99cf79bd5a246b12b7d34e8c58946e5`.
É uma página única, que roda no navegador sem acesso à rede e imita a agenda e a lista de atividades de
um CRM. As respostas do servidor são simuladas pelo próprio arquivo, os dados ficam em memória e o "hoje"
da aplicação é sempre 20 set. 2026, então toda abertura começa do mesmo estado. A aplicação e todos os
dados que ela exibe são fictícios e foram criados pelo pesquisador com auxílio de IA.

### Material de contexto

`instrumento/contexto/contexto.md`, SHA-256 `40b8bef5fc025c3e3d8670f8c219d6edd6d4fb4fd0d99032f0e376b4e68b5e0e`.
Três partes: (A) descrição da funcionalidade e dos comportamentos, (B) cenários de uso e (C) dez tarefas
para guiar a inspeção. Vai colado na íntegra em toda chamada de avaliação e na caracterização. A linha
"Referência do objeto" traz o caminho do arquivo na máquina da coleta; ela ficou como estava porque o
hash do arquivo inteiro está registrado nos cabeçalhos.

### Núcleo heurístico

`instrumento/protocolo/nucleo_heuristico.md`, o mesmo nos três formatos. Tem seis seções: (1) papel e
objetivo, (2) entradas, (3) as dez heurísticas, cada uma com definição, "por que importa", dicas e
exemplo de referência, (4) rubrica de severidade de 0 a 4, (5) formato de saída e (6) regras gerais.
Cada chamada recebe as seções 1, 4 e 6 e apenas os blocos da seção 3 que lhe cabem; o formato de saída
chega ao avaliador como esquema JSON, dentro da definição do subagente. A seção 3 é texto de terceiros
(ver `LICENSE.md`).

### Formatos A, B e C

| | Formato A | Formato B | Formato C |
|---|---|---|---|
| Skill | `/formato-a` | `/formato-b` | `/formato-c` |
| Chamadas por execução | 10 | 4 | 1 |
| Heurísticas por chamada | uma, de H1 a H10 | G1: H1, H5, H9 · G2: H2, H4, H8 · G3: H3, H7 · G4: H6, H10 | as dez |
| Subagentes e navegadores | 10, em paralelo | 4, em paralelo | 1 |
| Identificador do achado | `A-H<k>-NNN` | `B-G<n>-NNN` | `C-H<k>-NNN` |

O texto de cada chamada está, literal, no §3 de cada skill; o agente orquestrador só preenche os campos
entre chaves. De um formato para outro mudam a frase de abertura, os blocos de heurística e as instruções
de escopo: em A, o avaliador descreve o problema apenas pela heurística da chamada; em B e C, registra um
achado para cada heurística violada. Em B, o texto não diz qual é o grupo nem o que une as heurísticas
dele. O restante é idêntico nos três.

### Orquestração: skill, agente orquestrador e subagentes avaliadores

Cada skill de formato é executada pela própria conversa, que atua como agente orquestrador e não avalia
nada. Os passos estão numerados na skill:

- **0. Verificação inicial.** Abre e recarrega o objeto em cada navegador, confirma o material de
  contexto, deriva a proveniência (versões, commit, hashes), mede a área visível em cada navegador,
  confere as definições de avaliador e a árvore limpa do git e grava o cabeçalho do JSONL depois do "ok"
  do pesquisador.
- **3. Disparo.** Delega todas as chamadas numa única mensagem; cada subagente recebe uma pasta com nome
  aleatório para gravar os achados e as capturas.
- **4. Fechamento de cada chamada.** Lê o `achados.json` de cada subagente, acrescenta formato, `id` e
  `fora_do_escopo`, move as capturas para a pasta da execução e grava os achados no JSONL.
- **5. Encerramento.** Grava a linha de encerramento, com tempos, tokens e usos de ferramenta, e roda as
  conferências finais.

O **subagente avaliador** é definido por `instrumento/.claude/avaliador_modelo.template`. Ele tem só a
ferramenta `Write` e as 20 ferramentas do Chrome DevTools MCP listadas no campo `tools:` do modelo, que
cobrem navegação, cliques e teclado, formulários, diálogos, capturas, árvore de acessibilidade, script na
página, console, rede e tamanho da janela. Não tem leitura de arquivo nem shell. Na coleta rodaram dez
cópias, `avaliador-heuristico-01` a `-10`, geradas por `gerar_avaliadores.mjs` e diferentes do modelo
apenas no nome e no servidor (`cdp-01` a `cdp-10`): cada avaliador enxerga somente o próprio navegador.
As cópias não estão publicadas por serem idênticas ao modelo fora desses dois pontos.

`instrumento/.mcp.json` declara dez servidores `chrome-devtools-mcp@1.8.0`, cada um com um Chrome próprio,
perfil temporário (`--isolated`), sem janela (`--headless`) e área visível de 1440 por 900.
`instrumento/.claude/settings.json` fixa o modelo `claude-opus-5` e as permissões da sessão: ferramentas
dos dez servidores, escrita em `evidencias/` e `contexto/` e os comandos de shell do orquestrador.

As nove execuções correram em três rodadas, sempre na ordem A, B, C, cada uma em conversa nova (horário
de Brasília, do campo `datahora_inicio` dos cabeçalhos):

| Rodada | Formato A | Formato B | Formato C |
|---|---|---|---|
| 1 | 21/09 23:20 · 76 achados | 22/09 00:06 · 48 achados | 22/09 00:52 · 26 achados |
| 2 | 22/09 23:39 · 77 achados | 23/09 00:45 · 58 achados | 23/09 03:38 · 37 achados |
| 3 | 23/09 21:44 · 74 achados | 23/09 22:29 · 53 achados | 23/09 23:11 · 27 achados |

### Caracterização

A skill `/caracterizar` (`instrumento/.claude/skills/caracterizar/SKILL.md`) e o subagente
`caracterizador-objeto` (`instrumento/.claude/agents/caracterizador-objeto.md`) rodam em sessão própria,
com o modelo da coleta e o servidor `cdp-01`. Medem os elementos do DOM visíveis no estado
inicial e contam telas e modais explorando as tarefas do material de contexto; o resultado nunca entra
numa chamada de avaliação. Saídas: `coleta-2026-09-24/resultados/caracterizacao_79f2e33c.json` (294
elementos visíveis de 295 no DOM, duas telas e dois modais) e `coleta-2026-09-24/caracterizacao_79f2e33c/`,
com o instantâneo de cada tela e modal e o `exploracao.json`. O cabeçalho dela registra o commit
`a87bb85`, anterior ao da coleta; nenhum arquivo usado pela caracterização mudou entre os dois.

### Unificação

- `.claude/skills/unificar/SKILL.md`: a skill que orquestra a unificação. Roda de uma conversa aberta na
  raiz do repositório: monta o prompt, dispara o subagente, guarda e valida a saída, registra a
  proveniência e depois pede as leituras em lotes.
- `.claude/agents/unificador.md`: o subagente, só com a ferramenta de leitura e restrito ao arquivo que
  recebe.
- `instrumento/protocolo/unificacao.md`: a régua de unificação (enunciado, elemento, correção), os campos
  de cada achado que entram no prompt (localização, descrição da falha e sugestão de correção), o texto
  do prompt, o registro da verificação em amostra desse corte de campos e o prompt das leituras.
- `analise-2026-09-24/prompt_unificacao.md`: o prompt tal como foi enviado, com os 476 achados sob chaves
  `K###`.
- `analise-2026-09-24/unificacao_ia.json`: os 93 achados unificados validados, com as leituras.
- `analise-2026-09-24/unificacao_proveniencia.json`: data, modelo, nível de raciocínio, versão do
  aplicativo, semente e rodadas.

As saídas brutas do subagente, os lotes das leituras e a pasta cega não foram publicados. O conjunto cego
e o mapa de chaves se regeneram idênticos a partir da coleta e da semente (ver "Como recalcular as
métricas").

### Revisão e análise

`instrumento/protocolo/analise.md` define as unidades, a ordem das operações, o critério de falso positivo
fixado antes da coleta, a trilha de decisões, as fórmulas das métricas e o que a análise não pode
afirmar. Os scripts ficam em `instrumento/analise/` (Python 3.13, só biblioteca padrão; todos aceitam
`--help`):

| Script | O que faz | Entrada → saída |
|---|---|---|
| `reunir_cegar.py` | reúne os nove JSONL, embaralha com a semente e troca o `id` pela chave `K###` | JSONL → `achados_cegos.json`; na pasta `-fechado`, `mapa_chaves.json`, `encerramentos.json`, `fora_do_escopo.json` |
| `unificar_prompt.py` | monta e valida o prompt da unificação e os lotes das leituras | `achados_cegos.json` → `prompt_unificacao.md`; saída da IA → `unificacao_ia.json` |
| `revisar.py` | página local de revisão (127.0.0.1), uma decisão por achado unificado | → `decisoes.json` |
| `validar_revisao.py` | confere que todo achado unificado tem decisão válida | `decisoes.json` → `integridade.md` |
| `reatar_trilha.py` | devolve a cada achado `id`, formato, execução e chamada e grava a trilha | decisões, unificação e mapa → `trilha_decisoes.csv` |
| `metricas.py` | métricas por formato e por execução | trilha, encerramentos, fora do escopo → `metricas.json`, `metricas.md` |
| `comum.py` | leitura dos JSONL, convenção do `id`, colunas da trilha | |

### Versões

Publica-se a versão atual do instrumento e dos scripts. O campo `commit_instrumento` dos cabeçalhos
(`9b8413a`) identifica o repositório de desenvolvimento, cujo histórico não foi publicado. Antes da
publicação, `git diff 9b8413a HEAD` confirmou que nada mudou no núcleo heurístico, no material de
contexto, nas definições dos subagentes e no modelo do avaliador, no `.mcp.json`, no `settings.json`, na
skill de caracterização e no texto da delegação das três skills de formato.

> As skills de avaliação publicadas incluem correções de descrição feitas após a coleta, em 24 set.
> 2026: o campo `registro` nas linhas de achado e ajustes nas conferências finais do agente
> orquestrador. O texto entregue aos subagentes avaliadores, o núcleo heurístico, o material de
> contexto e o objeto são idênticos aos da coleta; o objeto e o material de contexto conferem com os
> hashes registrados nos cabeçalhos das nove execuções. Como o campo `registro` só passou a ser
> prescrito depois da coleta, ele não é uniforme nos achados publicados: aparece apenas nas execuções 1
> e 3 do Formato A (150 achados), em que o agente orquestrador o gravou por iniciativa própria, e falta
> nos outros 326.

A skill de unificação publicada é a que rodou, sem alteração. Dos scripts da análise, só o `metricas.py`
mudou depois de rodar, junto com o §5 do `analise.md`: em 3 e 4 out. 2026 saíram dele os índices de
sobreposição e de concordância de severidade que o estudo deixou de usar, e entraram a contagem de
defeitos em comum por par de formatos e, na concordância de severidade, a proporção de notas a até um
nível de distância e a direção da discordância. `metricas.json` e `metricas.md` foram regerados com a
versão publicada, sem mudança em nenhum outro valor. Refeitos sobre os arquivos deste repositório, os
scripts reproduzem byte a byte `prompt_unificacao.md` e `trilha_decisoes.csv`, e `metricas.json` com os
mesmos números.

Alguns textos citam arquivos internos do desenvolvimento que não foram publicados: `roteiro_estudo.md`,
`embasamento_formatos.md`, o `README.md` do instrumento e o artefato "Roteiro do estudo", que a skill de
unificação manda marcar ao final. Nada disso é necessário para executar a coleta ou a análise.

## Mapa: Metodologia do TCC → repositório

| Seção da Metodologia | Onde está |
|---|---|
| Visão geral do método | este README; `instrumento/`, `coleta-2026-09-24/`, `analise-2026-09-24/` |
| Caracterização da pesquisa | classificação metodológica, sem arquivo correspondente |
| Objeto de avaliação | `objeto/tarefas_crm.html`; `coleta-2026-09-24/resultados/caracterizacao_79f2e33c.json` e `coleta-2026-09-24/caracterizacao_79f2e33c/`; skill `caracterizar` e subagente `caracterizador-objeto` |
| Manipulação do objeto | `instrumento/.mcp.json`; `instrumento/.claude/avaliador_modelo.template` e `gerar_avaliadores.mjs`; campos de versão e área visível dos cabeçalhos |
| Estrutura do prompt heurístico | `instrumento/protocolo/nucleo_heuristico.md`; §3 de `formato-a`, `formato-b` e `formato-c` (texto literal de cada chamada); `instrumento/contexto/contexto.md` |
| Execução das avaliações heurísticas | passos 0, 4 e 5 das skills de formato; `instrumento/.claude/settings.json`; cabeçalhos e encerramentos em `coleta-2026-09-24/resultados/`; registros visuais em `coleta-2026-09-24/exec-*/` |
| Revisão dos achados | `instrumento/protocolo/analise.md` §2 a §4; `instrumento/protocolo/unificacao.md`; `.claude/skills/unificar/` e `.claude/agents/unificador.md`; `reunir_cegar.py`, `unificar_prompt.py`, `revisar.py`, `validar_revisao.py`, `reatar_trilha.py`; em `analise-2026-09-24/`, `semente.txt`, `prompt_unificacao.md`, `unificacao_ia.json`, `unificacao_proveniencia.json`, `decisoes.json`, `trilha_decisoes.csv` |
| Análise | `instrumento/protocolo/analise.md` §5; `metricas.py`; `analise-2026-09-24/metricas.json` e `metricas.md`, com `encerramentos.json` e `fora_do_escopo.json` |
| Limitações do método | `instrumento/protocolo/analise.md` §6 |

## Como reproduzir uma execução

Versões registradas nos nove cabeçalhos:

| Componente | Versão |
|---|---|
| Aplicativo de desktop do Claude (aba Code) | 2.2553.1 |
| Modelo | Claude Opus 5 (`claude-opus-5`), nível de raciocínio alto |
| Chrome DevTools MCP | 1.8.0 (fixado no `.mcp.json`) |
| Google Chrome | 152.0.7977.83, sem janela |
| Área visível | 1440 × 900 pixels CSS, escala 1 |

Requisitos: o aplicativo de desktop do Claude, Node.js com `npx`, Google Chrome e Git. O aplicativo e o
Chrome se atualizam sozinhos, e as versões exatas podem não estar mais disponíveis; as skills medem e
gravam no cabeçalho as versões em uso, de modo que uma diferença fica registrada.

1. Clone o repositório e confira a integridade:

   ```bash
   sha256sum -c MANIFESTO.sha256
   ```

2. Gere as dez definições de avaliador e faça commit delas. O passo 0 das skills exige árvore limpa no
   git, e arquivos novos sem commit a sujam.

   ```bash
   cd instrumento
   node .claude/gerar_avaliadores.mjs
   git add .claude/agents
   git commit -m "Avaliadores gerados do modelo"
   ```

3. Abra a pasta `instrumento/` no aplicativo de desktop do Claude, aba Code, aprove os dez servidores MCP
   do `.mcp.json` e ajuste o nível de raciocínio da sessão para alto.
4. Opcional, em conversa própria: `/caracterizar <caminho absoluto de objeto/tarefas_crm.html>`. A skill
   compara o caminho com a "Referência do objeto" do material de contexto, que é o da máquina da coleta,
   e vai perguntar qual vale.
5. Para cada rodada `n` de 1 a 3, cada execução em conversa nova e nesta ordem:
   `/formato-a n <caminho do objeto>`, `/formato-b n <caminho do objeto>`, `/formato-c n <caminho do objeto>`.
   Cada skill pede confirmações no passo 0 (material de contexto, nível de raciocínio, versão do
   aplicativo) e mostra o cabeçalho antes de delegar.
6. As saídas ficam em `instrumento/resultados/exec-n/resultados_<F>.jsonl` e
   `instrumento/evidencias/exec-n/<F>/`, ambas fora do git. Os campos `objeto_hash_sha256` e
   `contexto_hash_sha256` do cabeçalho têm de bater com os valores acima. Na coleta publicada, essas duas
   pastas foram copiadas para `coleta-2026-09-24/resultados/` e `coleta-2026-09-24/exec-n/`.

## Como recalcular as métricas

Os comandos são de shell bash (no Windows, o Git Bash) e rodam da raiz do repositório. Use `py` no
Windows e `python3` nos demais sistemas. Tudo é gravado em `refazer/`, que o git ignora; nada do que está
publicado é sobrescrito.

**A partir da trilha de decisões**, em um comando:

```bash
py instrumento/analise/metricas.py --pasta refazer/metricas --trilha analise-2026-09-24/trilha_decisoes.csv --encerramentos analise-2026-09-24/encerramentos.json --fora-do-escopo analise-2026-09-24/fora_do_escopo.json
```

**A partir da coleta**, refazendo a cadeia inteira com a semente e as decisões publicadas:

```bash
py instrumento/analise/reunir_cegar.py --coleta coleta-2026-09-24 --semente 20260924 --saida refazer/analise --sem-evidencias
py instrumento/analise/unificar_prompt.py montar --pasta refazer/analise
cp analise-2026-09-24/unificacao_ia.json analise-2026-09-24/decisoes.json refazer/analise/
py instrumento/analise/validar_revisao.py --pasta refazer/analise
py instrumento/analise/reatar_trilha.py --pasta refazer/analise
py instrumento/analise/metricas.py --pasta refazer/analise
```

O `prompt_unificacao.md` e a `trilha_decisoes.csv` gerados são idênticos aos publicados, byte a byte. O
`metricas.json` traz os mesmos números; mudam só os caminhos do campo `fontes` e, no `metricas.md`, a
ordem em que um dicionário de contagens é impresso.

**Para abrir a página de revisão com as capturas**, o conjunto cego precisa das capturas, que nesta
coleta ficam fora de `evidencias/`. Monte uma lista de fontes e passe-a com `--manifesto` (caminhos
relativos à pasta `instrumento/`):

```bash
mkdir -p refazer
py -c "import json; json.dump({'fontes': [{'jsonl': f'../coleta-2026-09-24/resultados/exec-{e}/resultados_{F}.jsonl', 'evidencias': f'../coleta-2026-09-24/exec-{e}/{F}', 'execucao': e} for e in (1, 2, 3) for F in 'ABC']}, open('refazer/fontes.json', 'w'), indent=1)"
py instrumento/analise/reunir_cegar.py --manifesto refazer/fontes.json --semente 20260924 --saida refazer/pagina
cp analise-2026-09-24/unificacao_ia.json analise-2026-09-24/decisoes.json refazer/pagina/
py instrumento/analise/revisar.py --pasta refazer/pagina
```

A página abre em `http://127.0.0.1:8765/` com as decisões do estudo já marcadas. A ordem das fontes é
a da semente: execução 1 (A, B, C), execução 2, execução 3.

## Dicionário de dados

### Linhas dos JSONL da coleta

`coleta-2026-09-24/resultados/exec-<n>/resultados_<F>.jsonl`: a primeira linha é o cabeçalho, as do meio
são os achados e a última é o encerramento. Horários em ISO-8601, com o fuso escrito em cada valor.

**Cabeçalho** (`"registro": "cabecalho"`)

| Campo | Conteúdo |
|---|---|
| `formato`, `execucao` | formato (A, B ou C) e rodada (1 a 3) |
| `objeto_arquivo`, `objeto_hash_sha256` | caminho do objeto na máquina da coleta e SHA-256 dele |
| `contexto_arquivo`, `contexto_hash_sha256` | caminho e SHA-256 do material de contexto |
| `estado_inicial` | como o objeto foi preparado antes da delegação |
| `modo_execucao`, `paralelismo` | `paralela` ou `chamada_unica`, e quantos subagentes correram juntos |
| `navegador` | `headless` |
| `viewport_alvo`, `viewport_medido_css`, `device_pixel_ratio` | área visível pedida, área medida na página e escala |
| `viewport_divergente`, `viewport_identico_entre_navegadores` | se a medida divergiu do alvo e se foi a mesma em todos os navegadores |
| `modelo`, `nivel_raciocinio` | modelo e nível de raciocínio da sessão |
| `versao_mcp_chrome_devtools`, `versao_chrome`, `versao_app_desktop` | versões do servidor MCP, do Chrome (medida na página) e do aplicativo |
| `commit_instrumento`, `branch`, `arvore_limpa` | commit do instrumento, branch e confirmação de que não havia alteração pendente |
| `datahora_inicio` | início da execução |

**Achado**

| Campo | Conteúdo |
|---|---|
| `registro` | `"achado"`; presente só nas execuções 1 e 3 do Formato A (ver "Versões") |
| `formato` | A, B ou C |
| `id` | `A-H<k>-NNN`, `B-G<n>-NNN` ou `C-H<k>-NNN`; `NNN` conta dentro da chamada em A e B e dentro da heurística em C; não traz a execução, que está no cabeçalho |
| `heuristica` | `H<k> — <nome>`, a heurística que o achado viola |
| `fora_do_escopo` | `true` se a heurística não pertence à chamada; nenhum achado da coleta saiu assim |
| `localizacao` | tela e elemento |
| `registro_visual` | nomes dos arquivos de captura e de instantâneo do achado e a descrição do que eles mostram |
| `descricao_falha` | o que está errado na interface |
| `justificativa_violacao` | por que isso viola a heurística |
| `severidade`, `severidade_rotulo` | nota de 0 a 4 do avaliador e rótulo: 0 não é um problema, 1 cosmético, 2 menor, 3 maior, 4 catastrófico |
| `justificativa_severidade` | o que sustenta a nota |
| `sugestao_correcao` | correção proposta |
| `arquivos_evidencia` | lista dos arquivos do achado; presente só nos Formatos B e C da execução 3, onde o orquestrador a acrescentou |

**Encerramento** (`"registro": "encerramento"`)

| Campo | Conteúdo |
|---|---|
| `datahora_disparo`, `datahora_ultimo_retorno`, `datahora_fim` | disparo dos subagentes, retorno do último e gravação do encerramento |
| `duracao_total_s` | do disparo ao encerramento |
| `duracao_avaliacao_s` | do disparo ao último retorno |
| `duracao_execucao_s` | do início do passo 0 ao encerramento |
| `chamadas` | uma entrada por chamada: `chamada`, `duracao_ms`, `tokens`, `usos_ferramenta`, `erros_ferramenta`, `timeouts`, `achados` |
| `tokens_total`, `usos_ferramenta_total`, `erros_ferramenta_total`, `timeouts_total`, `achados_total` | somas das chamadas |
| `arquivos_evidencia` | número de arquivos de evidência gravados |
| `duracao_ms_soma`, `duracao_ms_max`, `concorrencia_observada` | soma e máximo das durações das chamadas e o paralelismo constatado a partir delas |

### Registros visuais

`coleta-2026-09-24/exec-<n>/<F>/H<kk>/` guarda os arquivos de cada achado, na pasta da heurística que ele
nomeia (inclusive em B e C):

- `<id>.png`, ou `<id>.1.png`, `<id>.2.png`… quando há mais de um quadro: captura de tela;
- `<id>.elemento.png`: recorte de um controle, que acompanha a captura da área visível;
- `<id>.snapshot.txt`: instantâneo da árvore de acessibilidade no estado capturado;
- `<id>.achado.md`: o achado em texto legível.

`coleta-2026-09-24/exec-<n>/<F>/_indice.md` resume a execução daquele formato. Quatro arquivos saíram com
uma letra depois do número (por exemplo `A-H5-003b.1.png`); eles pertencem ao achado sem a letra, que os
cita no `registro_visual`.

### Trilha de decisões

`analise-2026-09-24/trilha_decisoes.csv`: uma linha por achado (476), separador `;`, campos de texto entre
aspas duplas.

| Coluna | Conteúdo | Quem decide |
|---|---|---|
| `chave` | chave substituta usada na revisão (`K###`) | sorteio com a semente |
| `id`, `formato`, `execucao` | identificação do achado | coleta |
| `chamada` | derivada do `id`: `H<k>` em A, `G<n>` em B, `unica` em C | coleta |
| `heuristica` | heurística do achado | subagente avaliador |
| `severidade_ia` | o campo `severidade` do JSONL | subagente avaliador |
| `achado_unificado` | identificador do achado unificado (`U###`) | IA, na unificação |
| `classificacao` | `defeito` ou `falso_positivo`, igual para todos os achados do achado unificado | pesquisador |
| `severidade_pesquisador` | 1 a 4 por defeito; vazio em falso positivo | pesquisador |
| `elemento` | elemento da interface que sustenta o achado unificado | IA, na unificação |
| `pontos_manifestacao` | onde o problema aparece (tela ou estado), separados por `\|` | IA, na unificação |
| `observacao` | nota livre, opcional | pesquisador |

As colunas `chave` e `id` lado a lado são o mapa de chaves do estudo.

### Demais arquivos da análise

| Arquivo | Conteúdo |
|---|---|
| `semente.txt` | semente, algoritmo e ordem de entrada do embaralhamento |
| `unificacao_ia.json` | `achados_unificados`: para cada um, `unificado`, as chaves dos `achados` reunidos, `enunciado`, `elemento`, `pontos_manifestacao`, `justificativa` da fusão e `leituras` (por heurística: `heuristica`, `nome_heuristica`, `achados`, `localizacao`, `descricao_falha`, `justificativa_violacao`, `registro_visual`, `sugestao_correcao`) |
| `decisoes.json` | decisão do pesquisador por achado unificado: `classificacao`, `severidade`, `observacao` e o instante da decisão (`quando`) |
| `encerramentos.json` | as nove linhas de encerramento, reunidas para o cálculo de custo |
| `fora_do_escopo.json` | achados com heurística fora da chamada, por formato; vazio nesta coleta |
| `metricas.json`, `metricas.md` | métricas por formato e por execução; as fórmulas estão em `analise.md` §5 |

## Licença

Textos e dados sob CC BY 4.0; código sob MIT; a seção 3 do núcleo heurístico e as bibliotecas embutidas no
objeto seguem as licenças de seus autores. Detalhes em `LICENSE.md`.

## Como citar

Damião, E.T. 2026. Avaliação heurística com LLM e granularidade do prompt: instrumento, coleta e análise.
Disponível em: <https://github.com/brozploomes/avaliacao-heuristica-llm-granularidade>. Acesso em: [dd mmm. 2026].
