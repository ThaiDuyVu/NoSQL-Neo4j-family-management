"""Dashboard service unit tests."""
from features.dashboard import service


def test_dashboard_stats_basic(monkeypatch):
    expected = {"total": 16, "male": 8, "female": 8}
    monkeypatch.setattr(service.person_service, "get_statistics", lambda: expected)
    assert service.get_dashboard_stats() == expected


def test_dashboard_stats_empty_database(monkeypatch):
    monkeypatch.setattr(service.person_service, "get_statistics", lambda: {"total": 0, "male": 0, "female": 0})
    assert service.get_dashboard_stats() == {"total": 0, "male": 0, "female": 0}
