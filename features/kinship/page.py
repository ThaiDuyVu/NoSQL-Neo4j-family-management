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
from shared.ui import page_header, person_label


def render() -> None:
    page_header("Kinship Search", owner="Đạt", description="Tìm đường đi quan hệ và cách xưng hô giữa 2 người.")
    try:
        persons = service.list_selectable_persons()
    except Exception as exc:  # noqa: BLE001 - lỗi kết nối được hiển thị trên UI
        st.error(f"Không thể tải danh sách Person: {exc}")
        return

    if len(persons) < 2:
        st.warning("Cần ít nhất hai Person để tìm quan hệ.")
        return

    persons_by_id = {person["id"]: person for person in persons}
    person_ids = list(persons_by_id)
    col_a, col_b = st.columns(2)
    with col_a:
        person_a_id = st.selectbox(
            "Person A",
            person_ids,
            format_func=lambda person_id: person_label(persons_by_id[person_id]),
        )
    with col_b:
        person_b_id = st.selectbox(
            "Person B",
            person_ids,
            index=1,
            format_func=lambda person_id: person_label(persons_by_id[person_id]),
        )

    if not st.button("Tìm quan hệ", type="primary", use_container_width=True):
        return

    try:
        result = service.find_kinship(person_a_id, person_b_id)
    except Exception as exc:  # noqa: BLE001 - không để lỗi Neo4j làm page crash
        st.error(f"Không thể tìm quan hệ: {exc}")
        return

    if not result.found:
        st.warning(result.message)
        return

    person_a = persons_by_id[person_a_id]
    person_b = persons_by_id[person_b_id]
    result_col_a, result_col_b = st.columns(2)
    with result_col_a:
        st.subheader(f"{person_a['full_name']} gọi {person_b['full_name']}")
        st.success(result.a_calls_b)
    with result_col_b:
        st.subheader(f"{person_b['full_name']} gọi {person_a['full_name']}")
        st.success(result.b_calls_a)

    if result.message:
        st.info(result.message)
    st.markdown("#### Đường đi quan hệ")
    st.write(result.path_text)

    with st.expander("Chi tiết từng bước"):
        for index, step in enumerate(result.steps, start=1):
            st.write(
                f"{index}. {step.from_name or step.from_id} → "
                f"{step.to_name or step.to_id} "
                f"({step.rel_type}, {step.direction})"
            )
