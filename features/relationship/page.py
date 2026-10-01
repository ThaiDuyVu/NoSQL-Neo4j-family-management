"""
============================================================
FEATURE OWNER: SƠN
DOMAIN: RELATIONSHIP MANAGEMENT
============================================================

Responsibilities:
- UI Streamlit: thêm / xóa / xem relationship
- CHỈ gọi features/relationship/service.py
  (và features/person/service.py để lấy danh sách Person cho selectbox)
- KHÔNG viết Cypher

============================================================
"""
import streamlit as st

from features.relationship import service  # noqa: F401
from shared.ui import page_header, show_todo


def render() -> None:
    page_header("Quản lý Relationship", owner="Sơn", description="FATHER_OF, MOTHER_OF, SPOUSE_OF.")

    tab_add, tab_view, tab_remove = st.tabs(["➕ Thêm quan hệ", "👀 Xem quan hệ", "🗑️ Xóa quan hệ"])
    with tab_add:
        show_todo("Sơn", ["Selectbox Person A, Person B (lấy từ person.service.list_persons)",
                          "Chọn loại quan hệ", "Gọi service.add_relationship, hiển thị lỗi validation"])
    with tab_view:
        show_todo("Sơn", ["Chọn Person -> bảng quan hệ (service.get_relationships_of_person)",
                          "Bảng toàn bộ quan hệ (service.list_relationships)"])
    with tab_remove:
        show_todo("Sơn", ["Chọn quan hệ cần xóa + xác nhận (service.remove_relationship)"])
