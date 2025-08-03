import streamlit as st

# Streamlit 前端入口


def register_form():
    """注册表单界面"""
    pass


def login_form():
    """登录表单界面"""
    pass


def display_current_user():
    """显示当前登录用户信息"""
    pass


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
