# PulseCRM

PulseCRM agora possui uma base de produto mais estruturada, com backend modular em Python, banco SQLite real, sessao persistida e frontend responsivo servidos juntos. A proposta passou a considerar explicitamente um modelo gratuito e compartilhavel, ideal para voce e seus amigos usarem no trabalho sem custo de licenca.

## O que foi entregue

- arquitetura e documentacao de produto;
- modelagem inicial de banco para futura evolucao com Prisma;
- API local com autenticacao demo, multi-tenant basico, sessao persistida e modulos core;
- frontend responsivo conectado a API;
- fluxo de convite para compartilhar o workspace com outras pessoas;
- placeholder arquitetural para app mobile nativo.

## Estrutura principal

- [apps/api/server.py](/C:/Users/Pablo/OneDrive/Desktop/CRM%20projeto/apps/api/server.py)
- [apps/api/app/bootstrap.py](/C:/Users/Pablo/OneDrive/Desktop/CRM%20projeto/apps/api/app/bootstrap.py)
- [apps/api/app/router.py](/C:/Users/Pablo/OneDrive/Desktop/CRM%20projeto/apps/api/app/router.py)
- [apps/api/app/repositories/crm_repository.py](/C:/Users/Pablo/OneDrive/Desktop/CRM%20projeto/apps/api/app/repositories/crm_repository.py)
- [apps/api/app/services/crm_service.py](/C:/Users/Pablo/OneDrive/Desktop/CRM%20projeto/apps/api/app/services/crm_service.py)
- [apps/api/schema.sql](/C:/Users/Pablo/OneDrive/Desktop/CRM%20projeto/apps/api/schema.sql)
- [apps/web/index.html](/C:/Users/Pablo/OneDrive/Desktop/CRM%20projeto/apps/web/index.html)
- [apps/web/styles.css](/C:/Users/Pablo/OneDrive/Desktop/CRM%20projeto/apps/web/styles.css)
- [apps/web/app.js](/C:/Users/Pablo/OneDrive/Desktop/CRM%20projeto/apps/web/app.js)
- [apps/mobile/README.md](/C:/Users/Pablo/OneDrive/Desktop/CRM%20projeto/apps/mobile/README.md)
- [packages/shared/src/constants.mjs](/C:/Users/Pablo/OneDrive/Desktop/CRM%20projeto/packages/shared/src/constants.mjs)
- [docs/architecture.md](/C:/Users/Pablo/OneDrive/Desktop/CRM%20projeto/docs/architecture.md)
- [docs/navigation-flows.md](/C:/Users/Pablo/OneDrive/Desktop/CRM%20projeto/docs/navigation-flows.md)
- [docs/access-control.md](/C:/Users/Pablo/OneDrive/Desktop/CRM%20projeto/docs/access-control.md)
- [docs/implementation-plan.md](/C:/Users/Pablo/OneDrive/Desktop/CRM%20projeto/docs/implementation-plan.md)
- [docs/openapi.yaml](/C:/Users/Pablo/OneDrive/Desktop/CRM%20projeto/docs/openapi.yaml)
- [prisma/schema.prisma](/C:/Users/Pablo/OneDrive/Desktop/CRM%20projeto/prisma/schema.prisma)

## Como rodar

No ambiente atual:

```powershell
& 'C:\Users\Pablo\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' .\apps\api\server.py
```

Depois abra [http://localhost:3000](http://localhost:3000).

## Deploy

- configuracao pronta para deploy em [render.yaml](/C:/Users/Pablo/OneDrive/Desktop/CRM%20projeto/render.yaml)
- instrucoes em [DEPLOY.md](/C:/Users/Pablo/OneDrive/Desktop/CRM%20projeto/DEPLOY.md)
- roteiro curto em [PUBLISH_READY.md](/C:/Users/Pablo/OneDrive/Desktop/CRM%20projeto/PUBLISH_READY.md)
- variaveis de ambiente em [.env.example](/C:/Users/Pablo/OneDrive/Desktop/CRM%20projeto/.env.example)
- imagem pronta em [Dockerfile](/C:/Users/Pablo/OneDrive/Desktop/CRM%20projeto/Dockerfile)
- suporte a SQLite local e PostgreSQL via `DATABASE_URL`

## Login demo

- `ana@pulsecrm.demo` / `demo123`
- `mariana@pulsecrm.demo` / `demo123`
- `joao@pulsecrm.demo` / `demo123`
- `julia@pulsecrm.demo` / `demo123`

## Modulos iniciais ativos

- autenticacao demo com sessao persistida em SQLite
- dashboard executivo
- gestao de leads
- pipeline comercial
- agenda
- automacoes
- equipe e perfis
- convites para compartilhar o CRM com amigos e colaboradores
- aceite de convite com criacao de conta e entrada no workspace
- banco real com inicializacao automatica

## Modelo de uso gratuito

- foco em edicao gratuita e auto-hospedavel
- multiusuario para compartilhamento com amigos ou equipe
- sem dependencia obrigatoria de servicos pagos para a base local
- pronto para evoluir depois para hospedagem publica ou SaaS

## Fluxo de convite

1. Um usuario autenticado gera o convite na area de compartilhamento.
2. O CRM mostra o link no formato `/?invite=<token>`.
3. A pessoa convidada abre o link, informa nome e senha e cria a propria conta.
4. O sistema autentica automaticamente o novo usuario e libera o workspace.

## Stack-alvo recomendada

- Frontend web: Next.js + TypeScript + Tailwind CSS + TanStack Query + shadcn/ui
- Mobile: React Native com Expo
- Backend: NestJS + TypeScript
- Banco principal: PostgreSQL
- ORM: Prisma
- Cache e filas: Redis + BullMQ

## Observacao importante

Como o ambiente atual nao tem `npm` ou `pnpm`, a base executavel foi implementada com Python standard library + SQLite para garantir backend estruturado e persistencia real imediatamente. A estrutura de dominio e a documentacao continuam preparando o caminho para migracao posterior para `Next.js + NestJS + Prisma + PostgreSQL`.
