"""
============================================================
FEATURE OWNER: VŨ
DOMAIN: DASHBOARD
============================================================

Responsibilities:
- Tổng hợp số liệu cho Dashboard
- Lấy dữ liệu thông qua features/person/service.py (không viết Cypher ở đây)

============================================================
"""
from features.person import service as person_service  # noqa: F401


def get_dashboard_stats() -> dict:
    """
    OWNER: Vũ

    TODO:
    - lấy thống kê từ person_service.get_statistics()
    - trả {"total": int, "male": int, "female": int}
    - (tùy chọn) thêm tỉ lệ %, người mới thêm gần đây
    """
    raise NotImplementedError
