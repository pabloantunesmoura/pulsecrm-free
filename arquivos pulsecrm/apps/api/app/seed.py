import json

from .db import get_connection
from .security import hash_password, iso_now


def seed_database() -> None:
    with get_connection() as connection:
        tenant_count = connection.execute("SELECT COUNT(*) AS total FROM tenants").fetchone()["total"]
        if tenant_count:
            return

        created_at = iso_now()

        connection.execute(
            "INSERT INTO tenants (id, name, slug, timezone, plan) VALUES (?, ?, ?, ?, ?)",
            ("tenant-pulse-demo", "PulseCRM Demo", "pulse-demo", "America/Sao_Paulo", "Scale"),
        )

        connection.executemany(
            "INSERT INTO teams (id, tenant_id, name) VALUES (?, ?, ?)",
            [
                ("team-sales", "tenant-pulse-demo", "Comercial"),
                ("team-support", "tenant-pulse-demo", "Suporte"),
            ],
        )

        connection.executemany(
            "INSERT INTO roles (id, name, scope) VALUES (?, ?, ?)",
            [
                ("role-admin", "Administrador", "all"),
                ("role-manager", "Gestor", "team"),
                ("role-sales", "Vendedor", "portfolio"),
                ("role-support", "Suporte", "assigned"),
            ],
        )

        users = [
            (
                "user-admin",
                "tenant-pulse-demo",
                "team-sales",
                "role-admin",
                "Ana Souza",
                "ana@pulsecrm.demo",
                hash_password("demo123"),
                "+55 11 99999-1000",
                "CEO Comercial",
                created_at,
            ),
            (
                "user-manager",
                "tenant-pulse-demo",
                "team-sales",
                "role-manager",
                "Mariana Costa",
                "mariana@pulsecrm.demo",
                hash_password("demo123"),
                "+55 11 99999-2000",
                "Gestora de Vendas",
                created_at,
            ),
            (
                "user-sales-1",
                "tenant-pulse-demo",
                "team-sales",
                "role-sales",
                "Joao Lima",
                "joao@pulsecrm.demo",
                hash_password("demo123"),
                "+55 11 99999-3000",
                "Account Executive",
                created_at,
            ),
            (
                "user-support-1",
                "tenant-pulse-demo",
                "team-support",
                "role-support",
                "Julia Mendes",
                "julia@pulsecrm.demo",
                hash_password("demo123"),
                "+55 11 99999-4000",
                "Especialista de Suporte",
                created_at,
            ),
        ]

        connection.executemany(
            """
            INSERT INTO users (
              id, tenant_id, team_id, role_id, name, email, password_hash, phone, title, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            users,
        )

        connection.execute(
            "INSERT INTO pipelines (id, tenant_id, name) VALUES (?, ?, ?)",
            ("pipeline-sales", "tenant-pulse-demo", "Vendas B2B"),
        )

        stages = [
            ("stage-entry", "pipeline-sales", "Entrada", 1, 15),
            ("stage-qualification", "pipeline-sales", "Qualificacao", 2, 35),
            ("stage-proposal", "pipeline-sales", "Proposta", 3, 65),
            ("stage-closing", "pipeline-sales", "Fechamento", 4, 85),
        ]
        connection.executemany(
            "INSERT INTO pipeline_stages (id, pipeline_id, name, position, probability) VALUES (?, ?, ?, ?, ?)",
            stages,
        )

        leads = [
            (
                "lead-1",
                "tenant-pulse-demo",
                "user-sales-1",
                "Grupo Orion",
                "Carlos Almeida",
                "carlos@orion.com",
                "+55 11 91111-1001",
                "Meta Ads",
                "QUALIFIED",
                92,
                "stage-proposal",
                json.dumps(["Enterprise", "Inbound"]),
                "2026-04-22T11:00:00+00:00",
                "Enviar proposta comercial",
                "Conta com potencial de expansao para 40 usuarios.",
                created_at,
                created_at,
            ),
            (
                "lead-2",
                "tenant-pulse-demo",
                "user-manager",
                "Lume Retail",
                "Patricia Nunes",
                "patricia@lumeretail.com",
                "+55 21 92222-1002",
                "Google Ads",
                "NEW",
                71,
                "stage-entry",
                json.dumps(["E-commerce"]),
                "2026-04-22T08:30:00+00:00",
                "Qualificar lead em chamada inicial",
                "Busca centralizar vendas e suporte em uma unica operacao.",
                created_at,
                created_at,
            ),
            (
                "lead-3",
                "tenant-pulse-demo",
                "user-sales-1",
                "Atlas Foods",
                "Renata Prado",
                "renata@atlasfoods.com",
                "+55 31 93333-1003",
                "Referral",
                "NEGOTIATION",
                88,
                "stage-closing",
                json.dumps(["Mid Market", "Referral"]),
                "2026-04-21T18:00:00+00:00",
                "Confirmar assinatura",
                "Projeto priorizado pelo time financeiro.",
                created_at,
                created_at,
            ),
        ]
        connection.executemany(
            """
            INSERT INTO leads (
              id, tenant_id, owner_id, company, name, email, phone, source, status, score,
              stage_id, tags, last_interaction_at, next_action, notes, created_at, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            leads,
        )

        deals = [
            (
                "deal-1",
                "tenant-pulse-demo",
                "lead-1",
                "user-sales-1",
                "Grupo Orion - Licenca anual",
                120000,
                "stage-proposal",
                "OPEN",
                "2026-04-28T16:00:00+00:00",
                created_at,
                created_at,
            ),
            (
                "deal-2",
                "tenant-pulse-demo",
                "lead-3",
                "user-sales-1",
                "Atlas Foods - Expansao CRM",
                210000,
                "stage-closing",
                "OPEN",
                "2026-04-25T14:00:00+00:00",
                created_at,
                created_at,
            ),
            (
                "deal-3",
                "tenant-pulse-demo",
                "lead-2",
                "user-manager",
                "Lume Retail - Operacao Omnichannel",
                64000,
                "stage-entry",
                "OPEN",
                "2026-05-06T11:00:00+00:00",
                created_at,
                created_at,
            ),
        ]
        connection.executemany(
            """
            INSERT INTO deals (
              id, tenant_id, lead_id, owner_id, title, value, stage_id, status, expected_close_at, created_at, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            deals,
        )

        tasks = [
            ("task-1", "tenant-pulse-demo", "user-sales-1", "Enviar proposta para Grupo Orion", "PENDING", "Alta", "2026-04-22T15:00:00+00:00", created_at, created_at),
            ("task-2", "tenant-pulse-demo", "user-manager", "Daily comercial", "DONE", "Media", "2026-04-22T12:00:00+00:00", created_at, created_at),
            ("task-3", "tenant-pulse-demo", "user-support-1", "Responder fila de onboarding", "PENDING", "Alta", "2026-04-22T18:00:00+00:00", created_at, created_at),
        ]
        connection.executemany(
            """
            INSERT INTO tasks (id, tenant_id, owner_id, title, status, priority, due_at, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            tasks,
        )

        events = [
            ("event-1", "tenant-pulse-demo", "user-manager", "Demo Grupo Orion", "2026-04-22T14:00:00+00:00", "2026-04-22T15:00:00+00:00", "meeting", created_at),
            ("event-2", "tenant-pulse-demo", "user-sales-1", "Follow-up Atlas Foods", "2026-04-22T16:30:00+00:00", "2026-04-22T17:00:00+00:00", "follow-up", created_at),
        ]
        connection.executemany(
            """
            INSERT INTO calendar_events (id, tenant_id, owner_id, title, starts_at, ends_at, type, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            events,
        )

        automations = [
            ("automation-1", "tenant-pulse-demo", "Boas-vindas WhatsApp", "ACTIVE", "lead.created", "whatsapp", "Envia mensagem inicial, cria tarefa de qualificacao e registra evento.", created_at),
            ("automation-2", "tenant-pulse-demo", "Sem resposta por 48h", "ACTIVE", "lead.inactive", "email", "Alterna entre e-mail e WhatsApp para reengajar oportunidades.", created_at),
        ]
        connection.executemany(
            """
            INSERT INTO automations (id, tenant_id, name, status, trigger_event, channel, description, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            automations,
        )

        activity = [
            ("activity-1", "tenant-pulse-demo", "lead-1", "EMAIL", "Proposta enviada e abertura registrada.", "2026-04-22T11:20:00+00:00"),
            ("activity-2", "tenant-pulse-demo", "lead-2", "NOTE", "Lead importado de campanha Performance B2B Abril.", "2026-04-22T08:35:00+00:00"),
            ("activity-3", "tenant-pulse-demo", "lead-3", "WHATSAPP", "Cliente confirmou interesse e pediu proposta final.", "2026-04-21T18:10:00+00:00"),
        ]
        connection.executemany(
            """
            INSERT INTO activity_logs (id, tenant_id, lead_id, type, summary, happened_at)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            activity,
        )
