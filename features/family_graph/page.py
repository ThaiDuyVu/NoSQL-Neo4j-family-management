import streamlit as st
import streamlit.components.v1 as components
from features.family_graph.service import FamilyGraphService

# Import động PersonService/list_persons từ Vũ
try:
    from features.person import service as person_service_module
except Exception:
    person_service_module = None


def _get_all_persons():
    """Hàm lấy danh sách person linh hoạt không lo lỗi import."""
    if not person_service_module:
        return []
    
    if hasattr(person_service_module, "PersonService"):
        ps = person_service_module.PersonService()
        if hasattr(ps, "list_persons"):
            return ps.list_persons()
        elif hasattr(ps, "get_all_persons"):
            return ps.get_all_persons()
    elif hasattr(person_service_module, "list_persons"):
        return person_service_module.list_persons()
    elif hasattr(person_service_module, "get_all_persons"):
        return person_service_module.get_all_persons()
    
    return []


def render():
    st.header("🌳 Đồ Thị Gia Tộc (Family Graph)")

    graph_service = FamilyGraphService()
    persons = _get_all_persons()

    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("**Ghi chú màu sắc:** 🟢 Nam | 🔴 Nữ | 🔵 Quan hệ Cha/Mẹ-Con | 🟣 Quan hệ Vợ-Chồng")

    root_id = None
    depth = 2

    with col2:
        use_filter = st.checkbox("Lọc theo cá nhân tâm điểm")
        if use_filter and persons:
            person_options = {
                f"{p.get('name', p.get('id'))} ({p.get('id')})": p.get('id')
                for p in persons
            }
            selected_person = st.selectbox("Chọn cá nhân:", list(person_options.keys()))
            root_id = person_options[selected_person]
            depth = st.slider("Bán kính đào sâu (Depth):", min_value=1, max_value=5, value=2)

    html_graph = graph_service.render_graph_html(root_person_id=root_id, depth=depth)
    components.html(html_graph, height=600)