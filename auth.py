import jwt
from datetime import datetime, timedelta
from config import settings


# 密码哈希与验证


def get_password_hash(password: str) -> str:
    """对密码进行哈希处理"""
    pass


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """验证明文密码与哈希密码是否匹配"""
    pass


# 令牌生成与验证


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """生成 JWT 访问令牌"""
    pass


def verify_token(token: str) -> dict:
    """验证并解析 JWT 令牌"""
    pass
