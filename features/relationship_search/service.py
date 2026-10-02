"""
============================================================
FEATURE OWNER: ĐẠT
DOMAIN: RELATIONSHIP SEARCH
============================================================

Responsibilities:
- Tìm và phân tích đường đi quan hệ giữa 2 Person
- Chuyển raw path từ Neo4j thành list[PathStep]
- Format đường đi thành chuỗi hiển thị
- Dùng features/kinship/repository.py (cùng domain Đạt)

============================================================
"""
from typing import Optional

from features.kinship import repository  # noqa: F401
from features.kinship.resolver import PathStep


def search_relationship_path(person_a_id: str, person_b_id: str, max_depth: int = 10) -> Optional[list[PathStep]]:
    """Tìm raw path rồi chuyển thành danh sách ``PathStep`` từ A đến B."""
    raw_path = repository.find_shortest_path(person_a_id, person_b_id, max_depth)
    if raw_path is None:
        return None
    return build_steps_from_raw_path(raw_path, person_a_id)


def build_steps_from_raw_path(raw_path: dict, person_a_id: str) -> list[PathStep]:
    """Chuẩn hóa node/cạnh Neo4j thành các bước có hướng UP/DOWN/SPOUSE."""
    nodes = list(raw_path.get("nodes") or [])
    relationships = list(raw_path.get("relationships") or [])
    if not nodes:
        return []
    if len(relationships) != len(nodes) - 1:
        raise ValueError("Dữ liệu path không hợp lệ: số cạnh không khớp số node")

    if nodes[0].get("id") != person_a_id:
        if nodes[-1].get("id") != person_a_id:
            raise ValueError("Dữ liệu path không bắt đầu hoặc kết thúc tại Person A")
        nodes.reverse()
        relationships.reverse()

    steps: list[PathStep] = []
    for index, relationship in enumerate(relationships):
        from_node = nodes[index]
        to_node = nodes[index + 1]
        from_id = from_node.get("id", "")
        to_id = to_node.get("id", "")
        rel_type = relationship.get("type", "")
        start_id = relationship.get("start_id")
        end_id = relationship.get("end_id")

        if {from_id, to_id} != {start_id, end_id}:
            raise ValueError("Dữ liệu path không hợp lệ: cạnh không nối hai node liền kề")
        if rel_type == "SPOUSE_OF":
            direction = "SPOUSE"
        elif rel_type in {"FATHER_OF", "MOTHER_OF"}:
            direction = "DOWN" if from_id == start_id else "UP"
        else:
            raise ValueError(f"Loại quan hệ không được hỗ trợ: {rel_type}")

        steps.append(
            PathStep(
                from_id=from_id,
                to_id=to_id,
                rel_type=rel_type,
                direction=direction,
                from_gender=from_node.get("gender") or "",
                to_gender=to_node.get("gender") or "",
                from_birth_date=from_node.get("birth_date"),
                to_birth_date=to_node.get("birth_date"),
                from_name=from_node.get("full_name") or "",
                to_name=to_node.get("full_name") or "",
            )
        )
    return steps


def format_path_text(steps: list[PathStep], persons_by_id: dict[str, dict]) -> str:
    """Định dạng path thành câu dễ đọc để hiển thị trên Streamlit."""
    if not steps:
        return ""

    def display_name(person_id: str, fallback: str) -> str:
        person = persons_by_id.get(person_id, {})
        return person.get("full_name") or fallback or person_id

    parts = [display_name(steps[0].from_id, steps[0].from_name)]
    for step in steps:
        if step.direction == "UP":
            phrase = "con của"
        elif step.direction == "DOWN":
            phrase = "cha của" if step.rel_type == "FATHER_OF" else "mẹ của"
        else:
            phrase = "vợ/chồng của"
        parts.append(f"→ ({phrase}) {display_name(step.to_id, step.to_name)}")
    return " ".join(parts)
