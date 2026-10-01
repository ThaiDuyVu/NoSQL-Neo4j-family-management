"""
============================================================
FEATURE OWNER: SƠN
DOMAIN: RELATIONSHIP MANAGEMENT
============================================================

Responsibilities:
- Toàn bộ Cypher liên quan FATHER_OF / MOTHER_OF / SPOUSE_OF
- Query phục vụ validation relationship (đếm cha/mẹ, kiểm tra vòng lặp)
- Query dữ liệu graph cho family_graph
- KHÔNG query CRUD node Person (thuộc domain Vũ)

Lưu ý: relationship type KHÔNG parametrize được trong Cypher.
Nếu build query bằng f-string, PHẢI kiểm tra rel_type nằm trong
core.constants.RELATIONSHIP_TYPES trước (tránh Cypher injection).

============================================================
"""
from typing import Optional

from core.neo4j_connection import run_read, run_write  # noqa: F401


def create_relationship(from_id: str, to_id: str, rel_type: str) -> dict:
    """
    OWNER: Sơn

    TODO:
    - MATCH 2 Person theo id, MERGE relationship (tránh tạo trùng)
    - whitelist rel_type
    """
    raise NotImplementedError


def delete_relationship(from_id: str, to_id: str, rel_type: str) -> bool:
    """OWNER: Sơn — TODO: xóa đúng 1 relationship; trả True nếu có xóa."""
    raise NotImplementedError


def relationship_exists(from_id: str, to_id: str, rel_type: str) -> bool:
    """OWNER: Sơn — TODO: kiểm tra đã tồn tại (SPOUSE_OF cần kiểm tra cả 2 chiều)."""
    raise NotImplementedError


def find_relationships_of_person(person_id: str) -> list[dict]:
    """
    OWNER: Sơn

    TODO:
    - trả mọi relationship liên quan person (cả đi ra và đi vào)
    - mỗi phần tử gồm: from_id, from_name, to_id, to_name, type
    """
    raise NotImplementedError


def find_all_relationships(skip: int = 0, limit: int = 200) -> list[dict]:
    """OWNER: Sơn — TODO: liệt kê toàn bộ relationship (cùng format trên)."""
    raise NotImplementedError


def count_parents(child_id: str, rel_type: str) -> int:
    """OWNER: Sơn — TODO: đếm số cha (FATHER_OF) hoặc mẹ (MOTHER_OF) hiện có của child."""
    raise NotImplementedError


def count_spouses(person_id: str) -> int:
    """OWNER: Sơn — TODO: đếm số vợ/chồng hiện có (query vô hướng)."""
    raise NotImplementedError


def is_ancestor(possible_ancestor_id: str, person_id: str) -> bool:
    """
    OWNER: Sơn

    TODO:
    - kiểm tra possible_ancestor có là tổ tiên của person không
      (dùng path độ dài biến đổi trên FATHER_OF|MOTHER_OF)
    - dùng để chặn vòng lặp: A là cha của B thì B không thể là cha/mẹ của A
    """
    raise NotImplementedError


def get_graph_edges(root_id: Optional[str] = None, depth: int = 2) -> list[dict]:
    """
    OWNER: Sơn

    TODO:
    - lấy các cạnh trong phạm vi `depth` quanh root_id (root_id=None -> toàn bộ graph)
    - kèm thông tin node (id, full_name, gender) hai đầu để vẽ graph
    """
    raise NotImplementedError
