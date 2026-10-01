# MEMBER SƠN — Relationship + Family Graph

## Owner & Domain
- **Owner:** Sơn
- **Domain:** Relationship management + Family graph visualization

## File được sở hữu
```
features/relationship/{__init__,page,service,repository}.py + README_SON.md
features/family_graph/{__init__,page,service}.py + README_SON.md
tests/relationship/*
```
Block `TAKE NOTE - SƠN` trong `app.py`.

## Chức năng phải làm
- Quản lý `FATHER_OF`, `MOTHER_OF`, `SPOUSE_OF`
- Thêm / xóa / xem relationship
- Validation relationship
- Family graph visualization

## Function cần implement

| File | Function |
|------|----------|
| `relationship/repository.py` | `create_relationship`, `delete_relationship`, `relationship_exists`, `find_relationships_of_person`, `find_all_relationships`, `count_parents`, `count_spouses`, `is_ancestor`, `get_graph_edges` |
| `relationship/service.py` | `add_relationship`, `remove_relationship`, `get_relationships_of_person`, `list_relationships`, `get_graph_edges`, `validate_relationship` |
| `relationship/page.py` | `render` (3 tab: thêm, xem, xóa) |
| `family_graph/service.py` | `build_graph_data`, `render_graph_html` |
| `family_graph/page.py` | `render` |

## Query cần viết (Cypher, trong `relationship/repository.py`)
1. Tạo relationship giữa 2 Person (không tạo trùng)
2. Xóa 1 relationship
3. Kiểm tra relationship tồn tại (SPOUSE_OF kiểm tra cả 2 chiều)
4. Lấy relationship của 1 Person (cả đi ra và đi vào)
5. Liệt kê toàn bộ relationship
6. Đếm cha / mẹ của 1 người
7. Đếm vợ/chồng hiện có
8. Kiểm tra tổ tiên (path độ dài biến đổi) để chặn vòng lặp
9. Lấy các cạnh trong phạm vi `depth` quanh Person gốc cho graph

> Relationship type không parametrize được → whitelist với `core.constants.RELATIONSHIP_TYPES`.

## Business rules cần quyết định & validate
- Cha phải `MALE`, mẹ phải `FEMALE`
- Mỗi người tối đa 1 cha, 1 mẹ
- Không tự quan hệ với chính mình; Person phải tồn tại
- Không vòng lặp tổ tiên; không trùng relationship
- SPOUSE_OF: giới hạn số vợ/chồng, không phải cha/mẹ/con của nhau
- (Tùy chọn) chênh lệch tuổi cha/mẹ - con hợp lý

## Phụ thuộc
- Dùng `features.person.service` (`list_persons`, `get_person`) — **không import** `person.repository`.
- Khi Vũ chưa xong: seed dữ liệu (`python -m database.seed_data --seed`) hoặc monkeypatch `person.service` trong test.
- Đạt phụ thuộc vào cấu trúc relationship (xem `docs/DATA_MODEL.md`) — đổi chiều lưu phải báo nhóm.

## Test cases (`tests/relationship/`)
- Thêm FATHER_OF thành công
- Cha là nữ / mẹ là nam → lỗi
- Tự quan hệ với chính mình → lỗi
- Con có 2 cha → lỗi
- Vòng lặp tổ tiên → lỗi
- Trùng relationship → lỗi
- SPOUSE_OF rules
- Person không tồn tại → lỗi
- Repository: create/delete, idempotent, count_parents, is_ancestor
- Graph: cấu trúc nodes/edges, dữ liệu rỗng

## Definition of Done
- [ ] Không còn `NotImplementedError` trong các hàm trên
- [ ] Mọi rule validation có thông báo lỗi hiển thị được trên UI
- [ ] `page.py` không có Cypher
- [ ] Graph hiển thị đúng với dữ liệu seed
- [ ] Test của `tests/relationship` pass
- [ ] `README_SON.md` cập nhật
- [ ] PR `feature/*` → `member/son` → `main` đã được review

## Chạy test
```bash
pytest tests/relationship -v
```

## File shared có thể cần chỉnh (báo nhóm trước)
- `core/constants.py` — chỉ thêm hằng số
- `shared/ui.py`, `shared/helpers.py`
- `requirements.txt` — nếu đổi thư viện vẽ graph (thêm ở cuối file)
- `app.py` — chỉ block `TAKE NOTE - SƠN`

## File KHÔNG nên chỉnh
- `features/person/*`, `features/dashboard/*` (Vũ)
- `features/kinship/*`, `features/relationship_search/*` (Đạt)
- `tests/person/*`, `tests/kinship/*`
- Block TAKE NOTE của Vũ / Đạt trong `app.py`
- Không import `features/person/repository.py`

# MEMBER SƠN — Relationship & Family Graph Domain

## Overview
Chịu trách nhiệm cho 2 domain chính trong hệ thống Family Management:
1. **Relationship Management (`features/relationship`)**: Quản lý các mối quan hệ `FATHER_OF`, `MOTHER_OF`, `SPOUSE_OF` giữa các cá nhân, đảm bảo toàn vẹn dữ liệu và kiểm tra các ràng buộc gia tộc.
2. **Family Graph Visualization (`features/family_graph`)**: Trực quan hóa cây gia tộc dạng Đồ thị tương tác trực quan (Vis.js HTML container).

## Business Rules Validations
- **Giao tiếp tầng**: `page` -> `service` -> `repository` -> `Neo4jConnection`.
- **Ràng buộc Cha/Mẹ**:
  - Cha (`FATHER_OF`) bắt buộc là Nam (`MALE`).
  - Mẹ (`MOTHER_OF`) bắt buộc là Nữ (`FEMALE`).
  - Mỗi cá nhân tối đa 1 Cha và 1 Mẹ.
  - Chống vòng lặp tổ tiên (Cycle Detection via Neo4j `*1..`).
- **Ràng buộc Hôn phối**:
  - `SPOUSE_OF` không được thiết lập giữa những người có quan hệ huyết thống trực hệ (Cha/Mẹ - Con).
  - Tối đa 1 vợ/chồng tại một thời điểm.
- **Ràng buộc chung**:
  - Không tạo quan hệ với chính mình.
  - Không duplicate relationship.

## Lệnh Chạy Test
```bash
pytest tests/relationship -v

