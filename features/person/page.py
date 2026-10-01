"""Streamlit page for managing people."""
import streamlit as st

from core.constants import GENDER_LABELS_VI
from features.person import service
from shared.ui import page_header, person_label


def _people() -> list[dict]:
    return service.search_persons()


def _optional(value: str) -> str | None:
    return value.strip() or None


def render() -> None:
    page_header("Quản lý Person", owner="Vũ", description="CRUD và tìm kiếm Person.")
    if notice := st.session_state.pop("person_notice", None):
        st.success(notice)
    tab_list, tab_add, tab_edit, tab_detail = st.tabs(
        ["📋 Danh sách & tìm kiếm", "➕ Thêm", "✏️ Sửa / 🗑️ Xóa", "🔎 Chi tiết"]
    )
    with tab_list:
        keyword = st.text_input("Tìm theo tên hoặc ID", key="person_search")
        gender_label = st.selectbox("Giới tính", ["Tất cả", "Nam", "Nữ"], key="person_gender")
        gender = {"Tất cả": None, "Nam": "MALE", "Nữ": "FEMALE"}[gender_label]
        try:
            people = service.search_persons(keyword, gender)
            st.caption(f"{len(people)} người")
            st.dataframe(
                [{"ID": p["id"], "Họ tên": p["full_name"],
                  "Giới tính": GENDER_LABELS_VI.get(p["gender"], p["gender"]),
                  "Ngày sinh": p.get("birth_date") or ""} for p in people],
                use_container_width=True, hide_index=True,
            )
        except Exception as exc:
            st.error(f"Không tải được danh sách: {exc}")

    with tab_add:
        with st.form("add_person"):
            person_id = st.text_input("ID *", placeholder="P017")
            name = st.text_input("Họ tên *")
            gender = st.selectbox("Giới tính *", ["MALE", "FEMALE"], format_func=GENDER_LABELS_VI.get)
            birth = st.text_input("Ngày sinh", placeholder="YYYY-MM-DD")
            address = st.text_input("Địa chỉ")
            phone = st.text_input("Số điện thoại")
            note = st.text_area("Ghi chú")
            submitted = st.form_submit_button("Thêm Person")
        if submitted:
            try:
                service.create_person(person_id, name, gender, _optional(birth),
                                      _optional(address), _optional(phone), _optional(note))
                st.session_state["person_notice"] = f"Đã thêm {name.strip()} ({person_id.strip()})."
                st.rerun()
            except ValueError as exc:
                st.error(str(exc))
            except Exception as exc:
                st.error(f"Không thể thêm Person: {exc}")

    with tab_edit:
        try:
            people = _people()
        except Exception as exc:
            st.error(f"Không tải được Person: {exc}")
            people = []
        if not people:
            st.info("Chưa có Person để sửa hoặc xóa.")
        else:
            selected = st.selectbox("Chọn Person", people, format_func=person_label, key="person_edit")
            with st.form(f"edit_{selected['id']}"):
                name = st.text_input("Họ tên *", value=selected.get("full_name") or "")
                gender = st.selectbox("Giới tính *", ["MALE", "FEMALE"],
                                      index=["MALE", "FEMALE"].index(selected["gender"]),
                                      format_func=GENDER_LABELS_VI.get)
                birth = st.text_input("Ngày sinh", value=selected.get("birth_date") or "")
                address = st.text_input("Địa chỉ", value=selected.get("address") or "")
                phone = st.text_input("Số điện thoại", value=selected.get("phone") or "")
                note = st.text_area("Ghi chú", value=selected.get("note") or "")
                save = st.form_submit_button("Lưu thay đổi")
            if save:
                try:
                    service.update_person(selected["id"], full_name=name, gender=gender,
                                          birth_date=_optional(birth), address=_optional(address),
                                          phone=_optional(phone), note=_optional(note))
                    st.session_state["person_notice"] = "Đã cập nhật Person."
                    st.rerun()
                except ValueError as exc:
                    st.error(str(exc))
                except Exception as exc:
                    st.error(f"Không thể cập nhật Person: {exc}")
            confirm = st.checkbox(f"Xác nhận xóa {person_label(selected)}", key=f"confirm_{selected['id']}")
            if st.button("Xóa Person", disabled=not confirm):
                try:
                    service.delete_person(selected["id"])
                    st.session_state["person_notice"] = "Đã xóa Person."
                    st.rerun()
                except ValueError as exc:
                    st.error(str(exc))
                except Exception as exc:
                    st.error(f"Không thể xóa Person: {exc}")

    with tab_detail:
        try:
            people = _people()
        except Exception as exc:
            st.error(f"Không tải được Person: {exc}")
            people = []
        if not people:
            st.info("Chưa có Person để xem.")
        else:
            selected = st.selectbox("Chọn Person", people, format_func=person_label, key="person_detail")
            try:
                person = service.get_person(selected["id"])
                if person:
                    st.write({
                        "ID": person["id"], "Họ tên": person["full_name"],
                        "Giới tính": GENDER_LABELS_VI.get(person["gender"], person["gender"]),
                        "Ngày sinh": person.get("birth_date") or "—",
                        "Địa chỉ": person.get("address") or "—",
                        "Số điện thoại": person.get("phone") or "—",
                        "Ghi chú": person.get("note") or "—",
                    })
            except Exception as exc:
                st.error(f"Không tải được chi tiết: {exc}")
