"""
删除记录页面 — 两步确认机制防止误删。
"""
import streamlit as st

from database import get_transactions, delete_transaction


def render_delete_page():
    """渲染删除记录界面，包含两步确认流程。"""
    st.header("删除记录")

    # 获取全部记录供选择
    transactions = get_transactions()
    if not transactions:
        st.info("暂无记录可供删除。")
        return

    # ---- Phase 2：确认删除 ----
    if st.session_state.get("delete_pending"):
        record = st.session_state["delete_pending"]
        st.warning(
            f"确定要删除以下记录吗？此操作**不可撤销**。\n\n"
            f"**ID**：{record['id']} | **日期**：{record['date']} | "
            f"**分类**：{record['category']} | **金额**：{record['amount']:.2f} 元 | "
            f"**备注**：{record['description']}"
        )

        col1, col2 = st.columns(2)
        with col1:
            if st.button("确定删除", type="primary"):
                ok = delete_transaction(record["id"])
                if ok:
                    st.success(f"ID={record['id']} 已删除")
                else:
                    st.error("删除失败，记录可能已被删除")
                st.session_state["delete_pending"] = None
                st.rerun()
        with col2:
            if st.button("取消"):
                st.session_state["delete_pending"] = None
                st.rerun()
        return

    # ---- Phase 1：选择记录 ----
    # 构建下拉选项："ID=1 | 2024-01-15 | 餐饮 | 35.00 元 | 午餐"
    options = {}
    for t in transactions:
        label = (
            f"ID={t['id']} | {t['date']} | {t['category']} | "
            f"{t['amount']:.2f} 元 | {t['description']}"
        )
        options[label] = t

    selected_label = st.selectbox("选择要删除的记录", list(options.keys()))
    selected_record = options[selected_label]

    # 显示选中记录的详情
    st.info(
        f"**日期**：{selected_record['date']} | "
        f"**分类**：{selected_record['category']} | "
        f"**金额**：{selected_record['amount']:.2f} 元\n\n"
        f"**备注**：{selected_record['description'] or '（无）'}"
    )

    if st.button("删除此记录", type="primary"):
        st.session_state["delete_pending"] = selected_record
        st.rerun()
