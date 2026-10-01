"""
============================================================
FEATURE OWNER: SƠN
DOMAIN: RELATIONSHIP MANAGEMENT
============================================================

Responsibilities:
- Thêm / xóa / xem relationship FATHER_OF, MOTHER_OF, SPOUSE_OF
- Validation relationship (business rules)
- Lấy thông tin Person thông qua features/person/service.py
  (KHÔNG import person.repository)

PUBLIC INTERFACE cho family_graph / kinship:
- get_relationships_of_person(person_id)
- get_graph_edges(root_id, depth)

============================================================
"""
from typing import Optional

from features.person import service as person_service  # noqa: F401
from features.relationship import repository  # noqa: F401


def add_relationship(from_id: str, to_id: str, rel_type: str) -> dict:
    """
    OWNER: Sơn

    TODO:
    - validate_relationship(...)
    - call repository.create_relationship
    - trả relationship vừa tạo
    """
    raise NotImplementedError


def remove_relationship(from_id: str, to_id: str, rel_type: str) -> None:
    """
    OWNER: Sơn

    TODO:
    - kiểm tra relationship tồn tại
    - call repository.delete_relationship
    """
    raise NotImplementedError


def get_relationships_of_person(person_id: str) -> list[dict]:
    """OWNER: Sơn — TODO: kiểm tra person tồn tại (person_service.get_person) rồi gọi repository."""
    raise NotImplementedError


def list_relationships(skip: int = 0, limit: int = 200) -> list[dict]:
    """OWNER: Sơn — TODO: gọi repository.find_all_relationships."""
    raise NotImplementedError


def get_graph_edges(root_id: Optional[str] = None, depth: int = 2) -> list[dict]:
    """OWNER: Sơn — TODO: validate depth (>=1, giới hạn trên) rồi gọi repository.get_graph_edges."""
    raise NotImplementedError


def validate_relationship(from_id: str, to_id: str, rel_type: str) -> None:
    """
    OWNER: Sơn

    TODO (raise ValueError với thông báo rõ ràng):
    - rel_type thuộc RELATIONSHIP_TYPES
    - from_id != to_id
    - hai Person đều tồn tại
    - FATHER_OF: người cha phải MALE; MOTHER_OF: người mẹ phải FEMALE
    - mỗi người tối đa 1 cha và 1 mẹ
    - không tạo vòng lặp tổ tiên (repository.is_ancestor)
    - không trùng relationship đã có
    - SPOUSE_OF: giới hạn số vợ/chồng; không cho vợ/chồng là cha/mẹ/con của nhau
    - (tùy chọn) kiểm tra chênh lệch tuổi cha/mẹ - con
    """
    raise NotImplementedError
