# Licenças

Este repositório usa duas licenças, conforme a natureza de cada arquivo, e contém conteúdo de terceiros
que nenhuma delas cobre.

| Conteúdo | Licença |
|---|---|
| Textos e dados: `README.md`, protocolos, núcleo heurístico (exceto a seção 3), material de contexto, skills, definições de subagentes, arquivos de configuração, caracterização, coleta (JSONL, capturas, instantâneos da árvore de acessibilidade, `.achado.md`, `_indice.md`) e arquivos de `analise-2026-09-24/` | [CC BY 4.0](#cc-by-40) |
| Código: `instrumento/analise/*.py`, `instrumento/.claude/gerar_avaliadores.mjs` e o objeto `objeto/tarefas_crm.html` | [MIT](#mit) |

Para atribuir, use a referência da seção "Como citar" do `README.md`.

## Conteúdo de terceiros

**Seção 3 de `instrumento/protocolo/nucleo_heuristico.md`.** As definições, os textos de "por que
importa", as dicas e os exemplos de referência das dez heurísticas são tradução e adaptação de textos da
Nielsen Norman Group, que detém os direitos sobre eles:

- Nielsen, J. 2024. 10 usability heuristics for user interface design.
  <https://www.nngroup.com/articles/ten-usability-heuristics/>
- Neusesser, T.; Sunwall, E. 2023. Error-message guidelines.
  <https://www.nngroup.com/articles/error-message-guidelines/>
- Kendrick, A. 2020. Help and documentation: usability heuristic #10.
  <https://www.nngroup.com/articles/help-and-documentation/>

O trecho está reproduzido na íntegra porque é o texto que os subagentes avaliadores receberam, e sem ele
a coleta não pode ser reproduzida. Ele fica fora da CC BY 4.0 deste repositório; para outro uso, consulte
os originais.

**Bibliotecas embutidas no objeto.** `objeto/tarefas_crm.html` inclui código de React (licença MIT,
Copyright (c) Facebook, Inc. and its affiliates) e de lucide-react v1.17.0 (licença ISC). Os avisos de
licença dessas bibliotecas estão preservados dentro do próprio arquivo, e essas partes seguem as licenças
delas.

## CC BY 4.0

Licença Creative Commons Atribuição 4.0 Internacional.
Resumo: <https://creativecommons.org/licenses/by/4.0/> ·
texto legal: <https://creativecommons.org/licenses/by/4.0/legalcode>

## MIT

```
MIT License

Copyright (c) 2026 Eduardo T. Damião

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
