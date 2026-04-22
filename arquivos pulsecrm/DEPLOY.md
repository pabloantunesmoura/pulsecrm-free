# Deploy Gratuito

Esta base foi preparada para deploy gratuito inicial com `render.yaml`.

## O que ja esta pronto

- a API agora aceita `DATABASE_URL` para PostgreSQL em producao;
- o ambiente local continua usando SQLite automaticamente;
- o projeto inclui `render.yaml` para provisionar web service + banco no Render;
- o endpoint de health check esta em `/api/health`.

## Passo a passo sugerido

1. Suba este projeto para um repositorio Git remoto.
2. No Render, crie o projeto usando Blueprint a partir do repositorio.
3. O Render vai ler `render.yaml`, criar:
   - um web service Python chamado `pulsecrm-free`
   - um banco PostgreSQL chamado `pulsecrm-db`
4. Aguarde o build e abra a URL publica gerada.
5. Faça login com:
   - `ana@pulsecrm.demo` / `demo123`

## Observacoes importantes

- localmente, o banco continua sendo `apps/api/data/pulsecrm.sqlite3`
- em deploy, com `DATABASE_URL` definido, a aplicacao usa PostgreSQL
- a camada de convites e criacao de conta continua funcionando no ambiente online
- o caminho gratuito escolhido foi o Render porque ele suporta web services Python e Postgres via Blueprint
- limitacoes oficiais do plano gratuito do Render:
  - o web service entra em idle apos 15 minutos sem trafego
  - arquivos locais sao efemeros, por isso o deploy usa PostgreSQL e nao SQLite
  - o Postgres gratuito do Render expira 30 dias apos a criacao

## Recomendacao pratica

Use esta configuracao gratuita para publicar, validar com amigos e testar o fluxo real pela web.

Se o CRM passar a ser usado diariamente como ferramenta de trabalho, o proximo passo recomendado e:

- manter o web service no Render e migrar para plano pago; ou
- mover o banco para um Postgres externo e estavel; ou
- reempacotar o backend para uma plataforma com camada gratuita mais duravel.
