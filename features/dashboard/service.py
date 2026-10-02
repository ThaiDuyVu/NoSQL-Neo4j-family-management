"""Dashboard statistics assembled through the Person public service."""
from features.person import service as person_service


def get_dashboard_stats() -> dict:
    return person_service.get_statistics()
