# MEMBER ĐẠT — Kinship + Relationship Search

## Owner & Domain
- **Owner:** Đạt
- **Domain:** Kinship resolver + Relationship search

## File được sở hữu
```
features/kinship/{__init__,page,service,repository,resolver}.py + README_DAT.md
features/relationship_search/{__init__,service}.py + README_DAT.md
tests/kinship/*
```
Block `TAKE NOTE - ĐẠT` trong `app.py`.

## Chức năng phải làm
- Chọn Person A, Person B
- Tìm `shortestPath`
- Phân tích relationship path
- Xác định cách xưng hô
- Hiển thị đường đi quan hệ

### Quan hệ cần hỗ trợ
Cha · Mẹ · Con trai · Con gái · Ông nội · Bà nội · Ông ngoại · Bà ngoại · Anh · Chị · Em · Anh/chị/em họ · Bác · Chú · Cô · Cậu · Dì · Vợ · Chồng · Cháu · Cụ

## Luồng
```
kinship/page → kinship/service
   → relationship_search/service.search_relationship_path → kinship/repository (Cypher)
   → kinship/resolver.resolve_kinship (logic thuần)
```

## Function cần implement

| File | Function |
|------|----------|
| `kinship/repository.py` | `find_shortest_path`, (`find_all_shortest_paths`) |
| `relationship_search/service.py` | `search_relationship_path`, `build_steps_from_raw_path`, `format_path_text` |
| `kinship/resolver.py` | `classify_path`, `resolve_kinship`, `compare_age` |
| `kinship/service.py` | `list_selectable_persons`, `find_kinship` |
| `kinship/page.py` | `render` |

`PathStep` và `KinshipResult` (dataclass) đã định nghĩa sẵn trong `resolver.py` — được phép chỉnh/bổ sung field trong domain của Đạt.

## Query cần viết (Cypher, trong `kinship/repository.py`)
1. shortestPath vô hướng giữa 2 Person trên `FATHER_OF|MOTHER_OF|SPOUSE_OF`, giới hạn độ sâu
2. Trả đủ thông tin node (id, tên, gender, birth_date) và relationship (type, start_id, end_id) để suy ra hướng từng bước
3. (Tùy chọn) allShortestPaths

## Điểm cần chốt khi viết resolver
- Phân biệt bên **nội** / **ngoại** (đi lên qua cha hay qua mẹ)
- Anh/chị/em, bác/chú, cô/cậu/dì phụ thuộc **giới tính** và **ngày sinh** (`compare_age`)
- Hành vi mặc định khi **thiếu birth_date** → ghi lại vào đây khi chốt
- Cách xử lý path quá xa hoặc chưa hỗ trợ
- Gọi hai chiều: A gọi B là gì, B gọi A là gì

## Phụ thuộc
- Danh sách/giới tính Person: `features.person.service.list_persons / get_person` (không import `person.repository`).
- Cấu trúc quan hệ: `docs/DATA_MODEL.md` (SPOUSE_OF lưu 1 chiều, query vô hướng).
- Dữ liệu demo: `python -m database.seed_data --reset`; bảng case: `docs/DEMO_FLOW.md`.

## Test cases (`tests/kinship/`)
- Resolver (không cần Neo4j, dùng `PathStep` giả): mỗi nhóm trong danh sách quan hệ, A == B, thiếu birth_date, path không hỗ trợ
- Service: không có path, A == B, direction UP/DOWN/SPOUSE, format path text
- Repository (integration): cousins qua ông nội, không có path, `max_depth`

## Definition of Done
- [ ] Hỗ trợ đủ danh sách quan hệ ở trên (hoặc ghi rõ phần chưa hỗ trợ)
- [ ] Hiển thị được đường đi + cả 2 chiều xưng hô trên UI
- [ ] Logic xưng hô chỉ nằm trong `resolver.py`/`service.py`, không nằm trong `app.py` hay `page.py`
- [ ] Các cặp trong `docs/DEMO_FLOW.md` cho kết quả đúng
- [ ] Test của `tests/kinship` pass
- [ ] `README_DAT.md` cập nhật
- [ ] PR `feature/*` → `member/dat` → `main` đã được review

## Chạy test
```bash
pytest tests/kinship -v
```

## File shared có thể cần chỉnh (báo nhóm trước)
- `core/constants.py` — chỉ thêm hằng số
- `shared/ui.py`, `shared/helpers.py`
- `app.py` — chỉ block `TAKE NOTE - ĐẠT`

## File KHÔNG nên chỉnh
- `features/person/*`, `features/dashboard/*` (Vũ)
- `features/relationship/*`, `features/family_graph/*` (Sơn)
- `tests/person/*`, `tests/relationship/*`
- Block TAKE NOTE của Vũ / Sơn trong `app.py`
- Không thêm query CRUD Person / thêm-xóa relationship vào `kinship/repository.py`
