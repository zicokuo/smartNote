"""
配置定义
"""
import os

# app 配置
HOST_PORT = 6006
# 路径
ROOT_PATH = os.path.join(os.path.abspath(f'{os.path.dirname(__file__)}/../'))  # 根目录
ASSETS_PATH = os.path.join(ROOT_PATH, 'assets')  # 静态文件目录
UPLOAD_PATH = os.path.join(ASSETS_PATH, 'uploads')  # 上传目录
LOCALE_PATH = os.path.join(ASSETS_PATH, 'locales')  # 语言包目录

# 多语言
LANG = os.getenv('LANG', 'en')

# 实装应用列表

# 合并环境变量
from core.venvs import *

# 调试
DEBUG = os.getenv('DEBUG') or DEBUG

# 字符集
CHATSET_UTF8 = "utf-8"