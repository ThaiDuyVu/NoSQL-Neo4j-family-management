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
    """Lấy và sắp xếp danh sách Person dùng cho hai selectbox."""
    persons = person_service.list_persons(limit=1000)
    return sorted(persons, key=lambda person: (person.get("full_name") or "", person.get("id") or ""))


def find_kinship(person_a_id: str, person_b_id: str) -> KinshipResult:
    """Điều phối validate, tìm path, resolve xưng hô và format kết quả."""
    person_a_id = (person_a_id or "").strip()
    person_b_id = (person_b_id or "").strip()
    if not person_a_id or not person_b_id:
        return KinshipResult(found=False, message="Vui lòng chọn đủ Person A và Person B.")
    if person_a_id == person_b_id:
        return KinshipResult(
            found=False,
            person_a_id=person_a_id,
            person_b_id=person_b_id,
            message="Person A và Person B phải là hai người khác nhau.",
        )

    person_a = person_service.get_person(person_a_id)
    person_b = person_service.get_person(person_b_id)
    if person_a is None or person_b is None:
        missing_id = person_a_id if person_a is None else person_b_id
        return KinshipResult(
            found=False,
            person_a_id=person_a_id,
            person_b_id=person_b_id,
            message=f"Không tìm thấy Person {missing_id}.",
        )

    steps = search_service.search_relationship_path(person_a_id, person_b_id)
    if steps is None:
        return KinshipResult(
            found=False,
            person_a_id=person_a_id,
            person_b_id=person_b_id,
            message="Không tìm thấy đường đi quan hệ giữa hai người.",
        )

    result = resolver.resolve_kinship(
        steps,
        person_a.get("gender") or "",
        person_b.get("gender") or "",
    )
    persons_by_id = {
        person_a_id: person_a,
        person_b_id: person_b,
    }
    for step in steps:
        persons_by_id.setdefault(step.from_id, {"full_name": step.from_name})
        persons_by_id.setdefault(step.to_id, {"full_name": step.to_name})

    result.person_a_id = person_a_id
    result.person_b_id = person_b_id
    result.steps = steps
    result.path_text = search_service.format_path_text(steps, persons_by_id)
    return result
