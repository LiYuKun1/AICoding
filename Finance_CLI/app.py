"""
Finance CLI 记账本 — 主入口。
启动命令：streamlit run app.py
"""
import streamlit as st

from database import init_db
from views.add import render_add_page
from views.delete import render_delete_page
from views.list import render_list_page
from views.statistics import render_statistics_page


def main():
    """初始化数据库，渲染侧边栏导航和对应页面。"""
    # 页面配置
    st.set_page_config(
        page_title="记账本 · Finance CLI",
        page_icon="💰",
        layout="wide",
    )

    # 初始化数据库（幂等操作，每次启动确保表存在）
    init_db()

    # ---- 侧边栏导航 ----
    st.sidebar.title("💰 记账本")
    st.sidebar.markdown("---")
    page = st.sidebar.radio(
        "导航",
        ["添加记录", "查看记录", "删除记录", "统计报表"],
    )
    st.sidebar.markdown("---")
    st.sidebar.caption("Finance CLI v1.0")

    # ---- 路由分发 ----
    if page == "添加记录":
        render_add_page()
    elif page == "查看记录":
        render_list_page()
    elif page == "删除记录":
        render_delete_page()
    elif page == "统计报表":
        render_statistics_page()


if __name__ == "__main__":
    main()
