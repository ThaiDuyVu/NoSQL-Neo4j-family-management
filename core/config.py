"""
============================================================
SHARED FILE - CẢ NHÓM
============================================================
Đọc cấu hình từ biến môi trường / file .env.

Quy tắc:
- Hạn chế chỉnh nếu không cần.
- Không xóa code của thành viên khác.
- Thay đổi interface dùng chung phải báo nhóm.
- Không đặt business logic riêng của feature vào shared.
============================================================
"""
import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    neo4j_uri: str = os.getenv("NEO4J_URI", "bolt://localhost:7687")
    neo4j_user: str = os.getenv("NEO4J_USER", "neo4j")
    neo4j_password: str = os.getenv("NEO4J_PASSWORD", "family12345")
    neo4j_database: str = os.getenv("NEO4J_DATABASE", "neo4j")


settings = Settings()
