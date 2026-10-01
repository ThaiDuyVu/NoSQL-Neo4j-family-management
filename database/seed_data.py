"""
============================================================
SHARED FILE - CẢ NHÓM  (seed infrastructure)
============================================================
Hạ tầng seed/reset database.

Cách dùng (chạy ở thư mục gốc project):
    python -m database.seed_data --init     # tạo constraint/index
    python -m database.seed_data --seed     # nạp dữ liệu mẫu (idempotent, dùng MERGE)
    python -m database.seed_data --reset    # XÓA TOÀN BỘ + init + seed

Quy tắc:
- Dữ liệu mẫu là bộ chung để demo; muốn thêm người/quan hệ mẫu thì
  THÊM vào cuối danh sách và báo nhóm. Không xóa dữ liệu của người khác.
- Không đặt business logic của feature vào đây.
============================================================
"""
import argparse
from pathlib import Path

from core.neo4j_connection import close_driver, run_read, run_write

CONSTRAINTS_FILE = Path(__file__).parent / "constraints.cypher"

# (id, full_name, gender, birth_date)
SAMPLE_PERSONS = [
    ("P001", "Nguyễn Văn An", "MALE", "1940-01-01"),
    ("P002", "Trần Thị Bình", "FEMALE", "1943-01-01"),
    ("P003", "Nguyễn Văn Cường", "MALE", "1965-01-01"),
    ("P004", "Nguyễn Văn Dũng", "MALE", "1968-01-01"),
    ("P005", "Nguyễn Thị Hoa", "FEMALE", "1971-01-01"),
    ("P006", "Lê Văn Khoa", "MALE", "1942-01-01"),
    ("P007", "Phạm Thị Lan", "FEMALE", "1945-01-01"),
    ("P008", "Lê Thị Mai", "FEMALE", "1970-01-01"),
    ("P009", "Lê Văn Nam", "MALE", "1973-01-01"),
    ("P010", "Lê Thị Oanh", "FEMALE", "1976-01-01"),
    ("P011", "Nguyễn Văn Phúc", "MALE", "1995-01-01"),
    ("P012", "Nguyễn Thị Quỳnh", "FEMALE", "1998-01-01"),
    ("P013", "Đặng Thị Rạng", "FEMALE", "1967-01-01"),
    ("P014", "Nguyễn Văn Thành", "MALE", "1993-01-01"),
    ("P015", "Hoàng Thị Uyên", "FEMALE", "1996-01-01"),
    ("P016", "Nguyễn Văn Vinh", "MALE", "2022-01-01"),
]

# (from_id, to_id, type)  -- FATHER_OF/MOTHER_OF: cha/mẹ -> con ; SPOUSE_OF: chồng -> vợ
SAMPLE_RELATIONSHIPS = [
    # Cha -> con
    ("P001", "P003", "FATHER_OF"), ("P001", "P004", "FATHER_OF"), ("P001", "P005", "FATHER_OF"),
    ("P006", "P008", "FATHER_OF"), ("P006", "P009", "FATHER_OF"), ("P006", "P010", "FATHER_OF"),
    ("P004", "P011", "FATHER_OF"), ("P004", "P012", "FATHER_OF"),
    ("P003", "P014", "FATHER_OF"), ("P011", "P016", "FATHER_OF"),
    # Mẹ -> con
    ("P002", "P003", "MOTHER_OF"), ("P002", "P004", "MOTHER_OF"), ("P002", "P005", "MOTHER_OF"),
    ("P007", "P008", "MOTHER_OF"), ("P007", "P009", "MOTHER_OF"), ("P007", "P010", "MOTHER_OF"),
    ("P008", "P011", "MOTHER_OF"), ("P008", "P012", "MOTHER_OF"),
    ("P013", "P014", "MOTHER_OF"), ("P015", "P016", "MOTHER_OF"),
    # Vợ chồng (chồng -> vợ)
    ("P001", "P002", "SPOUSE_OF"), ("P006", "P007", "SPOUSE_OF"), ("P004", "P008", "SPOUSE_OF"),
    ("P003", "P013", "SPOUSE_OF"), ("P011", "P015", "SPOUSE_OF"),
]


def run_constraints() -> None:
    text = CONSTRAINTS_FILE.read_text(encoding="utf-8")
    lines = [ln for ln in text.splitlines() if not ln.strip().startswith("//")]
    for statement in "\n".join(lines).split(";"):
        statement = statement.strip()
        if statement:
            run_write(statement)
    print("[init] constraints/indexes OK")


def clear_database() -> None:
    run_write("MATCH (n) DETACH DELETE n")
    print("[reset] đã xóa toàn bộ node/relationship")


def seed_sample_data() -> None:
    run_write(
        """
        UNWIND $rows AS row
        MERGE (p:Person {id: row.id})
        SET p.full_name = row.full_name, p.gender = row.gender, p.birth_date = row.birth_date
        """,
        {"rows": [dict(id=i, full_name=n, gender=g, birth_date=b) for i, n, g, b in SAMPLE_PERSONS]},
    )
    # Relationship type không parametrize được trong Cypher -> gom nhóm theo type (whitelist cố định).
    for rel_type in ("FATHER_OF", "MOTHER_OF", "SPOUSE_OF"):
        pairs = [dict(a=a, b=b) for a, b, t in SAMPLE_RELATIONSHIPS if t == rel_type]
        run_write(
            f"""
            UNWIND $pairs AS pair
            MATCH (a:Person {{id: pair.a}}), (b:Person {{id: pair.b}})
            MERGE (a)-[:{rel_type}]->(b)
            """,
            {"pairs": pairs},
        )
    persons = run_read("MATCH (p:Person) RETURN count(p) AS n")[0]["n"]
    rels = run_read("MATCH ()-[r]->() RETURN count(r) AS n")[0]["n"]
    print(f"[seed] OK - {persons} Person, {rels} relationship")


def main() -> None:
    parser = argparse.ArgumentParser(description="Seed / reset Neo4j database")
    parser.add_argument("--init", action="store_true", help="tạo constraint/index")
    parser.add_argument("--seed", action="store_true", help="nạp dữ liệu mẫu")
    parser.add_argument("--reset", action="store_true", help="xóa toàn bộ + init + seed")
    args = parser.parse_args()

    if not (args.init or args.seed or args.reset):
        parser.print_help()
        return
    try:
        if args.reset:
            clear_database()
            run_constraints()
            seed_sample_data()
        else:
            if args.init:
                run_constraints()
            if args.seed:
                seed_sample_data()
    finally:
        close_driver()


if __name__ == "__main__":
    main()
