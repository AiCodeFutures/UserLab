import sqlite3
from config import settings


def get_db():
    """获取 SQLite 连接"""
    db_path = settings.DATABASE_URL.replace("sqlite:///", "")
    conn = sqlite3.connect(db_path, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """初始化数据库并创建表"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            hashed_password TEXT NOT NULL,
            is_superuser INTEGER NOT NULL DEFAULT 0
        );
    """
    )
    conn.commit()
    conn.close()


def create_user(
    db: sqlite3.Connection, username: str, email: str, hashed_password: str
):
    """插入新用户"""
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO users (username, email, hashed_password) VALUES (?, ?, ?)",
        (username, email, hashed_password),
    )
    db.commit()


def get_hashed_password(db: sqlite3.Connection, username: str) -> str | None:
    """根据用户名获取存储的哈希密码"""
    cursor = db.cursor()
    cursor.execute("SELECT hashed_password FROM users WHERE username = ?", (username,))
    row = cursor.fetchone()
    return row["hashed_password"] if row else None


def get_user(db: sqlite3.Connection, username: str):
    """根据用户名获取用户基础信息"""
    cursor = db.cursor()
    cursor.execute(
        "SELECT username, email, is_superuser FROM users WHERE username = ?",
        (username,),
    )
    return cursor.fetchone()
