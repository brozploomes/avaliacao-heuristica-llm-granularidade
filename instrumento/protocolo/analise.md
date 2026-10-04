# Protocolo de análise — unidades, operações, trilha e métricas

> **Para que serve.** Define o que a análise faz com os achados das nove execuções, em que unidade cada
> número é contado, como as decisões ficam auditáveis e como cada métrica é calculada. É o documento que
> a Metodologia do TCC cita, e acompanha o material suplementar entregue à banca. A coleta está no
> `README.md`; o prompt da unificação, em `unificacao.md`; a execução passo a passo, em
> `roteiro_estudo.md`.

## 1. Unidades e glossário

| Termo | Definição | Equivalente na literatura |
|---|---|---|
| **Achado** | Item individual produzido pelo avaliador na coleta, vinculado a exatamente uma heurística | *discrepancy* (Campos et al., 2025) |
| **Achado unificado** | Conjunto de achados que a IA unificou como o mesmo problema da interface; unidade da classificação pelo pesquisador | estágio próprio deste desenho |
| **Defeito** | Achado unificado classificado pelo pesquisador como problema real | *unique defect* (Campos et al., 2025); *unique issue* (Zhong et al., 2025) |
| **Falso positivo** | Achado unificado classificado pelo pesquisador como problema que não se verifica no objeto; todos os seus achados são falsos positivos | Campos et al. (2025); Guerino et al. (2026) |
| **Duplicata** | Achado excedente, além do primeiro, de um mesmo defeito **dentro da mesma execução** | Campos, Guerino, Zhong |
| **Defeito exclusivo** | Defeito encontrado por um único formato | Campos et al. (2025) |
| **Conjunto agregado** | Todos os defeitos das nove execuções; denominador de cobertura e de *recall* | *master set* (Zhong et al., 2025) |
| **Unificação** | A operação, feita pela IA sob cegamento, que transforma achados em achados unificados | — |
| **Revisão** | A sequência da seção 2: unificação cega pela IA, depois classificação e severidade pelo pesquisador, que atua como **revisor único** | — |
| **Ponto de manifestação** | Cada tela ou estado em que um defeito aparece; atributo do defeito, registrado pela IA na unificação | — |

Regras de uso:

- **Achado** e **defeito** são as duas unidades de contagem, e toda métrica declara qual usa.
- A **heurística é atributo do defeito**: pode ser múltipla e nunca separa defeitos (Nielsen, 1994;
  Guerino et al., 2026). Três achados de heurísticas diferentes sobre o mesmo problema são um defeito
  com três heurísticas.
- **Recorrência** do mesmo defeito em telas ou estados diferentes é ponto de manifestação, não defeito
  novo. Elementos distintos com a mesma causa são defeitos distintos.
- **Severidade** nunca é critério de unificação nem de falso positivo.
- Termos que **não** se usam: "agrupamento" e "agrupar" para a unificação, e "grupo" para achado
  unificado ("grupo" é só dos grupos de heurísticas do Formato B, G1 a G4); "defeito único" ou "defeito
  distinto" (todo defeito já é único por construção); "achados distintos"; "registro" como sinônimo de
  achado; "deduplicação"; "master set"; "razão de expansão"; "fator de atribuição múltipla";
  "efetividade" (tem dois sentidos na literatura citada); "thoroughness"; e "recall" sem denominador
  declarado.

## 2. Ordem das operações

Esta sequência é a **revisão** a que a Metodologia do TCC se refere, feita uma vez, completa e cega,
sobre as nove execuções.

1. **Reunião.** Todos os achados dos nove JSONL, com metadados (`formato`, `execucao`, `chamada`, derivada
   do `id`, e o próprio `id`). Ficam **fora** de `|A(F,e)|` e da revisão, contados à parte por formato, os
   achados com `fora_do_escopo = true` (heurística fora da chamada, marcados pelo orquestrador no
   fechamento), porque pertencem a outra chamada e misturariam a manipulação. Achados com `severidade = 0`
   **entram** em `|A(F,e)|` e na revisão como qualquer outro: são candidatos que o avaliador registrou e não
   julgou violação, e quem decide se é defeito ou falso positivo é o pesquisador, não a nota do avaliador.
2. **Unificação única, global e cega, pela IA.** Um só passe sobre todos os achados, embaralhados com
   semente fixa e sob chave substituta `K###`, sem formato, execução nem `id`. A IA reúne os achados que
   descrevem o mesmo problema, dentro e entre heurísticas, pela régua declarada em `unificacao.md`
   (enunciado, elemento, correção), e devolve para cada achado unificado o enunciado, o elemento da
   interface, os pontos de manifestação e a justificativa. **Essa saída, conferida por script, é a lista
   de achados unificados do estudo**: o pesquisador não revisa fusões nem separações. Não há unificação em
   cascata por execução ou por formato: uma régua só, aplicada uma vez, para que a mesma decisão valha
   para todo mundo. Em seguida, em lotes e sob o mesmo cegamento, a IA escreve **leituras**: para cada
   heurística presente num achado unificado, uma redação dos achados daquela heurística com os cinco
   campos e o tamanho de um achado (localização, descrição da falha, justificativa da violação, registro
   visual, sugestão de correção). A separação por heurística é mecânica, pelo campo do avaliador; a
   leitura não é resumo nem soma, e sim um achado escrito de novo que representa fielmente os achados
   daquela heurística (`unificacao.md`). São as leituras, com as capturas dos achados reunidos, que o
   pesquisador lê; os textos originais ficam disponíveis, recolhidos.
3. **Classificação pelo pesquisador, por achado unificado.** Cada achado unificado é **defeito** ou
   **falso positivo**, pelo critério a priori da seção 3. A classificação é feita sob a chave
   substituta, sem ver formato, execução nem a severidade atribuída pelo avaliador.
4. **Severidade do pesquisador, por defeito.** Nota 1 a 4 na rubrica do núcleo (frequência, impacto,
   persistência), atribuída ao defeito, sem ver a nota do avaliador. Falso positivo não recebe nota. A
   `severidade` de cada achado no JSONL permanece intacta e passa a chamar-se `severidade_ia` na análise.
5. **Reatação.** Só agora o mapa `chave → id` é aberto e cada achado recebe de volta o id, o formato, a
   execução, a chamada e a `severidade_ia`. As decisões do pesquisador e a saída da IA se juntam a esses
   metadados na trilha de decisões (seção 4).
6. **Métricas por recorte** (seção 5). Nada é recalculado por nível: os quatro níveis (chamada,
   execução, formato, agregado) são recortes da mesma lista de achados unificados pelos metadados.

## 3. Critério a priori de falso positivo

Um achado unificado é **falso positivo** quando o problema que descreve **não se verifica no objeto**: o
comportamento ou a aparência descritos não ocorrem, ou a descrição não localiza nada que se possa
conferir (Campos et al., 2025; Guerino et al., 2026). O pesquisador confere contra as capturas e o
snapshot de acessibilidade dos achados reunidos e, se preciso, contra o próprio objeto.

Duas ressalvas. Um achado unificado que descreve um problema real, mas cujos achados atribuem heurística
discutível, **não** é falso positivo: a heurística é atributo. Um achado unificado cuja severidade parece
exagerada **não** é falso positivo: a severidade é julgada em separado (passo 4).

## 4. Trilha de decisões

Um CSV, `trilha_decisoes.csv`, com `;` como separador, **campos livres entre aspas duplas** (aspas
internas duplicadas), uma linha por achado, todas com o mesmo número de colunas, nesta ordem:

```
chave; id; formato; execucao; chamada; heuristica; severidade_ia;
achado_unificado; classificacao; severidade_pesquisador; elemento; pontos_manifestacao; observacao
```

| Coluna | Domínio | Origem |
|---|---|---|
| `chave` | chave substituta usada na revisão (`K###`) | reunião |
| `id`, `formato`, `execucao`, `chamada`, `heuristica`, `severidade_ia` | metadados do achado; `severidade_ia` é o campo `severidade` do JSONL; `chamada` deriva do `id`: `H<k>` em A, `G<n>` em B, `unica` em C | reatação |
| `achado_unificado` | identificador do achado unificado (`U###`) | IA |
| `classificacao` | `defeito` \| `falso_positivo`; a mesma para todos os achados do achado unificado | pesquisador |
| `severidade_pesquisador` | 1 a 4, por defeito; vazio em falso positivo | pesquisador |
| `elemento` | elemento ou região da interface que sustenta o achado unificado; é a âncora do defeito | IA |
| `pontos_manifestacao` | telas ou estados em que o defeito aparece, separados por `\|` | IA |
| `observacao` | texto livre do pesquisador, opcional | pesquisador |

Acompanham o CSV, como arquivos separados: a **semente** do embaralhamento, o **mapa de chaves**
(`chave → id`), as **saídas brutas** da unificação e da redação unificada (esta em lotes), e o arquivo
de **decisões** gravado pela página de revisão. Juntos, permitem refazer cada passo da revisão a partir dos JSONL.

## 5. Métricas e fórmulas

Notação: para o formato *F* e a execução *e*, `A(F,e)` é o conjunto de achados de (F,e); `D(F,e)` é o
conjunto de defeitos com pelo menos um achado de (F,e); `D(F)` é a união de `D(F,e)` nas três
execuções; `D` é o **conjunto agregado**, união de todos. Média e desvio-padrão entre execuções são
sobre três valores, com desvio-padrão amostral (n − 1).

### Volume
- **Achados**: `|A(F,e)|` por execução, e média e desvio-padrão sobre as três; `|A(F)|` por formato.
- **Defeitos**: `|D(F,e)|` por execução, média e desvio-padrão; `|D(F)|` por formato.
- As duas contagens são sempre reportadas lado a lado, com a unidade declarada.
- **Fora da contagem**: achados com `fora_do_escopo = true`, por formato, reportados ao lado.
  **Candidatos descartados pelo avaliador**: contagem de achados com `severidade_ia = 0`, por formato, que
  continuam dentro de `|A(F,e)|`.

### Precisão, *recall* e F1 (denominador: conjunto agregado)
- **Precisão por defeito** (principal): fração dos achados unificados de (F,e) classificados como
  defeito, `|D(F,e)| ÷ |achados unificados com pelo menos um achado de (F,e)|`. F1 é calculado sobre ela.
- **Precisão por achado** (comparável a Campos): `|achados de (F,e) em defeitos| ÷ |A(F,e)|`.
- **Taxa de falso positivo** = 1 − precisão, nas duas leituras.
- ***Recall*** de (F,e): `|D(F,e)| ÷ |D|`. ***Recall* do formato**: `|D(F)| ÷ |D|`. O denominador é o
  conjunto agregado do estudo, como em Campos et al. (2025); nunca é apresentado como proporção dos
  problemas que existem no objeto.
- **F1**: média harmônica de precisão por defeito e *recall*, por (F,e) e por F.

### Cobertura e consistência
- **Cobertura** é o *recall* acima, reportada por execução (três valores, média, desvio-padrão) e pela
  união do formato.
- **Consistência entre execuções** (Zhong et al., 2025): para cada F, `|D(F,e) ∩ D(F,1)| ÷ |D(F,1)|`
  para e = 2 e e = 3; média e desvio-padrão. Mede quanto da primeira execução as seguintes reencontram.

### Duplicação (achados excedentes de um mesmo defeito, dentro da mesma execução)
Para cada defeito d e cada (F,e), o **achado de referência** é o primeiro achado de (F,e) em d, na ordem
do `id`; os demais são **excedentes**. Cada excedente recebe uma causa, nesta ordem de precedência:
- **Por atribuição múltipla**: a heurística do excedente difere da do achado de referência.
- **Por recorrência**: mesma heurística, mas ponto de manifestação (tela ou estado) diferente.
- **Intrínseca**: mesma heurística e mesmo ponto de manifestação; o modelo registrou o mesmo problema
  duas vezes no mesmo lugar, contra a instrução do núcleo.
- **Ampla**: a soma das três; é o número comparável ao de Campos et al. (2025) e Guerino et al. (2026).

Os pontos de manifestação são os que a IA registrou por achado unificado, não por achado. Quando o
defeito tem um só ponto, todo excedente de mesma heurística é intrínseco; quando tem mais de um,
recorrência e intrínseca não se separam e são reportadas juntas, como **indeterminadas**. Taxas:
excedentes de cada causa ÷ `|A(F,e)|`. Achados do mesmo defeito em **execuções diferentes** não são
duplicação: são consistência. Em **formatos diferentes**, são sobreposição.

### Atribuição heurística
- **Índice de atribuição múltipla** de F: proporção dos defeitos de `D(F)` a que **F** atribuiu duas ou
  mais heurísticas, contando só as heurísticas dos achados de F; e a média de heurísticas por defeito.
  Comparável a Guerino et al. (2026).
- **Distribuição por heurística**: achados e defeitos por heurística, por F.

### Sobreposição entre formatos
- **Defeitos exclusivos** de F: os de `D(F)` que não estão em nenhum outro `D(G)`.
- **Sobreposição** por par: defeitos em comum por par, `|D(F) ∩ D(G)|`, e defeitos comuns aos três
  formatos.

### Severidade
- Distribuição de `severidade_ia` por F.
- **Consistência de severidade**: para defeitos com achados em mais de uma execução do mesmo F, se a
  moda da `severidade_ia` por execução coincide entre as execuções.
- **Concordância IA × pesquisador**: por defeito, a moda da `severidade_ia` dos seus achados (empate
  resolvido pelo menor valor) contra a `severidade_pesquisador`; proporção de coincidência exata,
  proporção de defeitos com notas a até um nível de distância e direção da discordância (pesquisador
  acima e abaixo).

### Custo
- **Tokens** e **tempo** por chamada e por (F,e), do registro de encerramento. Tempo de parede só é
  comparável entre formatos com a ressalva de `modo_execucao` e `concorrencia_observada`; tokens e usos
  de ferramenta não sofrem esse efeito.
- **Eficiência** (Campos et al., 2025): `|D(F,e)| ÷ (duracao_ms_soma ÷ 3.600.000)`, defeitos por hora de
  trabalho dos avaliadores, somadas as chamadas, o que independe de terem rodado em paralelo ou em fila;
  é descritiva, porque em A e B cada chamada sofre contenção. A extensão comparável entre formatos é
  `|D(F,e)| ÷ (tokens_total ÷ 1.000)`.

## 6. O que a análise não pode afirmar

- **Quanto escapou aos três formatos.** O conjunto agregado é feito do que eles encontraram; um defeito
  que nenhum formato registrou não existe na análise. Não há estimativa de completude.
- **Que a unificação é a única possível.** A unificação é decisão do modelo, com a régua declarada em
  `unificacao.md`; a análise mede os formatos com essa régua, e outra régua daria outras contagens de
  defeitos e outra sobreposição entre formatos. O que se garante é que a mesma régua valeu para todos os
  achados, sem que o modelo soubesse de onde cada um veio.
- **Que um formato é melhor.** Com três execuções e um objeto, os números descrevem o comportamento
  observado; não sustentam inferência estatística.
- **Que o exemplo de referência ajuda ou atrapalha.** A linha de exemplo integrou o bloco de cada
  heurística em todas as condições. Não há comparação com e sem exemplo, e nada se afirma sobre o
  efeito da sua presença.
- **Se cada frase de cada achado é verdadeira.** A revisão julga o problema, por achado unificado, não a
  fidelidade de cada afirmação do texto; uma afirmação falsa dentro de um defeito real não é medida.
- **Que as leituras são neutras.** O pesquisador decide sobre textos escritos pela IA a partir dos
  achados reunidos, com as capturas originais ao lado e os textos originais disponíveis; uma leitura que
  distorcesse os achados distorceria a decisão. O procedimento declara isso e mantém os originais à mão.

## 7. Referências usadas neste protocolo

Campos et al. (2025); Guerino et al. (2026); Zhong et al. (2025); Nielsen (1994); Chattratichart e
Lindgaard (2008). As entradas completas estão nas Referências do TCC.
