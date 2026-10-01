# README_DAT — Feature `kinship`

**Owner:** Đạt  |  **Domain:** Kinship resolver

## Phạm vi
Chọn Person A/B → tìm shortestPath → phân tích → cách xưng hô.

## File
| File | Vai trò |
|------|---------|
| `page.py` | UI, chỉ gọi `service` |
| `service.py` | điều phối `find_kinship` |
| `repository.py` | Cypher shortestPath |
| `resolver.py` | logic thuần: path → xưng hô (không DB, không streamlit) |

## Luồng
`page` → `kinship.service` → `relationship_search.service` → `kinship.repository` → Neo4j
rồi `kinship.service` → `resolver.resolve_kinship`.

## Phụ thuộc
- Danh sách/giới tính Person → `features.person.service` (không import repository của Vũ).
- Dữ liệu quan hệ → seed bằng `python -m database.seed_data --seed`.

## Test
```bash
pytest tests/kinship -v
```
`resolver.py` test được bằng `PathStep` giả, không cần Neo4j.

Chi tiết task: xem `docs/MEMBER_DAT.md`.
