"""
============================================================
FEATURE OWNER: VŨ
DOMAIN: DASHBOARD
============================================================

Responsibilities:
- UI Dashboard: tổng số người, thống kê nam / nữ
- CHỈ gọi features/dashboard/service.py

============================================================
"""
import streamlit as st  # noqa: F401

from features.dashboard import service  # noqa: F401
from shared.ui import page_header, show_todo


def render() -> None:
    page_header("Dashboard", owner="Vũ", description="Tổng quan dữ liệu nhân thân.")
    show_todo(
        "Vũ",
        [
            "Gọi service.get_dashboard_stats()",
            "st.metric: tổng số người, số nam, số nữ",
            "(tùy chọn) biểu đồ tỉ lệ nam/nữ",
            "Xử lý khi database trống hoặc chưa kết nối Neo4j",
        ],
    )
