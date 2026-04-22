from ..repositories.dashboard_repository import DashboardRepository


class DashboardService:
    def __init__(self) -> None:
        self.repository = DashboardRepository()

    def get_dashboard(self, tenant_id: str) -> dict:
        return self.repository.summarize(tenant_id)
