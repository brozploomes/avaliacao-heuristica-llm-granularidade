# Métricas (`protocolo/analise.md` §5)

Conjunto agregado |D| = **83** defeitos, de 93 achados unificados (10 falsos positivos). Recortes: A/1, A/2, A/3, B/1, B/2, B/3, C/1, C/2, C/3. Desvio-padrão amostral (n − 1).

## Conferências

| Execução | Achados na trilha | Encerramento − fora do escopo | Bate |
|---|---:|---:|---:|
| A/1 | 76 | 76 | sim |
| A/2 | 77 | 77 | sim |
| A/3 | 74 | 74 | sim |
| B/1 | 48 | 48 | sim |
| B/2 | 58 | 58 | sim |
| B/3 | 53 | 53 | sim |
| C/1 | 26 | 26 | sim |
| C/2 | 37 | 37 | sim |
| C/3 | 27 | 27 | sim |

## Volume (unidades: achados e defeitos)

| Execução | Achados A(F,e) | Achados unificados | Defeitos D(F,e) | Falsos positivos | Nota 0 | Fora do escopo |
|---|---:|---:|---:|---:|---:|---:|
| A/1 | 76 | 61 | 55 | 6 | 0 | 0 |
| A/2 | 77 | 57 | 53 | 4 | 0 | 0 |
| A/3 | 74 | 59 | 55 | 4 | 0 | 0 |
| B/1 | 48 | 36 | 35 | 1 | 0 | 0 |
| B/2 | 58 | 41 | 39 | 2 | 0 | 0 |
| B/3 | 53 | 43 | 37 | 6 | 0 | 0 |
| C/1 | 26 | 23 | 22 | 1 | 0 | 0 |
| C/2 | 37 | 31 | 30 | 1 | 0 | 0 |
| C/3 | 27 | 20 | 17 | 3 | 0 | 0 |

| Formato | Achados A(F) | média ± DP | Defeitos D(F) | média ± DP | Nota 0 | Fora do escopo |
|---|---:|---:|---:|---:|---:|---:|
| A | 227 | 75,7 ± 1,5 | 70 | 54,3 ± 1,2 | 0 | 0 |
| B | 159 | 53,0 ± 5,0 | 54 | 37,0 ± 2,0 | 0 | 0 |
| C | 90 | 30,0 ± 6,1 | 40 | 23,0 ± 6,6 | 0 | 0 |

## Precisão, recall e F1 (denominador do recall: |D| = 83)

| Execução | Precisão por defeito | Precisão por achado | Taxa FP (defeito) | Taxa FP (achado) | Recall | F1 |
|---|---:|---:|---:|---:|---:|---:|
| A/1 | 90,2% | 90,8% | 9,8% | 9,2% | 66,3% | 0,764 |
| A/2 | 93,0% | 94,8% | 7,0% | 5,2% | 63,9% | 0,757 |
| A/3 | 93,2% | 94,6% | 6,8% | 5,4% | 66,3% | 0,775 |
| B/1 | 97,2% | 95,8% | 2,8% | 4,2% | 42,2% | 0,588 |
| B/2 | 95,1% | 94,8% | 4,9% | 5,2% | 47,0% | 0,629 |
| B/3 | 86,0% | 86,8% | 14,0% | 13,2% | 44,6% | 0,587 |
| C/1 | 95,7% | 92,3% | 4,3% | 7,7% | 26,5% | 0,415 |
| C/2 | 96,8% | 97,3% | 3,2% | 2,7% | 36,1% | 0,526 |
| C/3 | 85,0% | 85,2% | 15,0% | 14,8% | 20,5% | 0,330 |

| Formato | Precisão por defeito (união) | média ± DP | Precisão por achado (união) | Recall (união) | Recall média ± DP | F1 (união) |
|---|---:|---:|---:|---:|---:|---:|
| A | 89,7% | 92,1% ± 0,017 | 93,4% | 84,3% | 65,5% ± 0,014 | 0,870 |
| B | 88,5% | 92,8% ± 0,059 | 92,5% | 65,1% | 44,6% ± 0,024 | 0,750 |
| C | 93,0% | 92,5% ± 0,065 | 92,2% | 48,2% | 27,7% ± 0,079 | 0,635 |

## Consistência entre execuções: D(F,e) ∩ D(F,1) ÷ D(F,1)

| Formato | e = 2 | e = 3 | média | DP | tamanho de D(F,1) |
|---|---:|---:|---:|---:|---:|
| A | 81,8% | 80,0% | 80,9% | 0,013 | 55 |
| B | 65,7% | 80,0% | 72,9% | 0,101 | 35 |
| C | 72,7% | 54,5% | 63,6% | 0,129 | 22 |

## Duplicação (excedentes de um mesmo defeito na mesma execução; taxas ÷ A(F,e))

| Execução | Atribuição múltipla | Intrínseca | Recorrência ou intrínseca (indeterminada) | Ampla | Taxa ampla |
|---|---:|---:|---:|---:|---:|
| A/1 | 13 | 0 | 1 | 14 | 18,4% |
| A/2 | 20 | 0 | 0 | 20 | 26,0% |
| A/3 | 12 | 0 | 3 | 15 | 20,3% |
| B/1 | 10 | 0 | 1 | 11 | 22,9% |
| B/2 | 15 | 0 | 1 | 16 | 27,6% |
| B/3 | 9 | 0 | 0 | 9 | 17,0% |
| C/1 | 2 | 0 | 0 | 2 | 7,7% |
| C/2 | 5 | 0 | 1 | 6 | 16,2% |
| C/3 | 6 | 0 | 0 | 6 | 22,2% |

Os pontos de manifestação são os da IA, por achado unificado; quando o defeito tem mais de um ponto, recorrência e intrínseca não se separam.

## Atribuição heurística

| Formato | Defeitos de D(F) com ≥ 2 heurísticas | Índice de atribuição múltipla | Heurísticas por defeito (média) |
|---|---:|---:|---:|
| A | 19 | 27,1% | 1,41 |
| B | 18 | 33,3% | 1,48 |
| C | 9 | 22,5% | 1,25 |

| Heurística | A achados | B achados | C achados | A defeitos | B defeitos | C defeitos |
|---|---:|---:|---:|---:|---:|---:|
| H1 | 29 | 20 | 23 | 13 | 14 | 12 |
| H2 | 23 | 13 | 6 | 11 | 6 | 3 |
| H3 | 16 | 12 | 6 | 7 | 6 | 4 |
| H4 | 42 | 29 | 18 | 22 | 15 | 14 |
| H5 | 23 | 21 | 12 | 9 | 8 | 5 |
| H6 | 19 | 24 | 9 | 8 | 12 | 4 |
| H7 | 20 | 18 | 3 | 8 | 8 | 1 |
| H8 | 21 | 7 | 5 | 6 | 3 | 3 |
| H9 | 19 | 6 | 5 | 7 | 4 | 3 |
| H10 | 15 | 9 | 3 | 8 | 4 | 1 |

## Sobreposição entre formatos

| Formato | Defeitos exclusivos |
|---|---:|
| A | 22 |
| B | 8 |
| C | 3 |

| Par | Interseção | União | Jaccard |
|---|---:|---:|---:|
| A∩B | 44 | 80 | 0,550 |
| A∩C | 35 | 75 | 0,467 |
| B∩C | 33 | 61 | 0,541 |

Defeitos comuns a todos os formatos: **31**.

## Severidade

| Formato | nota 0 | nota 1 | nota 2 | nota 3 | nota 4 | Consistência entre execuções (defeitos em ≥ 2 exec.) | Concordância exata IA × pesquisador | Kappa linear |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| A | 0 | 18 | 107 | 98 | 4 | 34 de 54 (63,0%) | 68,6% | 0,560 |
| B | 0 | 4 | 67 | 87 | 1 | 20 de 37 (54,1%) | 53,7% | 0,236 |
| C | 0 | 3 | 35 | 52 | 0 | 12 de 17 (70,6%) | 60,0% | 0,416 |

Agregado (moda da severidade_ia por defeito × severidade_pesquisador, 83 defeitos): concordância exata 67,5%, kappa linear 0,550. Distribuição de severidade_pesquisador: {'4': 6, '2': 35, '3': 33, '1': 9}.

## Custo e eficiência

| Execução | Modo | Concorrência observada | Tokens | Usos de ferramenta | Soma das chamadas (min) | Chamada mais longa (min) | Parede (min) | Defeitos por hora | Defeitos por mil tokens |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| A/1 | paralela | paralela | 1.547.912 | 1.232 | 158,6 | 21,1 | 26,4 | 20,8 | 0,036 |
| A/2 | paralela | paralela | 1.760.238 | 1.516 | 262,3 | 50,2 | 57,7 | 12,1 | 0,030 |
| A/3 | paralela | paralela | 1.789.096 | 1.496 | 173,6 | 28,6 | 37,5 | 19,0 | 0,031 |
| B/1 | paralela | paralela | 923.218 | 824 | 81,5 | 27,8 | 32,0 | 25,8 | 0,038 |
| B/2 | paralela | paralela | 1.098.989 | 1.016 | 178,0 | 60,8 | 66,4 | 13,1 | 0,035 |
| B/3 | paralela | paralela | 826.331 | 764 | 100,6 | 28,8 | 34,5 | 22,1 | 0,045 |
| C/1 | chamada_unica | nao_aplicavel | 288.597 | 268 | 31,7 | 31,7 | 37,5 | 41,6 | 0,076 |
| C/2 | chamada_unica | nao_aplicavel | 395.019 | 410 | 50,6 | 50,6 | 54,9 | 35,6 | 0,076 |
| C/3 | chamada_unica | nao_aplicavel | 331.333 | 323 | 43,0 | 43,0 | 46,2 | 23,7 | 0,051 |

| Formato | Tokens (soma) | Tokens por execução (média ± DP) | Defeitos por hora (média) | Defeitos por mil tokens (média ± DP) |
|---|---:|---:|---:|---:|
| A | 5.097.246 | 1.699.082 ± 131.710 | 17,3 | 0,032 ± 0,003 |
| B | 2.848.538 | 949.513 ± 138.218 | 20,3 | 0,039 ± 0,005 |
| C | 1.014.949 | 338.316 ± 53.554 | 33,6 | 0,068 ± 0,014 |

Tempo de parede só é comparável entre formatos com a ressalva de `modo_execucao` e `concorrencia_observada`; defeitos por hora usa a soma das durações das chamadas (descritiva, porque em A e B cada chamada sofre contenção).

## Contagens à parte

| Formato | Achados fora do escopo | Candidatos com nota 0 (dentro de A) |
|---|---:|---:|
| A | 0 | 0 |
| B | 0 | 0 |
| C | 0 | 0 |

