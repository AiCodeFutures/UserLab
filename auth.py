import jwt
import os
import hashlib
import hmac
from datetime import datetime, timedelta
from fastapi import HTTPException
from config import settings


# 密码哈希与验证


def get_password_hash(password: str) -> str:
    """对密码进行哈希处理"""
    # 生成随机盐值
    salt = os.urandom(16)
    # 使用 PBKDF2 算法进行哈希
    pwd_hash = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 100000)
    # 返回盐值和哈希值的十六进制字符串
    return salt.hex() + pwd_hash.hex()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """验证明文密码与哈希密码是否匹配"""
    try:
        # 提取盐值和哈希值
        salt = bytes.fromhex(hashed_password[:32])
        stored_hash = bytes.fromhex(hashed_password[32:])
        # 使用相同参数计算哈希
        pwd_hash = hashlib.pbkdf2_hmac("sha256", plain_password.encode(), salt, 100000)
        # 使用安全比较函数防止时序攻击
        return hmac.compare_digest(pwd_hash, stored_hash)
    except (ValueError, IndexError):
        return False


# 令牌生成与验证


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """生成 JWT 访问令牌"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def verify_token(token: str) -> dict:
    """验证并解析 JWT 令牌"""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="无效的token")
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="token已过期")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="无效的token")
