"""
============================================================
FEATURE OWNER: ĐẠT
DOMAIN: KINSHIP RESOLVER
============================================================

Responsibilities:
- Điều phối: tìm path -> phân tích path -> resolver -> KinshipResult
- Lấy danh sách Person qua features/person/service.py
  (KHÔNG import person.repository)
- Business logic kinship nằm Ở ĐÂY và resolver.py, KHÔNG nằm trong app.py

============================================================
"""
from features.kinship import resolver  # noqa: F401
from features.person import service as person_service  # noqa: F401
from features.relationship_search import service as search_service  # noqa: F401
from features.kinship.resolver import KinshipResult


def list_selectable_persons() -> list[dict]:
    """OWNER: Đạt — TODO: lấy Person cho selectbox A/B qua person_service.list_persons()."""
    raise NotImplementedError


def find_kinship(person_a_id: str, person_b_id: str) -> KinshipResult:
    """
    OWNER: Đạt

    TODO:
    - validate: A và B đã chọn, A != B (xử lý rõ ràng nếu A == B)
    - lấy genders của A, B (person_service.get_person)
    - steps = search_service.search_relationship_path(a, b)
    - nếu không có path -> KinshipResult(found=False, message=...)
    - resolver.resolve_kinship(steps, a_gender, b_gender)
    - gắn path_text bằng search_service.format_path_text
    """
    raise NotImplementedError
