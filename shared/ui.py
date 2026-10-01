"""
============================================================
SHARED FILE - CẢ NHÓM
============================================================
Helper UI Streamlit dùng chung (header trang, TODO box, thông báo).

Quy tắc:
- Hạn chế chỉnh nếu không cần.
- Không xóa code của thành viên khác.
- Thay đổi interface dùng chung phải báo nhóm.
- Không đặt UI/business logic riêng của feature vào shared.
============================================================
"""
import streamlit as st


def page_header(title: str, owner: str, description: str = "") -> None:
    st.title(title)
    st.caption(f"Feature owner: **{owner}**")
    if description:
        st.write(description)
    st.divider()


def show_todo(owner: str, items: list[str]) -> None:
    """Hiển thị danh sách TODO của skeleton. Xóa khi đã implement."""
    body = "\n".join(f"- [ ] {item}" for item in items)
    st.info(f"**TODO ({owner})**\n\n{body}")


def show_success(message: str) -> None:
    st.success(message)


def show_error(message: str) -> None:
    st.error(message)


def person_label(person: dict) -> str:
    """Nhãn hiển thị trong selectbox: 'Họ tên (P001)'."""
    return f"{person.get('full_name', '?')} ({person.get('id', '?')})"
