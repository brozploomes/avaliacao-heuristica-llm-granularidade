---
name: caracterizar
description: Caracteriza o objeto de avaliação — mede os elementos visíveis do estado de entrada e identifica, por exploração sistemática guiada pelo material de contexto (contexto/contexto.md), quantas telas e modais ele possui. Independente das três condições, grava em resultados/caracterizacao_<hash8>.json.
disable-model-invocation: true
model: claude-opus-5
---

# Orquestrador — Caracterização do objeto

Argumento opcional: `$ARGUMENTS`. Se vier preenchido, é o **caminho do arquivo `.html`** do objeto;
se vier vazio, pergunte.

Você é o **ORQUESTRADOR**. Você não avalia e não explora: você abre o objeto, dispara o subagente
`caracterizador-objeto`, confere o que ele devolveu e grava o arquivo de caracterização.

## O que se mede, e por quê

Duas grandezas, e só elas:

1. **Elementos visíveis do DOM** no estado de entrada. É a medida principal de densidade da interface,
   e é o análogo, em aplicação web, da contagem de componentes visíveis usada na literatura para
   estratificar complexidade de interface. O DOM é o análogo correto porque, como a hierarquia de views
   do Android, é a **árvore estrutural** que expõe todos os elementos que compõem a tela e as relações
   entre eles — ao contrário da árvore de acessibilidade, que é dela derivada e podada.
2. **Quantidade de telas e de modais**, obtida por exploração. É a forma de caracterização empregada
   pelos estudos de referência, que contam telas ou capturas submetidas.

**Não se contam estados.** A contagem de estados distintos foi considerada e descartada: exigiria uma
regra de equivalência própria, sem precedente na literatura, cujo resultado varia conforme decisões
finas de normalização — e o ganho não compensa a superfície de questionamento que abre.

Com **objeto único**, estas medidas são **constantes** entre as três condições e não explicam a
variação entre formatos. A função delas é descritiva, de controle da identidade do objeto e de base de
comparação para estudo futuro com outro objeto. Não prometa correlação que um objeto só não sustenta.

## Por que esta skill é independente das três condições

Ela **não é chamada** por `/formato-a`, `/formato-b` nem `/formato-c`, e o resultado dela **não entra
em nenhuma delegação**. Pode rodar antes ou depois delas, em sessão própria.

O vínculo com os resultados é o **SHA-256 do objeto**, gravado tanto aqui quanto no cabeçalho de cada
condição: é por ele que a análise junta caracterização e resultados. A independência é deliberada —
qualquer caminho pelo qual o inventário de telas e modais chegasse a um avaliador operaria como mapa
da interface e contaminaria a exploração, sobretudo nos Formatos A e B.

A independência é de **mão única**. O que não pode circular é o inventário de telas e modais em direção
a um avaliador. O caminho inverso — o **material de contexto** chegar ao caracterizador — não contamina
nada: `contexto/contexto.md` é o mesmo texto padronizado que as três condições entregam, descreve o que
a funcionalidade é e o que percorrer, e não aponta problema nem direciona heurística. Sem ele a
exploração é cega e a cobertura sai incompleta, porque há parte da aplicação que só se alcança por um
percurso com dado plausível — um formulário preenchido com valor que o domínio aceita, um fluxo de
criação levado até o fim — e uma varredura de controle sozinha não chega lá. Com ele, o que se conta é
o objeto **no mesmo recorte que os avaliadores viram**, e a contagem passa a ser base de comparação
para a cobertura declarada nas três condições.

O objeto do estudo é um `.html` autocontido e offline, com dados em memória: a exploração altera o estado da página, mas **recarregar
restaura**, e tanto esta skill quanto as três condições recarregam o objeto antes de começar. Por isso
a ordem entre a caracterização e as condições é indiferente.

## 0. Verificação de estado inicial

1. **Objeto.** Obtenha o caminho do `.html`. Abra-o com o `new_page` do servidor `cdp-01`, o único que o
   caracterizador enxerga, no `file://` correspondente, e **recarregue** com `navigate_page` (`type: reload`). Se houver mais de uma aba com o mesmo título,
   feche as demais: o subagente fixa a aba pelo título e não pode escolher errado.
2. **Contexto.** Leia `contexto/contexto.md`, o mesmo material padronizado que as três condições
   entregam. É ele que impede a cobertura de sair incompleta: a lista de tarefas da seção C leva a
   fluxos que a varredura de controle não alcança sozinha. Se o arquivo não existir, **pare** e peça-o
   ao pesquisador — caracterizar sobre material diferente do que as condições usaram torna os dois
   incomparáveis. Confira também que a **Referência do objeto** declarada nos metadados do contexto é o
   `.html` do item 1; se divergir, pare, registre em `ocorrencias` e pergunte ao pesquisador qual vale.
3. **Proveniência.** Derive sozinho: versão do `chrome-devtools-mcp` (do `.mcp.json`); versão do Chrome
   **medida na própria página**, como nas skills de formato, com `evaluate_script` e
   `() => navigator.userAgentData.getHighEntropyValues(['fullVersionList']).then(v => v.fullVersionList)`,
   gravando a marca `Google Chrome` (em headless o `userAgent` entrega a versão reduzida); hash do commit
   (`git rev-parse --short HEAD`) e **nome da branch** (`git rev-parse --abbrev-ref HEAD`); **SHA-256 do
   `.html` e do `contexto/contexto.md`**; data/hora agora.
   Pergunte ao pesquisador o nível de raciocínio da sessão e a versão do ambiente, como nas outras
   skills. O nível de raciocínio é **por sessão**, no menu de esforço (Ctrl+Shift+E no Windows). A
   versão é **uma só**: a partir da série 2.x do aplicativo de desktop, o Claude Code e o aplicativo
   compartilham o mesmo número (Ajuda → Sobre, ou Configurações → Geral). Confira na execução, nunca
   copie de um cabeçalho anterior, e registre em `ocorrencias` se ele mudar durante a caracterização.
4. **Viewport.** Meça com `evaluate_script`: `() => ({w: innerWidth, h: innerHeight, dpr: devicePixelRatio})`.
   Registre. A contagem de elementos visíveis usa o predicado **"renderizado"**, não "dentro da área
   visível", justamente para não depender da tela da máquina — mas o viewport vai ao arquivo como
   proveniência.
5. **Confirmação única.** Mostre o que vai rodar — objeto, os dois hashes e o viewport — e espere o "ok".

## 1. Dispare o caracterizador

Dispare **um** subagente `caracterizador-objeto` (contexto isolado; **não** use fork). Na delegação,
inclua **somente**:

- a referência do objeto, já aberto e recarregado no navegador;
- o **caminho absoluto de `evidencias/_incoming/`** como pasta de trabalho;
- a geometria do viewport medida no passo 0;
- o **conteúdo integral de `contexto/contexto.md`**, colado literalmente sob o rótulo
  `Material de contexto:`, como nas três condições, com a instrução de **percorrer a lista de tarefas
  da seção C** além do ciclo por controle, e a de reportar, tarefa a tarefa, o que percorreu e o que
  não percorreu.

Cole o contexto **íntegro e sem comentário**: não resuma, não recorte a lista de tarefas e não
acrescente observação sua sobre a interface. Apontar onde há uma tela ou um modal entrega a resposta
que ele tem de alcançar sozinho, e a contagem deixa de valer.

**Não** inclua heurística alguma nem nada sobre a condição de qualquer execução. O cabeçalho do
material de contexto diz que ele é o mesmo nas três condições, e isso pode ir: não identifica nenhuma
delas nem descreve como elas operam. O caracterizador não avalia e não precisa saber mais que isso.

## 2. Confira o que voltou

O subagente gravou o `exploracao.json` e os snapshots em `evidencias/_incoming/`, e respondeu uma
linha. Confira **por script** (`node`):

1. o `exploracao.json` existe e parseia;
2. os totais de telas e modais batem com o que ele declarou na resposta;
3. cada tela e cada modal em página tem o snapshot que cita; modal nativo tem transcrição, não
   snapshot;
4. as `medidas_entrada` estão completas, e `elementos_visiveis` ≤ `elementos_no_dom`;
5. a `cobertura_contexto` cita **todas** as tarefas da seção C do material de contexto, cada uma como
   percorrida ou como não percorrida com motivo — nenhuma pode ficar de fora das duas listas, e a soma
   delas tem de dar o número de itens da seção C.

Se algo faltar, repeça ao mesmo subagente por `SendMessage` — não improvise e não preencha por conta.

## 3. Grave a caracterização

Grave `resultados/caracterizacao_<primeiros 8 do SHA-256 do objeto>.json`. O hash no nome deixa o
vínculo visível no próprio arquivo e impede colisão entre objetos diferentes.

```json
{"registro":"caracterizacao","objeto_arquivo":"<caminho>","objeto_hash_sha256":"<hash>","contexto_arquivo":"contexto/contexto.md","contexto_hash_sha256":"<hash>","datahora":"<ISO-8601>","modelo":"claude-opus-5","nivel_raciocinio":"<confirmado no passo 0.3>","commit_instrumento":"<hash>","branch":"<branch>","versao_mcp_chrome_devtools":"<versão>","versao_chrome":"<versão>","versao_app_desktop":"<versão>","viewport_alvo":"1440x900","viewport_medido_css":"<L>x<A>","device_pixel_ratio":<n>,"medidas_entrada":{...},"totais":{"telas":<n>,"modais":<n>},"pasta_snapshots":"evidencias/caracterizacao_<hash8>/","snapshot_entrada":"entrada.txt","telas":[{"id":1,"nome":"<…>","alcancada_por":"<…>","snapshot":"tela_1.txt"}],"modais":[{"id":1,"tipo":"nativo|em_pagina","origem":"<…>","transcricao":"<…>","snapshot":"modal_1.txt"}],"cobertura_contexto":{"tarefas_percorridas":[<ids>],"tarefas_nao_percorridas":[{"id":<n>,"motivo":"<…>"}]},"protocolo_seguido":"<…>","ocorrencias":[]}
```

Grave pelo shell, com caminho absoluto e um comando por invocação — monte o JSON num arquivo da pasta
temporária da sessão e anexe com um único `cat`. Não encadeie comandos com `&&`.

**No `objeto_arquivo`, escreva o caminho com barras normais**
(`C:/Users/EduardoDamiao/Documents/MBA USPEsalq/objeto/tarefas_crm.html`): a barra invertida do
Windows é comida na montagem do JSON pelo shell e o campo sai truncado — quando não quebra o
parse do arquivo inteiro. Depois de gravar, leia o arquivo de volta e confirme que ele parseia e
que o caminho está íntegro.

## 4. Feche

1. **Mova os snapshots (`entrada.txt`, `tela_<id>.txt`, `modal_<id>.txt`) e o `exploracao.json`** de
   `evidencias/_incoming/` para `evidencias/caracterizacao_<primeiros 8 do SHA-256>/`. São o rastro de como o
   caracterizador chegou às contagens, e ficam para conferência posterior.
2. **`evidencias/_incoming/` tem de terminar vazia: nenhuma subpasta e nenhum arquivo além do `.gitkeep`**, que mantém a pasta no repositório. Confira.
3. **Confira o objeto**: recarregue e confirme que voltou ao estado inicial.
4. **Resumo no chat**: elementos visíveis e a decomposição; total de telas e modais, com o que cada um
   é; o protocolo efetivamente percorrido, **quais tarefas do material de contexto foram percorridas e
   quais não, com o motivo de cada uma**, e o que mais ficou fora; o caminho do arquivo gravado.

## O que a saída afirma, e o que não afirma

**Afirma:** o objeto tem esta densidade de interface no estado de entrada, e estas telas e modais foram
**alcançados** sob o protocolo declarado, que é reexecutável e inclui a lista de tarefas do material de
contexto — o mesmo recorte que as três condições entregaram aos avaliadores.

**Não afirma** que sejam todas as telas e todos os modais existentes — exaustividade não é verificável
num objeto de estado dinâmico. É a mesma classe de limitação dos estudos de referência, em que a
cobertura do objeto também é deliberada e declarada. O que o material de contexto acrescenta é um
**piso declarado de cobertura**, não exaustividade: ele garante que o recorte avaliado foi percorrido,
e a `cobertura_contexto` diz, tarefa a tarefa, se foi.

**Não afirma** nada sobre estados da interface: eles não são contados, por decisão declarada.

**Sobre a medida de densidade:** ela depende da semântica da marcação, e por isso **não é comparável
entre estudos nem entre objetos construídos com convenções diferentes** — só o construto é. Dentro
deste estudo, em que o objeto é um só, isso não é confundidor: a marcação é a mesma nas três condições.
