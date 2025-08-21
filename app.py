from fastapi import FastAPI, Depends, HTTPException, Form
from fastapi.security import OAuth2PasswordBearer
import sqlite3
from datetime import timedelta
from config import settings
from database import get_db, init_db, create_user, get_user
from auth import get_password_hash, verify_password, create_access_token, verify_token

app = FastAPI()

# OAuth2 scheme for token extraction
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


@app.on_event("startup")
def on_startup():
    init_db()


@app.post("/register")
def register(
    username: str = Form(...), email: str = Form(...), password: str = Form(...), db: sqlite3.Connection = Depends(get_db)
):
    """用户注册接口"""
    # 使用auth模块的密码哈希函数
    hashed_password = get_password_hash(password)
    try:
        create_user(db, username, email, hashed_password)
    except sqlite3.IntegrityError:
        # 用户名或邮箱已存在
        raise HTTPException(status_code=400, detail="用户名或邮箱已存在")
    return {"msg": "注册成功"}


@app.post("/login")
def login(username: str = Form(...), password: str = Form(...), db: sqlite3.Connection = Depends(get_db)):
    """用户登录接口"""
    # 获取用户信息
    user_row = get_user(db, username)
    if not user_row:
        raise HTTPException(status_code=400, detail="用户名或密码错误")
    
    # 获取存储的哈希密码
    cursor = db.cursor()
    cursor.execute("SELECT hashed_password FROM users WHERE username = ?", (username,))
    row = cursor.fetchone()
    if not row:
        raise HTTPException(status_code=400, detail="用户名或密码错误")
    
    stored_password = row["hashed_password"]
    
    # 验证密码
    if not verify_password(password, stored_password):
        raise HTTPException(status_code=400, detail="用户名或密码错误")
    
    # 生成 JWT 访问令牌
    access_token = create_access_token(data={"sub": username})
    return {"access_token": access_token, "token_type": "bearer"}


def get_current_user(token: str = Depends(oauth2_scheme), db: sqlite3.Connection = Depends(get_db)):
    """获取当前用户的依赖函数"""
    # 验证并解析 JWT
    payload = verify_token(token)
    username = payload.get("sub")
    
    # 查询用户信息
    user_row = get_user(db, username)
    if not user_row:
        raise HTTPException(status_code=404, detail="用户不存在")
    return user_row


@app.get("/me")
def read_users_me(current_user = Depends(get_current_user)):
    """获取当前用户信息"""
    return {
        "username": current_user["username"],
        "email": current_user["email"],
        "is_superuser": bool(current_user["is_superuser"]),
    }
