# Evidências — Formato C, execução 2

Condição C (dez heurísticas em chamada única), objeto `tarefas_crm.html`, 37 achados.

## Distribuição por heurística

| Heurística | Achados |
| :--- | ---: |
| H1 | 11 |
| H2 | 2 |
| H3 | 2 |
| H4 | 7 |
| H5 | 6 |
| H6 | 4 |
| H7 | 1 |
| H8 | 1 |
| H9 | 2 |
| H10 | 1 |
| **Total** | **37** |

## Distribuição por severidade

| Severidade | Rótulo | Achados |
| :--: | :--- | ---: |
| 1 | Cosmetico | 1 |
| 2 | Menor | 11 |
| 3 | Maior | 25 |
| | **Total** | **37** |

## Achados

| id | Heurística | Sev. | Localização | Arquivos |
| :--- | :--- | :--: | :--- | ---: |
| `C-H1-001` | H1 — Visibilidade do status do sistema | 2 | Barra superior, botão "Hoje" + calendário lateral (cabeçalho "Outubro 2026") | 2 |
| `C-H1-002` | H1 — Visibilidade do status do sistema | 3 | Visualização em Lista com modo "Dia" — cabeçalho de período + linhas da coluna "Quando" | 3 |
| `C-H1-003` | H1 — Visibilidade do status do sistema | 3 | Visualização em Calendário (Dia, Semana e Mês) — área da grade, após pesquisa sem resultados | 2 |
| `C-H1-004` | H1 — Visibilidade do status do sistema | 3 | Campo "Pesquisar tarefas…" + visualização em Lista — mensagem "Nenhuma tarefa encontrada." | 2 |
| `C-H4-001` | H4 — Consistência e padrões | 2 | Alternância Calendário / Lista (botões uid 1_73 e 1_74) — estado de resultado vazio | 3 |
| `C-H2-001` | H2 — Correspondência entre o sistema e o mundo real | 3 | Diálogo de detalhes da tarefa — título "Editar tarefa" (uid 12_51) com todos os campos desabilitados | 2 |
| `C-H6-001` | H6 — Reconhecer em vez de lembrar | 3 | Diálogo de tarefa (leitura e edição) — campos "Duração" e "Repetir a cada" | 3 |
| `C-H2-002` | H2 — Correspondência entre o sistema e o mundo real | 3 | Diálogo de detalhes da tarefa — botão primário "Concluir" (uid 12_110), ao lado de "Fechar" (uid 12_109) | 3 |
| `C-H5-001` | H5 — Prevenção de erros | 3 | Diálogo de detalhes (modo somente leitura) — botões "×" dos chips de Cliente, Oportunidade, Usuários, Contatos e Marcadores | 3 |
| `C-H4-002` | H4 — Consistência e padrões | 2 | Barra de pesquisa e filtros — botão "Limpar" (× do campo, uid 19_0), "Limpar tudo" (uid 19_4) e "Redefinir" (uid 18_10/20_10) no painel de Busca avançada | 2 |
| `C-H6-002` | H6 — Reconhecer em vez de lembrar | 3 | Painel de Busca avançada, reaberto com um filtro já aplicado | 2 |
| `C-H5-002` | H5 — Prevenção de erros | 3 | Painel de Busca avançada — botão "Pesquisar" e barra "Filtros:" | 3 |
| `C-H1-005` | H1 — Visibilidade do status do sistema | 3 | Painel lateral — filtros "Exibir tarefas de…" (uid 1_59) e "Marcadores" (uid 1_61) | 4 |
| `C-H1-006` | H1 — Visibilidade do status do sistema | 3 | Botão "Recolher painel" (uid 1_64) com filtros de Marcador e Tipo aplicados | 2 |
| `C-H6-003` | H6 — Reconhecer em vez de lembrar | 3 | Tela com painel lateral recolhido — barra superior sem qualquer representação dos filtros ativos | 2 |
| `C-H1-007` | H1 — Visibilidade do status do sistema | 2 | Calendário lateral (pontos indicadores de tarefa nos dias) com o filtro de status em "Finalizadas" | 2 |
| `C-H5-003` | H5 — Prevenção de erros | 3 | Diálogo "Nova tarefa" — botão "Criar" (uid 34_45) com o formulário em branco | 2 |
| `C-H1-008` | H1 — Visibilidade do status do sistema | 2 | Diálogo "Nova tarefa" / "Editar tarefa" — retorno após "Criar" e após "Salvar" | 2 |
| `C-H3-001` | H3 — Controle e liberdade do usuário | 3 | Diálogo de tarefa em modo de edição — rodapé com apenas "Cancelar" e "Salvar"; ausência de comando de exclusão em toda a interface | 2 |
| `C-H4-003` | H4 — Consistência e padrões | 2 | Diálogos modais ("Nova tarefa", "Editar tarefa") e listas suspensas ("Exibir tarefas de…", "Marcadores") — tecla Esc | 2 |
| `C-H4-004` | H4 — Consistência e padrões | 2 | Cartão de tarefa na agenda e linha da Lista — controle de conclusão | 3 |
| `C-H1-009` | H1 — Visibilidade do status do sistema | 3 | Visualização em Mês — controle de conclusão no cartão da tarefa | 4 |
| `C-H5-004` | H5 — Prevenção de erros | 3 | Diálogo de detalhes da tarefa — botão "Concluir" | 3 |
| `C-H3-002` | H3 — Controle e liberdade do usuário | 3 | Diálogo de uma tarefa já concluída — rodapé com apenas "Fechar"; cartão com controle "Concluída" desabilitado | 2 |
| `C-H1-010` | H1 — Visibilidade do status do sistema | 2 | Diálogo de detalhes de uma tarefa concluída — cabeçalho e corpo do modal | 2 |
| `C-H4-005` | H4 — Consistência e padrões | 3 | Controle de conclusão do cartão de tarefa — comportamento em Semana versus Mês | 3 |
| `C-H6-004` | H6 — Reconhecer em vez de lembrar | 2 | Visualização em Semana — cartões de tarefas de 30 minutos e truncamento do título | 3 |
| `C-H7-001` | H7 — Flexibilidade e eficiência de uso | 3 | Tela inteira — ausência de atalhos de teclado e de acesso por teclado aos cartões de tarefa | 2 |
| `C-H4-006` | H4 — Consistência e padrões | 3 | Grade da agenda (Dia, Semana, Mês) — cartão de tarefa como elemento clicável | 2 |
| `C-H10-001` | H10 — Ajuda e documentação | 2 | Produto inteiro — nenhuma entrada de ajuda em nenhuma tela | 2 |
| `C-H8-001` | H8 — Estética e design minimalista | 2 | Diálogo de detalhes da tarefa (modo somente leitura) — corpo do modal | 2 |
| `C-H9-001` | H9 — Ajudar o usuário a reconhecer, diagnosticar e recuperar-se de erros | 3 | Faixa de erro "Falha ao carregar" acima da lista de tarefas | 2 |
| `C-H1-011` | H1 — Visibilidade do status do sistema | 3 | Barra superior (rótulo de período) e tabela da Lista durante a falha de carregamento | 2 |
| `C-H9-002` | H9 — Ajudar o usuário a reconhecer, diagnosticar e recuperar-se de erros | 3 | Visualização em Semana — controle de conclusão do cartão "Envio de proposta comercial — aline utiel" (uid 57_113); diálogo nativo do navegador | 2 |
| `C-H5-005` | H5 — Prevenção de erros | 3 | Diálogo de detalhes durante o carregamento — botão "Concluir" habilitado sobre um corpo ainda vazio | 2 |
| `C-H4-007` | H4 — Consistência e padrões | 1 | Barra superior — rótulo de período nas visualizações Semana, Mês e Dia; régua de horas da grade | 4 |
| `C-H5-006` | H5 — Prevenção de erros | 3 | Diálogo "Nova tarefa" — fechamento por clique fora do modal (fundo escurecido) | 3 |
