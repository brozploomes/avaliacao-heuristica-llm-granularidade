# Material de contexto — Tarefas do CRM Ploomes

> Material de contexto padronizado da parte avaliada. Idêntico nas três condições (A, B e C) e nas nove
> execuções. Descreve o que a funcionalidade é, como se comporta, para que serve e o que percorrer; não
> aponta problemas nem direciona heurísticas.

---

## Metadados

- **Funcionalidade avaliada:** Tarefas do CRM Ploomes: agenda e lista de atividades comerciais
- **Objeto:** aplicação web em execução, arquivo `.html` autocontido, aberto no navegador
- **Referência do objeto:** `C:\Users\EduardoDamiao\Documents\MBA USPEsalq\objeto\tarefas_crm.html`

---

## A. Descrição da funcionalidade e comportamentos principais

A aplicação permite consultar e gerenciar as tarefas do CRM Ploomes: as atividades comerciais que um usuário
programa em relação a clientes, como reuniões, ligações, visitas e e-mails.

As tarefas são exibidas em uma agenda com as visualizações Dia, Semana e Mês, e em uma visualização em
Lista. Um calendário lateral permite navegar entre meses e selecionar uma data; os controles Anterior,
Próximo e Hoje movem o período exibido. Há um campo de pesquisa por texto e uma Busca avançada, com
palavras-chave no título, palavras-chave na descrição e cliente. Os filtros permitem exibir tarefas de outros
usuários (Exibir tarefas de…) e restringir a lista por Marcadores, Tipo e Status (Abertas, Finalizadas ou
Todas); Limpar e Limpar tudo removem a pesquisa e os filtros.

O usuário pode abrir os detalhes de uma tarefa, criar uma tarefa nova, editar uma tarefa existente, movê-la
para outra data ou horário, alterar sua duração e concluí-la. Uma tarefa tem título, descrição, data, horário,
duração, tipo, cliente, oportunidade (o negócio do cliente em um funil do CRM), responsáveis, contatos
relacionados, marcadores, endereço, lembrete por e-mail e repetição. As alterações feitas na aplicação passam a valer imediatamente na própria tela.

A interface exibe estado de carregamento enquanto busca as tarefas, uma mensagem quando nenhuma tarefa
corresponde à pesquisa ou aos filtros, e uma mensagem de falha quando um carregamento não se completa.

---

## B. Cenários de uso típicos

- Um usuário de CRM consulta as atividades comerciais programadas para determinado período.
- Um usuário de CRM cria uma tarefa relacionada a um cliente ou a uma oportunidade de um funil do CRM.
- Um usuário de CRM pesquisa e filtra tarefas por responsável, tipo, marcador ou status.
- Um usuário de CRM reorganiza compromissos alterando datas, horários e durações.
- Um usuário de CRM registra a conclusão de uma atividade comercial.
- Um usuário de CRM consulta as tarefas de outros integrantes da equipe.

---

## C. Lista de tarefas para guiar a avaliação

1. Usar o calendário lateral para navegar entre setembro e outubro de 2026 e selecionar uma data da primeira
   semana de outubro.
2. Navegar entre períodos com os controles Anterior, Próximo e Hoje, e alternar entre as visualizações Mês,
   Semana, Dia e Lista.
3. Localizar a tarefa Reunião de descoberta, do cliente ABC PARARRAIOS, abrir seus detalhes e voltar à agenda.
4. Pesquisar uma tarefa pelo título, fazer em seguida uma pesquisa que não retorne resultado e depois limpar
   a pesquisa.
5. Exibir as tarefas de outro usuário e aplicar filtros por marcador, tipo e status. Em seguida, remover os
   filtros.
6. Usar a Busca avançada para localizar tarefas por palavra-chave no título, na descrição e por cliente.
   Depois, redefinir a busca.
7. Criar uma tarefa chamada Avaliação de retorno comercial, informando descrição, data, horário, duração,
   tipo, cliente, oportunidade, responsável e marcador.
8. Localizar a tarefa criada, abrir seus detalhes, alterar o título ou a descrição e salvar.
9. Abrir a tarefa criada no modo de edição, alterar sua data, horário e duração e salvar as modificações.
10. Concluir a tarefa criada, localizá-la com o filtro de status Finalizadas e consultá-la na visualização em
    Lista.
