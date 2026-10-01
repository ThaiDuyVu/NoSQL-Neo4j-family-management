"""
============================================================
FEATURE OWNER: ĐẠT
DOMAIN: KINSHIP RESOLVER
============================================================

Responsibilities:
- UI: chọn Person A, Person B, hiển thị cách xưng hô + đường đi quan hệ
- CHỈ gọi features/kinship/service.py
- KHÔNG viết Cypher, KHÔNG viết logic xưng hô ở đây

============================================================
"""
import streamlit as st  # noqa: F401

from features.kinship import service  # noqa: F401
from shared.ui import page_header, show_todo


def render() -> None:
    page_header("Kinship Search", owner="Đạt", description="Tìm đường đi quan hệ và cách xưng hô giữa 2 người.")
    show_todo(
        "Đạt",
        [
            "Selectbox Person A và Person B (service.list_selectable_persons)",
            "Nút 'Tìm quan hệ' -> service.find_kinship",
            "Hiển thị: A gọi B là ..., B gọi A là ...",
            "Hiển thị đường đi quan hệ (path_text / từng step)",
            "Thông báo khi không tìm thấy quan hệ hoặc chọn A == B",
        ],
    )
