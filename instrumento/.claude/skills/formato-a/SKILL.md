---
name: formato-a
description: Orquestra a condição A da coleta — uma heurística por chamada, dez subagentes avaliadores independentes disparados em paralelo, um navegador headless por avaliador — e grava os achados em resultados/exec-<n>/resultados_A.jsonl.
disable-model-invocation: true
model: claude-opus-5
---

# Orquestrador — Formato A (uma heurística por chamada)

Argumentos: `$ARGUMENTS` = `<n> [caminho-do-.html]`. O primeiro, **obrigatório**, é o número da
execução (1, 2 ou 3): define as pastas `resultados/exec-<n>/` e `evidencias/exec-<n>/` em que esta
condição grava, e vai no cabeçalho como `execucao`. Se vier vazio ou não for um inteiro, **pare e peça**.
O segundo, opcional, é o caminho do `.html` do objeto; se não vier, pergunte na verificação de estado
inicial. O material de contexto é sempre `contexto/contexto.md`, o mesmo nas nove execuções.

Você é o **ORQUESTRADOR**. Você **não avalia**. Você abre o objeto, dispara subagentes avaliadores
independentes, coleta os retornos e grava o arquivo de resultados. Siga exatamente:

## 0. Verificação de estado inicial (antes de qualquer delegação)

1. **Objeto, nos dez navegadores.** Obtenha o caminho do `.html` (do argumento ou perguntando). Este
   formato usa **dez servidores MCP independentes**, `cdp-01` a `cdp-10`, um por avaliador. Em **cada
   um dos dez**, abra o objeto com `new_page` no `file://` correspondente e **recarregue** com
   `navigate_page` (`type: reload`). Reporte no chat os dez, confirmando que abriu e recarregou.

   Cada servidor sobe a própria instância do Chrome, **headless**, com perfil temporário
   (`--isolated`): o estado não vem contaminado das condições anteriores **nem dos outros
   avaliadores desta condição**. É isolamento de processo, garantia mais forte do que recarregar uma
   aba compartilhada — e é por isso que não há recarga entre delegações neste formato.
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
4. **Viewport, medido nos dez.** O `.mcp.json` declara um viewport **alvo**, e `resize_page` **retorna
   sucesso mesmo sem aplicar** a dimensão pedida — então meça, não declare. Em **cada um dos dez**
   servidores, rode `evaluate_script` na página do objeto:
   `() => ({w: innerWidth, h: innerHeight, dpr: devicePixelRatio})`.

   Em headless o viewport não fica preso ao tamanho da tela, então o esperado é **1440×900 com DPR 1
   nos dez**. Duas conferências, antes da confirmação:

   - **as dez geometrias têm de ser idênticas entre si.** Divergência aqui quebra a constância da
     largura das capturas *dentro* da condição, que é requisito da evidência — **não prossiga**;
   - se o medido divergir do alvo, **diga isso no chat**. Divergência não impede a coleta desde que
     fique registrada e seja a mesma nas três condições.
5. **Guardas de pasta (P1 e P2).** Esta execução grava em `resultados/exec-<n>/` e em `evidencias/exec-<n>/`, e rodar
   na árvore errada contaminaria dados de outra execução. Antes da confirmação, reporte no chat:

   - **P1** — a listagem de `resultados/exec-<n>/` registrada abaixo, que é a linha de base da conferência de
     escritor único. Ela **pode** conter os arquivos dos outros formatos já rodados nesta execução: isso é
     esperado, porque a pasta da execução acumula por desenho — é justamente por isso que a conferência
     compara contra uma linha de base, e não contra uma lista fixa. **O que reprova é encontrar ali o
     arquivo desta condição** (`resultados_A.jsonl`): significaria que você está prestes a anexar a um
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

**Crie `resultados/exec-<n>/` e `evidencias/exec-<n>/` se não existirem, e registre a listagem de `resultados/exec-<n>/` como ela está agora**, antes de gravar qualquer coisa. Ela é a
linha de base da conferência de escritor único do passo 5: no fechamento, o que aparecer ali e não
tiver sido gravado por você é inesperado.

Grave então a **primeira linha** de `resultados/exec-<n>/resultados_A.jsonl`:

```json
{"registro":"cabecalho","formato":"A","execucao":<n>,"objeto_arquivo":"<caminho>","objeto_hash_sha256":"<hash>","estado_inicial":"aberto e recarregado pelo orquestrador nos 10 navegadores","modo_execucao":"paralela","paralelismo":10,"navegador":"headless","viewport_alvo":"1440x900","viewport_medido_css":"<L>x<A>","device_pixel_ratio":<n>,"viewport_divergente":<true|false>,"viewport_identico_entre_navegadores":<true|false>,"modelo":"claude-opus-5","nivel_raciocinio":"<confirmado no passo 0.3>","versao_mcp_chrome_devtools":"<versão>","versao_chrome":"<versão>","versao_app_desktop":"<versão>","commit_instrumento":"<hash>","branch":"<branch>","arvore_limpa":<true|false>,"datahora_inicio":"<ISO-8601>","contexto_arquivo":"contexto/contexto.md","contexto_hash_sha256":"<hash>"}
```

**Grave sempre pelo shell, com caminho absoluto e um comando por invocação** — por exemplo
`printf '%s\n' '<json>' >> "<caminho absoluto>/resultados/exec-<n>/resultados_A.jsonl"`. Não encadeie comandos com
`&&`: comando composto exige que cada parte esteja pré-aprovada e a execução para pedindo permissão.

**No `objeto_arquivo`, escreva o caminho com barras normais**
(`C:/Users/EduardoDamiao/Documents/MBA USPEsalq/objeto/tarefas_crm.html`): a barra invertida do
Windows é comida na montagem do JSON pelo shell e o campo sai truncado — quando não quebra o
parse da linha inteira, porque `\U` de `\Users` e `\D` de `\Documents` não são escapes
válidos em JSON. Depois de gravar, leia a linha de volta e confirme que ela parseia e que o caminho
está íntegro.

**Não delegue nada** antes das confirmações e do cabeçalho gravado.

## 1. Leia o núcleo

Leia `protocolo/nucleo_heuristico.md`. Separe dele:

- as **seções compartilhadas**: papel/objetivo, rubrica de severidade (0–4) e regras gerais de avaliação;
- os **10 blocos de heurística** (H1…H10) da seção de definições — cada um com definição, "por que
  importa", dicas e exemplo.

## 2. Leia o contexto

Leia `contexto/contexto.md`.

## 3. Dispare os dez subagentes **de uma vez, em paralelo**

**Antes, confira que `evidencias/_incoming/` está vazia** — nenhuma subpasta e nenhum arquivo além do
`.gitkeep`. Um `achados.json` de execução anterior seria lido e carimbado com os identificadores desta.

**Prepare as dez pastas neutras.** Para cada heurística k, sorteie um **token aleatório e opaco** (8
caracteres hexadecimais, por exemplo) e crie `evidencias/_incoming/<token>/`. Guarde o mapa
`heurística k → token` **só para você**.

O token é o que permite dez avaliadores simultâneos sem colisão: o nome `achados.json` é fixo, e dez
avaliadores gravando na mesma pasta se sobrescreveriam. E por ser aleatório ele não carrega
informação: não diz a condição, não diz a heurística, não diz quantos são. De quebra, a ameaça de
"ler o `achados.json` de outra chamada" some por construção — cada pasta nasce vazia e nenhum outro
avaliador conhece o token dela.

**Registre `datahora_disparo`** (ISO-8601) imediatamente antes de disparar. Como as dez partem
juntas, esse instante **é** o início do primeiro avaliador, e é dele que sai a duração da condição
no passo 5.

**Dispare as dez delegações numa única mensagem**, para que rodem concorrentes. Cada heurística k vai
para o seu próprio avaliador e o seu próprio navegador:

| Heurística | Subagente | Servidor MCP | Pasta de evidências |
|---|---|---|---|
| H1 | `avaliador-heuristico-01` | `cdp-01` | `evidencias/_incoming/<token de H1>/` |
| H2 | `avaliador-heuristico-02` | `cdp-02` | … |
| … | … | … | … |
| H10 | `avaliador-heuristico-10` | `cdp-10` | … |

Contexto isolado; **não** use fork. Cada avaliador enxerga **apenas** as ferramentas do seu servidor,
e é isso que garante que ele não alcance o navegador de outro — o que seria contaminação do estado do
objeto.

**Não há recarga entre delegações neste formato.** Cada avaliador tem processo, perfil e aba próprios,
carregados do zero no passo 0: a independência do **estado do objeto** — que é a manipulação
metodológica deste formato — vem do isolamento de processo, garantia mais forte do que recarregar uma
aba compartilhada.

Monte a delegação com o texto abaixo, **literalmente**, preenchendo só o que está entre chaves. Nada
mais entra e nada sai: o texto é o mesmo nas nove execuções e nos três formatos no que é comum, e o
que varia entre chamadas é só o bloco de heurística e a pasta de token.

```
Avalie a aplicação web já aberta no navegador exclusivamente quanto à heurística a seguir, segundo as regras de avaliação reproduzidas ao final (papel, rubrica de severidade e regras gerais).

Heurística-alvo desta avaliação:
{bloco da heurística k, do núcleo: definição, por que importa, dicas e exemplo}

Escopo e restrições:
- Reporte todo problema da interface que viole a heurística acima; o campo "heuristica" de cada achado é sempre ela.
- Não force achados: se um problema não a violar, não o registre.
- Se um mesmo problema violar também outra heurística, descreva-o aqui apenas sob a ótica desta.
- Inspecione todo o objeto e percorra as tarefas do material de contexto; não se limite a uma tela.
- Um achado por violação, no formato JSON das suas instruções. Sem violação, grave uma lista vazia.

Material de contexto:
{conteúdo integral de contexto/contexto.md}

Pasta de evidências: {caminho absoluto da pasta de token desta heurística}
Geometria do viewport medida: {largura} × {altura} pixels CSS, DPR {dpr}

Regras de avaliação:
{seções 1, 4 e 6 do núcleo: papel e objetivo, rubrica de severidade, regras gerais}
```

Não passe para o subagente os achados de nenhuma outra chamada, **não revele a que condição ele
pertence** e não diga que há outros avaliadores rodando. Cada delegação é autossuficiente e idêntica
em estrutura — variam apenas o bloco da heurística e o token da pasta.
Não acrescente à delegação nenhuma pergunta sobre isolamento de contexto, nem qualquer instrução que
restrinja a exploração da interface.

## 4. Feche os dez ciclos, depois que todos voltarem

Os dez avaliadores rodam juntos e você só retoma quando **todos** tiverem terminado. A partir daí,
processe **uma chamada por vez**, na ordem de H1 a H10, aplicando 4.1 a 4.4 em cada uma antes de
passar à seguinte. Feche um ciclo antes de abrir o próximo: o contador de `id` e o vínculo entre arquivo e achado não podem
se embaralhar.

O custo de contexto não muda com o paralelismo: cada avaliador responde **uma única linha**, e os
achados vêm de arquivo. Dez linhas são triviais.

**Anote `datahora_ultimo_retorno`** (ISO-8601) no instante em que o décimo voltar.

### 4.1 Leia o retorno

O avaliador **não devolve os achados na resposta**: ele os grava em
`achados.json` **dentro da pasta de token dele** e responde uma única linha, com o caminho e o número
de achados.
É assim de propósito — o texto dos achados não pode ocupar a sua janela de contexto. O ambiente
entrega retornos longos ora inline, ora persistidos em arquivo, a critério dele; em ensaio o
comportamento se manifestou das duas formas, e gravar em arquivo é o que torna o custo do
orquestrador independente do tamanho do retorno.

1. Confira **por script** (`node`) que `evidencias/_incoming/<token>/achados.json` existe, parseia
   como array e tem o número de elementos que o avaliador declarou. Confira também que o caminho que
   ele reportou é o **token daquela heurística**, e não o de outra.
2. Mova o arquivo para a pasta temporária da sessão, **fora do repositório**: ele não é evidência, e
   `evidencias/_incoming/` precisa terminar a condição vazia — nenhuma subpasta e nenhum arquivo além do `.gitkeep`, que mantém a pasta no repositório.
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
- `"formato": "A"`
- `"id": "A-H<k>-<NNN>"`, com `<NNN>` sequencial (001, 002, …) **dentro daquela heurística**.
- `"fora_do_escopo": true` se o campo `heuristica` do achado **não for a heurística da chamada**;
  `false` caso contrário. O achado fica no JSONL; a análise o exclui de `|A(F,e)|` e o conta à parte.

### 4.3 Evidência visual

O subagente gravou os arquivos na **pasta de token dele** com o nome `<heuristica>_<NNN>`, contador
dele, e citou esses nomes no campo `registro_visual` de cada achado. **O vínculo entre arquivo e
achado é o caminho reportado nesse campo**, nunca a ordem dos arquivos na pasta: o contador do
arquivo e o `<NNN>` do `id` são numerações distintas e podem divergir. Neste formato eles tendem a
coincidir, porque a chamada tem uma heurística só — não confie nisso: use sempre o `registro_visual`.

A evidência é organizada **por condição e por heurística**, e cada achado leva consigo a própria
análise. O arquivamento é feito **em duas passagens**, por script — nunca em uma só. A razão está
verificada em ensaio: o avaliador às vezes cita, na prosa do `registro_visual`, um arquivo de **outro**
achado, para comparação ("comparar com `H5_001.1.png`"). Em passagem única esse arquivo seria movido e
renomeado para o achado errado, arrancando a evidência de quem é dono dela — e o estrago é silencioso.
Neste formato a chamada tem uma heurística só, então a referência cruzada, quando ocorre, aponta para
outro achado da **mesma** heurística; a regra vale igual.

**Passagem 1 — descubra o dono de cada arquivo.** Para cada achado, o arquivo próprio é o
`H<k>_<NNN>` cujo `H<k>` é a heurística **do próprio achado**; havendo mais de um, o que aparece mais
vezes no `registro_visual`. Monte um mapa global `base do arquivo → id carimbado`. Toda citação que
não case com o arquivo próprio é **referência cruzada**, não posse.

**Passagem 2 — arquive e reescreva.** Para cada achado:

1. Determine a pasta de destino pelo campo `heuristica`: `evidencias/exec-<n>/A/H<nn>/`, com `<nn>` de dois
   dígitos (`H01`…`H10`). Crie-a se não existir.
2. Mova para lá **apenas os arquivos do próprio achado**, segundo o mapa da passagem 1, renomeando
   cada um para o identificador que você carimbou e preservando o sufixo — `A-H1-001.png`,
   `A-H1-001.snapshot.txt`, `A-H1-001.elemento.png`, e `A-H1-001.1.png` / `A-H1-001.2.png` quando o
   achado tiver sido registrado por capturas sucessivas.
3. Reescreva **todas** as menções a arquivo no `registro_visual` usando o mapa global — inclusive as
   referências cruzadas, que passam a apontar para o nome final do arquivo na pasta do achado dono.
   Preserve o resto do texto que o subagente escreveu.
4. Grave, na mesma pasta, **`A-H1-001.achado.md`** — a análise do achado ao lado da evidência que a
   sustenta, gerada a partir do mesmo registro já carimbado, para que as duas não possam divergir.
   *Front-matter* YAML com `id`, `formato`, `heuristica`, `severidade`, `severidade_rotulo` e
   `chamada`; corpo com Localização, Arquivos de evidência, Registro visual, Descrição da falha,
   Justificativa da violação, Justificativa da severidade e Sugestão de correção.

Se algum arquivo citado não existir, registre a ausência no resumo final: não invente caminho e não
descarte o achado. Arquivo que sobre na pasta de token sem ser citado por achado nenhum é
**órfão** — captura que o avaliador gravou e não usou. Não é evidência de coisa alguma: não entra na
pasta da condição e não ganha identificador. Mova-o para a pasta temporária da sessão e **nomeie-o no
resumo**. Ao fim de cada ciclo, **remova a pasta de token, que tem de estar vazia**; ao fim da
condição, `evidencias/_incoming/` não pode ter nem arquivo nem subpasta.

Como cada chamada tem a sua própria pasta, os arquivos de uma nunca se misturam aos de outra — nem
quando as dez rodam ao mesmo tempo. Um arquivo encontrado na pasta de token errada é defeito, e vai
para o resumo.

### 4.4 Grave os achados da chamada

Anexe os achados como linhas JSON a `resultados/exec-<n>/resultados_A.jsonl`. Você é o **único** que
escreve esse arquivo.

Monte as linhas em um arquivo na pasta temporária da sessão, **fora do repositório**, e anexe com um
único comando — `cat "<temporário>" >> "<caminho absoluto>/resultados/exec-<n>/resultados_A.jsonl"`.
Gravar linha a linha é custoso e sujeito a erro de *quoting*. O que a regra protege permanece:
escritor único, caminho absoluto e nenhum comando composto com `&&`.

## 5. Feche a condição

Depois da última chamada, anexe ao mesmo arquivo uma **última linha** com o registro de
encerramento, que é o dado de custo e de tempo da condição:

```json
{"registro":"encerramento","formato":"A","execucao":<n>,"modo_execucao":"paralela","paralelismo":10,"datahora_disparo":"<ISO-8601>","datahora_ultimo_retorno":"<ISO-8601>","datahora_fim":"<ISO-8601>","duracao_total_s":<n>,"duracao_execucao_s":<n>,"duracao_avaliacao_s":<n>,"chamadas":[{"chamada":"<a heurística da chamada (por exemplo `H1`)>","duracao_ms":<n>,"tokens":<n>,"usos_ferramenta":<n>,"erros_ferramenta":<n>,"timeouts":<n>,"achados":<n>}],"tokens_total":<n>,"usos_ferramenta_total":<n>,"erros_ferramenta_total":<n>,"timeouts_total":<n>,"achados_total":<n>,"arquivos_evidencia":<n>,"duracao_ms_soma":<n>,"duracao_ms_max":<n>,"concorrencia_observada":"<paralela|serializada|parcial>"}
```

**Os três tempos, e o que cada um significa:**

- `duracao_total_s` = `datahora_fim` − **`datahora_disparo`**. Como as dez partem juntas, o disparo é
  o início do primeiro avaliador; o fim é esta gravação. É a duração da condição.
- `duracao_avaliacao_s` = `datahora_ultimo_retorno` − `datahora_disparo`. É só a fase de avaliação,
  sem o arquivamento — é ela que se compara com `duracao_ms_max`.
- `duracao_execucao_s` = `datahora_fim` − `datahora_inicio` (do cabeçalho). É a execução inteira, do
  começo do passo 0 ao encerramento, o tempo que o pesquisador esperou.

**`concorrencia_observada` é derivada, e é a conferência que diz se o paralelismo aconteceu de fato:**
compare `duracao_avaliacao_s` com `duracao_ms_soma` e com `duracao_ms_max`. Perto do **máximo** →
`"paralela"`. Perto da **soma** → `"serializada"`, e o harness enfileirou os subagentes apesar do
disparo único — registre isso com destaque no resumo, porque invalida a leitura de tempo da condição.
Entre os dois → `"parcial"`.

**`duracao_ms` por chamada inclui contenção** — os dez avaliadores disputam CPU e o servidor MCP de
cada um —, então **não é comparável a uma execução sequencial**. Registre isso. Os números por chamada
são os que você anotou em 4.1.

A soma de `tokens_total` cobre **as chamadas de avaliação**, que é o custo comparável entre formatos;
o consumo do próprio orquestrador não é observável de dentro da execução. Tokens e usos de ferramenta
**não** são afetados pelo paralelismo: são propriedade da trajetória de cada avaliador. São eles, e
não a parede, a métrica limpa de custo entre formatos.

**Gere o índice da condição** em `evidencias/exec-<n>/A/_indice.md`, por script: a distribuição dos achados
(por chamada, por heurística e por severidade) e uma linha por achado com id, heurística, severidade,
localização e número de arquivos de evidência. É por onde se entra na pasta.

**Rode as conferências de fechamento.** Todas obrigatórias, e o resultado de cada uma vai no resumo —
são elas que transformam "confio no vínculo" em "verifiquei o vínculo":

1. **Vínculo arquivo↔achado, nos dois sentidos.** Todo arquivo citado em `registro_visual` existe em
   disco, e todo arquivo em `evidencias/exec-<n>/A/` é citado por algum achado. Nenhum dos dois lados pode
   sobrar. **Os `<id>.achado.md` do passo 4.4 ficam fora desta conferência**: são a análise do
   achado, não evidência dele, nenhum `registro_visual` os cita e eles também não entram em
   `arquivos_evidencia`.
2. **`evidencias/_incoming/` vazia** — **nenhuma subpasta e nenhum arquivo além do `.gitkeep`**, que mantém a pasta no repositório. As dez pastas de token têm de
   ter sido removidas em 4.3, e nenhum `achados.json` pode ter sobrado (você os moveu em 4.1).
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
   sequencial dentro de cada chamada.
5. **Escritor único.** Compare a listagem de `resultados/exec-<n>/` com a **linha de base registrada no passo
   0**. O esperado é: os arquivos que já existiam antes desta condição começar, mais o desta
   condição. Qualquer outra coisa é inesperada e vai no resumo. A comparação é contra a linha de
   base, e não contra uma lista fixa, porque a pasta da execução acumula os arquivos dos formatos já
   rodados nela — e uma lista fixa envelheceria. As ferramentas de captura do
   MCP gravam por `filePath` próprio e não passam pelas regras de permissão de escrita, então é esta
   comparação que fecha a garantia.
6. **Definições de avaliador íntegras.** Rode `node .claude/gerar_avaliadores.mjs --verificar`. As dez
   têm de ser idênticas ao modelo exceto `name:` e o namespace de `tools:`. É isso que sustenta a
   afirmação de que as dez delegações são idênticas em estrutura; dez arquivos que derivam entre si
   quebrariam a manipulação em silêncio.
7. **Nenhum arquivo cruzou de pasta.** Cada achado só cita arquivos que vieram da pasta de token da
   **sua** heurística. Um arquivo que tenha aparecido na pasta de outro avaliador é defeito grave —
   significaria que dois avaliadores alcançaram o mesmo destino de escrita.
8. **Concorrência observada.** O valor derivado no encerramento. Se sair `"serializada"`, diga no
   resumo, em destaque, que o paralelismo não ocorreu e que a leitura de tempo desta condição não
   vale.
9. **Custo completo.** Nenhuma chamada do encerramento com `tokens`, `duracao_ms` ou `usos_ferramenta`
   nulos. Se houver, o encerramento não é gravado até o número ser recuperado do bloco de uso.
10. **Escopo das heurísticas.** Reporte quantos achados saíram com `fora_do_escopo: true`, por chamada.
   Eles ficam no JSONL; a análise os exclui de `|A(F,e)|` e os conta à parte.

**Ao final**, mostre no chat um resumo: nº de achados por heurística, o caminho do arquivo de
resultados, a duração total, a duração da fase de avaliação contra a soma e o máximo das chamadas,
os tokens consumidos e o resultado das **dez** conferências.

**Não** numere de outra forma, **não** agrupe achados, **não** classifique falsos positivos e **não**
julgue os achados além do que está aqui — isso é trabalho de análise posterior, fora deste projeto.
A **independência** entre as 10 avaliações é o ponto metodológico central deste formato: garanta que cada subagente veja apenas a sua heurística e nunca os achados das demais.
