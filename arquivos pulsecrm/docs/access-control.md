# Perfis de Usuario e Regras de Permissao

## Modelo recomendado

O PulseCRM deve usar RBAC com escopo por tenant, complemento por equipe e filtros por carteira. A permissao final pode depender de:

- perfil principal do usuario;
- permissoes adicionais concedidas individualmente;
- equipe do usuario;
- ownership do registro;
- carteira associada;
- modulo e acao desejada.

## Perfis padrao

### Administrador

- acesso total ao tenant
- configura usuarios, equipes, pipelines, integracoes e billing
- visualiza todos os dados, logs e configuracoes sensiveis
- gerencia perfis e permissoes personalizadas

### Gestor

- visualiza desempenho global ou da equipe sob sua gestao
- redistribui leads e negocios
- acompanha metas, forecast e produtividade
- pode editar regras operacionais definidas pelo admin, se autorizado

### Vendedor

- acessa sua carteira, leads, negocios, tarefas e agenda
- move oportunidades no pipeline
- envia mensagens e registra interacoes
- nao acessa configuracoes criticas nem dados financeiros globais

### Suporte

- acessa contatos, clientes, tickets relacionados e historico de atendimento
- responde mensagens e executa rotinas de atendimento
- visualiza apenas dados necessarios ao suporte
- nao altera metas, pipeline comercial ou configuracoes estruturais

## Matriz resumida por modulo

| Modulo | Administrador | Gestor | Vendedor | Suporte |
| --- | --- | --- | --- | --- |
| Dashboard executivo | total | total ou equipe | carteira | limitado |
| Leads | total | total ou equipe | carteira | leitura parcial |
| Pipeline | total | total ou equipe | carteira | leitura |
| Agenda e tarefas | total | equipe | propria e compartilhada | propria e compartilhada |
| Mensagens | total | equipe | carteira | atendimento |
| Automacoes | total | parcial | sem acesso ou leitura | sem acesso |
| Relatorios | total | total ou equipe | performance propria | operacionais |
| Integracoes | total | sem acesso por padrao | sem acesso | sem acesso |
| Configuracoes | total | parcial por politica | sem acesso | sem acesso |
| Auditoria | total | leitura restrita | sem acesso | sem acesso |

## Regras granulares recomendadas

### Escopo de dados

- `all`: acesso a todo o tenant
- `team`: acesso apenas a registros da equipe
- `portfolio`: acesso apenas aos registros sob ownership ou carteira permitida
- `assigned`: acesso apenas aos registros diretamente atribuidos ao usuario
- `self`: acesso apenas aos proprios dados operacionais

### Acoes por entidade

- `view`
- `create`
- `update`
- `delete`
- `assign`
- `export`
- `manage`
- `approve`

## Exemplos de permissoes

- `leads.view.team`
- `leads.assign.portfolio`
- `deals.update.assigned`
- `reports.export.team`
- `automations.manage.all`
- `settings.manage.all`
- `audit.view.all`

## Regras sensiveis

- exclusao definitiva deve exigir perfil elevado e auditoria obrigatoria
- exportacao de base deve respeitar perfil, escopo e mascaramento de dados
- credenciais de integracao devem ficar restritas ao administrador
- alteracoes em pipeline, automacoes e regras de roteamento devem gerar trilha de auditoria
- dados pessoais sensiveis devem respeitar consentimento e finalidade LGPD
