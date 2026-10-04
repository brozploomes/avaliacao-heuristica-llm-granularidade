# Evidências — Formato A, execução 1

76 achados, em 10 heurísticas.

## Distribuição por chamada

| Chamada | Achados |
| :-- | --: |
| H1 | 8 |
| H2 | 9 |
| H3 | 5 |
| H4 | 12 |
| H5 | 8 |
| H6 | 7 |
| H7 | 8 |
| H8 | 7 |
| H9 | 7 |
| H10 | 5 |

## Distribuição por heurística

| Heurística | Achados |
| :-- | --: |
| H01 | 8 |
| H02 | 9 |
| H03 | 5 |
| H04 | 12 |
| H05 | 8 |
| H06 | 7 |
| H07 | 8 |
| H08 | 7 |
| H09 | 7 |
| H10 | 5 |

## Distribuição por severidade

| Nota | Rótulo | Achados |
| :-: | :-- | --: |
| 1 | Cosmético | 6 |
| 2 | Menor | 35 |
| 3 | Maior | 35 |

## Achados

| id | Heurística | Sev. | Localização | Arquivos |
| :-- | :-- | :-: | :-- | --: |
| A-H1-001 | H01 | 3 | Agenda, visualizações Semana, Mês e Dia — área da grade de horários, após pesquisa sem resultado no campo "Pesquisar tarefas…" (textbox uid 1_69) | 2 |
| A-H1-002 | H01 | 3 | Painel lateral esquerdo — mini calendário de navegação (cabeçalho "Setembro 2026", uids 1_4 a 1_6, e grade de dias uids 1_16 a 1_57), em relação ao título do período na barra superior (uid 1_68) | 2 |
| A-H1-003 | H01 | 3 | Barra superior e painel lateral — botão "Recolher painel" (uid 1_64) com filtros "Exibir tarefas de… Alana" e "Marcadores: Retornar o contato" aplicados | 3 |
| A-H1-004 | H01 | 3 | Agenda, visualização Semana — botão de conclusão (role=radio, aria-label "Concluir") no cartão da tarefa "Follow-up de negociação — Ambev" (uid 1_131 no snapshot inicial), e o mesmo controle "Concluir" no rodapé do diálogo de detalhes | 3 |
| A-H1-005 | H01 | 3 | Visualização em Lista — coluna Status, controle role=radio "Tarefa concluída" da linha "Negociação de condições — ALL MOR GESTAO DE MARCAS E PRODUTOS LTDA" (uid 9_7 / 9_17), e o mesmo registro na visualização Calendário com filtro de status "Abertas" | 3 |
| A-H1-006 | H01 | 2 | Diálogo de detalhes de tarefa em modo somente leitura — título "Editar tarefa" (uid 11_137) e botão de lápis também rotulado "Editar tarefa" (uid 11_138), aberto a partir do cartão "Negociação de condições — ALL MOR GESTAO DE MARCAS E PRODUTOS LTDA" | 2 |
| A-H1-007 | H01 | 2 | Painel lateral — marcadores de presença de tarefa (pontos sob os números dos dias) do mini calendário, com filtro de Busca avançada "Título: \"proposta\"" ativo | 2 |
| A-H1-008 | H01 | 2 | Diálogo "Nova tarefa" — campo "Endereço" (input com placeholder "Endereço da tarefa"), preenchido automaticamente ao selecionar um valor no campo "Cliente" | 3 |
| A-H2-001 | H02 | 2 | Painel lateral esquerdo, filtro "Tipo de tarefa" (lista aberta) e, no modal "Nova tarefa"/"Editar tarefa", o seletor "Tipo" — opções "Simples" e "Telefone" | 2 |
| A-H2-002 | H02 | 1 | Modal "Nova tarefa", campo "Tipo" — valor padrão exibido como "(nenhum)" | 2 |
| A-H2-003 | H02 | 3 | Modais "Nova tarefa" e "Editar tarefa", campo "Duração" — número sem unidade; o seletor de unidade é desenhado fora da área visível do modal | 4 |
| A-H2-004 | H02 | 2 | Modais "Nova tarefa" e "Editar tarefa", campo rotulado "Usuários" (espaço reservado "Adicionar usuário") — o mesmo conceito aparece como "Responsáveis" no painel de Busca avançada | 3 |
| A-H2-005 | H02 | 3 | Modal de detalhes da tarefa (intitulado "Editar tarefa"), rodapé — botão primário "Concluir", na mesma posição em que o modo de edição exibe "Salvar" | 2 |
| A-H2-006 | H02 | 2 | Modal de detalhes da tarefa — título "Editar tarefa" sobre uma tela somente de leitura, que traz um botão de lápis também chamado "Editar tarefa" | 2 |
| A-H2-007 | H02 | 1 | Visualização Semana da agenda, eixo de horas à esquerda — rótulo "GMT-03" no lugar da primeira hora e horas grafadas sem zero à esquerda ("1:00" a "9:00") | 2 |
| A-H2-008 | H02 | 1 | Barra superior, rótulo do período exibido — "20 – 26 de Setembro 2026" na visualização Semana e "Setembro de 2026" na visualização Mês; também o cabeçalho "Setembro 2026" do calendário lateral | 2 |
| A-H2-009 | H02 | 2 | Cartões de tarefa na agenda (visualizações Dia, Semana e Mês) e primeira coluna da visualização Lista — o círculo de marcar a atividade como realizada é um botão de opção (radio) | 3 |
| A-H3-001 | H03 | 3 | Agenda (visualização Semana e Lista) e modal de detalhe "Editar tarefa" — ação Concluir: botão "Concluir" no rodapé do modal e controle redondo "Concluir" no cartão da tarefa / na coluna Status da Lista | 3 |
| A-H3-002 | H03 | 3 | Modal de detalhe/edição de tarefa ("Editar tarefa") — cabeçalho (ícone de lápis e botão "Fechar") e rodapé ("Fechar" / "Concluir"); também ausente no modo de edição ("Cancelar" / "Salvar") e nos cartões da agenda e nas linhas da Lista | 2 |
| A-H3-003 | H03 | 2 | Modais "Nova tarefa" e "Editar tarefa" (sobreposição `div.fixed.inset-0.z-50`) — resposta à tecla Esc | 3 |
| A-H3-004 | H03 | 2 | Painel lateral esquerdo — lista suspensa do filtro "Exibir tarefas de…" (campo de texto de adicionar usuário, uid 11_60 no snapshot do estado) | 2 |
| A-H3-005 | H03 | 3 | Modal "Nova tarefa" — fundo escurecido da sobreposição (`div.fixed.inset-0.z-50`, área fora do cartão branco do formulário) | 4 |
| A-H4-001 | H04 | 2 | Modal "Nova tarefa" (e "Editar tarefa") — campos relacionais Cliente, Oportunidade, Usuários, Contatos e Marcadores | 2 |
| A-H4-002 | H04 | 2 | Modal "Nova tarefa" — lista de sugestões do campo Cliente (comparada com a lista suspensa do campo Tipo, na mesma tela) | 2 |
| A-H4-003 | H04 | 3 | Campo Marcadores — no modal "Nova tarefa" e no filtro "Marcadores" do painel lateral | 3 |
| A-H4-004 | H04 | 2 | Painel "Busca avançada" (barra superior) comparado ao modal de tarefa, ao painel lateral e à barra de filtros aplicados | 3 |
| A-H4-005 | H04 | 3 | Modal de detalhes da tarefa — título do diálogo e botão primário do rodapé (estado de leitura versus estado de edição) | 3 |
| A-H4-006 | H04 | 2 | Modal de detalhes/edição de tarefa — descarte pelo teclado (tecla Escape) | 2 |
| A-H4-007 | H04 | 3 | Modal de detalhes da tarefa em modo somente leitura — chips dos campos Cliente, Oportunidade, Usuários, Contatos e Marcadores | 2 |
| A-H4-008 | H04 | 1 | Etiqueta de tipo da tarefa e controle de conclusão — visualização Calendário (Dia/Semana/Mês) comparada à visualização Lista | 3 |
| A-H4-009 | H04 | 2 | Controle de conclusão da tarefa — círculo à esquerda do cartão no calendário e da linha na Lista | 4 |
| A-H4-010 | H04 | 1 | Formatos de data e hora — título do calendário lateral, título do período na barra superior, régua de horas da grade e horários dos cartões | 2 |
| A-H4-011 | H04 | 2 | Barra superior — seletor "Modo de visualização" (Dia/Semana/Mês) e par de botões de ícone "Calendário" / "Lista" | 2 |
| A-H4-012 | H04 | 2 | Visualização Lista — ordenação das linhas pela coluna "Quando" | 2 |
| A-H5-001 | H05 | 3 | Modal "Nova tarefa" (aberto pelo botão "Criar tarefa" do painel lateral) — botão "Criar" do rodapé; efeito na agenda (Semana, DOM. 20) e na visualização em Lista | 4 |
| A-H5-002 | H05 | 3 | Diálogo "Editar tarefa" em modo de edição (aberto pelo lápis no cabeçalho), tarefa "Negociação de condições — ALL MOR GESTAO DE MARCAS E PRODUTOS LTDA" — botão "×" (Fechar) do cabeçalho | 3 |
| A-H5-003 | H05 | 3 | Agenda, visualização Semana — controle circular "Concluir" no canto superior esquerdo do card de tarefa (testado no card "Follow-up de negociação — Ambev", SEX. 25, 10:00). O mesmo controle existe na coluna Status da visualização em Lista | 4 |
| A-H5-004 | H05 | 3 | Diálogo "Editar tarefa" em modo de leitura (aberto pelo clique no card, antes de acionar o lápis) — botões "×" dos chips dos campos Cliente, Usuários, Contatos e Marcadores (testado nos chips "Ambev" e "ALL MOR GESTAO DE MARCAS E PRODUTOS LTDA") | 4 |
| A-H5-005 | H05 | 3 | Modal "Nova tarefa" e modo de edição — seletores de unidade dos campos "Duração" e "Repetir a cada", renderizados fora da largura visível do modal | 3 |
| A-H5-006 | H05 | 2 | Modal "Nova tarefa" — campo "Duração" e botão "Criar" | 3 |
| A-H5-007 | H05 | 2 | Modal "Nova tarefa" e agenda, visualização Semana — criação de tarefa em horário já ocupado (22/09/2026, 09:00, sobrepondo "Negociação de condições — ALL MOR GESTAO DE MARCAS E PRODUTOS LTDA", 09:00–10:00) | 3 |
| A-H5-008 | H05 | 2 | Modal "Nova tarefa" logo após o carregamento da aplicação — campo "Data" (valor padrão 20/09/2026) confrontado com o dia corrente, SEG. 21, destacado no calendário lateral e no cabeçalho da semana | 2 |
| A-H6-001 | H06 | 3 | Modal "Nova tarefa" (e o mesmo modal em modo "Editar tarefa") — campo "Duração" e linha "Repetir": os seletores de unidade que acompanham esses dois campos ficam fora da borda direita do modal | 4 |
| A-H6-002 | H06 | 3 | Área de conteúdo com o painel lateral recolhido pelo botão "Recolher painel" (uid 1_64) — filtros "Exibir tarefas de…", "Marcadores" e "Tipo de tarefa" | 2 |
| A-H6-003 | H06 | 3 | Visualização em Lista (cabeçalhos Título · Cliente · Contatos · Quando · Tipo · Descrição) e blocos de tarefa das visualizações Dia, Semana e Mês, com "Exibir tarefas de…" preenchido com outros usuários | 3 |
| A-H6-004 | H06 | 2 | Visualização "Mês" — itens de tarefa dentro das células dos dias | 2 |
| A-H6-005 | H06 | 3 | Barra superior (botão de recolher/expandir painel, "Anterior", "Próximo", "Busca avançada", alternador Calendário/Lista), ícone de lápis do modal de detalhes e círculo de conclusão dos blocos de tarefa e das linhas da Lista | 3 |
| A-H6-006 | H06 | 3 | Visualizações "Semana" e "Dia" — texto dentro dos blocos de tarefa da grade horária | 3 |
| A-H6-007 | H06 | 2 | Painel "Busca avançada" (aberto pelo chevron do campo de pesquisa, uid 1_70) — campos Título, Descrição, Responsáveis, Cliente e Contatos | 2 |
| A-H7-001 | H07 | 2 | Tela principal de Tarefas — barra superior (botões Hoje, Anterior, Próximo, seletor Dia/Semana/Mês, alternador Calendário/Lista) e botão Criar tarefa do painel lateral | 2 |
| A-H7-002 | H07 | 2 | Modais Editar tarefa e Nova tarefa — teclas Esc, Enter e Ctrl+Enter | 2 |
| A-H7-003 | H07 | 2 | Busca avançada — campo Título (Palavras-chave no título) e botão Pesquisar | 2 |
| A-H7-004 | H07 | 3 | Visualização em Lista — cabeçalhos das colunas (Título, Cliente, Contatos, Quando, Tipo, Descrição) e primeira coluna de status | 2 |
| A-H7-005 | H07 | 3 | Agenda, visualizações Dia/Semana/Mês — blocos de tarefa na grade de horários | 2 |
| A-H7-006 | H07 | 2 | Aplicação inteira — persistência de preferências: modo de visualização, filtro de Status, Exibir tarefas de…, Marcadores e Tipo de tarefa | 3 |
| A-H7-007 | H07 | 3 | Agenda, visualizações Dia/Semana/Mês — blocos de tarefa como alvo de teclado | 2 |
| A-H7-008 | H07 | 2 | Modal Nova tarefa (botão Criar tarefa do painel lateral) e modal Editar tarefa — ausência de modelos, duplicação e padrões configuráveis | 2 |
| A-H8-001 | H08 | 2 | Visualização em Lista (botão "Lista", modo Mês, Setembro de 2026) — coluna "Descrição" da tabela de tarefas | 2 |
| A-H8-002 | H08 | 2 | Visualização em Lista — coluna "Contatos" da tabela de tarefas | 2 |
| A-H8-003 | H08 | 2 | Modal de detalhes da tarefa (título "Editar tarefa"), aberto pelo clique na tarefa "Reunião de descoberta — ABC PARARRAIOS" na visualização em Lista — corpo rolável do modal | 2 |
| A-H8-004 | H08 | 2 | Modal "Nova tarefa", aberto pelo botão "Criar tarefa" da barra lateral — ordenação e peso visual dos campos do formulário | 2 |
| A-H8-005 | H08 | 3 | Agenda, visualização Semana (20 – 26 de Setembro 2026) — cartões de tarefa na grade de horários | 2 |
| A-H8-006 | H08 | 2 | Visualização em Lista — coluna "Título" em relação à coluna "Cliente" | 2 |
| A-H8-007 | H08 | 1 | Agenda, visualização Mês (Setembro de 2026) — mini calendário "Setembro 2026" no topo da barra lateral esquerda | 2 |
| A-H9-001 | H09 | 3 | Modal "Nova tarefa" (botão Criar tarefa) — caixa de erro no rodapé do corpo do formulário, abaixo do campo "Lembrete por e-mail" | 3 |
| A-H9-002 | H09 | 3 | Modal "Nova tarefa" — posição da caixa de erro dentro do corpo rolável do formulário, em relação ao botão "Criar" no rodapé fixo | 2 |
| A-H9-003 | H09 | 3 | Modal "Nova tarefa" → agenda, visualização Semana, coluna DOM. 20 — tarefas rotuladas "(sem título)" às 09:00 | 3 |
| A-H9-004 | H09 | 3 | Agenda, área principal — faixa "Falha ao carregar" acima da grade, após navegar com o controle "Próximo" para a semana 27 set – 3 out 2026 | 2 |
| A-H9-005 | H09 | 3 | Modal "Editar tarefa" aberto a partir do bloco "Negociação de condições — ALL MOR GESTAO DE MARCAS E PRODUTOS LTDA" na agenda (visualização Semana, 22/09) | 3 |
| A-H9-006 | H09 | 3 | Agenda, visualização Semana — botão circular "Concluir tarefa" do bloco "Negociação de condições — ALL MOR GESTAO DE MARCAS E PRODUTOS LTDA" (22/09, 09:00 – 10:00) | 3 |
| A-H9-007 | H09 | 2 | Modal "Nova tarefa" — lista suspensa de resultados do campo "Cliente" (caixa "Pesquisar cliente") | 4 |
| A-H10-001 | H10 | 3 | Aplicação inteira (tela de Tarefas: barra superior, painel lateral e modais) — ausência de qualquer ponto de entrada para ajuda | 2 |
| A-H10-002 | H10 | 2 | Visualização em Lista, estado sem resultados após pesquisa/filtro — mensagem "Nenhuma tarefa encontrada." | 2 |
| A-H10-003 | H10 | 3 | Barra superior, campo "Pesquisar tarefas…" com a visualização Calendário (Semana 20–26 de Setembro 2026) — pesquisa restrita ao período exibido, sem qualquer explicação | 2 |
| A-H10-004 | H10 | 2 | Visualização Calendário (Semana) — bloco de tarefa na grade, gestos de arrastar para mover e de redimensionar para alterar a duração | 3 |
| A-H10-005 | H10 | 2 | Modal "Nova tarefa" (e "Editar tarefa") — campos "Duração", "Repetir a cada" e "Lembrete por e-mail" | 2 |
