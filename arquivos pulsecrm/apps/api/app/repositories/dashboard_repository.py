from ..db import get_connection


class DashboardRepository:
    def summarize(self, tenant_id: str) -> dict:
        with get_connection() as connection:
            open_deals = connection.execute(
                "SELECT COALESCE(SUM(value), 0) AS total FROM deals WHERE tenant_id = ? AND status = 'OPEN'",
                (tenant_id,),
            ).fetchone()["total"]
            qualified_leads = connection.execute(
                "SELECT COUNT(*) AS total FROM leads WHERE tenant_id = ? AND score >= 70",
                (tenant_id,),
            ).fetchone()["total"]
            pending_tasks = connection.execute(
                "SELECT COUNT(*) AS total FROM tasks WHERE tenant_id = ? AND status <> 'DONE'",
                (tenant_id,),
            ).fetchone()["total"]
            active_automations = connection.execute(
                "SELECT COUNT(*) AS total FROM automations WHERE tenant_id = ? AND status = 'ACTIVE'",
                (tenant_id,),
            ).fetchone()["total"]

        return {
            "metrics": [
                {
                    "label": "Receita em aberto",
                    "value": f"R$ {int(open_deals):,}".replace(",", "."),
                    "trend": "+12,4%",
                },
                {
                    "label": "Leads qualificados",
                    "value": str(qualified_leads),
                    "trend": "+18 em 7 dias",
                },
                {
                    "label": "Tarefas pendentes",
                    "value": str(pending_tasks),
                    "trend": "-6 hoje",
                },
                {
                    "label": "Automacoes ativas",
                    "value": str(active_automations),
                    "trend": "100% operando",
                },
            ]
        }
