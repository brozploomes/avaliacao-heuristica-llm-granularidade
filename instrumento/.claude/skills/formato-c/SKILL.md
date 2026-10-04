---
name: formato-c
description: Orquestra a condição C da coleta — as dez heurísticas em uma única chamada, um subagente avaliador em navegador headless — e grava os achados em resultados/exec-<n>/resultados_C.jsonl.
disable-model-invocation: true
model: claude-opus-5
---

# Orquestrador — Formato C (todas as heurísticas de uma vez)

Argumentos: `$ARGUMENTS` = `<n> [caminho-do-.html]`. O primeiro, **obrigatório**, é o número da
execução (1, 2 ou 3): define as pastas `resultados/exec-<n>/` e `evidencias/exec-<n>/` em que esta
condição grava, e vai no cabeçalho como `execucao`. Se vier vazio ou não for um inteiro, **pare e peça**.
O segundo, opcional, é o caminho do `.html` do objeto; se não vier, pergunte na verificação de estado
inicial. O material de contexto é sempre `contexto/contexto.md`, o mesmo nas nove execuções.

Você é o **ORQUESTRADOR**. Você **não avalia**. Você abre o objeto, dispara **um único** subagente
avaliador, coleta o retorno e grava o arquivo. Siga exatamente:

## 0. Verificação de estado inicial (antes de qualquer delegação)

1. **Objeto.** Obtenha o caminho do `.html` (do argumento ou perguntando). Este formato tem chamada
   única e usa **um** servidor MCP, `cdp-01`. Abra o objeto com `new_page` no `file://` correspondente
   e **recarregue** com `navigate_page` (`type: reload`). Reporte no chat o que abriu e que recarregou.

   O servidor sobe a própria instância do Chrome, **headless**, com perfil temporário (`--isolated`),
   então esta condição **não** herda a aplicação já modificada pelos Formatos A e B.
2. **Contexto.** Se `contexto/contexto.md` não existir, peça o material de contexto no chat e grave-o
   nesse caminho antes de prosseguir, para que as três condições usem exatamente o mesmo texto.
   Se você o gravou agora, **commite-o** antes do item 7 (`git add contexto/contexto.md` e
   `git commit -m "Material de contexto do objeto"`): um arquivo não rastreado deixa a árvore suja.

   **Se existir, não presuma que é o do objeto desta coleta.** O caminho é fixo e o arquivo é
   reaproveitado entre execuções — pode ter sobrado de um ensaio anterior, e nesse caso os avaliadores
   receberiam a descrição de uma tela **diferente** da que estão vendo, sem que nada no artefato
   denunciasse: o hash gravado seria o do contexto errado, e bateria com ele mesmo. Mostre no chat o
   **título do contexto** e o **caminho do objeto**, e **pergunte se correspondem**. Só siga com o
   "sim"; se não corresponderem, peça o material novo e grave-o antes de prosseguir.
3. **Proveniência.** Derive sozinho: versão do `chrome-devtools-mcp` (do `.mcp.json`), versão do Chrome — **medida na
   própria página**, não deduzida do executável nem do `navigator.userAgent`: rode `evaluate_script`
   com `() => navigator.userAgentData.getHighEntropyValues(['fullVersionList']).then(v => v.fullVersionList)`
   e grave a versão da marca `Google Chrome`. Em **headless** o `navigator.userAgent` entrega a versão
   reduzida (`152.0.0.0` em vez de `152.0.7977.83`) e faria o cabeçalho parecer outro binário —
   aconteceu no ensaio do Formato C. Hash do commit (`git rev-parse --short HEAD`), **nome da branch**
   (`git rev-parse --abbrev-ref HEAD`), SHA-256 do `.html` e do `contexto/contexto.md`
   (`sha256sum <arquivo>`), data/hora agora.
   Pergunte ao pesquisador **o nível de raciocínio da sessão e a versão do ambiente**, que não são
   deriváveis de dentro da sessão, dizendo onde achar cada um. O nível de raciocínio é o valor que vai
   em `nivel_raciocinio` no cabeçalho, tal como confirmado, sem presumir "alto": ele é **por sessão**,
   no menu de esforço (Ctrl+Shift+E no Windows), e não um ajuste fixo em Configurações. A versão é
   **uma só**: a partir da série 2.x do aplicativo de desktop, o Claude Code e o aplicativo compartilham
   o mesmo número, e não há um segundo a registrar — leia em Ajuda → Sobre, ou em Configurações → Geral
   → "Versão do aplicativo para desktop", e grave em `versao_app_desktop`. O aplicativo tem atualizador
   próprio e se atualiza sozinho quando a máquina fica ociosa: **confira o número a cada execução** e
   nunca o copie do cabeçalho anterior; se ele mudar no meio de uma rodada, os cabeçalhos vão divergir e
   a divergência é o registro.
4. **Viewport.** O `.mcp.json` declara um viewport **alvo**, e `resize_page` **retorna sucesso mesmo
   sem aplicar** a dimensão pedida — então meça, não declare. Rode `evaluate_script` na página do
   objeto: `() => ({w: innerWidth, h: innerHeight, dpr: devicePixelRatio})`.

   Em headless o viewport não fica preso ao tamanho da tela, então o esperado é **1440×900 com DPR 1**.
   Registre **alvo e medido** no cabeçalho. Se divergirem, **diga isso no chat** antes de pedir a
   confirmação: a divergência não impede a coleta, desde que fique registrada e seja a mesma nas três
   condições.
5. **Guardas de pasta (P1 e P2).** Esta execução grava em `resultados/exec-<n>/` e em `evidencias/exec-<n>/`, e rodar
   na árvore errada contaminaria dados de outra execução. Antes da confirmação, reporte no chat:

   - **P1** — a listagem de `resultados/exec-<n>/` registrada abaixo, que é a linha de base da conferência de
     escritor único. Ela **pode** conter os arquivos dos outros formatos já rodados nesta execução: isso é
     esperado, porque a pasta da execução acumula por desenho — é justamente por isso que a conferência
     compara contra uma linha de base, e não contra uma lista fixa. **O que reprova é encontrar ali o
     arquivo desta condição** (`resultados_C.jsonl`): significaria que você está prestes a anexar a um
     artefato já existente, seja por repetir o formato dentro da mesma execução, seja por estar na árvore
     ou na pasta errada. Nesse caso **pare e avise**, sem gravar nada. Repetir o formato em **outra**
     execução é o desenho do estudo, e usa outra pasta;
   - **P2** — a branch derivada em (3), que vai no cabeçalho e faz o artefato se identificar sozinho.
6. **Definições de avaliador íntegras.** Rode `node .claude/gerar_avaliadores.mjs --verificar` **antes**
   de delegar: se as definições divergirem do modelo, a condição rodaria com avaliadores desiguais.
   A conferência se repete no fechamento.
7. **Árvore limpa.** Rode `git status --porcelain`. Saída vazia grava `arvore_limpa: true` no cabeçalho.
   Saída não vazia significa arquivo do instrumento alterado sem commit, e então o hash do commit não
   identifica o que vai rodar: **pare e avise**. As saídas da coleta estão no `.gitignore` e não
   aparecem aqui.
8. **Confirmação única.** Mostre o cabeçalho montado e espere o "ok" antes de delegar.
7. **Custo completo.** A chamada do encerramento não pode ter `tokens`, `duracao_ms` ou `usos_ferramenta`
   nulos. Se houver, o encerramento não é gravado até o número ser recuperado do bloco de uso.
8. **Escopo das heurísticas.** Reporte quantos achados saíram com `fora_do_escopo: true` (neste formato,
   só um campo `heuristica` fora de H1 a H10). Eles ficam no JSONL; a análise os exclui de `|A(F,e)|`.

**Crie `resultados/exec-<n>/` e `evidencias/exec-<n>/` se não existirem, e registre a listagem de `resultados/exec-<n>/` como ela está agora**, antes de gravar qualquer coisa. Ela é a
linha de base da conferência de escritor único do passo 5: no fechamento, o que aparecer ali e não
tiver sido gravado por você é inesperado.

Grave então a **primeira linha** de `resultados/exec-<n>/resultados_C.jsonl`:

```json
{"registro":"cabecalho","formato":"C","execucao":<n>,"objeto_arquivo":"<caminho>","objeto_hash_sha256":"<hash>","estado_inicial":"aberto e recarregado pelo orquestrador","modo_execucao":"chamada_unica","paralelismo":1,"navegador":"headless","viewport_alvo":"1440x900","viewport_medido_css":"<L>x<A>","device_pixel_ratio":<n>,"viewport_divergente":<true|false>,"viewport_identico_entre_navegadores":true,"modelo":"claude-opus-5","nivel_raciocinio":"<confirmado no passo 0.3>","versao_mcp_chrome_devtools":"<versão>","versao_chrome":"<versão>","versao_app_desktop":"<versão>","commit_instrumento":"<hash>","branch":"<branch>","arvore_limpa":<true|false>,"datahora_inicio":"<ISO-8601>","contexto_arquivo":"contexto/contexto.md","contexto_hash_sha256":"<hash>"}
```

**Grave sempre pelo shell, com caminho absoluto e um comando por invocação** — por exemplo
`printf '%s\n' '<json>' >> "<caminho absoluto>/resultados/exec-<n>/resultados_C.jsonl"`. Não encadeie comandos com
`&&`: comando composto exige que cada parte esteja pré-aprovada e a execução para pedindo permissão.

**No `objeto_arquivo`, escreva o caminho com barras normais**
(`C:/Users/EduardoDamiao/Documents/MBA USPEsalq/objeto/tarefas_crm.html`): a barra invertida do
Windows é comida na montagem do JSON pelo shell e o campo sai truncado — quando não quebra o
parse da linha inteira, porque `\U` de `\Users` e `\D` de `\Documents` não são escapes
válidos em JSON. Depois de gravar, leia a linha de volta e confirme que ela parseia e que o caminho
está íntegro.

**Não delegue nada** antes das confirmações e do cabeçalho gravado.

## 1. Leia o núcleo

Leia `protocolo/nucleo_heuristico.md`. Separe dele as **seções compartilhadas** (papel, severidade 0–4,
regras gerais) e os **10 blocos de heurística** (H1…H10).

## 2. Leia o contexto

Leia `contexto/contexto.md`.

## 3. Dispare o subagente único

**Antes de criar a pasta, confira que `evidencias/_incoming/` está vazia** — nenhum arquivo além do
`.gitkeep` e nenhuma subpasta. Se sobrar um `achados.json` de execução anterior e o avaliador desta
chamada falhar em gravar o dele, você leria o arquivo antigo e carimbaria os achados dele com os
identificadores desta. A conferência de contagem só pega isso quando as duas contagens diferem.

**Prepare a pasta neutra.** Sorteie um **token aleatório e opaco** (8 caracteres hexadecimais, por
exemplo) e crie `evidencias/_incoming/<token>/`.

O token não carrega informação — não diz a condição, não diz nada sobre a chamada —, e faz a ameaça de
"ler o `achados.json` de outra execução" sumir por construção: a pasta nasce vazia e é descartada ao
fim do ciclo. Nos Formatos A e B ele também evita colisão entre avaliadores simultâneos; aqui, com
chamada única, o benefício é só o segundo, mas a regra é a mesma nos três.

O objeto deve estar no estado inicial na hora de delegar; com chamada única, o passo 0 já garante isso.

**Registre `datahora_disparo`** (ISO-8601) imediatamente antes de disparar e **`datahora_ultimo_retorno`**
no instante em que ele voltar, como nos Formatos A e B.

Dispare **um** subagente `avaliador-heuristico-01`, no servidor `cdp-01` (contexto isolado; **não** use
fork), com a delegação montada a partir do texto abaixo, **literalmente**, preenchendo só o que está
entre chaves. Nada mais entra e nada sai: o texto é o mesmo nas nove execuções e nos três formatos no
que é comum, e o que varia entre chamadas é só o bloco de heurística e a pasta de token.

```
Avalie a aplicação web já aberta no navegador quanto às dez heurísticas a seguir, segundo as regras de avaliação reproduzidas ao final (papel, rubrica de severidade e regras gerais).

Heurísticas desta avaliação (as dez):
{blocos das dez heurísticas, H1 a H10, do núcleo, cada um com definição, por que importa, dicas e exemplo}

Escopo e restrições:
- Avalie o objeto contra todas as dez heurísticas e reporte todo problema da interface que viole qualquer uma delas.
- Cada achado nomeia exatamente uma heurística, aquela que ele viola, no campo "heuristica".
- Se um mesmo problema violar mais de uma das dez heurísticas, registre um achado por heurística violada, cada um com descrição e justificativas próprias daquela heurística.
- Não force achados: problemas que não violem nenhuma das dez heurísticas não são registrados.
- Inspecione todo o objeto e percorra as tarefas do material de contexto; não se limite a uma tela.
- Um achado por violação, no formato JSON das suas instruções. Sem violação, grave uma lista vazia.

Material de contexto:
{conteúdo integral de contexto/contexto.md}

Pasta de evidências: {caminho absoluto da pasta de token}
Geometria do viewport medida: {largura} × {altura} pixels CSS, DPR {dpr}

Regras de avaliação:
{seções 1, 4 e 6 do núcleo: papel e objetivo, rubrica de severidade, regras gerais}
```

**Não revele a que condição ele pertence** — por isso a pasta de evidências é uma neutra sob `_incoming/`,
e não a da condição.
Não acrescente à delegação nenhuma pergunta sobre isolamento de contexto, nem qualquer instrução que
restrinja a exploração da interface.

## 4. Feche o ciclo da chamada

### 4.1 Leia o retorno

O avaliador **não devolve os achados na resposta**: ele os grava em
`achados.json` **dentro da pasta de token dele** e responde uma única linha, com o caminho e o número de achados.
É assim de propósito — o texto dos achados não pode ocupar a sua janela de contexto. O ambiente
entrega retornos longos ora inline, ora persistidos em arquivo, a critério dele; em ensaio o
comportamento se manifestou das duas formas, e gravar em arquivo é o que torna o custo do
orquestrador independente do tamanho do retorno.

1. Confira **por script** (`node`) que `evidencias/_incoming/<token>/achados.json` existe, parseia
   como array e tem o número de elementos que o avaliador declarou.
2. Mova o arquivo para a pasta temporária da sessão, **fora do repositório**: ele não é evidência, e
   `evidencias/_incoming/` precisa terminar o ciclo vazia.
3. Se o arquivo não existir, não parsear ou divergir da contagem declarada, **não improvise e não
   reconstrua os achados**: repeça o array ao mesmo subagente por `SendMessage`, com o `agentId` que
   veio na resposta dele.

Daqui em diante processe tudo **por script**, lendo o arquivo e escrevendo direto o que precisa ser
gravado. **Não transcreva os achados no seu próprio texto** em nenhuma hipótese.

Anote, para o registro de encerramento, os números de cada chamada. **Duração, tokens e usos de
ferramenta** vêm do **bloco de uso que o Claude Code anexa ao resultado do subagente** (tokens, usos
de ferramenta e duração), não do texto dele. São **obrigatórios**: se faltar algum em qualquer chamada,
**pare antes de gravar o encerramento e avise**, porque o custo é dado essencial do estudo. **As duas
contagens de erro** — `<e>` erros de ferramenta e `<t>` deles por timeout de protocolo — vêm da linha
de resposta do subagente; se não forem reportadas, registre `null` — não estime, e **não registre
zero**: ausência de relato não é ausência de falha, e foi exatamente essa confusão que tornou o
critério inauditável no primeiro ensaio paralelo.

### 4.2 Carimbe os achados

Para cada achado, acrescente:

- `"registro": "achado"`, para a linha se identificar sozinha, como já fazem o cabeçalho e o
  encerramento. Sem ele, o leitor da análise teria de reconhecer o achado pela **ausência** de um
  campo, que é o que quebrou na coleta de 21 a 23/09/2026.
- `"formato": "C"`
- `"id": "C-H<k>-<NNN>"`, em que `H<k>` é a heurística nomeada no campo `heuristica` do próprio achado e `<NNN>` é sequencial (001, 002, …) **dentro daquela heurística**.
- `"fora_do_escopo": false`; `true` só se o campo `heuristica` não for uma das dez (H1 a H10). Neste
  formato as dez estão no escopo.

### 4.3 Evidência visual

O subagente gravou os arquivos na **pasta de token dele** com o nome `<heuristica>_<NNN>`, contador
dele, e citou esses nomes no campo `registro_visual` de cada achado. **O vínculo entre arquivo e
achado é o caminho reportado nesse campo**, nunca a ordem dos arquivos na pasta: o contador do
arquivo e o `<NNN>` do `id` são numerações distintas e podem divergir. Em ensaio deste formato eles
coincidiram, porque o avaliador devolveu os achados já agrupados por heurística — não confie nisso:
use sempre o `registro_visual`.

A evidência é organizada **por condição e por heurística**, e cada achado leva consigo a própria
análise. O arquivamento é feito **em duas passagens**, por script — nunca em uma só. A razão está
verificada em ensaio: o avaliador às vezes cita, na prosa do `registro_visual`, um arquivo de **outro**
achado, para comparação ("comparar com `H5_001.1.png`"). Em passagem única esse arquivo seria movido e
renomeado para o achado errado, arrancando a evidência de quem é dono dela — e o estrago é silencioso.

**Passagem 1 — descubra o dono de cada arquivo.** Para cada achado, o arquivo próprio é o
`H<k>_<NNN>` cujo `H<k>` é a heurística **do próprio achado**; havendo mais de um, o que aparece mais
vezes no `registro_visual`. Monte um mapa global `base do arquivo → id carimbado`. Toda citação que
não case com o arquivo próprio é **referência cruzada**, não posse.

**Passagem 2 — arquive e reescreva.** Para cada achado:

1. Determine a pasta de destino pelo campo `heuristica`: `evidencias/exec-<n>/C/H<nn>/`, com `<nn>` de dois
   dígitos (`H01`…`H10`). Crie-a se não existir.
2. Mova para lá **apenas os arquivos do próprio achado**, segundo o mapa da passagem 1, renomeando
   cada um para o identificador que você carimbou e preservando o sufixo — `C-H7-012.png`,
   `C-H7-012.snapshot.txt`, `C-H7-012.elemento.png`, e `C-H7-012.1.png` / `C-H7-012.2.png` quando o
   achado tiver sido registrado por capturas sucessivas.
3. Reescreva **todas** as menções a arquivo no `registro_visual` usando o mapa global — inclusive as
   referências cruzadas, que passam a apontar para o nome final do arquivo na pasta do achado dono.
   Preserve o resto do texto que o subagente escreveu.
4. Grave, na mesma pasta, **`C-H7-012.achado.md`** — a análise do achado ao lado da evidência que a
   sustenta, gerada a partir do mesmo registro já carimbado, para que as duas não possam divergir.
   *Front-matter* YAML com `id`, `formato`, `heuristica`, `severidade`, `severidade_rotulo` e
   `chamada`; corpo com Localização, Arquivos de evidência, Registro visual, Descrição da falha,
   Justificativa da violação, Justificativa da severidade e Sugestão de correção.

Se algum arquivo citado não existir, registre a ausência no resumo final: não invente caminho e não
descarte o achado. Arquivo que sobre na pasta de token sem ser citado por achado nenhum é
**órfão** — captura que o avaliador gravou e não usou. Não é evidência de coisa alguma: não entra na
pasta da condição e não ganha identificador. Mova-o para a pasta temporária da sessão e **nomeie-o no
resumo**. Ao fim do ciclo, **remova a pasta de token, que tem de estar vazia**; `evidencias/_incoming/`
não pode terminar a condição com arquivo nem com subpasta.

### 4.4 Grave os achados da chamada

Anexe os achados como linhas JSON a `resultados/exec-<n>/resultados_C.jsonl`. Você é o **único** que
escreve esse arquivo.

Monte as linhas em um arquivo na pasta temporária da sessão, **fora do repositório**, e anexe com um
único comando — `cat "<temporário>" >> "<caminho absoluto>/resultados/exec-<n>/resultados_C.jsonl"`.
Gravar linha a linha é custoso e sujeito a erro de *quoting*. O que a regra protege permanece:
escritor único, caminho absoluto e nenhum comando composto com `&&`.

## 5. Feche a condição

Depois da última chamada, anexe ao mesmo arquivo uma **última linha** com o registro de
encerramento, que é o dado de custo e de tempo da condição:

```json
{"registro":"encerramento","formato":"C","execucao":<n>,"modo_execucao":"chamada_unica","paralelismo":1,"datahora_disparo":"<ISO-8601>","datahora_ultimo_retorno":"<ISO-8601>","datahora_fim":"<ISO-8601>","duracao_total_s":<n>,"duracao_execucao_s":<n>,"duracao_avaliacao_s":<n>,"chamadas":[{"chamada":"unica","duracao_ms":<n>,"tokens":<n>,"usos_ferramenta":<n>,"erros_ferramenta":<n>,"timeouts":<n>,"achados":<n>}],"tokens_total":<n>,"usos_ferramenta_total":<n>,"erros_ferramenta_total":<n>,"timeouts_total":<n>,"achados_total":<n>,"arquivos_evidencia":<n>,"duracao_ms_soma":<n>,"duracao_ms_max":<n>,"concorrencia_observada":"nao_aplicavel"}
```

**Os três tempos, como em A e B:** `duracao_total_s` = `datahora_fim` − `datahora_disparo`; `duracao_execucao_s` =
`datahora_fim` − `datahora_inicio` (do cabeçalho); `duracao_avaliacao_s` = `datahora_ultimo_retorno` −
`datahora_disparo`. Com uma chamada só, `duracao_ms_soma` e `duracao_ms_max` coincidem, e
`concorrencia_observada` é `"nao_aplicavel"`: aqui não há paralelismo a conferir. Os números por chamada são os que você anotou em 4.1. Registre que a soma de `tokens_total`
cobre **as chamadas de avaliação**, que é o custo comparável entre formatos; o consumo do próprio
orquestrador não é observável de dentro da execução.

**Gere o índice da condição** em `evidencias/exec-<n>/C/_indice.md`, por script: a distribuição dos achados
(por heurística e por severidade) e uma linha por achado com id, heurística, severidade, localização
e número de arquivos de evidência. É por onde se entra na pasta.

**Rode as conferências de fechamento.** Todas obrigatórias, e o resultado de cada uma vai no resumo —
são elas que transformam "confio no vínculo" em "verifiquei o vínculo":

1. **Vínculo arquivo↔achado, nos dois sentidos.** Todo arquivo citado em `registro_visual` existe em
   disco, e todo arquivo em `evidencias/exec-<n>/C/` é citado por algum achado. Nenhum dos dois lados pode
   sobrar. **Os `<id>.achado.md` do passo 4.4 ficam fora desta conferência**: são a análise do
   achado, não evidência dele, nenhum `registro_visual` os cita e eles também não entram em
   `arquivos_evidencia`.
2. **`evidencias/_incoming/` vazia** — **nenhuma subpasta e nenhum arquivo além do `.gitkeep`**, que mantém a pasta no repositório. A pasta de token tem de ter
   sido removida em 4.3, e nenhum `achados.json` pode ter sobrado (você o moveu em 4.1).
3. **Geometria das capturas — relatório, não reprovação.** Leia as dimensões dos `.png` e reporte a
   distribuição por modo de enquadramento: quantas na altura da área visível medida no passo 0
   (largura e altura em CSS multiplicadas pelo DPR) e quantas em página inteira, com as dimensões de
   cada grupo, e quantas são **recorte de elemento** (`<id>.elemento.png`), que mostra um controle
   de perto. O recorte **acompanha** a captura de área visível do mesmo achado e nunca a
   substitui: reporte-o à parte e não lhe aplique a exigência de largura constante.
   **Nas capturas de área visível a largura tem de ser constante** — é ela que torna a
   renderização comparável, e variação ali é defeito. **Nas de página inteira, admite-se a variação
   da largura da barra de rolagem** (cerca de 15 px), que aparece de forma transitória durante a
   rolagem que esse modo força: reporte, não reprove. A altura varia por desenho, porque segue o que cada achado precisa
   demonstrar. O que este relatório revela é **divergência sistemática de comportamento entre
   avaliadores**: se uma condição documenta quase tudo em página inteira e outra quase tudo na área
   visível, as bases de evidência das duas não são comparáveis, e isso tem de aparecer no registro
   em vez de passar batido.
4. **Integridade do JSONL.** Toda linha parseia; nenhum campo faltando nem extra nos achados; `<NNN>`
   sequencial dentro de cada heurística.
5. **Escritor único.** Compare a listagem de `resultados/exec-<n>/` com a **linha de base registrada no passo
   0**. O esperado é: os arquivos que já existiam antes desta condição começar, mais o desta
   condição. Qualquer outra coisa é inesperada e vai no resumo. A comparação é contra a linha de
   base, e não contra uma lista fixa, porque a pasta da execução acumula os arquivos dos formatos já
   rodados nela — e uma lista fixa envelheceria. As ferramentas de captura do
   MCP gravam por `filePath` próprio e não passam pelas regras de permissão de escrita, então é esta
   comparação que fecha a garantia.
6. **Definições de avaliador íntegras.** Rode `node .claude/gerar_avaliadores.mjs --verificar`. As dez
   têm de ser idênticas ao modelo exceto `name:` e o namespace de `tools:` — este formato usa apenas a
   primeira, mas a conferência roda sobre todas, para que as três condições partam do mesmo avaliador.
7. **Custo completo.** A chamada do encerramento não pode ter `tokens`, `duracao_ms` ou
   `usos_ferramenta` nulos. Se houver, o encerramento não é gravado até o número ser recuperado do
   bloco de uso.
8. **Escopo das heurísticas.** Reporte quantos achados saíram com `fora_do_escopo: true`. Eles ficam
   no JSONL; a análise os exclui de `|A(F,e)|` e os conta à parte. Neste formato as dez heurísticas
   estão no escopo, então o esperado é zero.

**Ao final**, mostre no chat um resumo: nº total de achados e a distribuição por heurística, o caminho
do arquivo de resultados, a duração total, os tokens consumidos e o resultado das **oito** conferências.

**Não** numere de outra forma, **não** agrupe achados, **não** classifique falsos positivos e **não**
julgue os achados além do que está aqui — isso é trabalho de análise posterior, fora deste projeto.
No Formato C a avaliação ocorre em uma chamada única (exposição total das dez heurísticas), em contexto isolado do subagente.
