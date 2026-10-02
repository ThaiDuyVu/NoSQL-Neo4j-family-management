# README_DAT — Feature `relationship_search`

**Owner:** Đạt  |  **Domain:** Relationship search

## Phạm vi
Tìm đường đi quan hệ (shortestPath), chuyển raw path thành `PathStep`, format hiển thị.

## File
| File | Vai trò |
|------|---------|
| `service.py` | `search_relationship_path`, `build_steps_from_raw_path`, `format_path_text` |

Feature này không có page/repository riêng: Cypher nằm ở `features/kinship/repository.py`,
UI nằm ở `features/kinship/page.py` (cùng domain Đạt). Kết quả được `kinship.service` dùng tiếp.

## Test
```bash
pytest tests/kinship -v
```

## Quy ước dữ liệu
- Mỗi `PathStep` chứa ID, tên, giới tính và ngày sinh của hai đầu cạnh.
- Đi ngược cạnh cha/mẹ là `UP`; đi xuôi là `DOWN`; `SPOUSE_OF` luôn là `SPOUSE`.
- Service kiểm tra số node/cạnh, tính liền kề và loại relationship trước khi tạo `PathStep`.
- Chuỗi hiển thị mô tả từng cạnh, ví dụ: `Phúc → (con của) Dũng → (con của) An`.

Chi tiết task: xem `docs/MEMBER_DAT.md`.
