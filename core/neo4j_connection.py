"""
============================================================
SHARED FILE - CẢ NHÓM
============================================================
Kết nối Neo4j dùng chung. Repository của MỌI feature gọi qua đây.

Interface (đừng đổi signature nếu chưa báo nhóm):
- get_driver()
- close_driver()
- verify_connection() -> (ok, message)
- run_read(query, params) -> list[dict]
- run_write(query, params) -> list[dict]

Quy tắc:
- Hạn chế chỉnh nếu không cần.
- Không xóa code của thành viên khác.
- Không đặt business logic / Cypher riêng của feature vào đây.
============================================================
"""
from typing import Any, Optional

from neo4j import Driver, GraphDatabase

from core.config import settings

_driver: Optional[Driver] = None


def get_driver() -> Driver:
    """Lazy singleton driver."""
    global _driver
    if _driver is None:
        _driver = GraphDatabase.driver(
            settings.neo4j_uri,
            auth=(settings.neo4j_user, settings.neo4j_password),
        )
    return _driver


def close_driver() -> None:
    global _driver
    if _driver is not None:
        _driver.close()
        _driver = None


def verify_connection() -> tuple[bool, str]:
    try:
        get_driver().verify_connectivity()
        return True, "Connected"
    except Exception as exc:  # noqa: BLE001
        return False, str(exc)


def run_read(query: str, params: Optional[dict[str, Any]] = None) -> list[dict[str, Any]]:
    """Chạy query đọc. Node được trả về dạng dict các property."""
    with get_driver().session(database=settings.neo4j_database) as session:
        return session.execute_read(
            lambda tx: [record.data() for record in tx.run(query, params or {})]
        )


def run_write(query: str, params: Optional[dict[str, Any]] = None) -> list[dict[str, Any]]:
    """Chạy query ghi (CREATE / MERGE / SET / DELETE)."""
    with get_driver().session(database=settings.neo4j_database) as session:
        return session.execute_write(
            lambda tx: [record.data() for record in tx.run(query, params or {})]
        )
