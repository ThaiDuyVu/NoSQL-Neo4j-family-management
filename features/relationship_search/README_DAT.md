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

Chi tiết task: xem `docs/MEMBER_DAT.md`.
