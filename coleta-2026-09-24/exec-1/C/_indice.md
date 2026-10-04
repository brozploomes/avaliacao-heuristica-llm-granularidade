# Formato C — execucao 1 — indice da condicao

Achados: **26**. Objeto: `C:/Users/EduardoDamiao/Documents/MBA USPEsalq/objeto/tarefas_crm.html`.
Modo: chamada unica, as dez heuristicas expostas de uma vez. Avaliador unico, contexto isolado.

## Distribuicao por heuristica

| Heuristica | Achados |
| :--- | ---: |
| H01 — Visibilidade do status do sistema | 6 |
| H02 — Correspondência entre o sistema e o mundo real | 2 |
| H03 — Controle e liberdade do usuário | 2 |
| H04 — Consistência e padrões | 6 |
| H05 — Prevenção de erros | 3 |
| H06 — Reconhecer em vez de lembrar | 2 |
| H07 — Flexibilidade e eficiência de uso | 1 |
| H08 — Estética e design minimalista | 2 |
| H09 — Ajudar o usuário a reconhecer, diagnosticar e recuperar-se de erros | 1 |
| H10 — Ajuda e documentação | 1 |

## Distribuicao por severidade

| Nota | Rotulo | Achados |
| :--: | :--- | ---: |
| 1 | Cosmetico | 1 |
| 2 | Menor | 10 |
| 3 | Maior | 15 |

## Achados

| Id | Heuristica | Sev. | Localizacao | Arq. |
| :--- | :--- | :--: | :--- | ---: |
| [C-H1-001](H01/C-H1-001.achado.md) | H01 | 2 | Tela principal (agenda) — calendário lateral do painel esquerdo x cabeçalho do período, após acionar o botão Hoje | 2 |
| [C-H1-002](H01/C-H1-002.achado.md) | H01 | 3 | Visualização Calendário (modo Mês) — área da grade, após pesquisa "zzzzzzz" no campo Pesquisar tarefas (textbox uid 1_69) | 2 |
| [C-H1-003](H01/C-H1-003.achado.md) | H01 | 3 | Modal Nova tarefa — botão Criar (rodapé), e lista de tarefas logo após a criação | 3 |
| [C-H1-004](H01/C-H1-004.achado.md) | H01 | 2 | Modal de detalhes de uma tarefa já finalizada ("Avaliação de retorno comercial (revisada)") — cabeçalho e rodapé do modal | 2 |
| [C-H1-005](H01/C-H1-005.achado.md) | H01 | 3 | Barra superior — seletor de status (button "Status das tarefas", uid 1_71) com a opção Finalizadas selecionada, sobre a visualização Lista | 2 |
| [C-H1-006](H01/C-H1-006.achado.md) | H01 | 3 | Painel lateral recolhido (button "Expandir painel", uid 1_64) com filtros ativos — visualização Semana | 2 |
| [C-H2-001](H02/C-H2-001.achado.md) | H02 | 2 | Modal de detalhes de tarefa ("Reunião de descoberta — ABC PARARRAIOS") — título do modal e ícone de lápis no cabeçalho | 2 |
| [C-H2-002](H02/C-H2-002.achado.md) | H02 | 3 | Modal de detalhes de tarefa — rodapé, botão primário "Concluir" ao lado do botão "Fechar" | 2 |
| [C-H3-001](H03/C-H3-001.achado.md) | H03 | 3 | Visualização Lista — controle circular de conclusão da linha (radio "Concluir tarefa") e, em seguida, modal de detalhes da tarefa já finalizada | 4 |
| [C-H3-002](H03/C-H3-002.achado.md) | H03 | 3 | Visualização Calendário (modo Semana) — cartão de tarefa arrastado de quarta-feira 23 às 13:30 para sexta-feira 25 às 10:00 | 2 |
| [C-H4-001](H04/C-H4-001.achado.md) | H04 | 3 | Modal de detalhes em modo somente leitura — botões de remoção (×) dos chips de Cliente, Oportunidade, Usuários, Contatos e Marcadores | 2 |
| [C-H4-002](H04/C-H4-002.achado.md) | H04 | 1 | Painel lateral — lista suspensa do filtro Marcadores, item "No show" | 2 |
| [C-H4-003](H04/C-H4-003.achado.md) | H04 | 2 | Visualização Lista — última linha da tabela, após a criação de uma tarefa | 2 |
| [C-H4-004](H04/C-H4-004.achado.md) | H04 | 2 | Cartões da agenda e linhas da Lista — controle circular de conclusão da tarefa | 3 |
| [C-H4-005](H04/C-H4-005.achado.md) | H04 | 2 | Modal de tarefa ("Validação com decisores — alpha piscinas") — comportamento da tecla Esc | 2 |
| [C-H4-006](H04/C-H4-006.achado.md) | H04 | 3 | Coluna Contatos da visualização Lista x campo Contatos do modal de detalhes, para a mesma tarefa "Validação com decisores — alpha piscinas" | 3 |
| [C-H5-001](H05/C-H5-001.achado.md) | H05 | 2 | Modal de tarefa em modo de edição — botão Cancelar do rodapé | 3 |
| [C-H5-002](H05/C-H5-002.achado.md) | H05 | 3 | Modal de detalhes em modo somente leitura — botão × do chip de Cliente (button "Remover ABC PARARRAIOS") | 2 |
| [C-H5-003](H05/C-H5-003.achado.md) | H05 | 3 | Modal Nova tarefa — botão Criar acionado com o formulário inteiramente vazio; resultado na última linha da Lista | 2 |
| [C-H6-001](H06/C-H6-001.achado.md) | H06 | 3 | Modais Nova tarefa e Editar tarefa — seletores de unidade dos campos Duração e Repetir ("a cada") | 3 |
| [C-H6-002](H06/C-H6-002.achado.md) | H06 | 3 | Visualização Calendário (modo Semana) — cartões de tarefa, em especial os de 30 minutos e os sobrepostos de terça-feira 22 | 2 |
| [C-H7-001](H07/C-H7-001.achado.md) | H07 | 3 | Aplicação inteira — cartões da agenda, controles de navegação de período e de modo de visualização | 2 |
| [C-H8-001](H08/C-H8-001.achado.md) | H08 | 2 | Visualização Lista — colunas Título, Cliente e Contatos da tabela | 2 |
| [C-H8-002](H08/C-H8-002.achado.md) | H08 | 2 | Visualização Calendário (modo Semana) — rótulo de tipo em caixa alta dentro dos cartões de tarefa | 2 |
| [C-H9-001](H09/C-H9-001.achado.md) | H09 | 3 | Modal Editar tarefa ("Follow-up de negociação — Ambev") — campos Título e Duração e botão Salvar | 3 |
| [C-H10-001](H10/C-H10-001.achado.md) | H10 | 2 | Aplicação inteira — barra superior e painel lateral, controles representados apenas por ícone (recolher painel, busca avançada, alternância Calendário/Lista, Anterior/Próximo, lápis de edição) e ausência de qualquer ponto de ajuda | 2 |
