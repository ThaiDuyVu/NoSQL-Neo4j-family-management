"""
============================================================
FEATURE OWNER: VŨ
DOMAIN: PERSON MANAGEMENT
============================================================

Responsibilities:
- UI Streamlit: danh sách / thêm / sửa / xóa / tìm kiếm / chi tiết Person
- CHỈ gọi features/person/service.py
- KHÔNG viết Cypher, KHÔNG gọi repository trực tiếp

============================================================
"""
import streamlit as st

from features.person import service  # noqa: F401
from shared.ui import page_header, show_todo


def render() -> None:
    page_header("Quản lý Person", owner="Vũ", description="CRUD và tìm kiếm Person.")

    tab_list, tab_add, tab_edit, tab_detail = st.tabs(
        ["📋 Danh sách & tìm kiếm", "➕ Thêm", "✏️ Sửa / 🗑️ Xóa", "🔎 Chi tiết"]
    )
    with tab_list:
        show_todo("Vũ", ["Ô tìm kiếm + lọc giới tính", "Bảng danh sách Person (service.search_persons / list_persons)"])
    with tab_add:
        show_todo("Vũ", ["Form thêm Person", "Gọi service.create_person và hiển thị lỗi validation"])
    with tab_edit:
        show_todo("Vũ", ["Chọn Person -> form sửa (service.update_person)", "Nút xóa có xác nhận (service.delete_person)"])
    with tab_detail:
        show_todo("Vũ", ["Chọn Person -> hiển thị thông tin chi tiết (service.get_person)"])
