"""
查看记录页面 — 按月份和分类筛选，以表格形式展示。
"""
import streamlit as st

from config import CATEGORIES
from database import get_transactions, get_available_months


def render_list_page():
    """渲染记录列表（含筛选器）。"""
    st.header("查看记录")

    # ---- 筛选器 ----
    col1, col2 = st.columns(2)
    months = get_available_months()

    with col1:
        month_options = ["全部"] + months
        selected_month = st.selectbox(
            "按月份筛选",
            month_options,
            format_func=lambda m: f"{m} 月" if m != "全部" else "全部月份",
        )
    with col2:
        cat_options = ["全部"] + CATEGORIES
        selected_category = st.selectbox("按分类筛选", cat_options)

    # 查询（"全部" 传 None，不筛选）
    month = None if selected_month == "全部" else selected_month
    category = None if selected_category == "全部" else selected_category
    transactions = get_transactions(month=month, category=category)

    # ---- 结果展示 ----
    st.subheader(f"共 {len(transactions)} 条记录")

    if not transactions:
        st.info("暂无记录，请先在「添加记录」页面添加。")
        return

    # 先算合计（在修改数据之前）
    total = sum(t["amount"] for t in transactions)

    # 格式化金额列（保留两位小数），替换为格式化字符串供展示
    for t in transactions:
        t["amount"] = f"{t['amount']:.2f}"

    # 用中文表头展示
    st.dataframe(
        transactions,
        column_config={
            "id": "ID",
            "date": "日期",
            "category": "分类",
            "description": "备注",
            "amount": "金额(元)",
        },
        use_container_width=True,
        hide_index=True,
    )

    # 合计行
    st.write(f"**合计金额：{total:.2f} 元**")
