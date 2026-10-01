"""
============================================================
FEATURE OWNER: VŨ
DOMAIN: PERSON MANAGEMENT
============================================================

Responsibilities:
- Toàn bộ Cypher liên quan node (:Person)
- KHÔNG chứa query Relationship (thuộc domain Sơn / Đạt)
- KHÔNG chứa validation nghiệp vụ (nằm ở service.py)

============================================================
"""
from typing import Optional

from core.neo4j_connection import run_read, run_write  # noqa: F401


def create_person(person: dict) -> dict:
    """
    OWNER: Vũ

    TODO:
    - CREATE node (:Person) với các property của person
    - trả về property của node vừa tạo
    - để unique constraint bắt trùng id (service xử lý lỗi)
    """
    raise NotImplementedError


def find_by_id(person_id: str) -> Optional[dict]:
    """OWNER: Vũ — TODO: MATCH theo id, trả None nếu không có."""
    raise NotImplementedError


def exists_by_id(person_id: str) -> bool:
    """OWNER: Vũ — TODO: kiểm tra id đã tồn tại."""
    raise NotImplementedError


def find_all(skip: int = 0, limit: int = 100) -> list[dict]:
    """OWNER: Vũ — TODO: liệt kê Person, sắp xếp ổn định, có SKIP/LIMIT."""
    raise NotImplementedError


def search_by_keyword(keyword: str, gender: Optional[str] = None) -> list[dict]:
    """
    OWNER: Vũ

    TODO:
    - tìm theo full_name (không phân biệt hoa thường) hoặc id
    - lọc thêm theo gender nếu có
    """
    raise NotImplementedError


def update_person(person_id: str, changes: dict) -> Optional[dict]:
    """OWNER: Vũ — TODO: SET các property thay đổi, trả node sau update (None nếu không tồn tại)."""
    raise NotImplementedError


def delete_person(person_id: str) -> bool:
    """
    OWNER: Vũ

    TODO:
    - xóa node Person
    - quyết định: chặn xóa nếu còn relationship, hay DETACH DELETE? (thống nhất với Sơn)
    """
    raise NotImplementedError


def count_all() -> int:
    """OWNER: Vũ — TODO: tổng số Person (dùng cho Dashboard)."""
    raise NotImplementedError


def count_by_gender() -> dict[str, int]:
    """OWNER: Vũ — TODO: {"MALE": n, "FEMALE": m} (dùng cho Dashboard)."""
    raise NotImplementedError


def get_next_id() -> str:
    """OWNER: Vũ — TODO (tùy chọn): sinh id kế tiếp dạng P017 nếu muốn auto-id."""
    raise NotImplementedError
