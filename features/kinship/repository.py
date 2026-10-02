"""
============================================================
FEATURE OWNER: ĐẠT
DOMAIN: KINSHIP RESOLVER
============================================================

Responsibilities:
- Cypher tìm đường đi quan hệ giữa 2 Person (shortestPath)
- KHÔNG query CRUD Person, KHÔNG query thêm/xóa relationship

Gợi ý: shortestPath chạy vô hướng trên FATHER_OF|MOTHER_OF|SPOUSE_OF.
Cần trả đủ thông tin để suy ra HƯỚNG từng cạnh (cha->con hay con->cha)
và GIỚI TÍNH/NGÀY SINH từng node trên đường đi.

============================================================
"""
from typing import Optional

from core.neo4j_connection import run_read  # noqa: F401


def find_shortest_path(person_a_id: str, person_b_id: str, max_depth: int = 10) -> Optional[dict]:
    """Tìm đường quan hệ ngắn nhất và trả đủ node/cạnh để suy ra hướng."""
    depth = _validate_depth(max_depth)
    if not person_a_id or not person_b_id:
        return None
    query = f"""
        MATCH (a:Person {{id: $person_a_id}}), (b:Person {{id: $person_b_id}})
        MATCH path = shortestPath(
            (a)-[:FATHER_OF|MOTHER_OF|SPOUSE_OF*1..{depth}]-(b)
        )
        RETURN
            [node IN nodes(path) | node{{.id, .full_name, .gender, .birth_date}}] AS nodes,
            [rel IN relationships(path) | {{
                type: type(rel),
                start_id: startNode(rel).id,
                end_id: endNode(rel).id
            }}] AS relationships
        LIMIT 1
    """
    rows = run_read(
        query,
        {
            "person_a_id": person_a_id.strip(),
            "person_b_id": person_b_id.strip(),
        },
    )
    return rows[0] if rows else None


def find_all_shortest_paths(person_a_id: str, person_b_id: str, max_depth: int = 10) -> list[dict]:
    """Trả mọi đường đi ngắn nhất giữa hai Person trong giới hạn độ sâu."""
    depth = _validate_depth(max_depth)
    if not person_a_id or not person_b_id:
        return []
    query = f"""
        MATCH (a:Person {{id: $person_a_id}}), (b:Person {{id: $person_b_id}})
        MATCH path = allShortestPaths(
            (a)-[:FATHER_OF|MOTHER_OF|SPOUSE_OF*1..{depth}]-(b)
        )
        RETURN
            [node IN nodes(path) | node{{.id, .full_name, .gender, .birth_date}}] AS nodes,
            [rel IN relationships(path) | {{
                type: type(rel),
                start_id: startNode(rel).id,
                end_id: endNode(rel).id
            }}] AS relationships
    """
    return run_read(
        query,
        {
            "person_a_id": person_a_id.strip(),
            "person_b_id": person_b_id.strip(),
        },
    )


def _validate_depth(max_depth: int) -> int:
    if isinstance(max_depth, bool) or not isinstance(max_depth, int):
        raise ValueError("max_depth phải là số nguyên")
    if not 1 <= max_depth <= 20:
        raise ValueError("max_depth phải nằm trong khoảng 1 đến 20")
    return max_depth
