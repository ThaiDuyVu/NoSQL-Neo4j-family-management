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
    """
    OWNER: Đạt

    TODO:
    - gọi repository.find_shortest_path
    - None nếu không có đường đi
    - gọi build_steps_from_raw_path để chuyển kết quả
    """
    raise NotImplementedError


def build_steps_from_raw_path(raw_path: dict, person_a_id: str) -> list[PathStep]:
    """
    OWNER: Đạt

    TODO:
    - đi dọc path từ A đến B theo thứ tự
    - xác định direction từng step: UP / DOWN / SPOUSE
      (dựa vào type + start_id/end_id của relationship so với chiều đi)
    - điền giới tính, ngày sinh vào PathStep
    """
    raise NotImplementedError


def format_path_text(steps: list[PathStep], persons_by_id: dict[str, dict]) -> str:
    """
    OWNER: Đạt

    TODO:
    - ví dụ: "Phúc → (con của) Dũng → (con của) An"
    - xử lý path rỗng
    """
    raise NotImplementedError
