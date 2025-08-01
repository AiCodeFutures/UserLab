# UserLab

一个面向初学者的 **用户管理系统教学平台**。  
后端用 **FastAPI** 实现 API 与认证、授权逻辑；前端用 **Streamlit** 做交互界面和教学演示。  
适合用来带学生从零构建、理解身份/令牌/权限体系，并逐步扩展成真实可用的系统。

## 核心理念

- **学以致用**：学生不是看概念，而是一步步把用户管理系统「搭起来、用起来、改造它」。  
- **安全优先**：密码哈希、JWT 认证、受保护路由，从一开始就让学生理解安全边界。  
- **可扩展**：基础版做成后，可以拆出多个进阶任务（角色、审计、邮件验证、权限细化等）。  
- **可测试**：用自动化测试让学生明白“核心功能必须有保险”。

## 主要特性

- 用户注册 / 登录  
- 密码安全（bcrypt 哈希）  
- JWT 访问令牌  
- 普通用户与超级用户区分  
- 受保护接口（需要登录/权限检查）  
- Streamlit 前端：注册、登录、查看当前用户信息  
- 可扩展：角色、注销、令牌撤销、权限管理、审计日志

## 技术栈

- Python 版本建议：3.11+  
- 后端：FastAPI, SQLModel（基于 SQLAlchemy + Pydantic）  
- 认证：bcrypt / passlib, PyJWT  
- 前端：Streamlit  
- 数据库（开发）：SQLite；生产可换 PostgreSQL / MySQL  
- 测试：pytest, httpx  

## 快速开始

### 1. 克隆 & 安装依赖
```bash
git clone <你的仓库地址> userlab
cd userlab
python -m venv venv
source venv/bin/activate        # Linux/Mac；Windows 用 `venv\Scripts\activate`
pip install -r requirements.txt
