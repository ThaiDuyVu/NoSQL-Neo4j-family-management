# MEMBER VŨ — Person + Dashboard

## Owner & Domain
- **Owner:** Vũ
- **Domain:** Person management + Dashboard

## File được sở hữu
```
features/person/{__init__,page,service,repository,model}.py + README_VU.md
features/dashboard/{__init__,page,service}.py + README_VU.md
tests/person/*
```
Block `TAKE NOTE - VŨ` trong `app.py`.

## Chức năng phải làm
- Dashboard: tổng số người, số nam, số nữ
- Danh sách Person
- Thêm / sửa / xóa Person
- Tìm kiếm Person (tên, id, lọc giới tính)
- Xem chi tiết Person
- Validation Person

## Function cần implement

| File | Function |
|------|----------|
| `person/repository.py` | `create_person`, `find_by_id`, `exists_by_id`, `find_all`, `search_by_keyword`, `update_person`, `delete_person`, `count_all`, `count_by_gender`, (`get_next_id`) |
| `person/service.py` | `create_person`, `update_person`, `delete_person`, `list_persons`, `get_person`, `search_persons`, `get_statistics`, `validate_person_input` |
| `person/page.py` | `render` (4 tab: danh sách/tìm kiếm, thêm, sửa/xóa, chi tiết) |
| `dashboard/service.py` | `get_dashboard_stats` |
| `dashboard/page.py` | `render` |

### Public interface — Sơn và Đạt đang dùng, **không đổi signature khi chưa báo nhóm**
- `person.service.list_persons(skip, limit) -> list[dict]`
- `person.service.get_person(person_id) -> dict | None`
- `person.service.search_persons(keyword, gender) -> list[dict]`

Ưu tiên làm 3 hàm này **trước** để Sơn/Đạt có dữ liệu cho selectbox.

## Query cần viết (Cypher, trong `person/repository.py`)
1. Tạo node `:Person`
2. Lấy 1 Person theo id
3. Kiểm tra tồn tại theo id
4. Liệt kê có phân trang
5. Tìm theo tên/id, không phân biệt hoa thường, lọc gender tùy chọn
6. Cập nhật property
7. Xóa Person (quyết định chính sách khi còn relationship — thống nhất với Sơn)
8. Đếm tổng số Person
9. Đếm theo gender

## Test cases (`tests/person/`)
- Tạo thành công / trùng id / tên rỗng / gender sai / ngày sinh tương lai
- Update / delete person không tồn tại
- Search theo từ khóa + gender
- Repository: tạo + đọc, unique constraint, count, delete
- Dashboard: số liệu đúng, database trống = 0

## Definition of Done
- [ ] Tất cả function trên không còn `NotImplementedError`
- [ ] `page.py` không có Cypher, chỉ gọi `service`
- [ ] Validation báo lỗi rõ ràng trên UI
- [ ] Test của `tests/person` pass (bỏ `skip` các case đã làm)
- [ ] Dashboard hiển thị đúng với dữ liệu seed (16 người: 8 nam / 8 nữ)
- [ ] `README_VU.md` cập nhật nếu thay đổi hành vi/interface
- [ ] PR `feature/*` → `member/vu` → `main` đã được review

## Chạy test
```bash
pytest tests/person -v
```

## File shared có thể cần chỉnh (báo nhóm trước)
- `core/constants.py` — chỉ **thêm** hằng số
- `shared/ui.py`, `shared/validators.py`, `shared/helpers.py` — thêm helper dùng chung
- `app.py` — chỉ block `TAKE NOTE - VŨ`

## File KHÔNG nên chỉnh
- `features/relationship/*`, `features/family_graph/*` (Sơn)
- `features/kinship/*`, `features/relationship_search/*` (Đạt)
- `tests/relationship/*`, `tests/kinship/*`
- Block TAKE NOTE của Sơn / Đạt trong `app.py`
- Không thêm query Relationship vào `person/repository.py`
