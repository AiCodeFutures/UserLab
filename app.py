from fastapi import FastAPI, Depends, HTTPException, Body
import sqlite3
from config import settings
from database import get_db, init_db, create_user, get_user_by_login, get_user
from auth import (
    get_password_hash,
    verify_password,
    create_access_token,
    verify_token,
)

app = FastAPI()


@app.on_event("startup")
def on_startup():
    init_db()


@app.post("/register")
def register(
    username: str = Body(...),
    email: str = Body(...),
    password: str = Body(...),
    db: sqlite3.Connection = Depends(get_db),
):
    """用户注册接口"""
    hashed_password = get_password_hash(password)
    try:
        create_user(db, username, email, hashed_password)
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="用户名或邮箱已存在")
    return {"msg": "注册成功"}


@app.post("/login")
def login(
    login_identifier: str = Body(...),
    password: str = Body(...),
    db: sqlite3.Connection = Depends(get_db),
):
    """用户登录接口，支持用户名或邮箱"""
    user = get_user_by_login(db, login_identifier)
    if not user or not verify_password(password, user["hashed_password"]):
        raise HTTPException(status_code=400, detail="用户名或密码错误")

    access_token = create_access_token(data={"sub": user["username"]})
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/me")
def read_users_me(token: str, db: sqlite3.Connection = Depends(get_db)):
    """获取当前用户信息"""
    payload = verify_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="无效或已过期的token")

    username = payload.get("sub")
    if not username:
        raise HTTPException(status_code=401, detail="无效的token (sub not found)")

    user_row = get_user(db, username)
    if not user_row:
        raise HTTPException(status_code=404, detail="用户不存在")

    return {
        "username": user_row["username"],
        "email": user_row["email"],
        "is_superuser": bool(user_row["is_superuser"]),
    }
