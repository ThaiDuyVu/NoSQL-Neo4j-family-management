"""
============================================================
SHARED FILE - CẢ NHÓM  (app.py)
============================================================
Entry point của Streamlit. Chạy:  streamlit run app.py

Quy tắc:
- Mỗi người CHỈ sửa block TAKE NOTE của mình.
- Không viết business logic / Cypher ở đây.
- Muốn thêm trang mới: import page.render của feature rồi khai báo st.Page.
============================================================
"""
import streamlit as st

st.set_page_config(page_title="Quản lý nhân thân - Neo4j", page_icon="🌳", layout="wide")

from core.neo4j_connection import verify_connection  # noqa: E402


# ==========================================================
# TAKE NOTE - VŨ
#
# Vũ khai báo navigation/page của:
# - Dashboard
# - Person
#
# Không viết business logic tại đây.
# ==========================================================
from features.dashboard import page as dashboard_page  # noqa: E402
from features.person import page as person_page  # noqa: E402

VU_PAGES = [
    st.Page(dashboard_page.render, title="Dashboard", icon="📊", url_path="dashboard", default=True),
    st.Page(person_page.render, title="Person", icon="👤", url_path="person"),
]


# ==========================================================
# TAKE NOTE - SƠN
#
# Sơn khai báo navigation/page của:
# - Relationship
# - Family Graph
#
# Không viết business logic tại đây.
# ==========================================================
from features.family_graph import page as family_graph_page  # noqa: E402
from features.relationship import page as relationship_page  # noqa: E402

SON_PAGES = [
    st.Page(relationship_page.render, title="Relationship", icon="🔗", url_path="relationship"),
    st.Page(family_graph_page.render, title="Family Graph", icon="🌳", url_path="family-graph"),
]


# ==========================================================
# TAKE NOTE - ĐẠT
#
# Đạt khai báo navigation/page của:
# - Kinship Search
#
# Không viết business logic tại đây.
# ==========================================================
from features.kinship import page as kinship_page  # noqa: E402

DAT_PAGES = [
    st.Page(kinship_page.render, title="Kinship Search", icon="🧭", url_path="kinship"),
]


# ==========================================================
# KHU VỰC CHUNG - không chỉnh nếu không cần
# ==========================================================
navigation = st.navigation(
    {
        "Vũ · Person & Dashboard": VU_PAGES,
        "Sơn · Relationship & Graph": SON_PAGES,
        "Đạt · Kinship": DAT_PAGES,
    }
)

ok, message = verify_connection()
if ok:
    st.sidebar.success("Neo4j: đã kết nối")
else:
    st.sidebar.error("Neo4j: chưa kết nối")
    st.sidebar.caption(message)

navigation.run()
