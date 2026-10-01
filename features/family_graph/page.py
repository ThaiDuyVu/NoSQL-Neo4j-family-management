"""
============================================================
FEATURE OWNER: SƠN
DOMAIN: FAMILY GRAPH VISUALIZATION
============================================================

Responsibilities:
- UI hiển thị cây/graph gia đình
- CHỈ gọi features/family_graph/service.py

============================================================
"""
import streamlit as st  # noqa: F401

from features.family_graph import service  # noqa: F401
from shared.ui import page_header, show_todo


def render() -> None:
    page_header("Family Graph", owner="Sơn", description="Trực quan hóa quan hệ gia đình.")
    show_todo(
        "Sơn",
        [
            "Chọn Person gốc (hoặc 'toàn bộ') + slider độ sâu",
            "Gọi service.build_graph_data và service.render_graph_html",
            "Nhúng HTML bằng st.components.v1.html",
            "Chú thích màu (nam/nữ, loại quan hệ)",
        ],
    )
