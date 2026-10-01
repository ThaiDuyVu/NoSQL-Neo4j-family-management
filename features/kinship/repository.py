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
    """
    OWNER: Đạt

    TODO:
    - MATCH 2 Person, shortestPath giữa chúng, giới hạn max_depth
    - trả None nếu không có đường đi
    - trả dict: {"nodes": [{id, full_name, gender, birth_date}, ...],
                 "relationships": [{type, start_id, end_id}, ...]}
    """
    raise NotImplementedError


def find_all_shortest_paths(person_a_id: str, person_b_id: str, max_depth: int = 10) -> list[dict]:
    """OWNER: Đạt — TODO (tùy chọn): allShortestPaths khi có nhiều đường ngắn nhất."""
    raise NotImplementedError
