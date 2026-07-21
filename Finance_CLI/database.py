"""
数据库层 — 所有 SQLite3 操作集中在此模块。
不依赖 Streamlit，可独立导入和测试。
"""
import sqlite3
from config import DB_PATH


def get_connection():
    """返回数据库连接，设置 row_factory 使查询结果可按键名访问。"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    # WAL 模式提升并发读取性能
    conn.execute("PRAGMA journal_mode=WAL")
    return conn


def init_db():
    """创建 transactions 表（如果不存在）。应用启动时调用，幂等操作。"""
    conn = get_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            date        TEXT    NOT NULL,
            category    TEXT    NOT NULL,
            amount      REAL    NOT NULL CHECK(amount > 0),
            description TEXT    DEFAULT '',
            created_at  TEXT    DEFAULT (datetime('now','localtime'))
        )
    """)
    conn.commit()
    conn.close()


def add_transaction(date: str, category: str, amount: float, description: str = "") -> int | None:
    """插入一条记录，成功返回新 ID，失败返回 None。"""
    try:
        conn = get_connection()
        cursor = conn.execute(
            "INSERT INTO transactions (date, category, amount, description) VALUES (?, ?, ?, ?)",
            (date, category, amount, description),
        )
        conn.commit()
        return cursor.lastrowid
    except sqlite3.Error as e:
        print(f"[数据库错误] 添加记录失败: {e}")
        return None
    finally:
        conn.close()


def get_transactions(month: str | None = None, category: str | None = None) -> list[dict]:
    """查询交易记录，支持按月份（YYYY-MM）和分类筛选。返回 dict 列表。"""
    conn = get_connection()
    # 用 WHERE 1=1 动态拼接条件，避免复杂的条件判断
    sql = "SELECT id, date, category, amount, description FROM transactions WHERE 1=1"
    params = []

    if month:
        sql += " AND strftime('%Y-%m', date) = ?"
        params.append(month)
    if category:
        sql += " AND category = ?"
        params.append(category)

    sql += " ORDER BY date DESC, id DESC"
    cursor = conn.execute(sql, params)
    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return rows


def get_available_months() -> list[str]:
    """查询数据库中已有记录的月份列表，按时间倒序。"""
    conn = get_connection()
    cursor = conn.execute(
        "SELECT DISTINCT strftime('%Y-%m', date) AS month FROM transactions ORDER BY month DESC"
    )
    months = [row["month"] for row in cursor.fetchall()]
    conn.close()
    return months


def delete_transaction(transaction_id: int) -> bool:
    """按 ID 删除记录，返回是否成功删除（ID 不存在时返回 False）。"""
    try:
        conn = get_connection()
        cursor = conn.execute("DELETE FROM transactions WHERE id = ?", (transaction_id,))
        conn.commit()
        deleted = cursor.rowcount > 0
        return deleted
    except sqlite3.Error as e:
        print(f"[数据库错误] 删除记录失败: {e}")
        return False
    finally:
        conn.close()


def get_category_summary(month: str | None = None) -> list[dict]:
    """按分类汇总金额和笔数，可选按月份筛选。结果按总金额降序。"""
    conn = get_connection()
    sql = """
        SELECT category, SUM(amount) AS total, COUNT(*) AS count
        FROM transactions
        WHERE 1=1
    """
    params = []

    if month:
        sql += " AND strftime('%Y-%m', date) = ?"
        params.append(month)

    sql += " GROUP BY category ORDER BY total DESC"
    cursor = conn.execute(sql, params)
    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return rows
