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

## Quy ước resolver
- `compare_age` trả `-1` khi A lớn hơn B, `1` khi A nhỏ hơn B và `0` khi bằng tuổi hoặc không đủ dữ liệu.
- Khi thiếu/sai `birth_date`, không đoán thứ bậc; dùng nhãn trung tính như `Anh/chị/em`, `Anh/chị/em họ`, `Bác/chú`, `Bác/cô`, `Bác/cậu` hoặc `Bác/dì`.
- Quan hệ bên nội/ngoại được xác định bằng bước đầu đi lên qua `FATHER_OF` hay `MOTHER_OF`.
- Path có thật nhưng ngoài các pattern được hỗ trợ vẫn được hiển thị, với cách gọi `Chưa xác định` và thông báo rõ ràng.
- `max_depth` hợp lệ từ 1 đến 20; mặc định là 10.

## Chức năng đã triển khai
- Shortest path vô hướng trên `FATHER_OF|MOTHER_OF|SPOUSE_OF`.
- Xưng hô hai chiều cho cha/mẹ/con, ông bà nội ngoại, anh chị em, họ hàng, bác/chú/cô/cậu/dì, vợ/chồng, cháu và cụ.
- UI chọn hai Person, hiển thị hai chiều xưng hô, đường đi và chi tiết từng bước.
- Unit test resolver/service và integration test repository (tự skip khi Neo4j chưa chạy hoặc chưa seed).

Chi tiết task: xem `docs/MEMBER_DAT.md`.
