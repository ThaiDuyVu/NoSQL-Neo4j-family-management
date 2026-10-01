# README_SON — Feature `relationship`

**Owner:** Sơn  |  **Domain:** Relationship management

## Phạm vi
Thêm / xóa / xem `FATHER_OF`, `MOTHER_OF`, `SPOUSE_OF`; validation relationship.

## File
| File | Vai trò |
|------|---------|
| `page.py` | UI, chỉ gọi `service` |
| `service.py` | business logic + `validate_relationship` |
| `repository.py` | toàn bộ Cypher liên quan relationship |

## Luồng
`page.py` → `service.py` → `repository.py` → `core/neo4j_connection.py` → Neo4j

## Phụ thuộc
- Cần danh sách/kiểm tra Person → gọi `features.person.service` (`list_persons`, `get_person`).
  **Không** import `features.person.repository`.
- Trong lúc Vũ chưa xong: tạo dữ liệu bằng `python -m database.seed_data --seed` hoặc mock `person.service` trong test.

## Test
```bash
pytest tests/relationship -v
```

Chi tiết task: xem `docs/MEMBER_SON.md`.
