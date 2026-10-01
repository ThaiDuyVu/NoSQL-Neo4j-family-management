# DATA MODEL

## Node
`(:Person {id, full_name, gender, birth_date, address, phone, note})`

| Property | Kiểu | Ghi chú |
|----------|------|---------|
| `id` | string | **unique** (constraint), vd `P001` |
| `full_name` | string | bắt buộc |
| `gender` | string | `MALE` \| `FEMALE` |
| `birth_date` | string ISO `YYYY-MM-DD` | dùng để xác định anh/chị/em, bác/chú... |
| `address`, `phone`, `note` | string | tùy chọn |

Ngày lưu dạng chuỗi ISO để đơn giản; nếu đổi sang kiểu `date` của Neo4j phải báo cả nhóm.

## Relationship

| Type | Chiều lưu | Ý nghĩa |
|------|-----------|---------|
| `FATHER_OF` | `(cha)-[:FATHER_OF]->(con)` | cha của |
| `MOTHER_OF` | `(mẹ)-[:MOTHER_OF]->(con)` | mẹ của |
| `SPOUSE_OF` | `(chồng)-[:SPOUSE_OF]->(vợ)` | **lưu 1 chiều**, luôn query vô hướng `-[:SPOUSE_OF]-` |

> Nếu nhóm muốn lưu SPOUSE_OF hai chiều thì thống nhất lại **trước khi** Sơn và Đạt viết query.

## Quy ước chung
- Quan hệ cha/mẹ - con chỉ lưu theo hướng cha/mẹ → con. Quan hệ ngược (con → cha) suy ra bằng cách đi ngược chiều.
- Tên relationship type lấy từ `core/constants.py`.
- Hướng khi đi trên path: đi **ngược** mũi tên cha/mẹ → con (từ con lên cha/mẹ) là **UP**; đi **xuôi** mũi tên là **DOWN**; `SPOUSE_OF` là **SPOUSE**.

## Constraints & index
Xem `database/constraints.cypher`.

## Dữ liệu seed (`database/seed_data.py`)

```
Nội:   P001 An ═ P002 Bình ──▶ P003 Cường (═ P013 Rạng ──▶ P014 Thành)
                            ├▶ P004 Dũng  (═ P008 Mai ──▶ P011 Phúc, P012 Quỳnh)
                            └▶ P005 Hoa
Ngoại: P006 Khoa ═ P007 Lan ──▶ P008 Mai, P009 Nam, P010 Oanh
Đời 4: P011 Phúc ═ P015 Uyên ──▶ P016 Vinh
```
