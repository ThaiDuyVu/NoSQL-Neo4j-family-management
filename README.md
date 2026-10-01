# Family Management — Quản lý nhân thân với Neo4j

Bài tập demo nhóm môn **NoSQL**. Stack: **Python + Streamlit + Neo4j**.
Kiến trúc **FEATURE-BASED**: mỗi thành viên sở hữu một domain riêng (UI, service, repository/Cypher, business logic, test, README).

## 1. Phân chia công việc

| Thành viên | Domain | Folder |
|------------|--------|--------|
| Vũ | Person + Dashboard | `features/person`, `features/dashboard` |
| Sơn | Relationship + Family Graph | `features/relationship`, `features/family_graph` |
| Đạt | Kinship + Search | `features/kinship`, `features/relationship_search` |

Tài liệu chi tiết từng người: [`docs/MEMBER_VU.md`](docs/MEMBER_VU.md) · [`docs/MEMBER_SON.md`](docs/MEMBER_SON.md) · [`docs/MEMBER_DAT.md`](docs/MEMBER_DAT.md)

## 2. Cấu trúc

```
family-management/
├── app.py                 # Streamlit navigation (3 block TAKE NOTE, mỗi người 1 block)
├── core/                  # SHARED: config, kết nối Neo4j, constants
├── shared/                # SHARED: ui, validators, helpers
├── database/              # constraints.cypher + seed_data.py
├── features/
│   ├── person/            # Vũ
│   ├── dashboard/         # Vũ
│   ├── relationship/      # Sơn
│   ├── family_graph/      # Sơn
│   ├── kinship/           # Đạt
│   └── relationship_search/  # Đạt
├── tests/{person,relationship,kinship}/
└── docs/
```

Luồng bắt buộc: `page → service → repository → core/neo4j_connection → Neo4j`

Quy tắc:
- Không viết Cypher trong page.
- Repository của feature này không chứa query của feature khác.
- Feature gọi feature khác **chỉ qua `service.py`** (không import `repository.py` của người khác).
- Business logic Kinship nằm ở `features/kinship`, không nằm trong `app.py`.

## 3. Setup lần đầu

Yêu cầu: Python 3.10+, Docker Desktop.

```bash
git clone <repo-url> family-management
cd family-management

python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env               # Windows: copy .env.example .env
```

## 4. Chạy Neo4j bằng Docker

```bash
docker compose up -d
```
- Neo4j Browser: http://localhost:7474 (user/password theo `.env`, mặc định `neo4j` / `family12345`)
- Bolt: `bolt://localhost:7687`
- Dừng: `docker compose down` (giữ dữ liệu) · `docker compose down -v` (xóa luôn dữ liệu)

## 5. Seed data

```bash
python -m database.seed_data --init    # tạo constraint/index
python -m database.seed_data --seed    # nạp dữ liệu mẫu (16 người, 3 đời, idempotent)
```

## 6. Chạy Streamlit

```bash
streamlit run app.py
```
Mở http://localhost:8501. Sidebar hiển thị trạng thái kết nối Neo4j.

## 7. Reset database

```bash
python -m database.seed_data --reset   # XÓA TOÀN BỘ + init + seed lại
```
Hoặc reset sạch hoàn toàn: `docker compose down -v && docker compose up -d`, rồi chạy lại bước 5.

## 8. Test

```bash
pytest                       # tất cả
pytest tests/person -v       # Vũ
pytest tests/relationship -v # Sơn
pytest tests/kinship -v      # Đạt
```
Test integration cần Neo4j đang chạy (tự skip nếu chưa bật).

## 9. Demo flow

Xem [`docs/DEMO_FLOW.md`](docs/DEMO_FLOW.md): Dashboard → Person → Relationship → Family Graph → Kinship Search.

## 10. Git workflow

```
feature/*  ──PR──▶  member/<name>  ──PR──▶  main
```
- Nhánh cá nhân: `member/vu`, `member/son`, `member/dat`
- Nhánh feature: `feature/vu-person-crud`, `feature/vu-dashboard`, `feature/son-relationship`, `feature/son-family-graph`, `feature/dat-kinship-search`, `feature/dat-kinship-resolver`
- **Không push trực tiếp `main`.**

Chi tiết: [`docs/GIT_WORKFLOW.md`](docs/GIT_WORKFLOW.md). Data model: [`docs/DATA_MODEL.md`](docs/DATA_MODEL.md).

## 11. File shared (cả nhóm)

`app.py`, `core/*`, `shared/*`, `database/*`, `tests/conftest.py`, `docker-compose.yml`, `requirements.txt`.
Hạn chế chỉnh; không xóa code của người khác; đổi interface dùng chung phải báo nhóm.
