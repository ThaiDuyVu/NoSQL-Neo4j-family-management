import streamlit as st
from features.relationship.service import RelationshipService
from core.constants import RELATIONSHIP_TYPES

# Import động PersonService/list_persons từ Vũ
try:
    from features.person import service as person_service_module
except Exception:
    person_service_module = None


def _get_all_persons():
    """Hàm lấy danh sách person linh hoạt không lo lỗi import từ Person Service."""
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
    st.header("🔗 Quản Lý Quan Hệ Gia Đình (Relationship)")

    rel_service = RelationshipService()

    # Lấy danh sách person hiển thị trong selectbox
    persons = _get_all_persons()
    if not persons:
        st.warning("Chưa có thành viên nào trong hệ thống hoặc không tải được dữ liệu Person.")
        return

    person_options = {
        f"{p.get('name', p.get('id'))} ({p.get('id')})": p.get('id') 
        for p in persons
    }

    # Đảm bảo RELATIONSHIP_TYPES là danh sách hiển thị được
    if isinstance(RELATIONSHIP_TYPES, dict):
        rel_type_options = list(RELATIONSHIP_TYPES.values())
    elif isinstance(RELATIONSHIP_TYPES, (tuple, list, set)):
        rel_type_options = list(RELATIONSHIP_TYPES)
    else:
        rel_type_options = ["FATHER_OF", "MOTHER_OF", "SPOUSE_OF"]

    tab1, tab2, tab3 = st.tabs(["➕ Thêm Quan Hệ", "📋 Xem Danh Sách", "❌ Xóa Quan Hệ"])

    # ---------------- TAB 1: THÊM QUAN HỆ ----------------
    with tab1:
        st.subheader("Thêm mối quan hệ mới")
        col1, col2 = st.columns(2)

        with col1:
            source_label = st.selectbox("Thành viên gốc (Source/Nguồn):", list(person_options.keys()), key="add_rel_source")
            source_id = person_options[source_label]

            rel_type = st.selectbox("Loại quan hệ:", rel_type_options, key="add_rel_type")

        with col2:
            target_label = st.selectbox("Thành viên đích (Target/Đích):", list(person_options.keys()), key="add_rel_target")
            target_id = person_options[target_label]

        st.caption("Gợi ý: FATHER_OF/MOTHER_OF có nghĩa là [Nguồn] là Cha/Mẹ của [Đích].")

        if st.button("Xác nhận tạo quan hệ", type="primary"):
            try:
                success = rel_service.add_relationship(source_id, target_id, rel_type)
                if success:
                    st.success("Tạo mối quan hệ thành công!")
            except ValueError as e:
                st.error(f"Lỗi: {str(e)}")
            except Exception as e:
                st.error(f"Đã xảy ra lỗi hệ thống: {str(e)}")

    # ---------------- TAB 2: XEM QUAN HỆ ----------------
    with tab2:
        st.subheader("Danh sách quan hệ")
        filter_mode = st.radio("Chế độ xem:", ["Tất cả quan hệ", "Theo cá nhân"], horizontal=True)

        if filter_mode == "Tất cả quan hệ":
            rels = rel_service.list_relationships()
            if rels:
                st.dataframe(rels, use_container_width=True)
            else:
                st.info("Chưa có quan hệ nào được thiết lập.")
        else:
            selected_person_label = st.selectbox("Chọn cá nhân:", list(person_options.keys()), key="view_rel_person")
            selected_person_id = person_options[selected_person_label]
            person_rels = rel_service.get_relationships_of_person(selected_person_id)
            if person_rels:
                st.dataframe(person_rels, use_container_width=True)
            else:
                st.info("Cá nhân này chưa có quan hệ nào.")

    # ---------------- TAB 3: XÓA QUAN HỆ ----------------
    with tab3:
        st.subheader("Xóa mối quan hệ")
        all_rels = rel_service.list_relationships()

        if not all_rels:
            st.info("Không có quan hệ nào để xóa.")
        else:
            rel_del_options = {
                f"{r.get('source_name', r.get('source_id'))} --[{r.get('rel_type')}]--> {r.get('target_name', r.get('target_id'))}": r
                for r in all_rels
            }
            selected_del_label = st.selectbox("Chọn quan hệ cần xóa:", list(rel_del_options.keys()))
            selected_rel = rel_del_options[selected_del_label]

            if st.button("Xác nhận xóa quan hệ", type="primary"):
                try:
                    success = rel_service.remove_relationship(
                        selected_rel['source_id'],
                        selected_rel['target_id'],
                        selected_rel['rel_type']
                    )
                    if success:
                        st.success("Xóa quan hệ thành công!")
                        st.rerun()
                    else:
                        st.error("Xóa thất bại.")
                except Exception as e:
                    st.error(f"Lỗi khi xóa: {str(e)}")