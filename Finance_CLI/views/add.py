"""
添加记录页面 — 表单填写并提交到数据库。
"""
import datetime

import streamlit as st

from config import CATEGORIES
from database import add_transaction


def render_add_page():
    """渲染添加记录表单。"""
    st.header("添加记录")

    # 表单输入区域
    date = st.date_input("日期", value=datetime.date.today())
    category = st.selectbox("分类", CATEGORIES)
    amount = st.number_input("金额（元）", min_value=0.01, step=0.01, format="%.2f")
    description = st.text_area("备注（可选）", max_chars=200, placeholder="例如：午餐外卖")

    if st.button("提交", type="primary"):
        # 输入校验
        if amount <= 0:
            st.error("金额必须大于 0")
            return

        # 写入数据库
        new_id = add_transaction(
            date=date.strftime("%Y-%m-%d"),
            category=category,
            amount=amount,
            description=description.strip(),
        )

        if new_id:
            st.success(f"记录已添加！ID = {new_id}")
            st.rerun()
        else:
            st.error("添加失败，请重试")
