import streamlit as st
import requests

# Streamlit 前端入口


def register_form():
    """注册表单界面"""
    with st.form("register_form"):
        st.header("用户注册")
        username = st.text_input("用户名")
        email = st.text_input("邮箱")
        password = st.text_input("密码", type="password")
        submitted = st.form_submit_button("注册")
        if submitted:
            resp = requests.post(
                "http://localhost:8001/register",
                data={"username": username, "email": email, "password": password},
            )
            if resp.status_code == 200:
                st.success("注册成功，请登录。")
            else:
                st.error(f"注册失败：{resp.json().get('detail', resp.text)}")


def login_form():
    """登录表单界面"""
    with st.form("login_form"):
        st.header("用户登录")
        username = st.text_input("用户名", key="login_username")
        password = st.text_input("密码", type="password", key="login_password")
        submitted = st.form_submit_button("登录")
        if submitted:
            resp = requests.post(
                "http://localhost:8001/login",
                data={"username": username, "password": password},
            )
            if resp.status_code == 200:
                token = resp.json().get("access_token")
                st.session_state.token = token
                st.success("登录成功！")
            else:
                st.error(f"登录失败：{resp.json().get('detail', resp.text)}")


def display_current_user():
    """显示当前登录用户信息"""
    st.header("当前用户信息")
    token = st.session_state.get("token")
    if not token:
        st.warning("请先登录。")
        return
    
    # 使用正确的Authorization Bearer header
    headers = {"Authorization": f"Bearer {token}"}
    resp = requests.get(
        "http://localhost:8001/me",
        headers=headers
    )
    
    if resp.status_code == 200:
        user = resp.json()
        st.write("**用户名**：", user.get("username"))
        st.write("**邮箱**：", user.get("email"))
        st.write("**超级用户**：", user.get("is_superuser"))
    else:
        st.error(f"获取用户信息失败：{resp.json().get('detail', resp.text)}")
        # 如果token无效，清除session中的token
        if resp.status_code == 401:
            if "token" in st.session_state:
                del st.session_state.token
                st.warning("登录已过期，请重新登录。")


def main():
    st.title("UserLab 用户管理教学平台")
    st.sidebar.title("导航")
    page = st.sidebar.selectbox("选择页面", ["注册", "登录", "当前用户"])

    if page == "注册":
        register_form()
    elif page == "登录":
        login_form()
    elif page == "当前用户":
        display_current_user()


if __name__ == "__main__":
    main()
