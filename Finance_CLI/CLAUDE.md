# Finance CLI — 记账工具

基于 Python + Streamlit + SQLite3 的个人记账 Web 应用。

## 项目结构

```
Finance_CLI/
├── app.py                  # 入口：初始化数据库 + 侧边栏导航 + 页面路由
├── config.py               # 全局常量（数据库路径、预设分类）
├── database.py             # 数据库层：建表 + CRUD 操作（不依赖 Streamlit）
├── views/
│   ├── __init__.py
│   ├── add.py              # 添加记录页面（表单）
│   ├── list.py             # 查看记录页面（表格 + 筛选）
│   ├── delete.py           # 删除记录页面（两步确认）
│   └── statistics.py       # 统计报表（柱状图 + 汇总表）
├── requirements.txt        # streamlit, pandas
└── finance.db              # 自动生成，已加入 .gitignore
```

## 技术栈

- **Web 框架**：Streamlit（纯 Python，无需前端代码）
- **数据库**：SQLite3（Python 标准库，零依赖）
- **图表**：Streamlit 内置 `st.bar_chart`（基于 Altair）
- **数据处理**：pandas（用于 DataFrame 与图表对接）

## 启动方式

```powershell
pip install -r requirements.txt
streamlit run app.py
```

浏览器访问 `http://localhost:8501`。

## 预设分类

`config.py` 中定义，当前为：餐饮、交通、购物、娱乐、居住、其他。

## 数据库

单表结构：

```sql
CREATE TABLE transactions (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    date        TEXT    NOT NULL,  -- YYYY-MM-DD
    category    TEXT    NOT NULL,
    amount      REAL    NOT NULL CHECK(amount > 0),
    description TEXT    DEFAULT '',
    created_at  TEXT    DEFAULT (datetime('now','localtime'))
);
```

所有 SQL 使用 `?` 占位符，禁止 f-string 拼接。

## 代码规范

- UI 标签使用中文
- 函数和变量名使用英文
- 关键逻辑附加中文注释
- database.py 不依赖 Streamlit，方便独立测试
