"""
配置定义
"""
import os

import flet

# app 配置
HOST_PORT = 6006

# 路径
ROOT_PATH = os.path.join(os.path.abspath(f'{os.path.dirname(__file__)}/../'))  # 根目录
ASSETS_PATH = os.path.join(ROOT_PATH, 'assets')  # 静态文件目录
UPLOAD_PATH = os.path.join(ASSETS_PATH, 'uploads')  # 上传目录
LOCALE_PATH = os.path.join(ASSETS_PATH, 'locales')  # 语言包目录
LOG_PATH = os.path.join(ROOT_PATH, "temp")  # 日志目录

# 多语言
LANG = os.getenv('LANG', 'en')

# 字体声明
FONTS = {
    "Harmony": "/fonts/HarmonyOS.ttf",
    "PTMono": "/fonts/PT-Mono.ttf",
}

# 页面路由
PAGES = {
    "/": "index_view",
    "/dashboard": "dashboard_view",
    "/apps/pices":"apps.pices.index_view"
}
# 实装应用列表
APP_CONFIG = dict(
    version="0.1.1",
    title="SmartNote",
    theme_mode="light",
    window_width=1024,
    window_height=678)

# 合并环境变量
from core.venvs import *

# 调试
DEBUG = os.getenv('DEBUG') or DEBUG

# 字符集
CODING_SET = "utf-8"

DEFAULT_IMG = "/imgs/Icon - empty.png"
