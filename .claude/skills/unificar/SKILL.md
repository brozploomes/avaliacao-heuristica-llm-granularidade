---
name: unificar
description: Unificação cega dos achados por IA (passo 2.3 do roteiro do estudo). Monta o prompt de instrumento/protocolo/unificacao.md sobre achados_cegos.json, dispara o subagente unificador (Claude Opus, contexto isolado), guarda a saída bruta, valida (todo K### em exatamente um achado unificado) e registra a proveniência. Só roda quando invocada; nunca abre o mapa de chaves.
disable-model-invocation: true
---

# Unificação cega por IA

Argumento: `$ARGUMENTS` é a **pasta cega da análise** (por exemplo `entregas/analise-2026-09-21`). Se
vier vazio, pergunte. Toda a lógica de arquivo está em `instrumento/analise/unificar_prompt.py`; esta
skill só orquestra: prepara, dispara o subagente, guarda e confere. Você **não** unifica nada por conta
própria e **não** conserta a saída do modelo à mão. A saída aceita **é** a lista de achados unificados
do estudo: ninguém revisa fusões depois.

Regra que vale do início ao fim: **não abra a pasta `<pasta>-fechado`** nem qualquer arquivo dela
(`mapa_chaves.json`, `encerramentos.json`, `cabecalhos.json`, `fora_do_escopo.json`). Ela é aberta só no
passo 4.1, pelo script de reatação.

## 0. Verificação

1. A pasta existe e tem `achados_cegos.json` e `semente.txt`. Se não, pare: o passo 2.2 (reunião e
   cegamento) ainda não rodou.
2. `mapa_chaves.json` **não** está dentro da pasta cega. Se estiver, pare e avise: o cegamento foi quebrado.
3. Se já existir `unificacao_ia.json` ou `unificacao_ia_bruto.md` na pasta, pare e pergunte antes de
   sobrescrever. Uma unificação já aceita não se refaz sem decisão registrada.
4. Pergunte ao Eduardo, numa mensagem só: a versão do aplicativo (Ajuda → Sobre) e o **nível de
   raciocínio** da sessão (o subagente herda o da conversa; o protocolo pede **alto**, e ele deve estar
   assim antes do disparo). Mostre o que vai rodar e espere o "ok".

## 1. Montar o prompt

```bash
py instrumento/analise/unificar_prompt.py montar --pasta "<pasta>"
```

Grava `<pasta>/prompt_unificacao.md` (texto de `protocolo/unificacao.md` + os achados cegos, com os
campos do item 5 da "Preparação da entrada") e imprime o tamanho. Relate o número de achados e a
estimativa de tokens.

A estimativa do script é **caracteres ÷ 3, que é teto**: em português a razão real fica perto de ÷ 4,
então o número impresso é cerca de um terço maior que a contagem verdadeira. Só avise antes de
disparar se a estimativa passar de **250 mil** — aí a contagem real beira os 190 mil e a resposta pode
não caber junto com o prompt. Abaixo disso, siga. Referência medida: a coleta de 21 a 23/09/2026, com
476 achados, deu 452 mil caracteres, estimativa de 150.719 e contagem real perto de 113 mil.

## 2. Disparar o subagente

Use a ferramenta Agent com `subagent_type: unificador` (definido em `.claude/agents/unificador.md`,
modelo Opus, só a ferramenta de leitura). A delegação contém **apenas** o caminho absoluto de
`prompt_unificacao.md` e a frase: "Leia este arquivo inteiro e responda só com o JSON pedido nele."
Nada de contexto adicional, nada sobre formatos, execuções ou o estudo.

Se o tipo `unificador` não estiver disponível na sessão (sessão aberta antes de o arquivo existir), use
`general-purpose` com `model: opus`, a mesma delegação e as regras do arquivo do agente copiadas na
delegação, e registre isso na proveniência.

Aguarde o retorno. Não dispare dois agentes; não reenvie por impaciência.

## 3. Guardar a saída bruta

Grave o retorno do agente **na íntegra, sem editar**, em `<pasta>/unificacao_ia_bruto.md`, precedido de
um cabeçalho YAML com: `data` (ISO-8601), `modelo`, `nivel_raciocinio`, `versao_app`, `semente` (de
`semente.txt`), `achados` (n), `agente` (unificador ou general-purpose), `rodada` (1). Se houver segunda
rodada (passo 4), anexe a nova saída ao mesmo arquivo, sob `rodada: 2`, sem apagar a primeira.

## 4. Validar

```bash
py instrumento/analise/unificar_prompt.py validar --pasta "<pasta>"
```

Confere: a saída parseia; todo `K###` está em exatamente um achado unificado; nenhuma chave desconhecida;
enunciado, elemento e justificativa preenchidos. Grava `unificacao_conferencia.md` e, se passar,
`unificacao_ia.json` (normalizado: identificadores `U###`, achados ordenados).

Se **reprovar**: não corrija o JSON. Envie ao **mesmo** agente, por SendMessage, só a lista de erros
que o script imprimiu (por exemplo, as chaves que ficaram sem achado unificado), pedindo o JSON completo
de novo. Uma rodada extra, no máximo. Se ainda reprovar, pare e traga o relatório ao Eduardo.

## 4b. Leituras (redação unificada por heurística), em lotes

Com `unificacao_ia.json` aceito:

```bash
py instrumento/analise/unificar_prompt.py montar-redacao --pasta "<pasta>" --lote 8
```

Grava `redacao_lote_01.md`, `redacao_lote_02.md`, … (oito achados unificados por lote, com os achados
originais completos já separados por heurística; cada par achado unificado × heurística vira uma leitura). Dispare **um subagente `unificador` por lote, todos em paralelo, numa só mensagem**,
cada um com a delegação "Leia este arquivo inteiro e responda só com o JSON pedido nele: <caminho do
lote>". Grave cada retorno **na íntegra** em `redacao_lote_NN_bruto.md`, com o mesmo cabeçalho YAML do
passo 3 mais `lote: NN`. Depois:

```bash
py instrumento/analise/unificar_prompt.py validar-redacao --pasta "<pasta>"
```

Confere que todo par achado unificado × heurística recebeu uma leitura com os cinco campos, no tamanho
de um achado (mais de 1,5 vez o maior achado representado reprova), e grava as leituras dentro de
`unificacao_ia.json` (campo `leituras`), mais `redacao_conferencia.md`. Avisos (leitura um pouco maior
que o maior achado, travessão) não reprovam, mas vão ao relato. Se um par reprovar, reenvie **ao agente
do lote que contém aquele achado unificado** (confira o intervalo `U###` de cada lote antes de enviar)
só a linha de erro, pedindo o JSON com aquele par apenas, uma vez; grave o retorno em
`redacao_lote_NN_bruto_r2.md` (a rodada posterior substitui o par na conferência). `montar-redacao
--so-faltantes` remonta só o que ficou sem leitura. Um lote com a saída truncada (JSON que não fecha) é
sinal de lote grande demais: refaça esse lote com `--lote 4`.

## 5. Proveniência e fechamento

Grave `<pasta>/unificacao_proveniencia.json`:

```json
{"data":"<ISO-8601>","modelo":"claude-opus-5","nivel_raciocinio":"<confirmado>","versao_app":"<confirmada>",
 "semente":<n>,"achados":<n>,"achados_unificados":<n>,"agente":"unificador","rodadas":<n>,
 "leituras":{"total":<n>,"lotes":<n>,"tamanho_lote":8,"rodadas":<n>},
 "prompt":"prompt_unificacao.md","saida_bruta":"unificacao_ia_bruto.md","protocolo":"instrumento/protocolo/unificacao.md"}
```

Depois, e só se a validação passou, marque o passo 2.3 no artefato "Roteiro do estudo" (`ArtifactData`,
coleção `etapas`, documento `e2-3`, `{status:"feito", quando:"dd/mm/aaaa hh:mm", por:"Claude"}`).

Resumo no chat: achados, achados unificados, quantos têm um só achado, o maior, rodadas, e o caminho dos
quatro arquivos. **Não** liste o conteúdo dos achados unificados: a leitura deles é a revisão do Eduardo
(Fase 3), na página de `revisar.py`.

## Limites

- **A conta do agente é uma chamada só, com todos os achados no contexto**, e é assim de propósito:
  cada achado é comparado com todos os outros, lendo o texto original. Dividir em blocos faria a
  segunda etapa decidir sobre enunciados, que são texto derivado, e erro do primeiro estágio não teria
  como ser corrigido depois.
- O prompt cabe porque leva só três campos por achado (`unificacao.md`, "Preparação da entrada", item
  5). Com os nove campos do conjunto cego, os 476 achados da coleta real dariam 1,1 milhão de
  caracteres, cerca de 372 mil tokens, o que não caberia. O corte foi medido antes de ser adotado:
  amostra de 100 achados unificada duas vezes, com os nove campos e com os três, concordância de 0,999
  entre as partições e 44 dos 48 achados unificados idênticos.
- **Se a saída truncar duas vezes** — o `validar` reprova no parse nas duas rodadas —, pare e traga o
  relatório. O plano B decidido em 24/09/2026 é unificar **por execução**: um bloco para exec-1
  (A1, B1 e C1), um para exec-2, um para exec-3, e uma quarta chamada recebendo os achados unificados
  dos três blocos **embaralhados e sem rótulo de origem**. Cada bloco leva os três formatos, então a
  comparação entre formatos, que é a medição principal do estudo, continua sendo feita sobre o texto
  original; o que passa para a segunda etapa é a identificação entre execuções. **Nunca dividir por
  formato:** o corte coincidiria com a variável comparada e a fusão entre formatos passaria a ser
  decidida por um agente que enxerga a origem.
- O subagente tem a ferramenta de leitura porque o prompt não cabe na delegação. A instrução restringe a
  leitura ao arquivo do prompt; a pasta fechada fica fora do caminho por convenção de nome, não por
  bloqueio técnico. É garantia de instrução, e fica declarada como tal.
