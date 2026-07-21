"""
全局常量配置
"""
import os

# 数据库文件路径（项目根目录）
DB_PATH = os.path.join(os.path.dirname(__file__), "finance.db")

# 预设分类（按此顺序显示）
CATEGORIES = ["餐饮", "交通", "购物", "娱乐", "居住", "其他"]
