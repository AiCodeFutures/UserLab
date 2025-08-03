from fastapi import FastAPI, Depends, HTTPException
import sqlite3
import os
import hashlib
import hmac
import jwt
from datetime import datetime, timedelta
from config import settings
from database import get_db, init_db, create_user, get_hashed_password, get_user

app = FastAPI()


@app.on_event("startup")
def on_startup():
    init_db()


@app.post("/register")
def register(
    username: str, email: str, password: str, db: sqlite3.Connection = Depends(get_db)
):
    """用户注册接口"""
    # 使用内置 hashlib.pbkdf2_hmac 生成带盐哈希
    salt = os.urandom(16)
    pwd_hash = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 100000)
    hashed_password = salt.hex() + pwd_hash.hex()
    try:
        create_user(db, username, email, hashed_password)
    except sqlite3.IntegrityError:
        # 用户名或邮箱已存在
        raise HTTPException(status_code=400, detail="用户名或邮箱已存在")
    return {"msg": "注册成功"}


@app.post("/login")
def login(username: str, password: str, db: sqlite3.Connection = Depends(get_db)):
    """用户登录接口"""
    # 获取存储的哈希密码
    stored = get_hashed_password(db, username)
    if not stored:
        raise HTTPException(status_code=400, detail="用户名或密码错误")
    # 提取 salt 和 hash
    salt = bytes.fromhex(stored[:32])
    stored_hash = bytes.fromhex(stored[32:])
    # 使用相同参数计算哈希并比较
    pwd_hash = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 100000)
    if not hmac.compare_digest(pwd_hash, stored_hash):
        raise HTTPException(status_code=400, detail="用户名或密码错误")
    # 生成 JWT 访问令牌
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {"sub": username, "exp": expire}
    access_token = jwt.encode(
        payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/me")
def read_users_me(token: str, db: sqlite3.Connection = Depends(get_db)):
    """获取当前用户信息"""
    # 验证并解析 JWT
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        username = payload.get("sub")
        if not username:
            raise HTTPException(status_code=401, detail="无效的token")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="token已过期")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="无效的token")

    # 查询并返回用户信息
    user_row = get_user(db, username)
    if not user_row:
        raise HTTPException(status_code=404, detail="用户不存在")
    return {
        "username": user_row["username"],
        "email": user_row["email"],
        "is_superuser": bool(user_row["is_superuser"]),
    }
