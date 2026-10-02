"""Dashboard for Person counts."""
import streamlit as st

from features.dashboard import service
from shared.ui import page_header


def render() -> None:
    page_header("Dashboard", owner="Vũ", description="Tổng quan dữ liệu nhân thân.")
    try:
        stats = service.get_dashboard_stats()
    except Exception as exc:
        st.error(f"Không tải được thống kê từ Neo4j: {exc}")
        return
    total, male, female = st.columns(3)
    total.metric("Tổng số người", stats["total"])
    male.metric("Nam", stats["male"])
    female.metric("Nữ", stats["female"])
    if stats["total"] == 0:
        st.info("Chưa có dữ liệu Person.")
