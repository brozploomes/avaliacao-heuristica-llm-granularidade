# Evidências — Formato C · execução 3

Objeto: `C:/Users/EduardoDamiao/Documents/MBA USPEsalq/objeto/tarefas_crm.html` · commit `9b8413a` · branch `main`

Total de achados: **27** · arquivos de evidência: **71**

## Distribuição por heurística

| Heurística | Achados |
| :--- | ---: |
| H1 | 6 |
| H2 | 2 |
| H3 | 2 |
| H4 | 5 |
| H5 | 3 |
| H6 | 3 |
| H7 | 1 |
| H8 | 2 |
| H9 | 2 |
| H10 | 1 |

## Distribuição por severidade

| Nota | Rótulo | Achados |
| :--: | :--- | ---: |
| 1 | Cosmético | 1 |
| 2 | Menor | 14 |
| 3 | Maior | 12 |

## Achados

| ID | Heurística | Sev. | Localização | Arquivos |
| :--- | :--- | :--: | :--- | ---: |
| C-H1-001 | H1 — Visibilidade do status do sistema | 2 | Tela principal de Tarefas — calendário lateral (cabeçalho "Outubro 2026", dia 1 marcado) versus barra superior e grade principal ("Setembro de 2026", dia 23 marcado), após acionar o botão Hoje | 2 |
| C-H1-002 | H1 — Visibilidade do status do sistema | 3 | Modal de detalhes da tarefa "Ligação de qualificação — Advocacia Águia" (3/9/2026) — botão Concluir do rodapé; e grade do mês de setembro após a ação | 3 |
| C-H1-003 | H1 — Visibilidade do status do sistema | 3 | Visualização Calendário (Mês, setembro de 2026) com o campo de pesquisa preenchido com "zzzzqqq"; e a mesma visualização com o filtro Marcadores = "Reclamação" | 3 |
| C-H1-004 | H1 — Visibilidade do status do sistema | 3 | Tela principal com o painel lateral recolhido pelo botão "Recolher painel", mantendo ativo o filtro Tipo de tarefa = Reunião | 2 |
| C-H1-005 | H1 — Visibilidade do status do sistema | 2 | Modal de detalhes da tarefa concluída "Envio de proposta comercial — aline utiel" (21/9/2026), aberto pela visualização Lista com status Todas | 2 |
| C-H1-006 | H1 — Visibilidade do status do sistema | 3 | Modal de edição da tarefa "Avaliação de retorno comercial" — alteração de Data para 05/10/2026, Horário para 11:00 e Duração para 45, seguida de Salvar; visualização Semana de 20–26/9/2026 | 3 |
| C-H2-001 | H2 — Correspondência entre o sistema e o mundo real | 3 | Modal de detalhes da tarefa "Reunião de descoberta — ABC PARARRAIOS" — botão primário "Concluir" no rodapé, ao lado de "Fechar" | 2 |
| C-H2-002 | H2 — Correspondência entre o sistema e o mundo real | 2 | Barra "Filtros:" do topo — ação "Limpar tudo", com o filtro Tipo de tarefa = Reunião ativo na barra lateral | 3 |
| C-H3-001 | H3 — Controle e liberdade do usuário | 3 | Modal de detalhes da tarefa finalizada "Kickoff comercial — Aramis" (1/10/2026) e o respectivo card na agenda com o filtro Finalizadas | 2 |
| C-H3-002 | H3 — Controle e liberdade do usuário | 2 | Modal de detalhes da tarefa ("Envio de proposta comercial — aline utiel") e painel suspenso do campo "Adicionar usuário" da barra lateral — tecla Esc | 3 |
| C-H4-001 | H4 — Consistência e padrões | 3 | Rodapé do modal de tarefa — par "Fechar / Concluir" no modo de leitura contra o par "Cancelar / Salvar" no modo de edição, na mesma posição e com o mesmo estilo | 3 |
| C-H4-002 | H4 — Consistência e padrões | 2 | Três pontos da tela para o mesmo conceito: barra lateral "Exibir tarefas de…", modal de tarefa "Usuários" e painel de Busca avançada "Responsáveis"; e três rótulos de limpeza: "Limpar" (x da pesquisa), "Redefinir" (busca avançada) e "Limpar tudo" (barra de filtros) | 3 |
| C-H4-003 | H4 — Consistência e padrões | 2 | Barra "Filtros:" logo abaixo da barra superior — representação dos critérios da busca avançada contra os filtros da barra lateral (Exibir tarefas de…, Marcadores, Tipo de tarefa) | 3 |
| C-H4-004 | H4 — Consistência e padrões | 2 | Barra lateral — campos "Pesquisar marcadores" (Marcadores) e "Todos os tipos" (Tipo de tarefa), visualmente idênticos e adjacentes | 2 |
| C-H4-005 | H4 — Consistência e padrões | 1 | Modal "Nova tarefa" — campo "Tipo": lista suspensa permanece aberta após a seleção, cobrindo Duração, Repetir e Cliente | 2 |
| C-H5-001 | H5 — Prevenção de erros | 3 | Modal de edição de tarefa — campo Título esvaziado e campo Duração com valor 0, ambos aceitos pelo botão Salvar | 4 |
| C-H5-002 | H5 — Prevenção de erros | 3 | Modal de detalhes da tarefa "Ligação de qualificação — Advocacia Águia" — botão primário "Concluir" do rodapé | 3 |
| C-H5-003 | H5 — Prevenção de erros | 3 | Cards da agenda (visualização Semana) — marcador circular "Concluir" no canto superior esquerdo de cada card, por exemplo no card "Follow-up de negociação — Ambev" (25/9, 10:00) | 4 |
| C-H6-001 | H6 — Reconhecer em vez de lembrar | 3 | Modal de tarefa (edição e criação) — campos "Duração" e "Repetir a cada": os seletores de unidade são renderizados fora dos limites do painel e ficam ocultos pelo recorte do modal | 3 |
| C-H6-002 | H6 — Reconhecer em vez de lembrar | 3 | Tela principal com o painel lateral recolhido, mantendo ativo o filtro Tipo de tarefa = Reunião | 2 |
| C-H6-003 | H6 — Reconhecer em vez de lembrar | 2 | Cards da agenda na visualização Semana — títulos truncados ("Negoci…", "Validaç…", "Follow-u…", "Envio d…") e linha de horário cortada nos cards de 30 minutos | 2 |
| C-H7-001 | H7 — Flexibilidade e eficiência de uso | 2 | Grade da agenda (visualizações Dia, Semana e Mês) e cabeçalhos da visualização Lista — ausência de aceleradores | 2 |
| C-H8-001 | H8 — Estética e design minimalista | 2 | Cards da agenda na visualização Semana — selo de tipo ("REUNIÃO", "SIMPLES", "E-MAIL") ocupando a parte inicial da linha de título | 2 |
| C-H8-002 | H8 — Estética e design minimalista | 2 | Modal de detalhes da tarefa "Validação com decisores — alpha piscinas" em modo de leitura — formulário completo com campos vazios e controles desabilitados | 3 |
| C-H9-001 | H9 — Ajudar o usuário a reconhecer, diagnosticar e recuperar-se de erros | 2 | Visualização Lista, mês de setembro de 2026, com a pesquisa "zzzzqqq" e o status Abertas — mensagem "Nenhuma tarefa encontrada." | 2 |
| C-H9-002 | H9 — Ajudar o usuário a reconhecer, diagnosticar e recuperar-se de erros | 2 | Modal de edição da tarefa "Negociação de condições — ALL MOR GESTAO DE MARCAS E PRODUTOS LTDA" — campo Duração com valor 0 e botão Salvar | 3 |
| C-H10-001 | H10 — Ajuda e documentação | 2 | Toda a funcionalidade de Tarefas — barra superior, painel lateral, agenda, visualização Lista e modais de criação e de detalhes | 3 |
