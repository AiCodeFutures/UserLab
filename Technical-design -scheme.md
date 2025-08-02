# UserLab 用户管理教学平台技术设计方案

UserLab 是一个面向初学者的用户管理系统教学平台，其目标是在真实项目实践中帮助学生理解身份认证、授权和权限管理。
平台后端基于 FastAPI 开发 API 与认证/授权逻辑，前端采用 Streamlit 搭建交互界面，用以展示教学示例和演示效果。
系统强调“学以致用”和“安全优先”，引导学生逐步构建从用户注册、密码安全、访问令牌到权限细化的完整体系。

项目具有以下特点：

- 学用结合：通过代码演练和交互界面，让学生“搭起来、用起来、改造它”；

- 安全优先：使用 bcrypt 算法对密码进行哈希处理，并使用 JSON Web Token（JWT）实现 stateless 身份认证

- 可扩展性：从基础版出发，逐步加入角色管理、权限细化、审计日志、邮箱验证等功能；

- 可测试性：提供自动化测试用例，确保核心功能可靠，并让学生认识到测试的重要性；

- 简单易部署：后端默认采用 SQLite 数据库，适合快速搭建和本地实验，也可拓展为生产级数据库。

## 一、系统架构设计

```
                 +-----------------------+
                 |      浏览器客户端       |
                 +-----------------------+
                          |
                          | HTTP/WebSocket
                          v
                 +-----------------------+
                 |     Streamlit 前端      |
                 |  (用户注册/登录界面)    |
                 +-----------------------+
                          |
                          | 调用 REST API (JSON)
                          v
+------------------+   +--------------------------------------+
| SQLite 数据库     |<->|        FastAPI 后端服务               |
+------------------+   |  • 用户注册/登录接口                 |
                       |  • 密码哈希与验证 (bcrypt):contentReference[oaicite:2]{index=2}|
                       |  • JWT 令牌生成与校验:contentReference[oaicite:3]{index=3}|
                       |  • 受保护路由、权限检查               |
                       +--------------------------------------+
                                         |
                                         | 调用安全库
                                         v
                       +--------------------------------------+
                       |  认证/授权模块 (passlib, PyJWT 等)   |
                       +--------------------------------------+
```


数据流和关键流程：

- 注册：用户通过 Streamlit 填写注册表单，前端将用户名、邮箱和密码发送至 FastAPI /register 接口。后端使用 bcrypt 哈希密码，存入数据库。
- 登录：前端向 /login 提交用户名和密码。后端调用密码验证函数，使用 CryptContext.verify 将明文密码与存储的哈希比较；验证成功后，用 jwt.encode 生成包含 sub（用户名）和过期时间的 JWT 令牌，返回给前端。
- 访问受保护接口：前端在请求头中携带 Authorization: Bearer <token> 访问 /users/me 等接口。后端通过依赖项 oauth2_scheme 抽取令牌，使用 jwt.decode 验证签名并解析出用户名，然后查询数据库返回当前用户信息。
- 超级用户与权限：用户表包含 is_superuser 字段，用于区分普通用户和管理者。在访问管理接口时，后端通过依赖项检查该字段，确保只有超级用户可执行相关操作。

## 二、代码结构建议

```
userlab/
├── app.py           # FastAPI 应用和路由
├── auth.py          # 密码哈希、令牌生成和验证函数
├── models.py        # SQLAlchemy 用户模型
├── database.py      # 数据库连接和表创建
├── frontend.py      # Streamlit 应用入口
├── requirements.txt # 依赖列表
└── README.md

```

每个文件的作用：

- app.py：定义 FastAPI 实例和三个基础路由：/register、/login、/me（返回当前登录用户）；
- auth.py：包含两个核心函数：get_password_hash() 利用 bcrypt 对密码进行哈希；create_access_token() 使用 jwt.encode 生成令牌；同时提供 verify_token() 用于验证令牌；
- models.py：定义一个简单的 User 模型（id、username、email、hashed_password）；
- database.py：创建 SQLite 连接和用户表；
- frontend.py：使用 Streamlit 创建注册、登录和显示当前用户信息的页面；
- requirements.txt：列出主要依赖，如 fastapi、uvicorn、passlib[bcrypt]、streamlit 等。

## 三、功能模块

- 注册接口 (POST /register)
  - 接收用户名、邮箱和密码；
  - 调用 get_password_hash() 将密码哈希后存入数据库；
  - 返回注册成功信息。

- 登录接口 (POST /login)

  - 验证用户名和密码；
  - 登录成功后调用 create_access_token() 返回 JWT 令牌；

- 受保护接口 (GET /me)

  - 前端在请求头中携带 Authorization: Bearer <token>；
  - 后端通过 verify_token() 解码令牌并获取用户名；
  - 返回对应用户的信息。

除了上述核心功能，可以在教学过程中逐步增加：

  - 用户列表接口（仅用于演示，返回所有用户）；
  - 注销或刷新令牌（可简单记录当前令牌并将其作废）；
  - 简易角色标记：在 User 模型中加入 is_admin 字段，并在后台路由判断是否为管理员。
