import os
import hashlib
import hmac
import jwt
from datetime import datetime, timedelta
from config import settings

# 密码哈希与验证

def get_password_hash(password: str) -> str:
    """对密码进行哈希处理"""
    salt = os.urandom(16)
    pwd_hash = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 100000)
    return salt.hex() + pwd_hash.hex()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """验证明文密码与哈希密码是否匹配"""
    if len(hashed_password) < 34:  # 至少16字节的salt (32 hex) + 1字节的hash (2 hex)
        return False
    salt = bytes.fromhex(hashed_password[:32])
    stored_hash = bytes.fromhex(hashed_password[32:])
    pwd_hash = hashlib.pbkdf2_hmac("sha256", plain_password.encode(), salt, 100000)
    return hmac.compare_digest(pwd_hash, stored_hash)


# 令牌生成与验证

def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """生成 JWT 访问令牌"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt


def verify_token(token: str) -> dict | None:
    """验证并解析 JWT 令牌"""
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        return payload
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        return None
