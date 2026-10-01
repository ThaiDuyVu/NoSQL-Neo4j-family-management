"""
============================================================
FEATURE OWNER: SƠN
DOMAIN: FAMILY GRAPH VISUALIZATION
============================================================

Responsibilities:
- Chuyển dữ liệu relationship thành nodes/edges để vẽ graph
- Lấy dữ liệu qua features/relationship/service.py
  (family_graph không có repository riêng, không viết Cypher ở đây)

============================================================
"""
from typing import Optional

from features.relationship import service as relationship_service  # noqa: F401


def build_graph_data(root_id: Optional[str] = None, depth: int = 2) -> dict:
    """
    OWNER: Sơn

    TODO:
    - lấy edges từ relationship_service.get_graph_edges
    - trả {"nodes": [{id, label, gender}], "edges": [{source, target, type}]}
    - loại node trùng
    """
    raise NotImplementedError


def render_graph_html(graph_data: dict) -> str:
    """
    OWNER: Sơn

    TODO:
    - dùng pyvis (hoặc thư viện khác) tạo HTML graph
    - màu node theo giới tính, màu/nhãn cạnh theo loại quan hệ
    - trả chuỗi HTML để page nhúng bằng st.components.v1.html
    """
    raise NotImplementedError
