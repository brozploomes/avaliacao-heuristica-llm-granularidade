# Unificação dos achados — prompt declarado

> **Para que serve.** Este é o prompt com que a IA **unifica** os achados das nove execuções em
> **achados unificados**, cada um candidato a um defeito. É documento de análise, não de coleta: nenhum
> orquestrador o lê e ele nunca chega a um avaliador. As unidades e a ordem das operações estão em
> `analise.md`.

## O que a IA faz, e o que não faz

Faz: recebe todos os achados das nove execuções, embaralhados e sob chave substituta, e devolve a lista
de achados unificados, cada um com os achados que reúne, um enunciado, o elemento da interface, os
pontos de manifestação e a justificativa da fusão. **Essa lista é a lista de achados unificados do
estudo**: o pesquisador não revisa fusões nem separações.

Não faz: não classifica falso positivo, não julga severidade, não atribui heurística, não vê formato,
execução, chamada nem `id`.

## Modelo e proveniência

Mesmo modelo da coleta: **Claude Opus 5**, raciocínio alto. A sessão de unificação registra a versão do
aplicativo, o nível de raciocínio, a data, a **semente** do embaralhamento e a saída bruta do modelo,
gravadas ao lado da trilha de decisões.

## Preparação da entrada (feita fora do modelo)

1. Reunir os achados dos nove `resultados/exec-<n>/resultados_<F>.jsonl`, deixando de fora os que têm
   `fora_do_escopo: true`.
2. Embaralhar com semente fixa, declarada.
3. Atribuir a cada achado uma chave substituta `K001`, `K002`, … na ordem embaralhada.
4. Remover `id`, `formato`, chamada e qualquer campo que revele a execução. No `registro_visual`,
   remover os nomes de arquivo, porque eles carregam o `id`. Ficam **no conjunto cego**: `heuristica`,
   `localizacao`, `registro_visual` (só a âncora em prosa), `descricao_falha`,
   `justificativa_violacao`, `severidade`, `severidade_rotulo`, `justificativa_severidade`,
   `sugestao_correcao`.
5. **Ao prompt da unificação vão apenas `localizacao`, `descricao_falha` e `sugestao_correcao`**, sob a
   chave. Heurística e severidade ficam de fora porque este protocolo já as declara fora dos critérios
   de fusão, e mandá-las convida o modelo a usar como pista o que não deve pesar — em especial no
   índice de atribuição múltipla, que mede justamente sob quantas heurísticas o mesmo problema foi
   registrado. `registro_visual` e `justificativa_violacao` ficam de fora porque a coleta real não
   caberia no contexto do modelo com eles: 476 achados dariam cerca de 372 mil tokens com os nove
   campos e cabem em cerca de 150 mil com estes três. O corte foi medido antes de ser adotado, sobre
   uma amostra de 100 achados unificada duas vezes, com os nove campos e com estes três: concordância
   de 0,999 entre as duas partições e 44 dos 48 achados unificados idênticos. Os nove campos
   permanecem em `achados_cegos.json` e alimentam as leituras, a página de revisão, a trilha e as
   métricas.
6. Guardar o mapa `chave → (id, formato, execucao, chamada)` fora do que o modelo e o pesquisador veem.
   Ele só é aberto na reatação, depois de fechada a classificação.

## Texto do prompt

> Você recebe uma lista de achados de avaliação heurística de usabilidade, todos sobre a **mesma
> aplicação web**, identificados por chaves `K###`. Achados diferentes podem descrever o **mesmo
> problema da interface** com palavras diferentes, sob heurísticas diferentes ou em telas diferentes.
> Sua tarefa é **unificar** os achados que descrevem o mesmo problema.
>
> **O que define "mesmo problema".** Aplique nesta ordem:
>
> 1. **Enunciado.** Reescreva cada achado como uma afirmação verificável sobre a interface, **sem
>    mencionar heurística** (por exemplo: "a validação exibe o código interno em vez de mensagem
>    legível"). Achados cujo enunciado coincide descrevem o mesmo problema.
> 2. **Elemento.** Achados com o mesmo enunciado sobre o **mesmo elemento ou região** da interface são o
>    mesmo problema. Enunciados iguais sobre **elementos distintos** são problemas distintos, ainda que
>    compartilhem a causa; registre a causa comum na justificativa.
> 3. **Correção.** Se uma única correção eliminaria todos os achados reunidos, eles são o mesmo problema.
>    Se exigem correções independentes, são problemas distintos, ainda que estejam no mesmo elemento.
>
> **O que não separa nem junta.** A entrada não traz a heurística nem a severidade de cada achado, de
> propósito: nenhuma das duas é critério de fusão. O mesmo problema pode ter sido registrado sob várias
> heurísticas e continua sendo um só. O mesmo problema observado em **telas ou estados diferentes** é um
> só achado unificado; registre em quantos pontos ele se manifesta.
>
> **Saída**, em JSON, sem texto fora dele:
>
> ```
> {
>   "achados_unificados": [
>     {"unificado": "U001",
>      "achados": ["K017", "K042", "K103"],
>      "enunciado": "afirmação verificável, sem heurística",
>      "elemento": "elemento ou região da interface",
>      "pontos_manifestacao": ["tela ou estado 1", "tela ou estado 2"],
>      "justificativa": "por que estes achados são o mesmo problema"}
>   ]
> }
> ```
>
> Todo achado aparece em exatamente um achado unificado; achado unificado de um só achado é normal.
> Numere os achados unificados em sequência, `U001`, `U002`, …

## Depois da unificação

A saída é conferida por script (`analise/unificar_prompt.py validar`): o JSON parseia, todo `K###`
aparece em exatamente um achado unificado, nenhum campo obrigatório está vazio. Se reprovar, a saída não
é corrigida à mão: o modelo é chamado de novo com a lista de erros, uma vez. A saída aceita é gravada
como `unificacao_ia.json`, ao lado da saída bruta e da proveniência. O `elemento` e os
`pontos_manifestacao` de cada achado unificado vão para a trilha de decisões como a âncora e os pontos de
manifestação do defeito (`analise.md` §4).

## Redação unificada (segundo passo, em lotes)

O pesquisador não lê os N achados de cada achado unificado, um a um: lê **leituras**, que a IA escreve
depois da unificação. Uma leitura é a redação unificada dos achados de **uma mesma heurística** dentro
de um achado unificado, com os cinco campos de um achado (localização, descrição da falha, justificativa
da violação, registro visual e sugestão de correção) e **o tamanho de um achado**. Um achado unificado
com achados de três heurísticas tem três leituras; com uma heurística só, uma. A separação por heurística
é mecânica, pelo campo `heuristica` que o avaliador preencheu; a IA não decide a que heurística um achado
pertence, só redige.

A leitura **não é resumo** nem é a soma dos textos: é um achado escrito de novo, que representa
fielmente o conjunto dos achados daquela heurística. A decisão do pesquisador continua uma por achado
unificado, porque a pergunta "o problema existe no objeto?" não depende da heurística e a severidade é
do problema. Os textos originais continuam disponíveis, recolhidos, na página de revisão.

A redação é feita em **lotes** de achados unificados (por padrão oito por chamada, com todas as suas
leituras), cada lote com os achados originais completos, porque a resposta de uma chamada só não caberia
para a coleta inteira. Cada lote roda numa chamada independente do mesmo modelo, sob o mesmo cegamento
(só chaves `K###` e identificadores `U###`).

### Texto do prompt da redação

> Você recebe achados unificados de uma avaliação heurística de usabilidade, todos sobre a **mesma
> aplicação web**. Cada achado unificado tem um identificador `U###`, um enunciado e os achados originais
> que ele reúne, **já separados por heurística**; cada achado original traz localização, registro visual,
> descrição da falha, justificativa da violação e sugestão de correção. Os achados de uma mesma
> heurística, dentro de um achado unificado, descrevem o **mesmo problema, pela mesma lente**, com
> palavras diferentes.
>
> Sua tarefa é escrever, para **cada par achado unificado × heurística**, **uma leitura**: um achado
> redigido de novo, com cinco campos (`localizacao`, `descricao_falha`, `justificativa_violacao`,
> `registro_visual`, `sugestao_correcao`), que represente fielmente o conjunto dos achados daquela
> heurística.
>
> **Regras da leitura.**
>
> 1. **Tamanho de um achado.** Cada campo tem o tamanho que teria num achado comum: a localização em uma
>    linha; a descrição, a justificativa e a sugestão em duas a quatro frases; o registro visual em uma ou
>    duas. A leitura não pode ficar maior que o maior dos achados que ela representa.
> 2. **Um texto que represente todos.** Onde os achados dizem a mesma coisa com palavras diferentes,
>    escreva uma vez, na forma mais precisa. O que só um achado traz entra apenas se muda o problema, a
>    localização ou a correção; não entra o que é incidental (listas de identificadores de elementos,
>    medidas repetidas, inventário captura por captura, dados de teste que só variam o exemplo).
> 3. **Não é resumo.** Nenhum fato que defina o problema, o elemento, o comportamento observado ou a
>    correção pode sumir. Se dois achados se contradizem num fato, registre a divergência em uma frase.
> 4. **Justificativa na lente da heurística.** A `justificativa_violacao` explica por que o comportamento
>    fere aquela heurística, como um achado faria; não misture lentes de outras heurísticas.
> 5. **Registro visual em prosa.** `registro_visual` descreve o que as capturas mostram (estado,
>    elementos, sequência antes e depois), sem nomes de arquivo e sem enumerar captura por captura.
> 6. **Escrita de achado.** Terceira pessoa, frases completas, português do Brasil, sem travessão.
> 7. Par com um só achado: reescreva os cinco campos desse achado nas regras acima, sem acrescentar nem
>    tirar informação.
>
> **Saída**, em JSON, sem texto fora dele:
>
> ```
> {
>   "redacoes": [
>     {"unificado": "U001",
>      "heuristica": "H2",
>      "localizacao": "…",
>      "descricao_falha": "…",
>      "justificativa_violacao": "…",
>      "registro_visual": "…",
>      "sugestao_correcao": "…"}
>   ]
> }
> ```
>
> Um objeto por par achado unificado × heurística recebido, na ordem recebida, todos os cinco campos
> preenchidos, `heuristica` só com o código (`H1` a `H10`).

### Depois da redação

Cada lote é conferido por script (`analise/unificar_prompt.py validar-redacao`): o JSON parseia, todo par
achado unificado × heurística do lote aparece uma vez, os cinco campos estão preenchidos e nenhuma
leitura é maior que uma vez e meia o maior achado que representa. As leituras aceitas são gravadas dentro
de `unificacao_ia.json`, no campo `leituras` de cada achado unificado, ao lado das saídas brutas dos
lotes. A página de revisão exibe as leituras, uma por heurística; os textos originais ficam recolhidos.
