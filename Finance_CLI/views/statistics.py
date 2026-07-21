"""
统计报表页面 — 柱状图 + 分类汇总表。
"""
import pandas as pd
import streamlit as st

from config import CATEGORIES
from database import get_category_summary, get_available_months, get_transactions


def render_statistics_page():
    """渲染统计报表：柱状图 + 分类汇总表 + 总计。"""
    st.header("统计报表")

    # ---- 筛选器 ----
    months = get_available_months()
    month_options = ["全部"] + months
    selected_month = st.selectbox(
        "按月份筛选",
        month_options,
        format_func=lambda m: f"{m} 月" if m != "全部" else "全部月份",
    )
    month = None if selected_month == "全部" else selected_month

    # ---- 查询汇总数据 ----
    summary = get_category_summary(month=month)
    if not summary:
        st.info("暂无数据，请先在「添加记录」页面录入。")
        return

    # 构建 DataFrame，确保所有 6 个分类都显示（即使金额为 0）
    summary_map = {s["category"]: s for s in summary}
    all_data = []
    for cat in CATEGORIES:
        if cat in summary_map:
            all_data.append(summary_map[cat])
        else:
            all_data.append({"category": cat, "total": 0.0, "count": 0})

    df = pd.DataFrame(all_data)

    # ---- 柱状图 ----
    st.subheader("分类支出柱状图")
    chart_df = df.set_index("category")[["total"]]
    chart_df.columns = ["金额(元)"]
    st.bar_chart(chart_df, y_label="金额（元）", x_label="分类")

    # ---- 汇总表 ----
    st.subheader("分类汇总表")
    display_df = pd.DataFrame({
        "分类": df["category"],
        "金额(元)": df["total"].apply(lambda x: f"{x:.2f}"),
        "笔数": df["count"],
    })
    st.dataframe(display_df, use_container_width=True, hide_index=True)

    # ---- 总计 ----
    total_amount = sum(s["total"] for s in summary)
    total_count = sum(s["count"] for s in summary)
    st.write(f"**总计：{total_amount:.2f} 元（{total_count} 笔）**")
